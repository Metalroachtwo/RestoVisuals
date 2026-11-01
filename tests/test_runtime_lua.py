import unittest
from pathlib import Path

try:
    from lupa.luajit21 import LuaRuntime
except ImportError:
    LuaRuntime = None


ROOT = Path(__file__).resolve().parents[1]
HARNESS = """
function make_fixture()
  local state = {version = '0.3.0-preview361', build = 3898, linear = false,
    registered = 0, disposed = 0, callback = nil, register_fail = false, dispose_fail = false}
  local host = {execution_scope = 'lua_contract_fixture', ac = {}, pure = {system = {}}}
  host.ac.getPatchVersion = function() return state.version end
  host.ac.getPatchVersionCode = function() return state.build end
  host.pure.system.isCSP_LCS = function() return state.linear end
  host.ac.getPerformanceCPUAndGPUTime = function() return 0.01, 0.02 end
  host.ac.onPostProcessing = function(callback)
    if state.register_fail then error('synthetic registration failure') end
    state.registered = state.registered + 1
    state.callback = callback
    return function()
      state.disposed = state.disposed + 1
      if state.dispose_fail then error('synthetic disposal failure') end
      state.callback = nil
    end
  end
  return host, state
end
"""


@unittest.skipUnless(LuaRuntime is not None, "Optional LuaJIT contract dependency; see requirements-lua-tests-win-cp314.txt")
class RuntimeLuaTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True, register_eval=False, register_builtins=False)
        self.module = self.lua.execute((ROOT / "runtime/lua/restovisuals_observer.lua").read_text())
        self.lua.execute(HARNESS)
        self.host, self.state = self.lua.globals().make_fixture()
        self.config = self.lua.table_from({"csp_version": "0.3.0-preview361", "pure_mode": "gamma", "max_samples": 2})

    def create(self):
        return self.module.new(self.host, self.config)

    def invoke(self, *, main=True, update=True, width=1920, height=1080, params=None):
        return self.state.callback(params, 1.0, main, update, self.lua.table_from({"x": width, "y": height}))

    def test_constructing_module_does_not_register_or_enable(self):
        adapter = self.create()
        self.assertEqual(self.state.registered, 0)
        self.assertEqual(adapter.receipt(adapter).state, "disabled")

    def test_start_observe_stop_preserves_yebis(self):
        adapter = self.create()
        self.assertTrue(adapter.start(adapter))
        params = self.lua.eval("setmetatable({}, {__index=function() error('parameter read forbidden') end, __newindex=function() error('parameter write forbidden') end})")
        self.assertIsNone(self.invoke(params=params))
        report = adapter.receipt(adapter)
        self.assertEqual(report.state, "observing")
        self.assertEqual(report.main_callbacks, 1)
        self.assertFalse(report.settings_written)
        self.assertFalse(report.exposure_owned)
        self.assertFalse(report.shader_executed)
        self.assertFalse(report.gameplay_validated)
        self.assertEqual(report.execution_scope, "lua_contract_fixture")
        self.assertEqual(report.pure_fork_identity, "unknown")
        self.assertTrue(adapter.stop(adapter))
        self.assertEqual(self.state.disposed, 1)

    def test_duplicate_start_and_stop_do_not_duplicate_handles(self):
        adapter = self.create()
        adapter.start(adapter)
        adapter.start(adapter)
        self.assertEqual(self.state.registered, 1)
        adapter.stop(adapter)
        self.assertTrue(adapter.stop(adapter))
        self.assertEqual(self.state.disposed, 1)

    def test_unknown_registration_handle_is_inert_and_cannot_restart(self):
        self.host.ac.onPostProcessing = self.lua.eval("function(callback) return {} end")
        adapter = self.create()
        self.assertFalse(adapter.start(adapter))
        self.assertEqual(adapter.receipt(adapter).cleanup, "registration_return_contract_unknown")
        self.assertFalse(adapter.stop(adapter))
        self.assertFalse(adapter.start(adapter))

    def test_unknown_and_wrong_versions_are_blocked(self):
        for version in ("0.3.1", "0.3.0-preview362", "0.2.11", "unknown"):
            self.state.version = version
            adapter = self.create()
            self.assertFalse(adapter.start(adapter))
            self.assertEqual(self.state.registered, 0)

    def test_preview_build_mismatch_is_blocked(self):
        self.state.build = 3899
        adapter = self.create()
        self.assertFalse(adapter.start(adapter))
        self.assertEqual(adapter.receipt(adapter).reason, "preview_build_mismatch")

    def test_stable_track_requires_actual_apis_and_does_not_claim_certification(self):
        self.state.version, self.state.build = "0.2.11", 3465
        self.config.csp_version = "0.2.11"
        adapter = self.create()
        self.assertTrue(adapter.start(adapter))
        self.assertFalse(adapter.receipt(adapter).gameplay_validated)
        adapter.stop(adapter)

    def test_missing_runtime_api_is_blocked(self):
        for name in ("getPatchVersion", "getPatchVersionCode", "onPostProcessing"):
            original = self.host.ac[name]
            self.host.ac[name] = None
            adapter = self.create()
            self.assertFalse(adapter.start(adapter))
            self.assertEqual(self.state.registered, 0)
            self.host.ac[name] = original

    def test_pure_api_unavailable_stays_unknown(self):
        self.host.pure = None
        adapter = self.create()
        self.assertFalse(adapter.start(adapter))
        self.assertEqual(adapter.receipt(adapter).shader_space_mode, "unknown")

    def test_lcs_and_gamma_profiles_are_independent(self):
        self.state.linear = True
        adapter = self.create()
        self.assertFalse(adapter.start(adapter))
        self.config.pure_mode = "lcs"
        adapter = self.create()
        self.assertTrue(adapter.start(adapter))
        self.assertEqual(adapter.receipt(adapter).shader_space_mode, "lcs")
        adapter.stop(adapter)

    def test_mid_run_pure_change_latches_passthrough(self):
        adapter = self.create()
        adapter.start(adapter)
        self.state.linear = True
        self.assertIsNone(self.invoke())
        self.assertEqual(adapter.receipt(adapter).state, "blocked")
        self.state.linear = False
        self.assertIsNone(self.invoke())
        self.assertEqual(adapter.receipt(adapter).main_callbacks, 0)
        adapter.stop(adapter)

    def test_sample_history_is_bounded_and_timing_units_unverified(self):
        adapter = self.create()
        adapter.start(adapter)
        for _ in range(10):
            self.invoke()
        report = adapter.receipt(adapter)
        self.assertEqual(report.main_callbacks, 10)
        self.assertEqual(len(report.samples), 2)
        self.assertEqual(report.samples[1].timing_units, "unknown_do_not_compute_fps")
        adapter.stop(adapter)

    def test_auxiliary_and_second_eye_callbacks_do_not_adapt_exposure(self):
        adapter = self.create()
        adapter.start(adapter)
        self.assertIsNone(self.invoke(main=False))
        self.assertIsNone(self.invoke(update=False))
        report = adapter.receipt(adapter)
        self.assertEqual(report.auxiliary_callbacks, 1)
        self.assertFalse(report.samples[1].update_exposure)
        self.assertFalse(report.exposure_owned)
        adapter.stop(adapter)

    def test_resize_records_change_without_allocating_textures(self):
        adapter = self.create()
        adapter.start(adapter)
        self.invoke()
        self.invoke(width=1280, height=720)
        report = adapter.receipt(adapter)
        self.assertEqual(report.resolution_changes, 1)
        self.assertEqual(report.width, 1280)
        self.assertFalse(report.hdr_texture_accessed)
        self.assertEqual(report.texture_encoding, "unknown")
        adapter.stop(adapter)

    def test_callback_error_latches_inert_until_owned_cleanup(self):
        adapter = self.create()
        adapter.start(adapter)
        self.assertIsNone(self.invoke(width=-1))
        self.assertEqual(adapter.receipt(adapter).state, "blocked")
        self.assertFalse(adapter.start(adapter))
        self.assertIsNone(self.invoke())
        adapter.stop(adapter)
        self.assertEqual(self.state.disposed, 1)

    def test_registration_failure_does_not_publish_active_state(self):
        self.state.register_fail = True
        adapter = self.create()
        self.assertFalse(adapter.start(adapter))
        self.assertEqual(adapter.receipt(adapter).reason, "callback_registration_failed")
        self.assertEqual(self.state.registered, 0)
        self.assertFalse(adapter.start(adapter))
        self.assertFalse(adapter.stop(adapter))

    def test_partial_registration_failure_cannot_reactivate_or_retry_orphan(self):
        self.lua.globals().fixture_state = self.state
        self.host.ac.onPostProcessing = self.lua.eval("""function(callback)
          fixture_state.callback = callback
          fixture_state.registered = fixture_state.registered + 1
          error('synthetic failure after registration')
        end""")
        adapter = self.create()
        self.assertFalse(adapter.start(adapter))
        self.assertFalse(adapter.start(adapter))
        self.assertEqual(self.state.registered, 1)
        self.assertEqual(adapter.receipt(adapter).cleanup, "registration_failure_cleanup_unknown")
        self.assertIsNone(self.invoke())
        self.assertEqual(adapter.receipt(adapter).callbacks, 0)
        self.assertFalse(adapter.stop(adapter))

    def test_shutdown_failure_does_not_retry_or_touch_external_owner(self):
        adapter = self.create()
        adapter.start(adapter)
        self.state.dispose_fail = True
        callback = self.state.callback
        self.assertFalse(adapter.stop(adapter))
        self.assertIsNone(callback(None, 1, True, True, self.lua.table_from({"x": 1920, "y": 1080})))
        self.assertFalse(adapter.stop(adapter))
        self.assertFalse(adapter.start(adapter))
        self.assertEqual(self.state.disposed, 1)

    def test_receipt_is_a_copy(self):
        adapter = self.create()
        adapter.start(adapter)
        self.invoke()
        report = adapter.receipt(adapter)
        report.state = "forged"
        report.samples[1].width = 1
        self.assertEqual(adapter.receipt(adapter).state, "observing")
        self.assertEqual(adapter.receipt(adapter).samples[1].width, 1920)
        adapter.stop(adapter)

    def test_invalid_configuration_is_rejected_before_native_calls(self):
        for key, value in (("pure_mode", "auto"), ("max_samples", 0), ("max_samples", 65),
                           ("max_samples", float("nan")), ("made_up", True)):
            config = self.lua.table_from({"csp_version": "0.3.0-preview361", "pure_mode": "gamma"})
            config[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(Exception):
                self.module.new(self.host, config)
        self.assertEqual(self.state.registered, 0)

    def test_pipeline_queries_observe_without_registering_effects(self):
        self.host.pure.pp = self.lua.eval("""{
          isEnabled = function() return true end,
          YEBISisBypassed = function() return true end,
          spice = {
            addLDRFilter = function() error('must not register LDR effect') end,
            addHDRFilter = function() error('must not register HDR effect') end
          }
        }""")
        self.host.ac.getSim = self.lua.eval("function() return {isFSRActive=true, isTripleFSRActive=false, isHDR=false} end")
        adapter = self.create()
        self.assertTrue(adapter.start(adapter))
        self.assertIsNone(self.invoke())
        pipeline = adapter.receipt(adapter).pipeline
        self.assertTrue(pipeline.pure_pp_enabled)
        self.assertTrue(pipeline.pure_yebis_bypassed)
        self.assertTrue(pipeline.pure_ldr_registration_api)
        self.assertTrue(pipeline.pure_hdr_registration_api)
        self.assertTrue(pipeline.fsr_section_active)
        self.assertFalse(pipeline.triple_fsr_section_active)
        self.assertEqual(pipeline.upscaler_algorithm, "unknown")
        self.assertEqual(pipeline.frame_generation, "unknown")
        adapter.stop(adapter)

    def test_pipeline_missing_or_failed_queries_preserve_unknown(self):
        self.host.pure.pp = self.lua.eval("{isEnabled=function() error('unavailable') end, YEBISisBypassed=function() return 'not boolean' end}")
        self.host.ac.getSim = self.lua.eval("function() return nil end")
        adapter = self.create()
        self.assertTrue(adapter.start(adapter))
        self.invoke()
        pipeline = adapter.receipt(adapter).pipeline
        self.assertEqual(pipeline.pure_pp_enabled, "unknown")
        self.assertEqual(pipeline.pure_yebis_bypassed, "unknown")
        self.assertEqual(pipeline.fsr_section_active, "unknown")
        self.assertFalse(pipeline.pure_ldr_registration_api)
        adapter.stop(adapter)

    def test_pipeline_can_change_without_touching_pure_or_upscaler(self):
        self.host.pure.pp = self.lua.eval("{isEnabled=function() return true end, YEBISisBypassed=function() return false end}")
        adapter = self.create()
        adapter.start(adapter)
        self.assertFalse(adapter.receipt(adapter).pipeline.pure_yebis_bypassed)
        self.host.pure.pp.YEBISisBypassed = self.lua.eval("function() return true end")
        self.invoke()
        self.assertTrue(adapter.receipt(adapter).pipeline.pure_yebis_bypassed)
        self.assertFalse(adapter.receipt(adapter).settings_written)
        adapter.stop(adapter)

    def test_stable_optional_field_failure_does_not_hide_available_flags(self):
        self.state.version, self.state.build = "0.2.11", 3465
        self.config.csp_version = "0.2.11"
        self.host.ac.getSim = self.lua.eval("""function()
          return setmetatable({isFSRActive=true, isTripleFSRActive=false},
            {__index=function() error('field absent in stable SDK') end})
        end""")
        adapter = self.create()
        self.assertTrue(adapter.start(adapter))
        self.invoke()
        pipeline = adapter.receipt(adapter).pipeline
        self.assertTrue(pipeline.fsr_section_active)
        self.assertFalse(pipeline.triple_fsr_section_active)
        self.assertEqual(pipeline.hdr_mode_raw, "unknown")
        adapter.stop(adapter)

    def test_stable_sdk_build_mismatch_is_blocked(self):
        self.state.version, self.state.build = "0.2.11", 3466
        self.config.csp_version = "0.2.11"
        adapter = self.create()
        self.assertFalse(adapter.start(adapter))
        self.assertEqual(self.state.registered, 0)
