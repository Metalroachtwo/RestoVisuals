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
from .gpu_windows import AdapterDescription, GUID, VideoMemoryInfo
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
            self.native_adapter = adapter
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

    def texture(self, width, height, format_id, usage, bind, cpu_access, packed=None, *, mip_payloads=None):
        if mip_payloads is not None:
            if (format_id != 10 or usage != 1 or width != height or width not in (256,512)
                    or len(mip_payloads) != width.bit_length() or packed != mip_payloads[0]
                    or any(not isinstance(data,bytes) or len(data)!=max(1,width>>i)**2*8
                           for i,data in enumerate(mip_payloads))):
                raise ValueError("Invalid bounded immutable mip chain")
            desc = TextureDescription(width,height,len(mip_payloads),1,format_id,SampleDescription(1,0),usage,bind,cpu_access,0)
            buffers = [ct.create_string_buffer(data) for data in mip_payloads]
            data = (InitialData * len(buffers))(*(InitialData(ct.cast(raw,PTR),max(1,width>>i)*8,len(mip_payloads[i]))
                                                   for i,raw in enumerate(buffers)))
            return self.create(5,"CreateTexture2D mips",[ct.POINTER(TextureDescription),ct.POINTER(InitialData)],
                               [ct.byref(desc),data])
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

    def memory_info(self):
        """A sample of this process's local segment, never system free VRAM/peak."""
        adapter3 = PTR()
        guid = GUID.from_string("645967a4-1392-4310-a798-8053ce3e93fd")
        try:
            status = _method(self.native_adapter, 0, HRESULT, ct.POINTER(GUID), ct.POINTER(PTR))(
                self.native_adapter, ct.byref(guid), ct.byref(adapter3))
            if status < 0 or not adapter3.value:
                return {"status": "unavailable"}
            info = VideoMemoryInfo()
            status = _method(adapter3, 14, HRESULT, U32, U32, ct.POINTER(VideoMemoryInfo))(
                adapter3, 0, 0, ct.byref(info))
            if status < 0:
                return {"status": "unavailable"}
            return {"status": "measured", "scope": "calling_process_local_segment_node0",
                    "budget_bytes": info.budget, "current_usage_bytes": info.usage}
        finally:
            if adapter3.value:
                _method(adapter3, 2, U32)(adapter3)

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


def execute_texture(session, shaders, width, height, format_name, entry, parameters, packed, *, draws=1, warmup=0,
                    material_texture_size=None, material_mips=None, material_filter=None, material_wrap=False,
                    fixture_parameters=None, roughness_compensation=0):
    """Shared bounded dispatch/readback for both the small oracle and visual demo."""
    if (any(type(v) is not int for v in (width, height, draws, warmup))
            or not 8 <= width <= 1920 or not 8 <= height <= 1080
            or not 1 <= draws <= 5 or not 0 <= warmup <= 2):
        raise ValueError("Texture execution exceeds diagnostic bounds")
    procedural = entry in ("PSMaterial", "PSMaterialNormals", "PSFixtureCoordinates")
    textured_material = material_texture_size is not None
    if textured_material and (not procedural or type(material_texture_size) is not int
                              or material_texture_size not in (256, 512)):
        raise ValueError("Only the bounded 256/512 material fixtures are supported")
    if format_name not in ("rgba32f", "rgba16f") or entry not in ("PSLinear", "PSSrgb", "PSMaterial", "PSMaterialNormals", "PSFixtureCoordinates"):
        raise ValueError("Unsupported validation format or entry")
    filters = {None:(0x15,1),"point":(0,1),"bilinear":(0x14,1),"trilinear":(0x15,1),
               "aniso2":(0x55,2),"aniso4":(0x55,4),"aniso8":(0x55,8),"aniso16":(0x55,16)}
    if material_filter not in filters or type(material_wrap) is not bool:
        raise ValueError("Unsupported material sampler")
    if not textured_material and (material_mips is not None or material_filter is not None or material_wrap):
        raise ValueError("Texture options require the bounded material input")
    if fixture_parameters is not None:
        if (not procedural or len(fixture_parameters)!=4
                or any(type(v) not in (int,float) or not math.isfinite(v) for v in fixture_parameters)
                or not 0<=fixture_parameters[0]<=1 or not .1<=fixture_parameters[1]<=1
                or abs(fixture_parameters[0]**2+fixture_parameters[1]**2-1)>.00002
                or not 1<=fixture_parameters[2]<=12 or abs(fixture_parameters[3])>2):
            raise ValueError("Invalid pinhole fixture")
    if (entry=="PSFixtureCoordinates" and fixture_parameters is None
            or type(roughness_compensation) not in (int,float) or roughness_compensation not in (0,1)
            or roughness_compensation and fixture_parameters is None):
        raise ValueError("Invalid fixture or variance compensation")
    if len(parameters) != 3:
        raise ValueError("Expected three color parameters")
    if procedural:
        if (any(type(v) not in (int, float) or not math.isfinite(v) for v in parameters)
                or not 0 <= parameters[0] <= 1 or not 0 <= parameters[1] <= 1
                or parameters[2] not in (-1, 1) or (not textured_material and packed is not None)):
            raise ValueError("Invalid procedural material parameters or unexpected input texture")
    else:
        transform_rgba((0, 0, 0, 1), encoding="scene_linear",
                       **dict(zip(("exposure_ev", "shoulder_strength", "saturation"), parameters)))
    format_id, pixel_code, bytes_per_pixel = (2, "4f", 16) if format_name == "rgba32f" else (10, "4e", 8)
    if not procedural and (not isinstance(packed, bytes) or len(packed) != width * height * bytes_per_pixel):
        raise ValueError("Packed texture length mismatch")
    if textured_material and (not isinstance(packed, bytes) or len(packed) != material_texture_size**2*8):
        raise ValueError("Packed compact material texture length mismatch")
    if material_mips is not None and (len(material_mips)!=material_texture_size.bit_length()
            or packed!=material_mips[0] or any(not isinstance(data,bytes) or len(data)!=max(1,material_texture_size>>i)**2*8
                                             for i,data in enumerate(material_mips))):
        raise ValueError("Malformed bounded mip payload")
    support = U32()
    _check(_method(session.device, 29, HRESULT, U32, ct.POINTER(U32))(session.device, format_id, ct.byref(support)), "CheckFormatSupport")
    if support.value & (0x20 | 0x200 | 0x4000) != (0x20 | 0x200 | 0x4000):
        raise ValueError("Required texture/sample/render-target format support missing")
    if textured_material:
        _check(_method(session.device, 29, HRESULT, U32, ct.POINTER(U32))(
            session.device, 10, ct.byref(support)), "Check material RGBA16F support")
        if support.value & (0x20 | 0x200) != (0x20 | 0x200):
            raise ValueError("Material RGBA16F sampling support missing")
        if material_mips is not None and not support.value & 0x1000:
            raise ValueError("Material mip support missing")
    resource_mark = len(session.owned)
    input_bytes = sum(map(len,material_mips)) if material_mips is not None else material_texture_size**2*8 if textured_material else 0
    result = {"entry": entry, "format": format_name, "pixels": width * height,
              "parameters": list(parameters), "draws": draws, "warmup_draws": warmup,
              "declared_texture_payload_bytes": width * height * bytes_per_pixel * (2 if procedural else 3)
                  + input_bytes,
              "material_texture_payload_bytes": input_bytes,
              "material_mip_levels":len(material_mips) if material_mips is not None else 1,
              "material_filter":material_filter,"material_address":"wrap" if material_wrap else "clamp",
              "max_anisotropy":filters[material_filter][1] if textured_material else 1,
              "fixture_parameters":list(fixture_parameters) if fixture_parameters is not None else None,
              "roughness_compensation":roughness_compensation,
              "input_texture_allocated": not procedural or textured_material, "constant_buffer_payload_bytes":32 if fixture_parameters is not None else 16,
              "driver_allocation_measured": False,
              "memory_before": session.memory_info(), "owned_com_references_before": resource_mark}
    try:
        srv, sampler = PTR(), PTR()
        if not procedural or textured_material:
            source = session.texture(material_texture_size if textured_material else width,
                                     material_texture_size if textured_material else height,
                                     10 if textured_material else format_id, 1, 8, 0, packed,
                                     **({"mip_payloads":material_mips} if material_mips is not None else {}))
            srv = session.create(7, "CreateShaderResourceView", [PTR, PTR], [source, None])
        output = session.texture(width, height, format_id, 0, 32, 0)
        staging = session.texture(width, height, format_id, 3, 0, 0x20000)
        rtv = session.create(9, "CreateRenderTargetView", [PTR, PTR], [output, None])
        values = (*parameters,roughness_compensation,*(fixture_parameters or ()))
        constants = (ct.c_float * len(values))(*values)
        desc = BufferDescription(ct.sizeof(constants), 1, 4, 0, 0, 0)
        initial = InitialData(ct.cast(constants, PTR), 0, 0)
        buffer = session.create(3, "CreateBuffer", [ct.POINTER(BufferDescription), ct.POINTER(InitialData)],
                                [ct.byref(desc), ct.byref(initial)])
        if not procedural or textured_material:
            address = 1 if material_wrap else 3
            sampler_desc = SamplerDescription(filters[material_filter][0] if textured_material else 0,
                                              address,address,address,0,filters[material_filter][1],8,
                                              (ct.c_float * 4)(), 0, 3.402823466e38)
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
        for _ in range(warmup):
            _method(context, 13, None, U32, U32)(context, 3, 0)
        _method(context, 27, None, PTR)(context, disjoint)
        _method(context, 28, None, PTR)(context, start)
        for _ in range(draws):
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
        result.update({"mapped_row_pitch_bytes": row_pitch, "memory_resources_live": session.memory_info(),
                       "gpu_timestamp_disjoint": bool(clock.disjoint),
                       "gpu_timestamp_start": begin_ticks, "gpu_timestamp_end": end_ticks,
                       "gpu_timestamp_frequency_hz": clock.frequency,
                       "gpu_duration_ms": (end_ticks - begin_ticks) * 1000 / clock.frequency
                       if not clock.disjoint and clock.frequency > 0 and end_ticks >= begin_ticks else None,
                       "timing_scope": "bounded_synthetic_draw_batch_excludes_upload_readback_not_game_performance"})
    finally:
        _method(session.context, 110, None)(session.context)
        session.release_since(resource_mark)
        _method(session.context, 111, None)(session.context)
        result["owned_com_references_after"] = len(session.owned)
        result["memory_after_release"] = session.memory_info()
    return raw, result


def _render_case(session, shaders, width, height, format_name, entry, parameters):
    pixel_code = "<4f" if format_name == "rgba32f" else "<4e"
    packed = b"".join(struct.pack(pixel_code, *pixel)
                      for pixel in fixture_pixels(width * height, display=entry == "PSSrgb"))
    raw, result = execute_texture(session, shaders, width, height, format_name, entry, parameters, packed)
    uploaded, actual = list(struct.iter_unpack(pixel_code, packed)), list(struct.iter_unpack(pixel_code, raw))
    identity = tuple(parameters) == (0, 0, 1)
    if identity:
        expected = uploaded
    else:
        params = dict(zip(("exposure_ev", "shoulder_strength", "saturation"),
                          [ct.c_float(value).value for value in parameters]))
        expected = [transform_rgba(pixel, encoding="srgb_display" if entry == "PSSrgb" else "scene_linear", **params)
                    for pixel in uploaded]
        expected = [struct.unpack(pixel_code, struct.pack(pixel_code, *pixel)) for pixel in expected]
    result.update(compare_pixels(actual, expected, strict_identity=identity, format_name=format_name))
    return result


def compile_validation_program(source_path: Path, *, pixel_entries=("PSLinear", "PSSrgb")):
    source = source_path.read_bytes()
    vertex_path = Path(__file__).resolve().parents[1] / "shaders/RV_FullscreenValidation.hlsl"
    vertex_source = vertex_path.read_bytes()
    bytecode, compilation = {}, []
    programs = [("VSFullscreen", "vs_5_0", vertex_source)] + [(entry, "ps_5_0", source) for entry in pixel_entries]
    for entry, target, code in programs:
        binary, metadata = compile_bytecode(code, entry, target)
        bytecode[entry] = binary
        compilation.append(metadata)
    metadata = {"schema_version": 1, "execution_scope": "isolated_native_d3d11", "gameplay_validated": False,
              "csp_integration_validated": False, "source_sha256": hashlib.sha256(source).hexdigest(),
              "vertex_sha256": hashlib.sha256(vertex_source).hexdigest(),
              "window_created": False, "swap_chain_created": False, "compilation": compilation}
    return bytecode, metadata


def validate_gpu_shader(adapter_index, source_path: Path, *, width=63, height=31):
    if any(type(value) is not int or not 8 <= value <= 256 for value in (width, height)):
        raise ValueError("Validation dimensions must be integers from 8 to 256")
    bytecode, result = compile_validation_program(source_path)
    result.update({"width": width, "height": height, "identity_cases": [], "color_cases": [], "status": "not_executed"})
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
