import ctypes as ct
import hashlib
import math
import struct
import sys
import io
import unittest
from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch

from restovisuals.d3d11_validation import D3D11Session,execute_texture
from restovisuals.material_mips import (build_mips,camera_parameters,decode_moment,
                                      periodic_height,periodic_surface,plane_coordinates,sample_moment)
from restovisuals.material_reference import shade_surface,surface
from restovisuals.texture_stability import change_residual,image_metrics,matrix_cases,stability_source,verify_frame
from restovisuals.__main__ import main


class TextureStabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.levels,cls.stats=build_mips(256)

    def test_periodic_normal_derivatives_match_height_finite_differences(self):
        for u,v in ((.137,.293),(.9993,.0002),(1.413,-.619)):
            e=1e-6;dx=(periodic_height(u+e,v)-periodic_height(u-e,v))/(2*e)
            dy=(periodic_height(u,v+e)-periodic_height(u,v-e))/(2*e)
            n=periodic_surface(u,v)
            self.assertAlmostEqual(-n[0]/n[2],dx,places=6)
            self.assertAlmostEqual(-n[1]/n[2],dy,places=6)

    def test_opposite_analytic_edges_are_periodic_and_original_is_not(self):
        for t in (.13,.37,.71):
            for a,b in ((periodic_surface(0,t),periodic_surface(1,t)),(periodic_surface(t,0),periodic_surface(t,1))):
                for x,y in zip(a,b):self.assertAlmostEqual(x,y,places=12)
        self.assertGreater(max(abs(x-y) for x,y in zip(surface(.3,0),surface(.3,1))),.001)

    def test_mip_payloads_and_mean_vector_variance_are_retained(self):
        self.assertEqual(len(self.levels),9)
        self.assertEqual(sum(map(len,self.levels)),699048)
        self.assertEqual([len(p) for p in self.levels],[max(1,256>>i)**2*8 for i in range(9)])
        self.assertLess(self.stats[-1]['mean_vector_length_range'][1],.9999)
        self.assertGreater(self.stats[-1]['mean_direction_variance'],.0001)
        base=list(struct.iter_unpack('<4e',self.levels[0]));coarse=struct.unpack('<4e',self.levels[-1])
        for i in range(4):self.assertLess(abs(sum(v[i] for v in base)/len(base)-coarse[i]),.0005)

    def test_wrap_samples_match_opposite_boundaries_at_every_mip(self):
        for i,p in enumerate(self.levels):
            n=256>>i
            for t in (.13,.31,.79):
                for a,b in ((sample_moment(p,n,0,t),sample_moment(p,n,1,t)),
                            (sample_moment(p,n,t,0),sample_moment(p,n,t,1))):
                    for x,y in zip(a,b):self.assertAlmostEqual(x,y,places=12)

    def test_direction_variance_compensation_is_explicit_and_unit_normal(self):
        m=(0,0,math.sqrt(.96),.4**4)
        normal=decode_moment(m,compensation=0);compensated=decode_moment(m,compensation=1)
        self.assertEqual(normal[:3],(0,0,1));self.assertAlmostEqual(normal[3],.4)
        self.assertAlmostEqual(compensated[3],(.4**4+.04)**.25)
        self.assertEqual(decode_moment(m,normal_amount=0,roughness_amount=0,compensation=1),(0,0,1,.64))

    def test_pinhole_center_hits_plane_target_and_view_changes_physically(self):
        for angle in (0,55,78):
            fixture=camera_parameters(angle,4)
            p,v=plane_coordinates(.5,.5,fixture)
            self.assertAlmostEqual(p[0],0,places=7);self.assertAlmostEqual(p[1],0,places=6)
            self.assertAlmostEqual(sum(x*x for x in v),1,places=12)
            self.assertAlmostEqual(v[2],math.cos(math.radians(angle)),places=6)
            top,_=plane_coordinates(.5,0,fixture);bottom,_=plane_coordinates(.5,1,fixture)
            self.assertGreater(top[1],bottom[1])

    def test_projection_unprojection_round_trip(self):
        for angle in (0,55,78):
            fixture=camera_parameters(angle,4);s,c,d,_=fixture
            for x,y in ((0,0),(.1,.2),(-.2,-.1)):
                q=(x,y+d*s,-d*c);depth=q[1]*s-q[2]*c
                u=.5*(1+q[0]/(depth*math.tan(math.radians(9))*16/9))
                v=.5*(1-(q[1]*c+q[2]*s)/(depth*math.tan(math.radians(9))))
                p,_=plane_coordinates(u,v,fixture)
                self.assertAlmostEqual(p[0],x,places=6);self.assertAlmostEqual(p[1],y,places=6)

    def test_immutable_mip_subresources_have_correct_pitches_and_contents(self):
        session=D3D11Session.__new__(D3D11Session)
        def create(slot,operation,types,args):
            desc=args[0]._obj;data=args[1]
            self.assertEqual(desc.mips,9)
            for i,packed in enumerate(self.levels):
                self.assertEqual(data[i].pitch,(256>>i)*8)
                self.assertEqual(ct.string_at(data[i].data,len(packed)),packed)
            return 'owned'
        session.create=create
        self.assertEqual(session.texture(256,256,10,1,8,0,self.levels[0],mip_payloads=self.levels),'owned')

    def test_malformed_mips_and_sampler_fixture_bounds_fail_before_native(self):
        requests=[{'material_mips':()}, {'material_filter':'aniso32'}, {'material_wrap':1},
                  {'fixture_parameters':(0,.5,2,0)}, {'fixture_parameters':(0,1,0,0)},
                  {'fixture_parameters':(0,1,2,float('nan'))},{'roughness_compensation':1}]
        for options in requests:
            with self.subTest(options=options),self.assertRaises(ValueError):
                execute_texture(None,{},64,36,'rgba32f','PSMaterial',(1,1,1),self.levels[0],material_texture_size=256,**options)
        session=D3D11Session.__new__(D3D11Session);session.create=Mock()
        with self.assertRaises(ValueError):session.texture(256,256,10,1,8,0,self.levels[0],mip_payloads=self.levels[:-1])
        session.create.assert_not_called()

    def test_frame_gates_catch_nonfinite_alpha_and_nonunit_normals(self):
        for pixel,normal in (((float('nan'),0,0,1),False),((.1,.1,.1,.5),False),((0,0,2,.64),True)):
            with self.assertRaises(ValueError):verify_frame(struct.pack('<4f',*pixel)*64,8,8,normal=normal)

    def test_quality_metric_is_full_frame_and_detail_ratio_not_larger_is_better(self):
        reference=struct.pack('<4f',.1,.1,.1,1)*64
        actual=bytearray(reference);struct.pack_into('<f',actual,17*16,.2)
        self.assertEqual(image_metrics(reference,reference,8,8)['rgb_rmse_vs_4x4'],0)
        self.assertGreater(image_metrics(actual,reference,8,8)['rgb_rmse_vs_4x4'],0)

    def test_original_shader_and_previous_default_lighting_remain_intact(self):
        p=Path(__file__).resolve().parents[1]/'shaders/RV_MaterialRealism.hlsl'
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),'16cd16d0c183cf09666eb993bd36c1428aeea78aa6e3d0e81a6033fa4dae317f')
        n=periodic_surface(.13,.37)
        self.assertEqual(shade_surface(n),shade_surface(n,view=(0,0,1)))
        src=stability_source('texture')
        self.assertIn('float4 fixture;',src);self.assertIn('float3 h = normalize(l+v);',src)
        self.assertIn('float specular = distribution*gl*gv*fresnel',src)

    def test_unbounded_bakes_and_camera_are_rejected(self):
        for size in (True,128,1024):
            with self.assertRaises(ValueError):build_mips(size)
        for a,d,p in ((81,2,0),(55,13,0),(55,2,3)):
            with self.assertRaises(ValueError):camera_parameters(a,d,p)

    def test_reference_change_residual_removes_constant_bias_but_detects_new_jump(self):
        a=struct.pack('<4f',.25,.25,.25,1)*64;b=struct.pack('<4f',.125,.125,.125,1)*64
        c=struct.pack('<4f',.1875,.1875,.1875,1)*64;d=struct.pack('<4f',.0625,.0625,.0625,1)*64
        self.assertEqual(change_residual(a,b,c,d)['reference_change_residual_rgb_rms'],0)
        changed=bytearray(a);struct.pack_into('<f',changed,17*16,.5)
        self.assertGreater(change_residual(changed,b,c,d)['reference_change_residual_rgb_rms'],0)

    def test_case_identifiers_are_unique_even_for_trilinear_confirmation(self):
        for view in ('front-near','moderate','grazing-far'):
            cases=matrix_cases(view,'confirm','trilinear',0)
            self.assertEqual(len(cases),len({c['label'] for c in cases}))

    def test_cli_routes_failure_without_external_side_effects(self):
        with patch('restovisuals.__main__.run_stability_matrix',return_value={'status':'failed'}) as run,patch('sys.stdout',new_callable=io.StringIO):
            self.assertEqual(main(['texture-stability','--adapter-index','0','--output','.local/unused']),4)
            run.assert_called_once()

    @unittest.skipUnless(sys.platform=='win32','Native HLSL compiler regression')
    def test_compiled_implicit_path_does_not_force_sample_level(self):
        from restovisuals.shader_compile import compile_bytecode
        from restovisuals.d3d11_validation import _method
        binary,_=compile_bytecode(stability_source('texture').encode(),'PSMaterial')
        compiler=ct.WinDLL('d3dcompiler_47.dll',winmode=0x800)
        compiler.D3DDisassemble.argtypes=[ct.c_void_p,ct.c_size_t,ct.c_uint32,ct.c_char_p,ct.POINTER(ct.c_void_p)]
        compiler.D3DDisassemble.restype=ct.c_int32
        blob=ct.c_void_p();raw=ct.create_string_buffer(binary)
        self.assertGreaterEqual(compiler.D3DDisassemble(raw,len(binary),0,None,ct.byref(blob)),0)
        try:
            address=_method(blob,3,ct.c_void_p)(blob);length=_method(blob,4,ct.c_size_t)(blob)
            disassembly=ct.string_at(address,length).decode('utf-8',errors='replace')
            self.assertIn('sample_indexable',disassembly);self.assertNotIn('sample_l_indexable',disassembly)
        finally:_method(blob,2,ct.c_uint32)(blob)
