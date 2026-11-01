"""CPU mathematical reference for the original isolated color shader.

Not a GPU execution test or a Pure calibration. Inputs must be finite.
"""

import math


WEIGHTS = (0.2126, 0.7152, 0.0722)


def decode_srgb(value):
    value = min(1.0, max(0.0, value))
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def encode_srgb(value):
    value = min(1.0, max(0.0, value))
    return 12.92 * value if value <= 0.0031308 else 1.055 * value ** (1 / 2.4) - 0.055


def transform_rgba(color, *, exposure_ev=0.0, shoulder_strength=0.0, saturation=1.0, encoding="scene_linear"):
    if len(color) != 4 or any(type(v) not in (int, float) or not math.isfinite(v) or abs(v) > 65504 for v in color):
        raise ValueError("RGBA requires four finite values within FP16 magnitude")
    params = (exposure_ev, shoulder_strength, saturation)
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in params):
        raise ValueError("Color parameters must be finite numbers")
    if not (-4 <= exposure_ev <= 4 and 0 <= shoulder_strength <= 1 and 0 <= saturation <= 1.5):
        raise ValueError("Color parameters outside shader contract")
    if encoding not in ("scene_linear", "srgb_display"):
        raise ValueError("Unknown color encoding")
    if (exposure_ev, shoulder_strength, saturation) == (0, 0, 1):
        ceiling = 1 if encoding == "srgb_display" else 65504
        return (*[min(ceiling, max(0.0, value)) for value in color[:3]], color[3])
    rgb = [decode_srgb(v) for v in color[:3]] if encoding == "srgb_display" else [max(0.0, v) for v in color[:3]]
    exposed = [v * 2**exposure_ev for v in rgb]
    luminance = sum(v * w for v, w in zip(exposed, WEIGHTS))
    compressed = [v / (1 + shoulder_strength * luminance) for v in exposed]
    grey = sum(v * w for v, w in zip(compressed, WEIGHTS))
    result = [min(65504, max(0.0, grey + saturation * (v - grey))) for v in compressed]
    if encoding == "srgb_display":
        result = [encode_srgb(v) for v in result]
    return (*result, color[3])
