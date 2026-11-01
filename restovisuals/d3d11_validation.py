"""Bounded, windowless execution of original shaders on an explicit adapter.

This owns a separate D3D11 device and textures. It never loads a game/DCC,
attaches to a process, creates a window/swap chain, or changes application files.
COM slots and structures follow the installed Windows SDK d3d11.h interfaces.
"""

from __future__ import annotations

import ctypes as ct
import hashlib
import math
import struct
import sys
import time
from pathlib import Path

from .color_reference import transform_rgba
from .gpu_windows import AdapterDescription, GUID
from .shader_compile import compile_bytecode


U32, PTR, HRESULT = ct.c_uint32, ct.c_void_p, ct.c_int32


class SampleDescription(ct.Structure):
    _fields_ = [("count", U32), ("quality", U32)]


class TextureDescription(ct.Structure):
    _fields_ = [(name, U32) for name in ("width", "height", "mips", "array_size", "format")] + [
        ("samples", SampleDescription)] + [(name, U32) for name in ("usage", "bind", "cpu_access", "misc")]


class InitialData(ct.Structure):
    _fields_ = [("data", PTR), ("pitch", U32), ("slice_pitch", U32)]


class BufferDescription(ct.Structure):
    _fields_ = [(name, U32) for name in ("bytes", "usage", "bind", "cpu_access", "misc", "stride")]


class MappedResource(ct.Structure):
    _fields_ = [("data", PTR), ("row_pitch", U32), ("depth_pitch", U32)]


class Viewport(ct.Structure):
    _fields_ = [(name, ct.c_float) for name in ("x", "y", "width", "height", "near", "far")]


class RasterDescription(ct.Structure):
    _fields_ = [("fill", U32), ("cull", U32), ("front_ccw", ct.c_int32), ("depth_bias", ct.c_int32),
                ("bias_clamp", ct.c_float), ("slope_bias", ct.c_float)] + [
                (name, ct.c_int32) for name in ("depth_clip", "scissor", "multisample", "antialiased")]


class SamplerDescription(ct.Structure):
    _fields_ = [(name, U32) for name in ("filter", "u", "v", "w")] + [
        ("mip_bias", ct.c_float), ("anisotropy", U32), ("comparison", U32),
        ("border", ct.c_float * 4), ("min_lod", ct.c_float), ("max_lod", ct.c_float)]


class QueryDescription(ct.Structure):
    _fields_ = [("query", U32), ("misc", U32)]


class TimestampDisjoint(ct.Structure):
    _fields_ = [("frequency", ct.c_uint64), ("disjoint", ct.c_int32)]


def _method(pointer, slot, result, *arguments):
    table = ct.cast(pointer, ct.POINTER(ct.POINTER(PTR))).contents
    return ct.WINFUNCTYPE(result, PTR, *arguments)(table[slot])


def _check(status, operation):
    if status < 0:
        raise ValueError(f"{operation}: HRESULT 0x{status & 0xFFFFFFFF:08x}")


class D3D11Session:
    """Own/release only resources on a freshly created D3D11 device."""

    def __init__(self, adapter_index):
        if sys.platform != "win32":
            raise ValueError("Native shader execution requires Windows")
        if type(adapter_index) is not int or not 0 <= adapter_index < 32:
            raise ValueError("Adapter index outside diagnostic bound")
        self.owned, self.context, self.device = [], PTR(), PTR()
        try:
            dxgi = ct.WinDLL("dxgi.dll", winmode=0x800)
            d3d = ct.WinDLL("d3d11.dll", winmode=0x800)
            factory = self._own(PTR())
            guid = GUID.from_string("770aae78-f26f-4dba-a829-253c83d1b387")
            dxgi.CreateDXGIFactory1.argtypes = [ct.POINTER(GUID), ct.POINTER(PTR)]
            dxgi.CreateDXGIFactory1.restype = HRESULT
            _check(dxgi.CreateDXGIFactory1(ct.byref(guid), ct.byref(factory)), "CreateDXGIFactory1")
            adapter = self._own(PTR())
            _check(_method(factory, 12, HRESULT, U32, ct.POINTER(PTR))(factory, adapter_index, ct.byref(adapter)), "EnumAdapters1")
            desc = AdapterDescription()
            _check(_method(adapter, 10, HRESULT, ct.POINTER(AdapterDescription))(adapter, ct.byref(desc)), "GetDesc1")
            if desc.flags & 2:
                raise ValueError("Software adapters are not hardware validation targets")
            feature = U32()
            levels = (U32 * 1)(0xB000)
            self._own(self.device)
            self._own(self.context)
            d3d.D3D11CreateDevice.argtypes = [PTR, U32, PTR, U32, ct.POINTER(U32), U32, U32,
                                            ct.POINTER(PTR), ct.POINTER(U32), ct.POINTER(PTR)]
            d3d.D3D11CreateDevice.restype = HRESULT
            _check(d3d.D3D11CreateDevice(adapter, 0, None, 0, levels, 1, 7, ct.byref(self.device),
                                        ct.byref(feature), ct.byref(self.context)), "D3D11CreateDevice")
            self.adapter = {"index": adapter_index, "description": desc.description, "vendor_id": desc.vendor_id,
                            "device_id": desc.device_id, "dedicated_bytes": desc.dedicated_video,
                            "luid": f"{desc.luid.high & 0xFFFFFFFF:08x}:{desc.luid.low:08x}",
                            "created_feature_level": f"{feature.value >> 12}_{(feature.value >> 8) & 15}"}
        except BaseException:
            self.close()
            raise

    def _own(self, pointer):
        self.owned.append(pointer)
        return pointer

    def release_since(self, count):
        while len(self.owned) > count:
            pointer = self.owned.pop()
            if pointer.value:
                _method(pointer, 2, U32)(pointer)
                pointer.value = None

    def close(self):
        if self.context.value:
            _method(self.context, 110, None)(self.context)  # ClearState on our own context
            _method(self.context, 111, None)(self.context)  # Flush only our own queue
        self.release_since(0)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def create(self, slot, operation, argument_types, arguments):
        pointer = self._own(PTR())
        status = _method(self.device, slot, HRESULT, *argument_types, ct.POINTER(PTR))(
            self.device, *arguments, ct.byref(pointer))
        _check(status, operation)
        if not pointer.value:
            raise ValueError(operation + " returned no resource")
        return pointer

    def texture(self, width, height, format_id, usage, bind, cpu_access, packed=None):
        desc = TextureDescription(width, height, 1, 1, format_id, SampleDescription(1, 0), usage, bind, cpu_access, 0)
        raw = ct.create_string_buffer(packed) if packed is not None else None
        data = InitialData(ct.cast(raw, PTR), len(packed) // height, len(packed)) if raw is not None else None
        return self.create(5, "CreateTexture2D", [ct.POINTER(TextureDescription), ct.POINTER(InitialData)],
                           [ct.byref(desc), ct.byref(data) if data else None])

    def shader(self, slot, bytecode):
        raw = ct.create_string_buffer(bytecode)
        return self.create(slot, "CreateShader", [PTR, ct.c_size_t, PTR], [raw, len(bytecode), None])

    def query(self, kind):
        desc = QueryDescription(kind, 0)
        return self.create(24, "CreateQuery", [ct.POINTER(QueryDescription)], [ct.byref(desc)])

    def get_query(self, query, result):
        deadline = time.monotonic() + 2
        while True:
            status = _method(self.context, 29, HRESULT, PTR, PTR, U32, U32)(
                self.context, query, ct.byref(result), ct.sizeof(result), 1)
            _check(status, "GetData")
            if status == 0:
                return result
            if time.monotonic() >= deadline:
                raise TimeoutError("GPU query exceeded the two-second bound")
            time.sleep(0.001)

    def read_texture(self, texture, width, height, bytes_per_pixel):
        mapped = MappedResource()
        deadline = time.monotonic() + 2
        while True:
            status = _method(self.context, 14, HRESULT, PTR, U32, U32, U32, ct.POINTER(MappedResource))(
                self.context, texture, 0, 1, 0x100000, ct.byref(mapped))  # READ, DO_NOT_WAIT
            if status & 0xFFFFFFFF != 0x887A000A:
                _check(status, "Map staging texture")
                break
            if time.monotonic() >= deadline:
                raise TimeoutError("GPU readback exceeded the two-second bound")
            time.sleep(0.001)
        try:
            if mapped.row_pitch < width * bytes_per_pixel or not mapped.data:
                raise ValueError("Invalid GPU row pitch")
            return (b"".join(ct.string_at(mapped.data + y * mapped.row_pitch, width * bytes_per_pixel) for y in range(height)),
                    mapped.row_pitch)
        finally:
            _method(self.context, 15, None, PTR, U32)(self.context, texture, 0)


def fixture_pixels(count, *, display=False):
    palette = [(0, 0, 0, 0), (1, 1, 1, 1), (0.18, 0.36, 0.72, 0.25),
               (1e-6, 0.001, 32, 0.5), (65504, 0.001, 1e-6, 0.75),
               (2, 4, 8, 1), (0.04045, 0.0031308, 0.5, 0.125), (16, 64, 4, 1)]
    result = []
    for index in range(count):
        if index % 2:
            t = (index % 257) / 256
            pixel = (t, t * t, 1 - t, (index % 5) / 4)
        else:
            pixel = palette[(index // 2) % len(palette)]
        if display:
            pixel = (*[min(1, value) for value in pixel[:3]], pixel[3])
        result.append(pixel)
    return result


def compare_pixels(actual, expected, *, strict_identity, format_name):
    if not actual or len(actual) != len(expected) or any(len(pixel) != 4 for pixel in [*actual, *expected]):
        raise ValueError("Readback pixel shape mismatch")
    absolute, relative = ((3e-5, 5e-6) if format_name == "rgba32f" else (0.002, 0.002))
    failures, max_error, squared_error = 0, 0.0, 0.0
    first_failures = []
    for index, (pixel, reference) in enumerate(zip(actual, expected)):
        for channel, (observed, target) in enumerate(zip(pixel, reference)):
            error = abs(observed - target)
            if not math.isfinite(observed) or not math.isfinite(target):
                error = float("inf")
            threshold = 0 if strict_identity or channel == 3 else absolute + relative * abs(target)
            max_error = max(max_error, error)
            squared_error += error * error
            if error > threshold:
                failures += 1
                if len(first_failures) < 8:
                    first_failures.append({"pixel": index, "channel": channel,
                                           "gpu": observed if math.isfinite(observed) else "nonfinite",
                                           "expected": target if math.isfinite(target) else "nonfinite"})
    return {"passed": failures == 0, "failed_channels": failures,
            "max_absolute_error": max_error if math.isfinite(max_error) else "nonfinite",
            "rms_error": math.sqrt(squared_error / (len(actual) * 4)) if math.isfinite(squared_error) else "nonfinite",
            "strict_identity": strict_identity, "alpha_exact": all(a[3] == b[3] for a, b in zip(actual, expected)),
            "nonidentity_absolute_tolerance": absolute, "nonidentity_relative_tolerance": relative,
            "first_failures": first_failures}


def _render_case(session, shaders, width, height, format_name, entry, parameters):
    format_id, pixel_code, bytes_per_pixel = (2, "4f", 16) if format_name == "rgba32f" else (10, "4e", 8)
    support = U32()
    _check(_method(session.device, 29, HRESULT, U32, ct.POINTER(U32))(session.device, format_id, ct.byref(support)), "CheckFormatSupport")
    if support.value & (0x20 | 0x200 | 0x4000) != (0x20 | 0x200 | 0x4000):
        raise ValueError("Required texture/sample/render-target format support missing")
    source_pixels = fixture_pixels(width * height, display=entry == "PSSrgb")
    packed = b"".join(struct.pack("<" + pixel_code, *pixel) for pixel in source_pixels)
    uploaded = list(struct.iter_unpack("<" + pixel_code, packed))
    resource_mark = len(session.owned)
    try:
        source = session.texture(width, height, format_id, 1, 8, 0, packed)  # immutable SRV
        output = session.texture(width, height, format_id, 0, 32, 0)
        staging = session.texture(width, height, format_id, 3, 0, 0x20000)
        srv = session.create(7, "CreateShaderResourceView", [PTR, PTR], [source, None])
        rtv = session.create(9, "CreateRenderTargetView", [PTR, PTR], [output, None])
        constants = (ct.c_float * 4)(*parameters, 0)
        desc = BufferDescription(16, 1, 4, 0, 0, 0)
        initial = InitialData(ct.cast(constants, PTR), 0, 0)
        buffer = session.create(3, "CreateBuffer", [ct.POINTER(BufferDescription), ct.POINTER(InitialData)],
                                [ct.byref(desc), ct.byref(initial)])
        sampler_desc = SamplerDescription(0, 3, 3, 3, 0, 1, 8, (ct.c_float * 4)(), 0, 3.402823466e38)
        sampler = session.create(23, "CreateSamplerState", [ct.POINTER(SamplerDescription)], [ct.byref(sampler_desc)])
        raster_desc = RasterDescription(3, 1, 0, 0, 0, 0, 1, 0, 0, 0)
        raster = session.create(22, "CreateRasterizerState", [ct.POINTER(RasterDescription)], [ct.byref(raster_desc)])
        viewport = Viewport(0, 0, width, height, 0, 1)
        context = session.context
        _method(context, 43, None, PTR)(context, raster)
        _method(context, 44, None, U32, ct.POINTER(Viewport))(context, 1, ct.byref(viewport))
        _method(context, 24, None, U32)(context, 4)  # triangle list
        _method(context, 11, None, PTR, PTR, U32)(context, shaders["VSFullscreen"], None, 0)
        _method(context, 9, None, PTR, PTR, U32)(context, shaders[entry], None, 0)
        _method(context, 8, None, U32, U32, ct.POINTER(PTR))(context, 0, 1, (PTR * 1)(srv.value))
        _method(context, 10, None, U32, U32, ct.POINTER(PTR))(context, 0, 1, (PTR * 1)(sampler.value))
        _method(context, 16, None, U32, U32, ct.POINTER(PTR))(context, 0, 1, (PTR * 1)(buffer.value))
        _method(context, 33, None, U32, ct.POINTER(PTR), PTR)(context, 1, (PTR * 1)(rtv.value), None)
        _method(context, 50, None, PTR, ct.POINTER(ct.c_float))(context, rtv, (ct.c_float * 4)(-1, -1, -1, -1))
        disjoint, start, end = session.query(3), session.query(2), session.query(2)
        _method(context, 27, None, PTR)(context, disjoint)
        _method(context, 28, None, PTR)(context, start)
        _method(context, 13, None, U32, U32)(context, 3, 0)
        _method(context, 28, None, PTR)(context, end)
        _method(context, 28, None, PTR)(context, disjoint)
        _method(context, 8, None, U32, U32, ct.POINTER(PTR))(context, 0, 1, (PTR * 1)())
        _method(context, 33, None, U32, ct.POINTER(PTR), PTR)(context, 0, None, None)
        _method(context, 47, None, PTR, PTR)(context, staging, output)
        _method(context, 111, None)(context)
        clock = session.get_query(disjoint, TimestampDisjoint())
        begin_ticks = session.get_query(start, ct.c_uint64()).value
        end_ticks = session.get_query(end, ct.c_uint64()).value
        raw, row_pitch = session.read_texture(staging, width, height, bytes_per_pixel)
        actual = list(struct.iter_unpack("<" + pixel_code, raw))
        identity = tuple(parameters) == (0, 0, 1)
        if identity:
            expected = uploaded
        else:
            params = dict(zip(("exposure_ev", "shoulder_strength", "saturation"), [float(value) for value in constants[:3]]))
            expected = [transform_rgba(pixel, encoding="srgb_display" if entry == "PSSrgb" else "scene_linear", **params) for pixel in uploaded]
            expected = [struct.unpack("<" + pixel_code, struct.pack("<" + pixel_code, *pixel)) for pixel in expected]
        result = compare_pixels(actual, expected, strict_identity=identity, format_name=format_name)
        result.update({"entry": entry, "format": format_name, "pixels": width * height,
                       "parameters": list(parameters), "mapped_row_pitch_bytes": row_pitch,
                       "declared_texture_payload_bytes": width * height * bytes_per_pixel * 3,
                       "driver_allocation_measured": False,
                       "gpu_timestamp_disjoint": bool(clock.disjoint),
                       "gpu_duration_ms": (end_ticks - begin_ticks) * 1000 / clock.frequency
                       if not clock.disjoint and clock.frequency > 0 and end_ticks >= begin_ticks else None,
                       "timing_scope": "one_small_synthetic_draw_including_pipeline_overhead_not_game_performance"})
        return result
    finally:
        _method(session.context, 110, None)(session.context)
        session.release_since(resource_mark)


def validate_gpu_shader(adapter_index, source_path: Path, *, width=63, height=31):
    if any(type(value) is not int or not 8 <= value <= 256 for value in (width, height)):
        raise ValueError("Validation dimensions must be integers from 8 to 256")
    source = source_path.read_bytes()
    vertex_path = Path(__file__).resolve().parents[1] / "shaders/RV_FullscreenValidation.hlsl"
    vertex_source = vertex_path.read_bytes()
    bytecode, compilation = {}, []
    for entry, target, code in (("VSFullscreen", "vs_5_0", vertex_source), ("PSLinear", "ps_5_0", source), ("PSSrgb", "ps_5_0", source)):
        binary, metadata = compile_bytecode(code, entry, target)
        bytecode[entry] = binary
        compilation.append(metadata)
    result = {"schema_version": 1, "execution_scope": "isolated_native_d3d11", "gameplay_validated": False,
              "csp_integration_validated": False, "source_sha256": hashlib.sha256(source).hexdigest(),
              "vertex_sha256": hashlib.sha256(vertex_source).hexdigest(), "width": width, "height": height,
              "window_created": False, "swap_chain_created": False, "compilation": compilation,
              "identity_cases": [], "color_cases": [], "status": "not_executed"}
    with D3D11Session(adapter_index) as session:
        result["adapter"] = session.adapter
        shaders = {entry: session.shader(12 if entry == "VSFullscreen" else 15, code) for entry, code in bytecode.items()}
        for format_name in ("rgba32f", "rgba16f"):
            for entry in ("PSLinear", "PSSrgb"):
                result["identity_cases"].append(_render_case(session, shaders, width, height, format_name, entry, (0, 0, 1)))
        if not all(case["passed"] for case in result["identity_cases"]):
            result["status"] = "identity_failed_color_cases_not_executed"
        else:
            for format_name in ("rgba32f", "rgba16f"):
                for entry, params in (("PSLinear", (1, 0.35, 1)), ("PSLinear", (0, 0.2, 0)), ("PSSrgb", (0.5, 0.25, 1.05))):
                    result["color_cases"].append(_render_case(session, shaders, width, height, format_name, entry, params))
            result["status"] = "passed" if all(case["passed"] for case in result["color_cases"]) else "nonidentity_numerical_failure"
    result["owned_context_released"] = True
    return result
