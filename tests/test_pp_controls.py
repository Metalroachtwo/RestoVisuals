from pathlib import Path
import unittest
try:
    from lupa.luajit21 import LuaRuntime
except ImportError:
    LuaRuntime=None
from restovisuals.photographic import controlled, presets

@unittest.skipUnless(LuaRuntime, 'Existing optional isolated LuaJIT dependency required')
class PPControlsTests(unittest.TestCase):
    def setUp(self):
        self.lua=LuaRuntime(unpack_returned_tuples=True,register_eval=False,register_builtins=False)
        path=Path(__file__).resolve().parents[1]/'runtime/lua/restovisuals_pp_controls.lua'
        self.module=self.lua.execute(path.read_text())
        self.lua.execute('''
          values={}; calls=0; fail_create=false; fail_read=false
          function add(name,value,minimum,maximum,tooltip)
            calls=calls+1
            if fail_create and calls==3 then error('fixture creation failure') end
            values[name]=value
          end
          pure={script={ui={addSliderInteger=add,addSliderFloat=add,
            getValue=function(name) if fail_read then error('fixture read failure') end return values[name] end}}}
          capability={csp='0.3.0-preview361',build=3898,pure='3.50',mode='gamma'}
        ''')
        self.adapter=self.module.new(self.lua.globals().pure,self.lua.globals().capability)

    def test_import_and_construction_are_inert(self):
        self.assertEqual(self.lua.globals().calls,0)
        self.assertFalse(self.adapter.rendering_connected)
        self.assertEqual(self.adapter.read(self.adapter)[1],'not initialized')

    def test_initialization_once_has_exactly_seven_controls(self):
        self.assertTrue(self.adapter.init(self.adapter))
        self.assertEqual(self.lua.globals().calls,7)
        self.assertFalse(self.adapter.init(self.adapter)[0])
        self.assertEqual(self.lua.globals().calls,7)

    def test_all_preset_selections_map_to_same_validated_cpu_core(self):
        self.adapter.init(self.adapter)
        for index,name in enumerate(('balanced','warm','cool'),1):
            self.lua.globals()['values']['RestoVisuals preset']=index
            result=self.adapter.read(self.adapter)
            self.assertEqual(result['preset'],name)
            resolved=controlled(name,intensity=result['Intensity'],exposure_ev=result['Exposure EV'],
                highlight=result['Highlights'],shadow=result['Shadows'],saturation=result['Saturation'],contrast=result['Contrast'])
            self.assertEqual(resolved,presets()[name])

    def test_invalid_values_fail_closed(self):
        self.adapter.init(self.adapter)
        for value in [float('nan'),float('inf'),-1,2,'x']:
            self.lua.globals()['values']['RestoVisuals Intensity']=value
            result,error=self.adapter.read(self.adapter)
            self.assertIsNone(result)
            self.assertEqual(error,'invalid control')

    def test_wrong_mode_version_and_missing_host_are_rejected(self):
        self.lua.globals().capability.mode='lcs'
        result,error=self.module.new(self.lua.globals().pure,self.lua.globals().capability)
        self.assertIsNone(result)
        self.assertEqual(error,'unverified runtime capability')
        self.lua.globals().capability.mode='gamma'
        self.assertIsNone(self.module.new(self.lua.table(),self.lua.globals().capability)[0])

    def test_partial_creation_latches_no_retry(self):
        self.lua.globals().fail_create=True
        self.assertFalse(self.adapter.init(self.adapter)[0])
        before=self.lua.globals().calls
        self.assertFalse(self.adapter.init(self.adapter)[0])
        self.assertEqual(before,self.lua.globals().calls)

    def test_getter_failure_returns_error_without_touching_engine(self):
        self.adapter.init(self.adapter)
        self.lua.globals().fail_read=True
        self.assertIsNone(self.adapter.read(self.adapter)[0])
