"""Independent byte/mask checks for the one traditional DDS representation."""
import hashlib
from pathlib import Path
import struct
import unittest

from restovisuals.dds_compatibility import legacy_rgba8_dds
from restovisuals.material_assets import dds_bytes

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT/'examples/phase0k-normal-probe/textures/flat.dds'
CANDIDATE = ROOT/'examples/phase0n-dds-compatibility/flat-legacy-rgba8.dds'


def decode_mask_pixel(word, masks):
    """Inspect channel masks independently of the production adapter/parser."""
    values = []
    for mask in masks:
        shift = (mask & -mask).bit_length()-1
        values.append((word & mask) >> shift)
    return tuple(values)


class DDSCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = CONTROL.read_bytes()
        cls.candidate = legacy_rgba8_dds(cls.source)

    def test_header_fields_masks_flags_and_extension_removal(self):
        src, dst = self.source, self.candidate
        self.assertEqual((len(src), len(dst)), (349672, 349652))
        self.assertEqual(dst[:76], src[:76])
        self.assertEqual(dst[108:128], src[108:128])
        self.assertEqual(struct.unpack_from('<8I',dst,76),
                         (32,0x41,0,32,0xff,0xff00,0xff0000,0xff000000))
        for offset, value in ((4,124),(8,0x2100f),(12,256),(16,256),
                              (20,1024),(24,0),(28,9),(108,0x401008)):
            self.assertEqual(struct.unpack_from('<I',dst,offset)[0],value)
        self.assertEqual(src[84:88],b'DX10')
        self.assertEqual(struct.unpack_from('<5I',src,128),(28,3,0,1,0))
        self.assertEqual(dst[128:],src[148:])

    def test_every_mip_pixel_and_opaque_alpha_decode_identically(self):
        masks = struct.unpack_from('<4I',self.candidate,92)
        old_offset, new_offset = 148,128
        total = 0
        for level in range(9):
            width = 256 >> level
            size = width*width*4
            old = self.source[old_offset:old_offset+size]
            new = self.candidate[new_offset:new_offset+size]
            self.assertEqual(old,new)
            for raw, word in zip(struct.iter_unpack('<4B',old),struct.iter_unpack('<I',new)):
                self.assertEqual(raw,decode_mask_pixel(word[0],masks))
                self.assertEqual(raw,(128,128,255,255))
            total += width*width; old_offset += size; new_offset += size
        self.assertEqual(total,87381)
        self.assertEqual((old_offset,new_offset),(len(self.source),len(self.candidate)))

    def test_asymmetric_in_memory_canary_detects_rgba_bgra_swap(self):
        # No second experiment file: distinct channels exercise only the mask ABI.
        pixels = (bytes((17,34,51,255)),bytes((201,7,63,255)))
        levels = tuple((pixels[i%2]*((256>>i)**2)) for i in range(9))
        source = dds_bytes(levels)
        converted = legacy_rgba8_dds(source)
        masks = struct.unpack_from('<4I',converted,92)
        offset = 128
        for i in range(9):
            word = int.from_bytes(converted[offset:offset+4],'little')
            self.assertEqual(decode_mask_pixel(word,masks),tuple(pixels[i%2]))
            self.assertNotEqual(decode_mask_pixel(word,masks),tuple(pixels[i%2][2::-1])+ (255,))
            offset += (256>>i)**2*4
        self.assertEqual(converted[128:],source[148:])

    def test_unsupported_or_changed_source_is_rejected(self):
        for offset,value in ((128,29),(132,4),(136,4),(140,2),(144,3),
                              (20,256),(28,8),(80,0x40),(84,0)):
            changed=bytearray(self.source)
            struct.pack_into('<I',changed,offset,value)
            with self.subTest(offset=offset),self.assertRaises(ValueError):
                legacy_rgba8_dds(bytes(changed))
        for changed in (self.source[:-1],self.source+b'x',self.source[:151]+b'\x00'+self.source[152:]):
            with self.assertRaises(ValueError):legacy_rgba8_dds(changed)
        with self.assertRaises(ValueError):legacy_rgba8_dds(bytearray(self.source))

    def test_checked_in_candidate_reproduces_and_control_remains_immutable(self):
        self.assertEqual(CANDIDATE.read_bytes(),self.candidate)
        self.assertEqual(CONTROL.read_bytes(),self.source)
        self.assertEqual(hashlib.sha256(self.source).hexdigest(),
                         'ce82d560691c9fcd58ca30ba22f725e48b293048547e0f4c1a77f1ac360393d1')
        self.assertNotEqual(hashlib.sha256(self.source).digest(),hashlib.sha256(self.candidate).digest())
