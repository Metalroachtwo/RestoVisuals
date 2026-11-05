"""Compile original HLSL in memory with the system compiler, without rendering."""

import ctypes as ct
import hashlib
import sys
from pathlib import Path


def compile_bytecode(source: bytes, entry: str, target="ps_5_0") -> tuple[bytes, dict]:
    if sys.platform != "win32":
        raise ValueError("Native shader compilation requires Windows")
    if (entry, target) not in {("PSLinear", "ps_5_0"), ("PSSrgb", "ps_5_0"),
                              ("PSMaterial", "ps_5_0"), ("PSMaterialNormals", "ps_5_0"),
                              ("PSFixtureCoordinates", "ps_5_0"),
                              ("VSFullscreen", "vs_5_0")}:
        raise ValueError("Only prototype pixel and validation vertex entry points are allowed")
    compiler = ct.WinDLL("d3dcompiler_47.dll", winmode=0x800)
    compiler.D3DCompile.argtypes = [ct.c_void_p, ct.c_size_t, ct.c_char_p, ct.c_void_p, ct.c_void_p,
                                  ct.c_char_p, ct.c_char_p, ct.c_uint32, ct.c_uint32,
                                  ct.POINTER(ct.c_void_p), ct.POINTER(ct.c_void_p)]
    compiler.D3DCompile.restype = ct.c_int32
    code, errors = ct.c_void_p(), ct.c_void_p()

    def method(pointer, slot, restype):
        table = ct.cast(pointer, ct.POINTER(ct.POINTER(ct.c_void_p))).contents
        return ct.WINFUNCTYPE(restype, ct.c_void_p)(table[slot])

    def blob_data(pointer):
        address = method(pointer, 3, ct.c_void_p)(pointer)
        length = method(pointer, 4, ct.c_size_t)(pointer)
        return ct.string_at(address, length)

    # /Ges /Gis /O3 /WX. No debug symbols, includes, disk output or macros.
    flags = (1 << 11) | (1 << 13) | (1 << 15) | (1 << 18)
    source_buffer = ct.create_string_buffer(source)
    try:
        source_name = b"RV_MaterialRealism.hlsl" if entry.startswith("PSMaterial") else b"RV_ColorPrototype.hlsl"
        status = compiler.D3DCompile(source_buffer, len(source), source_name, None, None,
                                     entry.encode("ascii"), target.encode("ascii"), flags, 0, ct.byref(code), ct.byref(errors))
        if status < 0 or not code.value:
            raise ValueError("HLSL compilation failed" + (": " + blob_data(errors).decode("utf-8", errors="replace").rstrip("\x00") if errors.value else ""))
        compiled = blob_data(code)
        metadata = {"entry_point": entry, "target": target, "compiled_bytes": len(compiled),
                "bytecode_sha256": hashlib.sha256(compiled).hexdigest(), "hresult": f"0x{status & 0xFFFFFFFF:08x}",
                "warnings_as_errors": True, "debug_information": False}
        return compiled, metadata
    finally:
        for blob in (errors, code):
            if blob.value:
                method(blob, 2, ct.c_uint32)(blob)


def compile_hlsl(source: bytes, entry: str) -> dict:
    return compile_bytecode(source, entry)[1]


def compile_prototype(path: Path) -> dict:
    source = path.read_bytes()
    return {"schema_version": 1, "source_sha256": hashlib.sha256(source).hexdigest(),
            "compiler": "System32/d3dcompiler_47.dll", "minimum_shader_feature_level": "11_0",
            "gpu_executed": False, "csp_integration_validated": False,
            "results": [compile_hlsl(source, entry) for entry in ("PSLinear", "PSSrgb")]}
