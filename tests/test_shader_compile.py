import sys
import unittest
from pathlib import Path

from restovisuals.shader_compile import compile_hlsl, compile_prototype


@unittest.skipUnless(sys.platform == "win32", "Requires native Windows system HLSL compiler")
class ShaderCompileTests(unittest.TestCase):
    def test_both_encoding_entry_points_compile_as_sm5(self):
        path = Path(__file__).resolve().parents[1] / "shaders/RV_ColorPrototype.hlsl"
        result = compile_prototype(path)
        self.assertEqual([r["entry_point"] for r in result["results"]], ["PSLinear", "PSSrgb"])
        self.assertTrue(all(r["compiled_bytes"] > 0 and r["target"] == "ps_5_0" for r in result["results"]))
        self.assertFalse(result["gpu_executed"])
        self.assertFalse(result["csp_integration_validated"])

    def test_compiler_rejects_invalid_shader(self):
        with self.assertRaisesRegex(ValueError, "compilation failed"):
            compile_hlsl(b"float4 PSLinear() : SV_Target { return missing_symbol; }", "PSLinear")

    def test_include_processing_is_disabled(self):
        with self.assertRaisesRegex(ValueError, "compilation failed"):
            compile_hlsl(b'#include "not_allowed.hlsl"\nfloat4 PSLinear() : SV_Target { return 0; }', "PSLinear")
