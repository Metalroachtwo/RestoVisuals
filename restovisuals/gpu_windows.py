"""Windowless DXGI/D3D11 diagnostics using only Windows system DLLs.

No process attachment, swap chain, shader dispatch, game launch, or settings
write. Memory usage belongs to this probe process, never Assetto Corsa.
"""

from __future__ import annotations

import ctypes as ct
import sys
import uuid


class GUID(ct.Structure):
    _fields_ = [("data", ct.c_ubyte * 16)]

    @classmethod
    def from_string(cls, value):
        return cls((ct.c_ubyte * 16).from_buffer_copy(uuid.UUID(value).bytes_le))


class LUID(ct.Structure):
    _fields_ = [("low", ct.c_uint32), ("high", ct.c_int32)]


class AdapterDescription(ct.Structure):
    _fields_ = [
        ("description", ct.c_wchar * 128),
        ("vendor_id", ct.c_uint32), ("device_id", ct.c_uint32),
        ("subsystem_id", ct.c_uint32), ("revision", ct.c_uint32),
        ("dedicated_video", ct.c_size_t), ("dedicated_system", ct.c_size_t),
        ("shared_system", ct.c_size_t), ("luid", LUID), ("flags", ct.c_uint32),
    ]


class VideoMemoryInfo(ct.Structure):
    _fields_ = [(name, ct.c_uint64) for name in ("budget", "usage", "available_reservation", "reservation")]


def _hresult(value):
    return f"0x{value & 0xFFFFFFFF:08x}"


def probe_gpus() -> dict:
    if sys.platform != "win32":
        raise ValueError("GPU probe requires Windows")
    # LOAD_LIBRARY_SEARCH_SYSTEM32 prevents a game-local ReShade/proxy DLL from
    # being loaded by this diagnostic. Never load by a supplied application path.
    dxgi = ct.WinDLL("dxgi.dll", winmode=0x800)
    d3d = ct.WinDLL("d3d11.dll", winmode=0x800)
    factory_id = GUID.from_string("770aae78-f26f-4dba-a829-253c83d1b387")
    adapter3_id = GUID.from_string("645967a4-1392-4310-a798-8053ce3e93fd")
    factory = ct.c_void_p()
    dxgi.CreateDXGIFactory1.argtypes = [ct.POINTER(GUID), ct.POINTER(ct.c_void_p)]
    dxgi.CreateDXGIFactory1.restype = ct.c_int32
    d3d.D3D11CreateDevice.argtypes = [ct.c_void_p, ct.c_uint32, ct.c_void_p, ct.c_uint32,
                                     ct.POINTER(ct.c_uint32), ct.c_uint32, ct.c_uint32,
                                     ct.POINTER(ct.c_void_p), ct.POINTER(ct.c_uint32), ct.POINTER(ct.c_void_p)]
    d3d.D3D11CreateDevice.restype = ct.c_int32

    def method(pointer, slot, result_type, *args):
        table = ct.cast(pointer, ct.POINTER(ct.POINTER(ct.c_void_p))).contents
        return ct.WINFUNCTYPE(result_type, ct.c_void_p, *args)(table[slot])

    def release(pointer):
        if pointer.value:
            method(pointer, 2, ct.c_uint32)(pointer)

    status = dxgi.CreateDXGIFactory1(ct.byref(factory_id), ct.byref(factory))
    if status < 0:
        raise ValueError("DXGI factory unavailable: " + _hresult(status))
    adapters = []
    try:
        enumerate_adapter = method(factory, 12, ct.c_int32, ct.c_uint32, ct.POINTER(ct.c_void_p))
        for index in range(32):
            adapter = ct.c_void_p()
            status = enumerate_adapter(factory, index, ct.byref(adapter))
            if status & 0xFFFFFFFF == 0x887A0002:  # DXGI_ERROR_NOT_FOUND
                break
            if status < 0:
                raise ValueError("Adapter enumeration failed: " + _hresult(status))
            try:
                desc = AdapterDescription()
                status = method(adapter, 10, ct.c_int32, ct.POINTER(AdapterDescription))(adapter, ct.byref(desc))
                if status < 0:
                    raise ValueError("Adapter descriptor unavailable: " + _hresult(status))
                software = bool(desc.flags & 2)
                record = {
                    "adapter_index": index, "description": desc.description,
                    "vendor_id": desc.vendor_id, "device_id": desc.device_id,
                    "is_software": software,
                    "luid": f"{desc.luid.high & 0xFFFFFFFF:08x}:{desc.luid.low:08x}",
                    "dedicated_video_memory_bytes": desc.dedicated_video,
                    "shared_system_memory_bytes": desc.shared_system,
                    "feature_level": None,
                    "d3d11_create_hresult": None,
                    "probe_process_memory": None,
                }
                if not software:
                    device, context, feature = ct.c_void_p(), ct.c_void_p(), ct.c_uint32()
                    try:
                        levels = (ct.c_uint32 * 6)(0xC100, 0xC000, 0xB100, 0xB000, 0xA100, 0xA000)
                        status = d3d.D3D11CreateDevice(adapter, 0, None, 0, levels, len(levels), 7,
                                                      ct.byref(device), ct.byref(feature), ct.byref(context))
                        if status & 0xFFFFFFFF == 0x80070057:  # Older runtime: E_INVALIDARG
                            release(context)
                            release(device)
                            context, device = ct.c_void_p(), ct.c_void_p()
                            fallback = (ct.c_uint32 * 3)(0xB000, 0xA100, 0xA000)
                            status = d3d.D3D11CreateDevice(adapter, 0, None, 0, fallback, len(fallback), 7,
                                                          ct.byref(device), ct.byref(feature), ct.byref(context))
                        record["d3d11_create_hresult"] = _hresult(status)
                        if status >= 0:
                            record["feature_level"] = f"{feature.value >> 12}_{(feature.value >> 8) & 15}"
                    finally:
                        release(context)
                        release(device)
                    adapter3 = ct.c_void_p()
                    status = method(adapter, 0, ct.c_int32, ct.POINTER(GUID), ct.POINTER(ct.c_void_p))(
                        adapter, ct.byref(adapter3_id), ct.byref(adapter3))
                    if status >= 0:
                        try:
                            info = VideoMemoryInfo()
                            status = method(adapter3, 14, ct.c_int32, ct.c_uint32, ct.c_uint32, ct.POINTER(VideoMemoryInfo))(
                                adapter3, 0, 0, ct.byref(info))
                            if status >= 0:
                                record["probe_process_memory"] = {
                                    "budget_bytes": info.budget, "current_usage_bytes": info.usage,
                                    "scope": "calling_probe_process_only",
                                }
                        finally:
                            release(adapter3)
                adapters.append(record)
            finally:
                release(adapter)
        else:
            raise ValueError("Adapter enumeration exceeded the diagnostic bound")
    finally:
        release(factory)
    return {
        "schema_version": 1, "source": "dxgi_d3d11_native_probe",
        "adapters": adapters, "game_adapter_identified": False,
        "game_memory_usage_bytes": None, "system_free_vram_bytes": None,
        "note": "Feature level is measured on each hardware adapter. The game adapter, memory pressure, bandwidth, and FPS remain unmeasured.",
    }
