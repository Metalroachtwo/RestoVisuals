import ctypes as ct
import hashlib
import io
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import Mock, patch

from restovisuals.color_reference import transform_rgba
from restovisuals.__main__ import main
from restovisuals.d3d11_validation import D3D11Session, execute_texture
from restovisuals.gpu_demo import (calibration_texture, demonstrate_gpu_shader,
                                  png_bytes, verify_readback, _output_path)


class FullResolutionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_root = Path(__file__).resolve().parents[1] / ".local/test-tmp"
        cls.temp_root.mkdir(parents=True, exist_ok=True)

    def test_fixture_declares_encoding_and_covers_range_extremes(self):
        for fmt, code in (("rgba32f", "<4f"), ("rgba16f", "<4e")):
            linear = list(struct.iter_unpack(code, calibration_texture(128, 12, fmt, linear=True)))
            display = list(struct.iter_unpack(code, calibration_texture(128, 12, fmt, linear=False)))
            self.assertEqual(len(linear), 128 * 12)
            self.assertTrue(any(p[0] == 65504 for p in linear))
            self.assertTrue(any(p[0] == 8 for p in linear))
            self.assertTrue(all(0 <= v <= 1 for p in display for v in p))
            self.assertEqual({p[3] for p in linear}, {0, 0.25, 0.5, 0.75, 1})

    def test_full_frame_neutral_gate_rejects_single_pixel_drift(self):
        packed = calibration_texture(128, 24, "rgba32f", linear=True)
        raw = bytearray(packed)
        struct.pack_into("<f", raw, (5 * 128 + 71) * 16, 0.123)
        result = verify_readback(packed, bytes(raw), 128, 24, "rgba32f", "PSLinear", (0, 0, 1))
        self.assertFalse(result["passed"])
        self.assertFalse(result["full_frame_identity_exact"])
        self.assertTrue(result["all_pixels_alpha_exact"])

    def test_color_oracle_checks_both_encodings_and_precisions(self):
        for fmt, code in (("rgba32f", "<4f"), ("rgba16f", "<4e")):
            for entry in ("PSLinear", "PSSrgb"):
                with self.subTest(fmt=fmt, entry=entry):
                    packed = calibration_texture(128, 24, fmt, linear=entry == "PSLinear")
                    raw = b"".join(struct.pack(code, *transform_rgba(pixel, exposure_ev=0.25,
                                  shoulder_strength=0.25, encoding="scene_linear" if entry == "PSLinear" else "srgb_display"))
                                   for pixel in struct.iter_unpack(code, packed))
                    result = verify_readback(packed, raw, 128, 24, fmt, entry, (0.25, 0.25, 1))
                    self.assertTrue(result["passed"])
                    self.assertIsNone(result["full_frame_identity_exact"])
                    self.assertLess(result["color_comparison"]["sampled_pixels"], 128 * 24)
                    self.assertEqual(result["readback_sha256"], hashlib.sha256(raw).hexdigest())

    def test_full_frame_color_alpha_and_finite_checks_catch_unsampled_corruption(self):
        packed = calibration_texture(128, 24, "rgba32f", linear=False)
        for channel, value, field in ((3, 0.3, "all_pixels_alpha_exact"), (0, float("nan"), "all_pixels_finite")):
            raw = bytearray(packed)
            # Row 5 is absent from the declared edge/band-boundary probe grid.
            struct.pack_into("<f", raw, (5 * 128 + 71) * 16 + channel * 4, value)
            result = verify_readback(packed, bytes(raw), 128, 24, "rgba32f", "PSSrgb", (0, 0.25, 1))
            self.assertFalse(result[field])
            self.assertFalse(result["passed"])
            json.dumps(result, allow_nan=False)

    def test_png_has_valid_crc_explicit_srgb_and_known_preview_values(self):
        for linear, middle in ((False, 128), (True, 188)):
            raw = struct.pack("<4f", 0, 0.5, 1, 0)
            data = png_bytes(raw, 1, 1, "rgba32f", linear=linear)
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            chunks, offset = {}, 8
            while offset < len(data):
                size = struct.unpack_from(">I", data, offset)[0]
                kind, payload = data[offset + 4:offset + 8], data[offset + 8:offset + 8 + size]
                crc = struct.unpack_from(">I", data, offset + 8 + size)[0]
                self.assertEqual(crc, zlib.crc32(kind + payload))
                chunks[kind] = payload
                offset += size + 12
            self.assertEqual(set(chunks), {b"IHDR", b"sRGB", b"IDAT", b"IEND"})
            self.assertEqual(zlib.decompress(chunks[b"IDAT"]), bytes((0, 0, middle, 255)))

    def test_destination_bounds_reject_existing_and_outside_paths(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as directory, patch("restovisuals.gpu_demo.CHECKOUT_ROOT", Path(directory)):
            root = Path(directory)
            local = root / ".local"
            local.mkdir()
            for path in (root / "output", local, local / ".." / "outside"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    _output_path(path)
            self.assertEqual(_output_path(local / "new"), local / "new")
            with patch("restovisuals.gpu_demo.compile_validation_program") as compile_shader:
                with self.assertRaises(ValueError):
                    demonstrate_gpu_shader(0, "unread.hlsl", root / "output")
                compile_shader.assert_not_called()

    def test_later_identity_failure_prevents_all_color_draws_and_viewer(self):
        calls = []

        def execute(session, shaders, width, height, fmt, entry, params, packed, **kwargs):
            calls.append(params)
            raw = packed if len(calls) < 3 else bytes(len(packed))
            return raw, {"owned_com_references_before": 7, "owned_com_references_after": 7}

        with tempfile.TemporaryDirectory(dir=self.temp_root) as directory, \
             patch("restovisuals.gpu_demo.CHECKOUT_ROOT", Path(directory)), \
             patch("restovisuals.gpu_demo.PROFILES", {"tiny": (16, 12)}), \
             patch("restovisuals.gpu_demo.compile_validation_program", return_value=({}, {})), \
             patch("restovisuals.gpu_demo.D3D11Session") as session, \
             patch("restovisuals.gpu_demo.execute_texture", side_effect=execute):
            session.return_value.__enter__.return_value.adapter = {"synthetic": True}
            output = Path(directory) / ".local/demo"
            result = demonstrate_gpu_shader(0, "unread.hlsl", output)
            self.assertEqual(result["status"], "identity_failed_color_cases_not_executed")
            self.assertEqual(calls, [(0, 0, 1)] * 3)
            self.assertFalse((output / "index.html").exists())
            self.assertTrue((output / "report.json").is_file())
            self.assertTrue(result["owned_context_released"])
            session.return_value.__exit__.assert_called_once()

    def test_texture_execution_rejects_unbounded_requests_before_native_access(self):
        requests = [(1921, 1080, "rgba32f", "PSLinear", 1, 0),
                    (1920, 1081, "rgba32f", "PSLinear", 1, 0),
                    (8, 8, "rgba8", "PSLinear", 1, 0), (8, 8, "rgba32f", "Other", 1, 0),
                    (8, 8, "rgba32f", "PSLinear", 6, 0), (8, 8, "rgba32f", "PSLinear", 1, 3),
                    (True, 8, "rgba32f", "PSLinear", 1, 0), (8, 8, "rgba32f", "PSLinear", 1, 0)]
        for width, height, fmt, entry, draws, warmup in requests:
            with self.subTest(request=(width, height, fmt, entry, draws, warmup)), self.assertRaises(ValueError):
                execute_texture(None, {}, width, height, fmt, entry, (0, 0, 1), b"", draws=draws, warmup=warmup)

    def test_partial_native_allocation_failure_releases_only_case_resources(self):
        session = Mock()
        session.owned = [ct.c_void_p(1)] * 7
        session.memory_info.return_value = {"status": "unavailable"}

        def fail_texture(*args):
            session.owned.append(ct.c_void_p(2))
            raise ValueError("synthetic allocation failure")

        def method(pointer, slot, *signature):
            if slot == 29:
                def support(*args):
                    args[-1]._obj.value = 0x20 | 0x200 | 0x4000
                    return 0
                return support
            return lambda *args: None

        session.texture.side_effect = fail_texture
        session.release_since.side_effect = lambda mark: session.owned.__delitem__(slice(mark, None))
        with patch("restovisuals.d3d11_validation._method", side_effect=method), self.assertRaises(ValueError):
            execute_texture(session, {}, 8, 8, "rgba32f", "PSLinear", (0, 0, 1), bytes(8 * 8 * 16))
        session.release_since.assert_called_once_with(7)
        self.assertEqual(len(session.owned), 7)

    def test_unavailable_memory_query_releases_its_temporary_interface(self):
        session = D3D11Session.__new__(D3D11Session)
        session.native_adapter = ct.c_void_p(1)
        released = []

        def method(pointer, slot, *signature):
            if slot == 0:
                def query(*args):
                    args[-1]._obj.value = 2
                    return 0
                return query
            if slot == 14:
                return lambda *args: -1
            return lambda pointer: released.append(pointer.value)

        with patch("restovisuals.d3d11_validation._method", side_effect=method):
            self.assertEqual(session.memory_info(), {"status": "unavailable"})
        self.assertEqual(released, [2])

    def test_cli_reports_demo_numerical_failure_with_exit_four(self):
        with patch("restovisuals.__main__.demonstrate_gpu_shader", return_value={"status": "color_readback_validation_failed"}), \
             patch("sys.stdout", new_callable=io.StringIO) as output:
            status = main(["gpu-demo", "--adapter-index", "0", "--output", ".local/not-created"])
            self.assertEqual(status, 4)
            self.assertEqual(json.loads(output.getvalue())["status"], "color_readback_validation_failed")
