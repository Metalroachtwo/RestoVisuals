import ctypes as ct
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from restovisuals.d3d11_validation import (BufferDescription, D3D11Session, InitialData,
    RasterDescription, SamplerDescription, TextureDescription, TimestampDisjoint,
    Viewport, compare_pixels, fixture_pixels, validate_gpu_shader)


class ReadbackContractTests(unittest.TestCase):
    def test_identity_requires_exact_channels_even_for_small_drift(self):
        result = compare_pixels([(1, 0.00100001, 1e-6, 0.5)], [(1, 0.001, 1e-6, 0.5)],
                                strict_identity=True, format_name="rgba32f")
        self.assertFalse(result["passed"])
        self.assertEqual(result["failed_channels"], 1)
        self.assertTrue(result["alpha_exact"])

    def test_alpha_must_be_exact_for_color_cases(self):
        result = compare_pixels([(0.18, 0.2, 0.5, 0.500001)], [(0.18, 0.2, 0.5, 0.5)],
                                strict_identity=False, format_name="rgba32f")
        self.assertFalse(result["passed"])
        self.assertFalse(result["alpha_exact"])

    def test_nonfinite_gpu_data_is_failure_with_serializable_diagnostics(self):
        result = compare_pixels([(float("nan"), 0, 0, 1)], [(0, 0, 0, 1)],
                                strict_identity=True, format_name="rgba32f")
        self.assertFalse(result["passed"])
        json.dumps(result, allow_nan=False)

    def test_format_tolerance_does_not_hide_large_color_errors(self):
        result = compare_pixels([(1.1, 0, 0, 1)], [(1, 0, 0, 1)],
                                strict_identity=False, format_name="rgba16f")
        self.assertFalse(result["passed"])

    def test_readback_shape_mismatch_is_rejected(self):
        with self.assertRaises(ValueError):
            compare_pixels([(0, 0, 0, 1)], [], strict_identity=True, format_name="rgba32f")

    def test_synthetic_fixture_covers_hdr_small_channels_and_transfer_breakpoints(self):
        pixels = fixture_pixels(32)
        self.assertIn((65504, 0.001, 1e-6, 0.75), pixels)
        self.assertIn((0.04045, 0.0031308, 0.5, 0.125), pixels)
        self.assertTrue(all(0 <= v <= 1 for p in fixture_pixels(32, display=True) for v in p))

    def test_validation_dimensions_fail_before_native_or_file_access(self):
        for width, height in ((True, 31), (0, 31), (257, 31), (63, -1), (63, 31.5)):
            with self.subTest(size=(width, height)), self.assertRaises(ValueError):
                validate_gpu_shader(0, Path("not-read.hlsl"), width=width, height=height)

    def test_identity_failure_prevents_color_dispatch_and_closes_context(self):
        source = Path(__file__).resolve().parents[1] / "shaders/RV_ColorPrototype.hlsl"
        with patch("restovisuals.d3d11_validation.compile_bytecode", return_value=(b"synthetic", {})), \
             patch("restovisuals.d3d11_validation.D3D11Session") as session, \
             patch("restovisuals.d3d11_validation._render_case", return_value={"passed": False}) as draw:
            session.return_value.__enter__.return_value.adapter = {"synthetic": True}
            result = validate_gpu_shader(0, source)
            self.assertEqual(draw.call_count, 4)
            self.assertEqual(result["color_cases"], [])
            self.assertEqual(result["status"], "identity_failed_color_cases_not_executed")
            session.return_value.__exit__.assert_called_once()
            self.assertTrue(result["owned_context_released"])

    def test_query_timeout_is_bounded(self):
        session = D3D11Session.__new__(D3D11Session)
        session.context = ct.c_void_p(1)
        with patch("restovisuals.d3d11_validation._method", return_value=lambda *args: 1), \
             patch("restovisuals.d3d11_validation.time.monotonic", side_effect=[0, 2]), \
             patch("restovisuals.d3d11_validation.time.sleep") as sleep:
            with self.assertRaises(TimeoutError):
                session.get_query(ct.c_void_p(1), ct.c_uint64())
            sleep.assert_not_called()

    @unittest.skipUnless(sys.platform == "win32", "Windows SDK ABI")
    def test_native_resource_layouts_match_windows_sdk(self):
        expected = {TextureDescription: 44, BufferDescription: 24, RasterDescription: 40,
                    SamplerDescription: 52, TimestampDisjoint: 16, Viewport: 24}
        for structure, size in expected.items():
            self.assertEqual(ct.sizeof(structure), size)
        self.assertEqual(ct.sizeof(InitialData), 16 if ct.sizeof(ct.c_void_p) == 8 else 12)
