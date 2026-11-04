import ctypes as ct
import io
import math
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from restovisuals.d3d11_validation import execute_texture
from restovisuals.material_demo import demonstrate_material, probe_positions, verify_material
from restovisuals.material_reference import height, shade, surface
from restovisuals.__main__ import main


class MaterialMathTests(unittest.TestCase):
    def test_cli_returns_failure_status_for_a_failed_material_run(self):
        with patch('restovisuals.__main__.demonstrate_material',return_value={'status':'failed'}), \
             patch('sys.stdout',new_callable=io.StringIO):
            self.assertEqual(main(['material-demo','--adapter-index','0','--output','.local/unused']),4)

    def test_normals_agree_with_independent_finite_difference_of_height(self):
        for u,v in ((.137,.293),(.413,.619),(.791,.827)):
            epsilon = 1e-6
            dx = (height(u+epsilon,v)-height(u-epsilon,v))/(2*epsilon)
            dy = (height(u,v+epsilon)-height(u,v-epsilon))/(2*epsilon)
            n = surface(u,v)
            self.assertAlmostEqual(-n[0]/n[2],dx,places=6)
            self.assertAlmostEqual(-n[1]/n[2],dy,places=6)

    def test_normalization_roughness_bounds_and_flat_baseline(self):
        for i in range(101):
            u,v = i/100,((i*37)%101)/100
            n = surface(u,v)
            self.assertAlmostEqual(sum(x*x for x in n[:3]),1,places=12)
            self.assertTrue(.42<=n[3]<=.86)
            self.assertEqual(surface(u,v,0,0),(0,0,1,.64))
            for side in (-1,1):
                self.assertEqual(shade(u,v,0,0,side),shade(.5,.5,0,0,side))

    def test_independent_controls_and_light_response(self):
        baseline = shade(.17,.31,0,0,1)
        self.assertNotEqual(baseline,shade(.17,.31,1,0,1))
        self.assertNotEqual(shade(.17,.31,1,0,1),shade(.17,.31,1,1,1))
        self.assertNotEqual(shade(.17,.31,1,1,-1),shade(.17,.31,1,1,1))
        self.assertEqual(surface(.17,.31,0,1)[:3],(0,0,1))
        self.assertEqual(surface(.17,.31,1,0)[3],.64)

    def test_full_frame_checks_detect_unsampled_nan_alpha_and_bad_normal(self):
        width,height = 80,64
        self.assertNotIn((7,5),probe_positions(width,height))
        for normals,channel,value in ((False,0,float('nan')),(False,3,.5),(True,2,2)):
            pixels = [surface((x+.5)/width,(y+.5)/height) if normals else shade((x+.5)/width,(y+.5)/height)
                      for y in range(height) for x in range(width)]
            raw = bytearray(b''.join(struct.pack('<4f',*p) for p in pixels))
            struct.pack_into('<f',raw,(5*width+7)*16+channel*4,value)
            self.assertFalse(verify_material(raw,width,height,(1,1,1),normals=normals)['passed'])

    def test_cpu_fixture_passes_oracle_and_size_mismatch_fails(self):
        raw=b''.join(struct.pack('<4f',*shade((x+.5)/16,(y+.5)/12)) for y in range(12) for x in range(16))
        self.assertTrue(verify_material(raw,16,12,(1,1,1))['passed'])
        with self.assertRaises(ValueError):verify_material(raw[:-1],16,12,(1,1,1))

    def test_material_bounds_reject_before_native_access(self):
        for parameters,packed in (((-1,0,1),None),((0,2,1),None),((0,0,0),None),
                                  ((True,0,1),None),((0,float('nan'),1),None),((0,0,1),b'')):
            with self.subTest(parameters=parameters),self.assertRaises(ValueError):
                execute_texture(None,{},8,8,'rgba32f','PSMaterial',parameters,packed)

    def test_new_path_releases_partial_allocation_and_uses_no_input_texture(self):
        session=Mock();session.owned=[ct.c_void_p(1)]*7
        session.memory_info.return_value={'status':'unavailable'}
        def allocation(*args):
            self.assertEqual(args,(8,8,2,0,32,0))
            session.owned.append(ct.c_void_p(2));raise ValueError('synthetic allocation failure')
        def method(pointer,slot,*signature):
            if slot==29:
                def support(*args):args[-1]._obj.value=0x20|0x200|0x4000;return 0
                return support
            return lambda *args:None
        session.texture.side_effect=allocation
        session.release_since.side_effect=lambda mark:session.owned.__delitem__(slice(mark,None))
        with patch('restovisuals.d3d11_validation._method',side_effect=method),self.assertRaises(ValueError):
            execute_texture(session,{},8,8,'rgba32f','PSMaterial',(1,1,1),None)
        self.assertEqual(len(session.owned),7)
        session.release_since.assert_called_once_with(7)

    def test_invalid_destination_precedes_shader_or_native_access(self):
        with patch('restovisuals.material_demo.compile_validation_program') as compiler:
            with self.assertRaises(ValueError):
                demonstrate_material(0,'not-read.hlsl',Path(__file__).parent/'outside')
            compiler.assert_not_called()

    def test_numerical_failure_stops_before_large_profiles_and_closes_context(self):
        root=Path(__file__).resolve().parents[1]/'.local/test-tmp';root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as directory, \
             patch('restovisuals.gpu_demo.CHECKOUT_ROOT',Path(directory)), \
             patch('restovisuals.material_demo.compile_validation_program',return_value=({},{})), \
             patch('restovisuals.material_demo.D3D11Session') as factory, \
             patch('restovisuals.material_demo.execute_texture',return_value=(bytes(64*48*16),{'owned_com_references_before':7,'owned_com_references_after':7})) as draw:
            session=factory.return_value.__enter__.return_value
            session.adapter={'vendor_id':0x1002,'device_id':0x731f};session.owned=[]
            output=Path(directory)/'.local/material'
            with self.assertRaises(ValueError):demonstrate_material(0,'unused',output)
            self.assertEqual(draw.call_count,1)
            factory.return_value.__exit__.assert_called_once()
            self.assertFalse((output/'index.html').exists())
            self.assertIn('failed',(output/'report.json').read_text())
