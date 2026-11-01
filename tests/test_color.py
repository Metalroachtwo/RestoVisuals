import math
import unittest

from restovisuals.color_reference import decode_srgb, encode_srgb, transform_rgba


class ColorReferenceTests(unittest.TestCase):
    def test_linear_identity_black_dim_hdr_and_alpha(self):
        for color in ((0, 0, 0, 0.25), (1e-10, 2e-10, 3e-10, 0.5), (0.18, 0.3, 0.7, 1), (64, 32, 128, 0.75)):
            result = transform_rgba(color)
            for actual, expected in zip(result, color):
                self.assertAlmostEqual(actual, expected, places=12)

    def test_one_ev_doubles_uncompressed_light(self):
        self.assertEqual(transform_rgba((0.1, 0.2, 0.3, 1), exposure_ev=1), (0.2, 0.4, 0.6, 1))

    def test_identity_exactly_preserves_small_channels_beside_hdr_highlights(self):
        color = (65504, 0.001, 1e-6, 0.75)
        self.assertEqual(transform_rgba(color), color)
        color = (0.04045, 0.0031308, 1e-6, 0.5)
        self.assertEqual(transform_rgba(color, encoding="srgb_display"), color)

    def test_shoulder_is_monotonic_and_preserves_channel_ratios(self):
        previous = -1
        for step in range(1001):
            level = step / 10
            result = transform_rgba((level, level, level, 0.7), shoulder_strength=0.5)
            self.assertGreaterEqual(result[0], previous)
            previous = result[0]
            self.assertEqual(result[3], 0.7)
        result = transform_rgba((2, 4, 8, 1), shoulder_strength=0.5)
        self.assertAlmostEqual(result[1] / result[0], 2)
        self.assertAlmostEqual(result[2] / result[0], 4)

    def test_desaturation_equalizes_channels(self):
        result = transform_rgba((0.2, 0.5, 0.9, 1), saturation=0)
        self.assertEqual(result[0], result[1])
        self.assertEqual(result[1], result[2])

    def test_srgb_roundtrip_including_transfer_breakpoint(self):
        for value in [i / 1000 for i in range(1001)] + [0.04045]:
            self.assertAlmostEqual(encode_srgb(decode_srgb(value)), value, places=6)
            result = transform_rgba((value, value, value, 0.5), encoding="srgb_display")
            self.assertAlmostEqual(result[0], value, places=6)
            self.assertEqual(result[3], 0.5)

    def test_valid_finite_contract_stays_in_fp16_range(self):
        for level in (0, 1e-12, 0.18, 1, 100, 10000, 65504):
            for ev in (-4, 0, 4):
                for shoulder in (0, 0.5, 1):
                    for saturation in (0, 1, 1.5):
                        result = transform_rgba((level, level / 2, level / 4, 1), exposure_ev=ev,
                                                shoulder_strength=shoulder, saturation=saturation)
                        self.assertTrue(all(math.isfinite(v) and 0 <= v <= 65504 for v in result))

    def test_invalid_input_contract(self):
        for color in ((1, 2, 3), (1, 2, float("nan"), 1), (1, 2, float("inf"), 1), (1e10, 0, 0, 1)):
            with self.subTest(color=color), self.assertRaises(ValueError):
                transform_rgba(color)
        for params in ({"exposure_ev": 5}, {"shoulder_strength": -1}, {"saturation": 2},
                       {"exposure_ev": float("nan")}, {"encoding": "pure_gamma"}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                transform_rgba((0.1, 0.2, 0.3, 1), **params)
