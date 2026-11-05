"""One lossless container adapter for the fixed original normal DDS contract."""

import struct

from .material_assets import parse_dds


def legacy_rgba8_dds(source: bytes) -> bytes:
    """Represent our opaque 256x256/nine-mip DXGI-28 pixels in a legacy DDS.

    Preserve every RGBA byte, mip, pitch and non-pixel-format header field.
    Little-endian words are 0xAABBGGRR: R/G/B/A masks are 0x000000ff,
    0x0000ff00, 0x00ff0000, 0xff000000 (D3DFMT_A8B8G8R8 ordering).
    No compression, color conversion, normalization or premultiplication occurs.
    A traditional header has no explicit transfer-function field; non-color
    intent comes from the validated UNORM source and the normal-resource role.
    This is not a general DDS converter or a claim of native compatibility.
    """
    levels = parse_dds(source)  # Reject other formats, sRGB, arrays and alpha drift.
    pixel_format = struct.pack('<8I', 32, 0x41, 0, 32,
                               0x000000ff, 0x0000ff00, 0x00ff0000, 0xff000000)
    header = source[:76] + pixel_format + source[108:128]
    return header + b''.join(levels)
