import ctypes
import sys
import unittest
from unittest.mock import patch

from restovisuals.gpu_windows import AdapterDescription, GUID, VideoMemoryInfo, probe_gpus


class GpuInteropTests(unittest.TestCase):
    def test_guid_uses_windows_little_endian_layout(self):
        value = GUID.from_string("770aae78-f26f-4dba-a829-253c83d1b387")
        self.assertEqual(bytes(value.data), bytes.fromhex("78ae0a776ff2ba4da829253c83d1b387"))

    def test_memory_info_has_four_64_bit_fields(self):
        self.assertEqual(ctypes.sizeof(VideoMemoryInfo), 32)
        self.assertEqual(VideoMemoryInfo.usage.offset, 8)

    @unittest.skipUnless(sys.platform == "win32", "Windows native adapter ABI")
    def test_adapter_layout_matches_windows_abi(self):
        self.assertEqual(AdapterDescription.vendor_id.offset, 256)
        self.assertEqual(ctypes.sizeof(AdapterDescription), 312 if ctypes.sizeof(ctypes.c_void_p) == 8 else 296)

    def test_non_windows_probe_fails_without_loading_libraries(self):
        with patch("restovisuals.gpu_windows.sys.platform", "unsupported"):
            with self.assertRaises(ValueError):
                probe_gpus()
