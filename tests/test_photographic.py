import math
import sys
from dataclasses import replace
from pathlib import Path
import unittest
from restovisuals.photographic import Settings, presets, process, transition, controlled, shader_source, filter_ini
from restovisuals.shader_compile import compile_hlsl

class PhotographicTests(unittest.TestCase):
    def test_disabled_and_neutral_are_exact_in_both_encodings(self):
        for encoding,pixel in [('linear_rec709',(15,.000001,.18,.37)),('srgb_rec709',(.8,.00001,.18,.37))]:
            self.assertEqual(process(pixel,Settings(),encoding=encoding),pixel)
            self.assertEqual(process(pixel,presets()['warm'],encoding=encoding,enabled=False),pixel)
            self.assertEqual(process(pixel,replace(presets()['cool'],intensity=0),encoding=encoding),pixel)

    def test_full_presets_preserve_black_and_finite_boundaries(self):
        for setting in presets().values():
            self.assertEqual(process((0,0,0,.5),setting),(0,0,0,.5))
            for pixel in [(65504,0,0,0),(.000001,)*3+(1,),(.18,)*3+(.3,),(65504,)*3+(1,)]:
                result=process(pixel,setting)
                self.assertTrue(all(math.isfinite(v) and 0<=v<=1 for v in result))
                self.assertEqual(result[3],pixel[3])

    def test_shadow_and_hdr_grey_ramps_are_monotonic_distinct(self):
        ramp=[0,1e-6,.0001,.001,.01,.05,.18,.72,1,2,4,16,100]
        for setting in presets().values():
            values=[process((v,v,v,1),setting)[0] for v in ramp]
            self.assertTrue(all(a<b for a,b in zip(values,values[1:])))
            self.assertLess(values[-1],1)

    def test_highlight_clipping_reduction_and_midgrey_anchor(self):
        s=Settings(highlight=1)
        self.assertAlmostEqual(process((.18,.18,.18,1),s)[0],.18)
        self.assertEqual(process((.72,.72,.72,1),s),(.72,.72,.72,1))
        output=[process((v,v,v,1),s)[0] for v in (1,2,4,16)]
        self.assertTrue(all(0<v<1 for v in output))
        self.assertEqual(process((4,2,1,.2),s)[0]/process((4,2,1,.2),s)[1],2)

    def test_exposure_white_balance_and_saturation(self):
        self.assertAlmostEqual(process((.1,.1,.1,1),Settings(exposure_ev=1))[0],.2)
        self.assertEqual(process((.2,.3,.4,1),Settings(saturation=0))[0],process((.2,.3,.4,1),Settings(saturation=0))[2])
        values={k:process((.3,.3,.3,1),v) for k,v in presets().items()}
        self.assertGreater(values['warm'][0],values['warm'][2])
        self.assertGreater(values['cool'][2],values['cool'][0])
        self.assertEqual(len(set(values.values())),3)

    def test_parameter_and_color_validation_even_when_disabled(self):
        for value in [float('nan'),float('inf'),True,'1']:
            with self.assertRaises(ValueError):Settings(exposure_ev=value)
            with self.assertRaises(ValueError):process((value,0,0,1),enabled=False)
        for pixel in [(-1,0,0,1),(0,0,0,2),(65505,0,0,1),(0,0,0)]:
            with self.assertRaises(ValueError):process(pixel)
        with self.assertRaises(ValueError):Settings(white_balance=(1,1))
        with self.assertRaises(ValueError):process((0,0,0,1),encoding='unknown')

    def test_transition_has_frame_rate_independent_settling(self):
        a,b=Settings(),presets()['cool']
        once=transition(a,b,.2)
        twice=transition(transition(a,b,.1),b,.1)
        self.assertAlmostEqual(once.contrast,twice.contrast,places=14)
        self.assertEqual(transition(a,b,0),a)
        with self.assertRaises(ValueError):transition(a,b,float('nan'))

    def test_control_defaults_preserve_each_preset_and_clamp_effective_range(self):
        for name,setting in presets().items():self.assertEqual(controlled(name),setting)
        self.assertEqual(controlled('cool',contrast=1.2).contrast,1.2)
        with self.assertRaises(ValueError):controlled('missing')
        with self.assertRaises(ValueError):controlled(intensity=-1)

    def test_deterministic_processing_and_continuous_knee(self):
        s=presets()['balanced'];pixel=(2,.3,.01,.75)
        self.assertEqual(process(pixel,s),process(pixel,s))
        a=process((.72-1e-7,)*3+(1,),Settings(highlight=1))[0]
        b=process((.72+1e-7,)*3+(1,),Settings(highlight=1))[0]
        self.assertLess(b-a,3e-7)

    def test_configs_have_no_new_bridge_or_custom_hdr_callback(self):
        text=filter_ini(presets()['balanced'])
        self.assertIn('[YEBIS]\nENABLED=1',text)
        self.assertNotIn('SCRIPTABLE',text)
        self.assertNotIn('onPostProcessing',text)

    @unittest.skipUnless(sys.platform == 'win32', 'System HLSL compiler requires Windows')
    def test_all_presets_and_neutral_compile_both_encoding_entries(self):
        for setting in [Settings(),*presets().values()]:
            for entry in ['PSLinear','PSSrgb']:
                self.assertGreater(compile_hlsl(shader_source(setting),entry)['compiled_bytes'],0)

if __name__=='__main__':unittest.main()
