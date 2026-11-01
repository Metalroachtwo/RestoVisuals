"""Original calibration charts through the existing isolated D3D11 renderer.

Exports only to a new directory under this checkout's ignored .local directory.
The PNGs are display previews of measured floating-point readback, not game art.
"""

from __future__ import annotations

import ctypes as ct
import hashlib
import html
import json
import math
import struct
import zlib
from pathlib import Path

from .color_reference import encode_srgb, transform_rgba
from .d3d11_validation import D3D11Session, compare_pixels, compile_validation_program, execute_texture


CHECKOUT_ROOT = Path(__file__).resolve().parents[1]
PROFILES = {"720p": (1280, 720), "1080p": (1920, 1080)}


def calibration_pixel(x, band, width, *, linear):
    """Six analytically defined rows; no external images or protected assets."""
    t = x / (width - 1)
    patches = [(0, 0, 0), (1, 1, 1), (1, 0, 0), (0, 1, 0),
               (0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    if band == 0:
        rgb = (t * (8 if linear else 1),) * 3
    elif band == 1:
        rgb = patches[min(7, x * 8 // width)]
    elif band == 2:
        rgb = (t, t * t, 1 - t)
    elif band == 3:
        rgb = (t * (0.02 if linear else 0.1),) * 3
    elif band == 4:
        rgb = [(0.18, 0.36, 0.72), (0.04045, 0.0031308, 0.5),
               (1e-6, 0.001, 32 if linear else 1),
               (65504 if linear else 1, 0.001, 1e-6)][min(3, x * 4 // width)]
    else:
        rgb = (float((x * 64 // width) % 2),) * 3
    return (*rgb, (x * 5 // width) / 4)


def calibration_texture(width, height, format_name, *, linear):
    code = "<4f" if format_name == "rgba32f" else "<4e"
    rows = [b"".join(struct.pack(code, *calibration_pixel(x, band, width, linear=linear))
                     for x in range(width)) for band in range(6)]
    return b"".join(rows[min(5, y * 6 // height)] for y in range(height))


def verify_readback(packed, raw, width, height, format_name, entry, parameters):
    """Full-frame identity/finite/alpha checks; a declared grid for color math."""
    code, step, channel_bytes = ("<4f", 16, 4) if format_name == "rgba32f" else ("<4e", 8, 2)
    if len(raw) != len(packed) or len(raw) != width * height * step:
        raise ValueError("Readback size mismatch")
    finite = all(math.isfinite(v) for pixel in struct.iter_unpack(code, raw) for v in pixel)
    alpha_exact = all(raw[3 * channel_bytes + i::step] == packed[3 * channel_bytes + i::step]
                      for i in range(channel_bytes))
    identity = tuple(parameters) == (0, 0, 1)
    result = {"all_pixels_finite": finite, "all_pixels_alpha_exact": alpha_exact,
              "full_frame_identity_exact": raw == packed if identity else None,
              "input_sha256": hashlib.sha256(packed).hexdigest(),
              "readback_sha256": hashlib.sha256(raw).hexdigest()}
    if identity:
        result["passed"] = finite and alpha_exact and result["full_frame_identity_exact"]
    else:
        # Include image edges, every row type, color/alpha boundaries, and 65 ramp positions.
        xs = sorted({round(i * (width - 1) / 64) for i in range(65)}
                    | {max(0, min(width - 1, width * i // n + delta))
                       for n in (4, 5, 8, 64) for i in range(n + 1) for delta in (-1, 0, 1)})
        ys = sorted({0, height - 1} | {max(0, min(height - 1, height * i // 6 + delta))
                                      for i in range(7) for delta in (-1, 0, 1)})
        indices = [y * width + x for y in ys for x in xs]
        params = dict(zip(("exposure_ev", "shoulder_strength", "saturation"),
                          [ct.c_float(v).value for v in parameters]))
        actual = [struct.unpack_from(code, raw, index * step) for index in indices]
        expected = [transform_rgba(struct.unpack_from(code, packed, index * step),
                                  encoding="scene_linear" if entry == "PSLinear" else "srgb_display",
                                  **params) for index in indices]
        expected = [struct.unpack(code, struct.pack(code, *pixel)) for pixel in expected]
        comparison = compare_pixels(actual, expected, strict_identity=False, format_name=format_name)
        comparison["sampled_pixels"] = len(indices)
        comparison["scope"] = "deterministic_edge_boundary_and_ramp_grid_not_every_pixel"
        result["color_comparison"] = comparison
        result["passed"] = finite and alpha_exact and comparison["passed"]
    return result


def png_bytes(raw, width, height, format_name, *, linear):
    """RGB8 preview: explicit linear-to-sRGB when requested, then display clip.

    Alpha is checked numerically and omitted from the preview. PNG contains only
    IHDR, sRGB, IDAT and IEND; no author, application or machine metadata.
    """
    code, step = ("<4f", 16) if format_name == "rgba32f" else ("<4e", 8)
    if len(raw) != width * height * step:
        raise ValueError("Preview buffer size mismatch")
    cache, scanlines = {}, []
    for y in range(height):
        row = raw[y * width * step:(y + 1) * width * step]
        if row not in cache:
            values = bytearray()
            for pixel in struct.iter_unpack(code, row):
                for v in pixel[:3]:
                    if not math.isfinite(v):
                        raise ValueError("Nonfinite preview data")
                    v = encode_srgb(v) if linear else v
                    values.append(round(max(0, min(1, v)) * 255))
            if len(cache) >= 32:
                cache.clear()
            cache[row] = b"\0" + bytes(values)
        scanlines.append(cache[row])

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">2I5B", width, height, 8, 2, 0, 0, 0))
            + chunk(b"sRGB", b"\0") + chunk(b"IDAT", zlib.compress(b"".join(scanlines), 6)) + chunk(b"IEND", b""))


def _output_path(output_dir):
    root = CHECKOUT_ROOT.resolve()
    local = (root / ".local").resolve()
    output = Path(output_dir).resolve()
    if not local.is_relative_to(root) or not output.is_relative_to(local) or output == local or output.exists():
        raise ValueError("Use a new output directory under this checkout's .local directory")
    return output


def _write_viewer(output, groups):
    sections = []
    for label, files in groups:
        images = "".join(f'<figure><figcaption>{caption}</figcaption><img alt="{caption}" src="{html.escape(name)}"></figure>'
                         for caption, name in files)
        sections.append(f"<section><h2>{html.escape(label)}</h2><div class=images>{images}</div></section>")
    output.joinpath("index.html").write_text("""<!doctype html><html lang=en><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>RestoVisuals controlled GPU demonstration</title>
<style>body{background:#181b20;color:#eee;font:16px system-ui;margin:2rem}p{max-width:85ch}.images{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}figure{margin:0}img{width:100%}section{margin-block:2rem}@media(max-width:800px){.images{grid-template-columns:1fr}}</style>
<h1>Controlled GPU demonstration</h1><p>Original synthetic charts on a separate D3D11 device. These are not game captures, Pure calibration, an artistic improvement claim, or gameplay performance evidence. Input, exact identity readback, and processed readback are shown. See <a href="report.json">report.json</a> for hashes and numerical results.</p>
<p>Rows: neutral ramp; primary/secondary patches; color ramp; near-black ramp; transfer breakpoints and range extremes; hard edges. Exposure +0.25 EV, shoulder 0.25, saturation 1.0. Floating-point textures use explicit shader conversion rather than automatic sRGB views. Linear previews are encoded to sRGB and clipped for RGB8 display; HDR extremes can clip. Alpha is tested separately.</p>
""" + "".join(sections), encoding="utf-8")


def demonstrate_gpu_shader(adapter_index, source_path, output_dir, *, profile="both"):
    if profile not in (*PROFILES, "both"):
        raise ValueError("Unknown demonstration profile")
    output = _output_path(output_dir)  # Reject unsafe/existing destinations before native access.
    bytecode, result = compile_validation_program(Path(source_path))
    output.mkdir(parents=True, exist_ok=False)
    result.update({"demonstration": "original_synthetic_calibration_v1", "cases": [], "artifacts": {},
                   "status": "not_executed", "game_visuals_validated": False,
                   "memory_scope": "sampled_process_local_segment_not_peak_or_physical_allocation",
                   "timing_scope": "five_draw_batch_after_one_warmup_excludes_upload_readback",
                   "preview": "RGB8_sRGB_display_clipped_alpha_omitted_no_personal_metadata"})
    profiles = list(PROFILES.items()) if profile == "both" else [(profile, PROFILES[profile])]
    configurations = [(name, width, height, fmt, entry) for name, (width, height) in profiles
                      for fmt in ("rgba32f", "rgba16f") for entry in ("PSLinear", "PSSrgb")]
    with D3D11Session(adapter_index) as session:
        result["adapter"] = session.adapter
        shaders = {entry: session.shader(12 if entry == "VSFullscreen" else 15, binary)
                   for entry, binary in bytecode.items()}
        for label, params in (("identity", (0, 0, 1)), ("processed", (0.25, 0.25, 1))):
            for name, width, height, fmt, entry in configurations:
                prefix = f"{name}-{fmt}-{entry}"
                packed = calibration_texture(width, height, fmt, linear=entry == "PSLinear")
                raw, case = execute_texture(session, shaders, width, height, fmt, entry, params,
                                            packed, draws=5, warmup=1)
                case.update(verify_readback(packed, raw, width, height, fmt, entry, params))
                case.update({"profile": name, "width": width, "height": height, "kind": label})
                case["passed"] &= case["owned_com_references_before"] == case["owned_com_references_after"]
                result["cases"].append(case)
                if not case["passed"]:
                    result["status"] = ("identity_failed_color_cases_not_executed" if label == "identity"
                                        else "color_readback_validation_failed")
                    break
                filename = prefix + f"-{label}.png"
                data = png_bytes(raw, width, height, fmt, linear=entry == "PSLinear")
                output.joinpath(filename).write_bytes(data)
                result["artifacts"][filename] = hashlib.sha256(data).hexdigest()
                if label == "identity":
                    data = png_bytes(packed, width, height, fmt, linear=entry == "PSLinear")
                    output.joinpath(prefix + "-input.png").write_bytes(data)
                    result["artifacts"][prefix + "-input.png"] = hashlib.sha256(data).hexdigest()
            if result["status"] != "not_executed":
                break
    result["owned_context_released"] = True
    if result["status"] == "not_executed":
        result["status"] = "passed"
        groups = []
        for name, _, _, fmt, entry in configurations:
            prefix = f"{name}-{fmt}-{entry}"
            groups.append((f"{name}, {fmt}, {entry}", [(caption, prefix + suffix + ".png") for caption, suffix in
                          (("Uploaded input", "-input"), ("Identity GPU readback", "-identity"),
                           ("Processed GPU readback", "-processed"))]))
        _write_viewer(output, groups)
    output.joinpath("report.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return result
