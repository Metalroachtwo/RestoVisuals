import ctypes as ct
import hashlib
import io
import json
import math
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock,patch

from restovisuals.__main__ import main
from restovisuals.d3d11_validation import execute_texture
from restovisuals.material_optimization import bake_material,compare_readbacks,optimize_material,sample_material,shader_sources
from restovisuals.material_reference import shade,shade_surface,surface


class MaterialOptimizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.packed=bake_material(256)

    def test_bake_texel_centres_match_validated_model_after_half_quantization(self):
        self.assertEqual(len(self.packed),256*256*8)
        for x,y in ((0,0),(71,153),(255,255)):
            value=struct.unpack_from('<4e',self.packed,(y*256+x)*8)
            expected=struct.unpack('<4e',struct.pack('<4e',*surface((x+.5)/256,(y+.5)/256)))
            self.assertEqual(value,expected)

    def test_sampling_clamps_and_renormalizes_and_preserves_disabled_baseline(self):
        for u,v in ((0,0),(1,1),(.137,.293)):
            p=sample_material(self.packed,256,u,v,(1,1,1))
            self.assertAlmostEqual(sum(x*x for x in p[:3]),1,places=12)
            self.assertTrue(.42<=p[3]<=.86)
            self.assertEqual(shade_surface(sample_material(self.packed,256,u,v,(0,0,1))),shade(u,v,0,0,1))

    def test_linear_sampling_interpolates_texels_not_nearest(self):
        a=struct.unpack_from('<4e',self.packed,(40*256+50)*8)
        b=struct.unpack_from('<4e',self.packed,(40*256+51)*8)
        sampled=sample_material(self.packed,256,51/256,40.5/256,(0,1,1))
        self.assertAlmostEqual(sampled[3],(a[3]+b[3])/2,places=12)

    def test_assembly_preserves_original_shader_and_exact_lighting_body(self):
        path=Path(__file__).resolve().parents[1]/'shaders/RV_MaterialRealism.hlsl'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),'16cd16d0c183cf09666eb993bd36c1428aeea78aa6e3d0e81a6033fa4dae317f')
        procedural,sampled=shader_sources()
        marker='float4 PSMaterial(PixelInput input)'
        self.assertEqual(procedural[procedural.index(marker):],sampled[sampled.index(marker):])
        self.assertIn('input.uv * 2.0',shader_sources(2)[0])
        self.assertIn('input.uv * 2.0',shader_sources(2)[1])

    def test_comparison_detects_difference_and_rejects_invalid_buffers(self):
        a=struct.pack('<4f',.1,.2,.3,1);b=struct.pack('<4f',.2,.2,.3,1)
        self.assertEqual(compare_readbacks(a,a)['all_pixel_rgb_rmse'],0)
        self.assertGreater(compare_readbacks(a,b)['all_pixel_rgb_rmse'],.05)
        for other in (b'',b[:-1],struct.pack('<4f',float('nan'),0,0,1)):
            with self.assertRaises(ValueError):compare_readbacks(a,other)

    def test_rejects_unbounded_texture_before_native_access(self):
        for size in (True,128,1024,0):
            with self.assertRaises(ValueError):execute_texture(None,{},8,8,'rgba32f','PSMaterial',(1,1,1),b'',material_texture_size=size)
        with self.assertRaises(ValueError):execute_texture(None,{},8,8,'rgba32f','PSMaterial',(1,1,1),b'',material_texture_size=256)
        for size,domain in ((128,1),(256,3),(True,1)):
            with self.assertRaises(ValueError):bake_material(size,domain)

    def test_compact_input_partial_allocation_failure_releases_only_owned_case(self):
        session=Mock();session.owned=[ct.c_void_p(1)]*7;session.memory_info.return_value={'status':'unavailable'}
        def allocation(*args):
            self.assertEqual(args,(256,256,10,1,8,0,self.packed))
            session.owned.append(ct.c_void_p(2));raise ValueError('synthetic input failure')
        def method(pointer,slot,*signature):
            if slot==29:
                def support(*args):args[-1]._obj.value=0x20|0x200|0x4000;return 0
                return support
            return lambda *args:None
        session.texture.side_effect=allocation;session.release_since.side_effect=lambda mark:session.owned.__delitem__(slice(mark,None))
        with patch('restovisuals.d3d11_validation._method',side_effect=method),self.assertRaises(ValueError):
            execute_texture(session,{},8,8,'rgba32f','PSMaterial',(1,1,1),self.packed,material_texture_size=256)
        session.release_since.assert_called_once_with(7);self.assertEqual(len(session.owned),7)

    def test_cli_routes_bounded_comparison_and_propagates_failure(self):
        with patch('restovisuals.__main__.optimize_material',return_value={'status':'failed'}) as run,patch('sys.stdout',new_callable=io.StringIO):
            self.assertEqual(main(['material-compare','--adapter-index','0','--output','.local/not-created','--texture-size','256']),4)
            self.assertEqual(run.call_args.kwargs,{'texture_size':256,'profile':'both','domain':1})

    def test_compile_failure_retains_receipt_without_creating_native_device(self):
        root=Path(__file__).resolve().parents[1]/'.local/test-tmp';root.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as directory, \
             patch('restovisuals.material_optimization.bake_material',return_value=self.packed), \
             patch('restovisuals.material_optimization.compile_validation_program',side_effect=ValueError('synthetic compile failure')), \
             patch('restovisuals.material_optimization.D3D11Session') as native:
            output=Path(directory)/'failed'
            with self.assertRaises(ValueError):optimize_material(0,output)
            native.assert_not_called()
            r=json.loads((output/'report.json').read_text())
            self.assertEqual(r['status'],'failed');self.assertFalse(r['native_device_created'])
            self.assertTrue(r['owned_context_released']);self.assertFalse((output/'index.html').exists())
