import copy
import hashlib
import io
import json
import math
from pathlib import Path
import struct
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from restovisuals.__main__ import main
from restovisuals.material_assets import (KINDS, PACKAGE_FILES, ROOT, SIZE, _vector_mips,
    check_disabled_config, dds_bytes, decode_normal, disabled_config, encode_normal,
    fixture_contract, normal_levels, parse_dds, prepare_material_textures, unit_normal)
from restovisuals.material_recovery import (COMPONENT, FILES, RETIRED, STAGE, SimulatedInterruption,
    _begin, _no_links, _workspace, read_package, recover_material_rehearsal,
    rehearse_material_recovery, selection_matches, synthetic_material_baseline)


class MaterialAssetsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_root = ROOT/'.local/test-tmp'; cls.temp_root.mkdir(parents=True, exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(dir=cls.temp_root)
        cls.directory = Path(cls.temp.name).resolve()
        assert cls.directory.is_relative_to(ROOT/'.local')
        cls.output = cls.directory/'generated'
        cls.report = prepare_material_textures(cls.output)
        cls.package, cls.payloads = read_package(cls.output/'package')

    @classmethod
    def tearDownClass(cls):
        assert Path(cls.temp.name).resolve().is_relative_to(ROOT/'.local')
        cls.temp.cleanup()

    def folder(self, name):
        path = self.directory/self._testMethodName/name
        path.mkdir(parents=True)
        return path

    def scenario(self, fault):
        folder = self.folder('scenario')
        try: _begin(folder, self.package, self.payloads, fault)
        except SimulatedInterruption: pass
        return folder

    def cloned_package(self):
        folder = self.folder('copy'); (folder/'textures').mkdir()
        for name, raw in self.payloads.items(): (folder/name).write_bytes(raw)
        return folder

    def test_signed_mapping_has_bounded_precision_and_rejects_invalid_normals(self):
        for normal in ((0, 0, 1), (.6, 0, .8), (-.6, 0, .8), (0, -.6, .8), (.2, .3, .9)):
            encoded = encode_normal(normal); expected = unit_normal(normal)
            raw = [x/255*2-1 for x in encoded[:3]]
            self.assertLessEqual(max(abs(a-b) for a, b in zip(raw, expected)), 1/255+1e-12)
            self.assertAlmostEqual(sum(x*x for x in decode_normal(encoded)), 1, places=14)
            self.assertEqual(encoded[3], 255)
        for invalid in ((0, 0, 0), (0, 0, -1), (math.nan, 0, 1), (math.inf, 0, 1)):
            with self.assertRaises(ValueError): encode_normal(invalid)

    def test_neutral_is_opaque_128_and_its_quantization_bias_is_explicit(self):
        self.assertEqual(encode_normal((0, 0, 1)), bytes((128, 128, 255, 255)))
        levels = parse_dds(self.payloads['textures/flat.dds'])
        for i, level in enumerate(levels):self.assertEqual(level, bytes((128, 128, 255, 255))*(SIZE >> i)**2)
        decoded = decode_normal(bytes((128, 128, 255, 255)))
        angle = math.degrees(math.acos(decoded[2]))
        self.assertAlmostEqual(angle, .31775544206983286, places=10)
        self.assertNotEqual(decoded, (0, 0, 1))

    def test_orientation_ramps_have_correct_axis_sign_and_monotonicity(self):
        for axis in ('x', 'y'):
            channel = 0 if axis == 'x' else 1
            for sign in ('positive', 'negative'):
                data = parse_dds(self.payloads[f'textures/{axis}-{sign}.dds'])[0]
                samples = [decode_normal(data[(i if axis == 'x' else i*SIZE)*4:][:4])[channel] for i in range(SIZE)]
                direction = 1 if sign == 'positive' else -1
                self.assertTrue(all(v*direction > 0 for v in samples))
                self.assertTrue(all(direction*(b-a) >= -1e-12 for a, b in zip(samples, samples[1:])))
                for i in (13, 71, 209):
                    amount = direction*.6*(i+.5)/SIZE
                    intended = [0, 0, math.sqrt(1-amount*amount)]; intended[channel] = amount
                    pixel = data[(i if axis == 'x' else i*SIZE)*4:][:4]
                    self.assertEqual(pixel, encode_normal(intended))

    def test_reduction_keeps_vector_means_before_final_normalization(self):
        # Renormalizing each parent would incorrectly produce (0,.3,.9) here.
        row = ((.8, 0, .6), (-.8, 0, .6), (0, .6, .8), (0, .6, .8))
        values = [v for _ in range(4) for normal in row for v in normal]
        levels = list(_vector_mips(values, 4)); final = levels[-1][0]
        for a, b in zip(final, (0, .3, .7)):self.assertAlmostEqual(a, b, places=14)
        self.assertLess(sum(v*v for v in final), 1)
        self.assertEqual(encode_normal(final), encode_normal((0, .3, .7)))
        self.assertNotEqual(encode_normal(final), encode_normal((0, .3, .9)))

    def test_all_levels_are_finite_unit_after_decode_and_alpha_is_unmodified(self):
        for kind in KINDS:
            levels = parse_dds(self.payloads[f'textures/{kind}.dds'])
            self.assertEqual([len(p) for p in levels], [(SIZE >> i)**2*4 for i in range(9)])
            for level in levels:
                for pixel in struct.iter_unpack('<4B', level):
                    self.assertEqual(pixel[3], 255)
                    normal = decode_normal(pixel)
                    self.assertTrue(all(math.isfinite(x) for x in normal))
                    self.assertAlmostEqual(sum(x*x for x in normal), 1, places=12)

    def test_dds_header_offsets_and_payload_are_independently_checked(self):
        raw = self.payloads['textures/detail.dds']
        self.assertEqual(raw[:4], b'DDS ')
        for offset, expected in ((4, 124), (8, 0x2100f), (12, 256), (16, 256), (20, 1024),
                                 (28, 9), (76, 32), (80, 4), (108, 0x401008),
                                 (128, 28), (132, 3), (136, 0), (140, 1), (144, 0)):
            self.assertEqual(struct.unpack_from('<I', raw, offset)[0], expected)
        self.assertEqual(raw[84:88], b'DX10')
        self.assertEqual(len(raw), 349672)
        self.assertEqual(raw[148:], b''.join(parse_dds(raw)))

    def test_dds_rejects_srgb_arrays_bad_headers_and_truncated_mips(self):
        original = self.payloads['textures/detail.dds']
        for offset, bad in ((4, 125), (20, 1000), (28, 8), (76, 24), (128, 29),
                            (132, 4), (136, 4), (140, 2), (144, 3)):
            raw = bytearray(original); struct.pack_into('<I', raw, offset, bad)
            with self.assertRaises(ValueError):parse_dds(bytes(raw))
        for bad in (original[:147], original[:-1], original+b'\0'):
            with self.assertRaises(ValueError):parse_dds(bad)
        bad = bytearray(original); bad[151] = 0
        with self.assertRaises(ValueError):parse_dds(bytes(bad))

    def test_writer_rejects_incomplete_mips_and_nonopaque_packed_channels(self):
        levels = parse_dds(self.payloads['textures/flat.dds'])
        with self.assertRaises(ValueError):dds_bytes(levels[:-1])
        changed = list(levels); changed[-1] = bytes((128,128,255,0))
        with self.assertRaises(ValueError):dds_bytes(changed)
        with self.assertRaises(ValueError):normal_levels('unsupported-format')
        with self.assertRaises(ValueError):list(_vector_mips([0.0]*27, 3))

    def test_complete_asset_regeneration_is_byte_repeatable(self):
        second = self.directory/self._testMethodName/'again'
        result = prepare_material_textures(second)
        _, payloads = read_package(second/'package')
        self.assertEqual(payloads, self.payloads)
        self.assertEqual(result, self.report)
        self.assertEqual(hashlib.sha256(payloads['textures/flat.dds']).hexdigest(),
                         'ce82d560691c9fcd58ca30ba22f725e48b293048547e0f4c1a77f1ac360393d1')

    def test_payload_accounting_excludes_headers_and_driver_overhead(self):
        self.assertEqual(self.report['texture_payload_bytes_all_candidates'], 2097144)
        self.assertEqual(self.report['dds_file_bytes_all_candidates'], 2098032)
        self.assertEqual(self.report['package_file_bytes'], sum(map(len, self.payloads.values())))
        for kind in KINDS:
            data = self.report['candidates'][kind]
            self.assertEqual(data['texture_payload_bytes'], 349524)
            self.assertEqual(data['file_bytes']-data['texture_payload_bytes'], 148)

    def test_fixture_contract_is_original_but_explicitly_unavailable(self):
        contract = fixture_contract()
        self.assertFalse(contract['original_kn5_available'])
        self.assertFalse(contract['authoring_export_load_workflow_verified'])
        self.assertFalse(contract['native_material_verified'])
        t, b, n = (contract[k] for k in ('proposed_tangent', 'proposed_bitangent', 'proposed_normal'))
        cross = [t[1]*b[2]-t[2]*b[1], t[2]*b[0]-t[0]*b[2], t[0]*b[1]-t[1]*b[0]]
        self.assertEqual(cross, n)
        self.assertEqual(self.report['native_decision'], 'NO-GO')

    def test_configuration_stays_disabled_and_contains_only_exact_owned_assignment(self):
        check_disabled_config(disabled_config())
        for bad in (disabled_config().replace('ACTIVE = 0','ACTIVE = 1'),
                    disabled_config().replace('material:RV0K_OWNED_SURFACE','material:?'),
                    disabled_config()+'SHADER = arbitrary\n',
                    disabled_config().replace('textures/flat.dds','../outside.dds')):
            with self.assertRaises(ValueError):check_disabled_config(bad)

    def test_package_tampering_and_unknown_files_are_rejected(self):
        folder = self.cloned_package(); (folder/'textures/detail.dds').write_bytes(b'changed')
        with self.assertRaises(ValueError):read_package(folder)
        (folder/'textures/detail.dds').write_bytes(self.payloads['textures/detail.dds'])
        (folder/'unknown.txt').write_text('do not remove')
        with self.assertRaises(ValueError):read_package(folder)
        self.assertEqual((folder/'unknown.txt').read_text(), 'do not remove')

    def test_package_native_gate_cannot_be_turned_on(self):
        folder = self.cloned_package(); manifest = json.loads((folder/'manifest.json').read_bytes())
        manifest['native_ready'] = True; (folder/'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):read_package(folder)

    def test_output_paths_and_recovery_targets_cannot_address_the_installation(self):
        for path in (ROOT.parent/'outside', ROOT/'docs', ROOT/'.local'):
            with self.assertRaises(ValueError):_workspace(path, local=True)
        with self.assertRaises(ValueError):prepare_material_textures(self.output)
        with self.assertRaises(ValueError):prepare_material_textures(ROOT/'assets-forbidden')
        with patch.object(Path, 'is_symlink', return_value=True):
            with self.assertRaises(ValueError):_no_links(self.package)

    def test_all_file_fault_points_recover_and_recovery_is_idempotent(self):
        output = self.directory/self._testMethodName/'rehearsal'
        report = rehearse_material_recovery(self.package, output)
        self.assertEqual(report['status'], 'passed')
        self.assertEqual(report['fault_cases'], 45)
        self.assertEqual(len(report['synthetic_selection_rejections']), 8)
        self.assertTrue(all(c['baseline_unchanged'] and c['active_component_absent'] for c in report['cases']))
        for flag in ('collision_preserved','drift_refused_and_preserved','unexpected_file_preserved','interrupted_retirement_recovered'):
            self.assertTrue(report[flag])
        self.assertFalse(report['native_material_recovery_validated'])
        self.assertEqual(read_package(self.package)[1], self.payloads)

    def test_interrupted_retirement_recovers_from_disk_without_in_memory_state(self):
        folder = self.scenario('complete')
        with self.assertRaises(SimulatedInterruption):recover_material_rehearsal(folder, interrupt_after_retire=True)
        self.assertFalse((folder/COMPONENT).exists())
        self.assertTrue((folder/RETIRED).exists())
        self.assertTrue(recover_material_rehearsal(folder)['baseline_unchanged'])

    def test_pending_file_drift_is_preserved_and_not_silently_removed(self):
        folder = self.scenario('partial:textures/detail.dds'); pending = folder/STAGE/'.pending'
        pending.write_bytes(b'unrelated replacement')
        with self.assertRaises(ValueError):recover_material_rehearsal(folder)
        self.assertEqual(pending.read_bytes(), b'unrelated replacement')
        self.assertFalse((folder/RETIRED).exists())

    def test_unexpected_managed_file_drift_is_not_retired(self):
        folder = self.scenario('complete'); file = folder/COMPONENT/'disabled.ini'
        file.write_bytes(b'preserve changes')
        with self.assertRaises(ValueError):recover_material_rehearsal(folder)
        self.assertEqual(file.read_bytes(), b'preserve changes')
        self.assertFalse((folder/RETIRED).exists())

    def test_changed_original_baseline_stops_recovery_before_touching_component(self):
        folder = self.scenario('complete'); original = folder/'baseline/original.ini'
        original.write_bytes(b'new baseline from external work')
        with self.assertRaises(ValueError):recover_material_rehearsal(folder)
        self.assertTrue((folder/COMPONENT).exists())
        self.assertEqual(original.read_bytes(), b'new baseline from external work')

    def test_selection_rejects_unknown_or_ambiguous_material_descriptors(self):
        baseline = synthetic_material_baseline(); self.assertTrue(selection_matches(baseline))
        for key, value in (('shader','fuPBR'),('material_matches',2),('mesh_matches',0),('normal_usage','damage_only'),('uv_basis_known',False)):
            invalid = copy.deepcopy(baseline); invalid[key] = value
            self.assertFalse(selection_matches(invalid))
        self.assertFalse(selection_matches({}))

    def test_missing_owner_and_redirected_journal_do_not_authorize_recovery(self):
        folder = self.scenario('complete'); marker = folder/COMPONENT/'.rv0k-owner.json'
        marker.write_bytes(b'wrong owner')
        with self.assertRaises(ValueError):recover_material_rehearsal(folder)
        journal = json.loads((folder/'journal.json').read_bytes())
        journal['package'] = '../outside'; (folder/'journal.json').write_text(json.dumps(journal))
        with self.assertRaises(ValueError):recover_material_rehearsal(folder)

    def test_missing_baseline_receipt_cannot_bypass_immutable_original_check(self):
        folder = self.scenario('complete'); journal = json.loads((folder/'journal.json').read_bytes())
        journal['baseline'] = {}; (folder/'journal.json').write_text(json.dumps(journal))
        with self.assertRaises(ValueError):recover_material_rehearsal(folder)
        self.assertTrue((folder/COMPONENT).exists())

    def test_orphan_journal_update_is_preserved_and_blocks_further_writes(self):
        folder = self.scenario('complete'); orphan = folder/'.journal-next'
        orphan.write_bytes(b'uncertain interrupted journal update')
        with self.assertRaises(FileExistsError):recover_material_rehearsal(folder)
        self.assertEqual(orphan.read_bytes(), b'uncertain interrupted journal update')
        self.assertEqual((folder/'baseline/original.ini').read_bytes(), b'[RV0K_SYNTHETIC_BASELINE]\nIMMUTABLE=1\n')
        self.assertTrue((folder/COMPONENT).exists())

    def test_reparse_attribute_is_rejected_even_if_not_reported_as_symlink(self):
        with patch.object(Path,'lstat',return_value=SimpleNamespace(st_file_attributes=0x400)), patch.object(Path,'is_symlink',return_value=False):
            with self.assertRaises(ValueError):_no_links(self.package)

    def test_cli_routes_only_offline_preparation_and_rehearsal(self):
        for args, target in ((['prepare-material-textures','--output','.local/test-unused'], 'prepare_material_textures'),
                             (['rehearse-material-recovery','--package','.local/package','--output','.local/test-unused'], 'rehearse_material_recovery')):
            with patch('restovisuals.__main__.'+target, return_value={'status':'passed','native_decision':'NO-GO'}) as mocked, patch('sys.stdout',new_callable=io.StringIO):
                self.assertEqual(main(args), 0); mocked.assert_called_once()
            with patch('restovisuals.__main__.'+target, return_value={'status':'failed'}), patch('sys.stdout',new_callable=io.StringIO):
                self.assertEqual(main(args), 4)
