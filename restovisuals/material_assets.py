"""Experimental normal-only DDS assets; no native loading or installation."""
from array import array
import configparser
import hashlib
import json
import math
from pathlib import Path
import struct

from .gpu_demo import _output_path
from .material_mips import build_mips

SIZE = 256
KINDS = ('flat', 'x-positive', 'x-negative', 'y-positive', 'y-negative', 'detail')
PACKAGE_FILES = ('disabled.ini', 'fixture-contract.json', 'README.txt',
                 *(f'textures/{name}.dds' for name in KINDS))
COMPONENT = 'rv0k-material-probe'
ROOT = Path(__file__).resolve().parents[1]


def unit_normal(value):
    if len(value) != 3 or not all(math.isfinite(x) for x in value):
        raise ValueError('Expected three finite normal components')
    length = math.sqrt(sum(x*x for x in value))
    if length < 1e-10 or value[2] < 0:
        raise ValueError('Expected a nonzero positive-hemisphere normal')
    return tuple(x/length for x in value)


def encode_normal(value):
    n = unit_normal(value)
    return bytes([int(math.floor(max(0, min(1, x*.5+.5))*255+.5)) for x in n] + [255])


def decode_normal(pixel):
    if len(pixel) != 4 or pixel[3] != 255:
        raise ValueError('Expected opaque RGBA8 normal data')
    return unit_normal(tuple(x/255*2-1 for x in pixel[:3]))


def _vector_mips(values, width):
    """Keep unnormalized double means for reduction; normalize only each output."""
    values = array('d', values)
    if width < 1 or width > SIZE or width & (width-1) or len(values) != width*width*3:
        raise ValueError('Invalid bounded normal grid')
    while True:
        yield tuple(tuple(values[i:i+3]) for i in range(0, len(values), 3))
        if width == 1:
            break
        next_width = width//2
        reduced = array('d')
        for y in range(next_width):
            for x in range(next_width):
                indices = [((2*y+dy)*width+2*x+dx)*3 for dy in (0, 1) for dx in (0, 1)]
                reduced.extend(sum(values[i+c] for i in indices)/4 for c in range(3))
        values, width = reduced, next_width


def normal_levels(kind):
    if kind not in KINDS:
        raise ValueError('Unknown bounded normal candidate')
    if kind == 'detail':
        # Reuse the validated moment hierarchy, ignoring its roughness channel.
        moments, _ = build_mips(SIZE)
        vectors = [tuple(p[:3] for p in struct.iter_unpack('<4e', level)) for level in moments]
    else:
        values = array('d')
        for y in range(SIZE):
            for x in range(SIZE):
                axis = (x+.5)/SIZE if kind.startswith('x-') else (y+.5)/SIZE
                amount = 0 if kind == 'flat' else .6*axis*(-1 if kind.endswith('negative') else 1)
                values.extend((amount if kind.startswith('x-') else 0,
                               amount if kind.startswith('y-') else 0, math.sqrt(1-amount*amount)))
        vectors = _vector_mips(values, SIZE)
    levels, metrics = [], []
    for level, normals in enumerate(vectors):
        packed = bytearray()
        max_component = max_angle = max_unit = 0.0
        angle_squares = 0.0
        minimum_length, maximum_length = 2.0, 0.0
        for value in normals:
            intended = unit_normal(value)
            pixel = encode_normal(value)
            decoded = decode_normal(pixel)
            raw = tuple(x/255*2-1 for x in pixel[:3])
            length = math.sqrt(sum(x*x for x in raw))
            minimum_length, maximum_length = min(minimum_length, length), max(maximum_length, length)
            angle = math.degrees(math.acos(max(-1, min(1, sum(a*b for a, b in zip(intended, decoded))))))
            max_angle = max(max_angle, angle); angle_squares += angle*angle
            max_component = max(max_component, *(abs(a-b) for a, b in zip(raw, intended)))
            max_unit = max(max_unit, abs(math.sqrt(sum(x*x for x in decoded))-1))
            packed.extend(pixel)
        levels.append(bytes(packed))
        metrics.append({'width': SIZE >> level, 'payload_bytes': len(packed),
                        'component_max_absolute_error': max_component,
                        'normal_angle_max_degrees': max_angle,
                        'normal_angle_rms_degrees': math.sqrt(angle_squares/len(normals)),
                        'raw_normal_length_range': [minimum_length, maximum_length],
                        'decoded_unit_length_max_error': max_unit, 'alpha_all_255': True})
        if max_component > 1/255+1e-12 or max_angle > .5 or max_unit > 1e-12:
            raise ValueError('Normal quantization contract failed')
    return tuple(levels), metrics


def dds_bytes(levels):
    if len(levels) != 9 or any(not isinstance(p, bytes) or len(p) != (SIZE >> i)**2*4 for i, p in enumerate(levels)):
        raise ValueError('Expected complete 256 RGBA8 mip chain')
    if any(any(a != 255 for a in p[3::4]) for p in levels):
        raise ValueError('Normal asset alpha must remain opaque')
    # DDS magic + 124-byte header + 20-byte DX10 extension; no sRGB modifier.
    header = [124, 0x2100f, SIZE, SIZE, SIZE*4, 0, 9] + [0]*11
    header += [32, 4, int.from_bytes(b'DX10', 'little'), 0, 0, 0, 0, 0]
    header += [0x401008, 0, 0, 0, 0]
    # Keep alpha-mode metadata zero for legacy D3DX reader compatibility.
    return b'DDS '+struct.pack('<31I', *header)+struct.pack('<5I', 28, 3, 0, 1, 0)+b''.join(levels)


def parse_dds(data):
    """Strict reader for our one experimental file contract, not a general loader."""
    if not isinstance(data, bytes) or len(data) < 148 or data[:4] != b'DDS ':
        raise ValueError('Invalid experimental DDS header')
    h = struct.unpack_from('<31I', data, 4)
    extension = struct.unpack_from('<5I', data, 128)
    if (h[:7] != (124, 0x2100f, SIZE, SIZE, SIZE*4, 0, 9)
            or h[7:18] != (0,)*11 or h[18:26] != (32, 4, int.from_bytes(b'DX10', 'little'), 0, 0, 0, 0, 0)
            or h[26:] != (0x401008, 0, 0, 0, 0) or extension != (28, 3, 0, 1, 0)):
        raise ValueError('Unsupported experimental DDS contract')
    offset = 148; levels = []
    for i in range(9):
        size = (SIZE >> i)**2*4
        level = data[offset:offset+size]
        if len(level) != size or any(a != 255 for a in level[3::4]):
            raise ValueError('Truncated DDS or changed alpha channel')
        levels.append(level); offset += size
    if len(data) != offset:
        raise ValueError('Unexpected DDS trailing data')
    return tuple(levels)


def fixture_contract():
    return {'status': 'prerequisite_missing', 'original_kn5_available': False,
            'authoring_export_load_workflow_verified': False, 'native_material_verified': False,
            'ownership': 'Original RestoVisuals fixture required; no third-party car/track modification',
            'mesh': 'RV0K_OWNED_PLANE', 'material': 'RV0K_OWNED_SURFACE',
            'shader_candidate': 'ksPerPixelMultiMap', 'texture_slot_candidate': 'txNormal',
            'expected_mesh_count': 1, 'expected_material_count': 1,
            'proposed_asset_local_vertices': [[-1, 0, 1], [1, 0, 1], [1, 0, -1], [-1, 0, -1]],
            'proposed_uv1': [[0, 0], [1, 0], [1, 1], [0, 1]], 'proposed_triangles': [[0, 1, 2], [0, 2, 3]],
            'proposed_tangent': [1, 0, 0], 'proposed_bitangent': [0, 0, -1], 'proposed_normal': [0, 1, 0],
            'basis_scope': 'Asset-local proposal; exporter transform and tangent handedness must be verified',
            'requirements': ['supported authoring/export/load workflow', 'original source and KN5 hashes',
                             'verified always-on normal slot and decode', 'immutable complete baseline',
                             'exact config precedence and collision-free paths', 'separate authorization/safety review',
                             'owned session end and verified cold-load recovery'],
            'cold_recovery_plan': 'End owned session; remove only owned component; cold-load original assets/config; verify effective material state and protected hashes.'}


def disabled_config():
    return ('; Experimental normal-only proposal; never enabled by this tool.\n'
            '[SHADER_REPLACEMENT_RV0K_NORMAL_ONLY]\nACTIVE = 0\n'
            'MATERIALS = { material:RV0K_OWNED_SURFACE & shader:ksPerPixelMultiMap & materialResource:txNormal }\n'
            'RESOURCE_0 = txNormal\nRESOURCE_FILE_0 = textures/flat.dds\n')


def check_disabled_config(text):
    cfg = configparser.ConfigParser(interpolation=None, strict=True)
    try: cfg.read_string(text)
    except configparser.Error as error: raise ValueError('Malformed disabled configuration') from error
    if cfg.sections() != ['SHADER_REPLACEMENT_RV0K_NORMAL_ONLY']:
        raise ValueError('Unexpected material section')
    section = cfg[cfg.sections()[0]]
    expected = configparser.ConfigParser(interpolation=None); expected.read_string(disabled_config())
    if dict(section) != dict(expected[expected.sections()[0]]):
        raise ValueError('Configuration must retain exact disabled owned selection')


def prepare_material_textures(output_dir):
    output = _output_path(output_dir); output.mkdir(parents=True)
    package = output/'package'; package.mkdir()
    result = {'status': 'running', 'native_decision': 'NO-GO', 'native_compatible': False, 'candidates': {}}
    try:
        (package/'textures').mkdir()
        for kind in KINDS:
            levels, metrics = normal_levels(kind); data = dds_bytes(levels)
            if parse_dds(data) != levels: raise ValueError('DDS roundtrip failed')
            path = f'textures/{kind}.dds'; (package/path).write_bytes(data)
            result['candidates'][kind] = {'file': path, 'sha256': hashlib.sha256(data).hexdigest(),
                                          'file_bytes': len(data), 'texture_payload_bytes': sum(map(len, levels)), 'mips': metrics}
        (package/'disabled.ini').write_bytes(disabled_config().encode('utf-8'))
        contract = fixture_contract()
        (package/'fixture-contract.json').write_bytes((json.dumps(contract, indent=2, sort_keys=True)+'\n').encode())
        (package/'README.txt').write_bytes(b'Original RestoVisuals experimental normal-only assets. Native status: NO-GO.\n'
            b'All configuration remains disabled. No installer or game fixture is included.\n'
            b'RGBA8 DX10 DDS, unsigned RGB=(normal+1)/2, alpha=255; no sRGB conversion.\n'
            b'Actual shader decode, orientation, sampler and cold recovery require future validation.\n'
            b'Flat is the disabled default; orientation/detail selection needs a separately reviewed run-bound package.\n'
            b'100% freeware policy; repository licensing remains owner-undecided.\n')
        files = {name: {'sha256': hashlib.sha256((package/name).read_bytes()).hexdigest(), 'bytes': (package/name).stat().st_size}
                 for name in PACKAGE_FILES}
        manifest = {'schema_version': 1, 'component': COMPONENT, 'scope': 'disabled_offline_normal_candidates',
                    'native_ready': False, 'native_compatible': False, 'fixture_status': contract['status'],
                    'encoding': 'normalize(2*RGB/255-1); A=255; DXGI 28 UNORM; experimental host interpretation',
                    'size': SIZE, 'mip_count': 9, 'files': files}
        (package/'manifest.json').write_bytes((json.dumps(manifest, indent=2, sort_keys=True)+'\n').encode())
        result.update(status='passed', texture_payload_bytes_all_candidates=sum(c['texture_payload_bytes'] for c in result['candidates'].values()),
                      dds_file_bytes_all_candidates=sum(c['file_bytes'] for c in result['candidates'].values()),
                      package_file_bytes=sum(p.stat().st_size for p in package.rglob('*') if p.is_file()),
                      manifest_sha256=hashlib.sha256((package/'manifest.json').read_bytes()).hexdigest())
    except Exception as error:
        result.update(status='failed', failure=type(error).__name__); raise
    finally:
        (output/'report.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    return result
