"""Closed workspace-only rehearsal. Never accepts a game installation target."""
import hashlib
import json
import os
from pathlib import Path
import uuid

from .gpu_demo import _output_path
from .material_assets import (COMPONENT, PACKAGE_FILES, ROOT, check_disabled_config,
                              fixture_contract, parse_dds)

FILES = (*PACKAGE_FILES, 'manifest.json')
STAGE = '.rv0k-stage'
RETIRED = '.rv0k-retired-evidence'
MARKER = '.rv0k-owner.json'


class SimulatedInterruption(Exception):
    pass


def _no_links(path):
    try: attributes = getattr(path.lstat(), 'st_file_attributes', 0)
    except FileNotFoundError: attributes = 0
    if path.is_symlink() or attributes & 0x400:
        raise ValueError('Reparse points are not permitted in a rehearsal')


def _workspace(path, *, local=False):
    path = Path(path).absolute()
    _no_links(path)
    for parent in path.parents:
        _no_links(parent)
        if parent == ROOT: break
    resolved = path.resolve()
    allowed = (ROOT/'.local').resolve() if local else ROOT.resolve()
    if resolved == allowed or not resolved.is_relative_to(allowed):
        raise ValueError('Rehearsal path must stay inside the approved workspace')
    if not local and not (resolved.is_relative_to((ROOT/'.local').resolve())
                          or resolved == ROOT/'examples/phase0k-normal-probe'):
        raise ValueError('Use a generated or reviewed original package')
    return resolved


def _tree_files(folder):
    """Only this closed two-level component layout can be inspected or moved."""
    _no_links(folder)
    found = set()
    allowed = {*FILES, MARKER, '.pending'}
    for entry in folder.iterdir():
        _no_links(entry)
        if entry.name == 'textures' and entry.is_dir():
            for file in entry.iterdir():
                _no_links(file)
                relative = 'textures/'+file.name
                if not file.is_file() or relative not in allowed:
                    raise ValueError('Unexpected component content; preserve for review')
                found.add(relative)
        elif entry.is_file() and entry.name in allowed:
            found.add(entry.name)
        else:
            raise ValueError('Unexpected component content; preserve for review')
    return found


def read_package(path):
    folder = _workspace(path)
    if not folder.is_dir() or _tree_files(folder) != set(FILES):
        raise ValueError('Incomplete or extended normal package')
    data = {name: (folder/name).read_bytes() for name in FILES}
    manifest = json.loads(data['manifest.json'])
    if (manifest.get('component') != COMPONENT or manifest.get('schema_version') != 1
            or manifest.get('native_ready') is not False or manifest.get('native_compatible') is not False
            or set(manifest.get('files', {})) != set(PACKAGE_FILES)):
        raise ValueError('Wrong package ownership or native gate')
    for name in PACKAGE_FILES:
        receipt = manifest['files'][name]
        if receipt != {'sha256': hashlib.sha256(data[name]).hexdigest(), 'bytes': len(data[name])}:
            raise ValueError('Changed package payload')
        if name.endswith('.dds'): parse_dds(data[name])
    check_disabled_config(data['disabled.ini'].decode('utf-8'))
    if json.loads(data['fixture-contract.json']) != fixture_contract():
        raise ValueError('Unexpected fixture eligibility claim')
    return folder, data


def synthetic_material_baseline():
    return {'evidence': 'synthetic_workspace_descriptor_only', 'mesh': 'RV0K_OWNED_PLANE',
            'material': 'RV0K_OWNED_SURFACE', 'shader': 'ksPerPixelMultiMap', 'slots': ['txNormal'],
            'mesh_matches': 1, 'material_matches': 1, 'outside_sharing': 0,
            'normal_usage': 'always_on', 'uv_basis_known': True}


def selection_matches(descriptor):
    """Tests a synthetic prerequisite predicate, never discovers real materials."""
    return descriptor == synthetic_material_baseline()


def _json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2)+'\n').encode('utf-8')


def _journal(folder, value):
    temporary = folder/'.journal-next'
    _no_links(folder); _no_links(temporary); _no_links(folder/'journal.json')
    # Preserve an uncertain orphan update for review instead of overwriting it.
    with temporary.open('xb') as stream:
        stream.write(_json_bytes(value)); stream.flush(); os.fsync(stream.fileno())
    temporary.replace(folder/'journal.json')


def _assert_baseline(folder, journal):
    if set(journal.get('baseline', {})) != {'original.ini', 'material-state.json'}:
        raise ValueError('Incomplete immutable baseline receipt')
    for name, digest in journal['baseline'].items():
        if name not in ('original.ini', 'material-state.json'):
            raise ValueError('Unexpected baseline path')
        path = folder/'baseline'/name
        _no_links(path); _no_links(path.parent)
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Original baseline drift; preserve evidence')


def _begin(folder, package, payloads, fault):
    if any((folder/p).exists() for p in (STAGE, COMPONENT, RETIRED, 'journal.json')):
        raise ValueError('Component or transaction collision')
    (folder/'baseline').mkdir()
    (folder/'baseline/original.ini').write_bytes(b'[RV0K_SYNTHETIC_BASELINE]\nIMMUTABLE=1\n')
    (folder/'baseline/material-state.json').write_bytes(_json_bytes(synthetic_material_baseline()))
    baseline = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (folder/'baseline').iterdir()}
    journal = {'schema_version': 1, 'workspace_only': True, 'component': COMPONENT, 'nonce': uuid.uuid4().hex,
               'package': package.relative_to(ROOT).as_posix(), 'state': 'allocating', 'pending': None,
               'baseline': baseline, 'files': {name: hashlib.sha256(raw).hexdigest() for name, raw in payloads.items()}}
    _journal(folder, journal)
    def interrupt(point):
        if point == fault: raise SimulatedInterruption(point)
    interrupt('before-stage')
    stage = folder/STAGE; stage.mkdir()
    interrupt('empty-stage')
    (stage/MARKER).write_bytes(_json_bytes({'component': COMPONENT, 'nonce': journal['nonce'], 'workspace_only': True}))
    (stage/'textures').mkdir(); interrupt('after-owner')
    for name, raw in payloads.items():
        journal.update(state='staging', pending=name); _journal(folder, journal)
        with (stage/'.pending').open('xb') as stream:
            interrupt('opened:'+name)
            if fault == 'partial:'+name:
                stream.write(raw[:max(1, len(raw)//2)]); stream.flush(); os.fsync(stream.fileno())
                raise SimulatedInterruption(fault)
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        (stage/'.pending').rename(stage/name); interrupt('renamed:'+name)
        journal['pending'] = None; _journal(folder, journal); interrupt('copied:'+name)
    # Both absolute endpoints were resolved under this newly owned scenario.
    target = _workspace(folder/COMPONENT, local=True)
    if target.exists(): raise ValueError('Component collision before commit')
    _workspace(stage, local=True).rename(target); interrupt('after-commit')
    journal['state'] = 'committed'; _journal(folder, journal)


def recover_material_rehearsal(scenario, *, interrupt_after_retire=False):
    folder = _workspace(scenario, local=True)
    _no_links(folder/'.journal-next')
    if (folder/'.journal-next').exists():
        raise FileExistsError('Uncertain journal update; preserve transaction for review')
    _no_links(folder/'journal.json')
    journal = json.loads((folder/'journal.json').read_bytes())
    if (journal.get('schema_version') != 1 or journal.get('component') != COMPONENT
            or journal.get('workspace_only') is not True or not isinstance(journal.get('nonce'), str)
            or len(journal['nonce']) != 32 or journal.get('state') not in ('allocating','staging','committed','recovered')
            or journal.get('pending') is not None and journal['pending'] not in FILES):
        raise ValueError('No owned workspace transaction')
    _, payloads = read_package(ROOT/journal['package'])
    if journal['files'] != {name: hashlib.sha256(raw).hexdigest() for name, raw in payloads.items()}:
        raise ValueError('Recovery package changed')
    _assert_baseline(folder, journal)
    candidates = [folder/p for p in (STAGE, COMPONENT, RETIRED) if (folder/p).exists()]
    if len(candidates) > 1: raise ValueError('Ambiguous transaction directories')
    if candidates:
        owned = _workspace(candidates[0], local=True); names = _tree_files(owned)
        if names:
            marker = {'component': COMPONENT, 'nonce': journal['nonce'], 'workspace_only': True}
            if MARKER not in names or (owned/MARKER).read_bytes() != _json_bytes(marker):
                raise ValueError('Missing or changed ownership marker')
            for name in names-{MARKER, '.pending'}:
                if hashlib.sha256((owned/name).read_bytes()).hexdigest() != journal['files'][name]:
                    raise ValueError('Owned file drift; preserve evidence')
            if '.pending' in names:
                pending = journal.get('pending')
                if pending not in payloads: raise ValueError('Unknown interrupted file')
                partial = (owned/'.pending').read_bytes()
                if partial != payloads[pending][:len(partial)]:
                    raise ValueError('Interrupted file is not an owned source prefix')
        elif journal['state'] != 'allocating' and not (owned.name == RETIRED and journal['state'] == 'recovered'):
            raise ValueError('Unexpected empty transaction directory')
        if owned.name != RETIRED:
            retired = _workspace(folder/RETIRED, local=True)
            if retired.exists(): raise ValueError('Retirement collision')
            owned.rename(retired)
            if interrupt_after_retire: raise SimulatedInterruption('after-retire')
    # Retain pending identity while partial evidence is archived for audit/retry.
    journal['state'] = 'recovered'; _journal(folder, journal)
    _assert_baseline(folder, journal)
    if (folder/STAGE).exists() or (folder/COMPONENT).exists(): raise ValueError('Active component remains')
    return {'baseline_unchanged': True, 'active_component_absent': True,
            'retired_evidence_retained': (folder/RETIRED).exists(), 'workspace_only': True}


def rehearse_material_recovery(package_dir, output_dir):
    package, payloads = read_package(package_dir)
    output = _output_path(output_dir); output.mkdir(parents=True)
    result = {'status': 'running', 'native_decision': 'NO-GO', 'native_material_recovery_validated': False,
              'cases': [], 'scope': 'fresh workspace simulations, no game path or live material operations'}
    try:
        faults = ['before-stage', 'empty-stage', 'after-owner']
        faults += [stage+':'+name for name in payloads for stage in ('opened', 'partial', 'renamed', 'copied')]
        faults += ['after-commit', 'complete']
        for index, fault in enumerate(faults):
            folder = output/f'case-{index:02}'; folder.mkdir()
            try: _begin(folder, package, payloads, fault)
            except SimulatedInterruption: pass
            receipt = recover_material_rehearsal(folder)
            # Independent invocation must be safe after a completed recovery too.
            if recover_material_rehearsal(folder) != receipt: raise ValueError('Recovery is not idempotent')
            result['cases'].append({'fault': fault, **receipt})
        negative = []
        for key, value in [('mesh_matches', 0), ('mesh_matches', 2), ('material_matches', 2),
                           ('outside_sharing', 1), ('shader', 'wrong'), ('slots', []),
                           ('normal_usage', 'damage_only'), ('uv_basis_known', False)]:
            candidate = synthetic_material_baseline(); candidate[key] = value
            if selection_matches(candidate): raise ValueError('Ambiguous synthetic material accepted')
            negative.append({'changed_field': key, 'rejected': True})
        collision = output/'guard-collision'; collision.mkdir(); (collision/COMPONENT).mkdir()
        sentinel = collision/COMPONENT/'unrelated.txt'; sentinel.write_bytes(b'original sentinel')
        try: _begin(collision, package, payloads, 'complete')
        except ValueError: pass
        else: raise ValueError('Existing component accepted')
        if sentinel.read_bytes() != b'original sentinel' or (collision/'journal.json').exists():
            raise ValueError('Collision changed existing content')
        # Keep this pre-existing sentinel in place as negative-test evidence.
        drift = output/'guard-drift'; drift.mkdir(); _begin(drift, package, payloads, 'complete')
        managed = drift/COMPONENT/'disabled.ini'; managed.write_bytes(b'changed by simulated external actor')
        try: recover_material_rehearsal(drift)
        except ValueError: pass
        else: raise ValueError('Managed-file drift ignored')
        if managed.read_bytes() != b'changed by simulated external actor': raise ValueError('Drift was overwritten')
        managed.write_bytes(payloads['disabled.ini']); recover_material_rehearsal(drift)
        foreign = output/'guard-unexpected'; foreign.mkdir(); _begin(foreign, package, payloads, 'complete')
        extra = foreign/COMPONENT/'unrelated.txt'; extra.write_bytes(b'preserve unexpected content')
        try: recover_material_rehearsal(foreign)
        except ValueError: pass
        else: raise ValueError('Unexpected content ignored')
        if extra.read_bytes() != b'preserve unexpected content': raise ValueError('Unexpected content changed')
        extra.rename(_workspace(foreign/'foreign-preserved.txt', local=True)); recover_material_rehearsal(foreign)
        interrupted_remove = output/'guard-retire'; interrupted_remove.mkdir()
        _begin(interrupted_remove, package, payloads, 'complete')
        try: recover_material_rehearsal(interrupted_remove, interrupt_after_retire=True)
        except SimulatedInterruption: pass
        recover_material_rehearsal(interrupted_remove)
        result.update(status='passed', fault_cases=len(result['cases']), synthetic_selection_rejections=negative,
                      collision_preserved=True, drift_refused_and_preserved=True, unexpected_file_preserved=True,
                      interrupted_retirement_recovered=True,
                      evidence_retention='Owned directories are atomically retired inside each workspace scenario, not recursively deleted.')
    except Exception as error:
        result.update(status='failed', failure=type(error).__name__); raise
    finally:
        (output/'report.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    return result
