import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from restovisuals.__main__ import main
from restovisuals.runtime_probe import FILES, TARGET, prepare_observer_probe
from test_runtime_lua import HARNESS, LuaRuntime, ROOT


EXPERIMENT_HOST = """
function experiment_fixture()
  local host, state = make_fixture()
  state.timers, state.nextID, state.reports, state.releaseDisposed = {}, 0, {}, 0
  host.schedule = function(fn, seconds)
    state.nextID = state.nextID + 1
    state.timers[state.nextID] = {fn = fn, seconds = seconds}
    return state.nextID
  end
  host.cancel = function(id)
    if not state.timers[id] then return false end
    state.timers[id] = nil
    return true
  end
  host.on_release = function(fn)
    state.release = fn
    return function() state.releaseDisposed = state.releaseDisposed + 1; state.release = nil end
  end
  host.write = function(report) state.reports[#state.reports + 1] = report; return true end
  state.fire = function(id)
    local fn = state.timers[id].fn
    state.timers[id] = nil
    fn()
  end
  return host, state
end
"""


@unittest.skipUnless(LuaRuntime is not None, "Optional LuaJIT contract dependency")
class HostProbeTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime(unpack_returned_tuples=True, register_eval=False, register_builtins=False)
        self.observer = self.lua.execute((ROOT / "runtime/lua/restovisuals_observer.lua").read_text())
        self.probe = self.lua.execute((ROOT / "runtime/lua/restovisuals_host_probe.lua").read_text())
        self.lua.execute(HARNESS + EXPERIMENT_HOST)
        self.host, self.state = self.lua.globals().experiment_fixture()
        self.config = self.lua.table_from({"csp_version": "0.3.0-preview361", "pure_mode": "gamma", "max_samples": 2})

    def run_probe(self):
        return self.probe.run(self.host, self.observer, self.config, "fixture-run-0d")

    def invoke(self, callback=None):
        return (callback or self.state.callback)(self.lua.table(), 1, True, True,
                                                self.lua.table_from({"x": 1920, "y": 1080}))

    def test_timer_stop_and_post_stop_witness_release_only_owned_handles(self):
        experiment = self.run_probe()
        self.assertIsNone(self.invoke())
        self.assertEqual(self.state.timers[1].seconds, 10)
        self.state.fire(1)
        self.assertEqual(self.state.disposed, 1)
        self.assertIsNone(self.state.callback)
        self.assertEqual(self.state.timers[2].seconds, 1)
        self.state.fire(2)
        result = experiment.receipt(experiment)
        self.assertEqual(result.event, "stop_witness_completed")
        self.assertEqual(result.native_callback_invocations, 1)
        self.assertEqual(result.callbacks_after_stop, 0)
        self.assertTrue(result.owned_lifecycle_calls_succeeded)
        self.assertEqual(self.state.releaseDisposed, 1)
        self.assertEqual(len(self.state.timers), 0)
        self.assertFalse(result.shader_executed)
        self.assertFalse(result.named_pure_effect_registered)
        self.assertEqual(result.buffer_encoding, "unknown")

    def test_late_callback_after_disposal_fails_witness_without_processing(self):
        experiment = self.run_probe()
        orphan = self.state.callback
        self.invoke()
        self.state.fire(1)
        self.assertIsNone(self.invoke(orphan))
        self.state.fire(2)
        result = experiment.receipt(experiment)
        self.assertEqual(result.event, "callback_after_unsubscribe")
        self.assertFalse(result.owned_lifecycle_calls_succeeded)
        self.assertEqual(result.callbacks_after_stop, 1)
        self.assertEqual(result.observer.callbacks, 1)

    def test_zero_callbacks_are_preserved_without_promoting_capabilities(self):
        experiment = self.run_probe()
        self.state.fire(1); self.state.fire(2)
        result = experiment.receipt(experiment)
        self.assertEqual(result.native_callback_invocations, 0)
        self.assertFalse(result.observer.gameplay_validated)
        self.assertFalse(result.game_visuals_validated)

    def test_mid_run_mode_fault_survives_stop_and_fails_terminal_receipt(self):
        experiment = self.run_probe()
        self.invoke()
        self.state.linear = True
        self.invoke()
        self.state.fire(1); self.state.fire(2)
        result = experiment.receipt(experiment)
        self.assertEqual(result.observer.callbacks, 1)
        self.assertEqual(result.observer.state, 'disabled')
        self.assertEqual(result.observer_before_stop.state, 'blocked')
        self.assertEqual(result.observer_before_stop.reason, 'pure_shader_mode_changed_or_unavailable')
        self.assertEqual(result.event, 'observer_fault_before_stop')
        self.assertFalse(result.owned_lifecycle_calls_succeeded)

    def test_sink_failure_before_start_does_not_register_postprocessing(self):
        self.host.write = self.lua.eval("function() return false end")
        experiment = self.run_probe()
        self.assertEqual(self.state.registered, 0)
        self.assertEqual(experiment.receipt(experiment).event, "receipt_sink_failed_no_start")

    def test_sink_failure_after_start_immediately_cleans_owned_resources(self):
        self.host.write = self.lua.eval("(function() local n=0; return function() n=n+1; return n==1 end end)()")
        experiment = self.run_probe()
        self.assertEqual(self.state.registered, 1)
        self.assertEqual(self.state.disposed, 1)
        self.assertEqual(self.state.releaseDisposed, 1)
        self.assertEqual(len(self.state.timers), 0)
        self.assertEqual(experiment.receipt(experiment).event, "receipt_sink_failed_after_start")

    def test_unknown_release_handle_prevents_observer_registration(self):
        self.host.on_release = self.lua.eval("function() return {} end")
        experiment = self.run_probe()
        self.assertEqual(self.state.registered, 0)
        self.assertFalse(experiment.receipt(experiment).owned_lifecycle_calls_succeeded)

    def test_unknown_deadline_handle_prevents_observer_start_and_cancels_release(self):
        self.host.schedule = self.lua.eval("function() return nil end")
        experiment = self.run_probe()
        self.assertEqual(self.state.registered, 0)
        self.assertEqual(self.state.releaseDisposed, 1)
        self.assertFalse(experiment.receipt(experiment).owned_lifecycle_calls_succeeded)

    def test_host_release_cancels_pending_timer_and_stops_observer(self):
        experiment = self.run_probe()
        self.state.release()
        self.assertEqual(self.state.disposed, 1)
        self.assertEqual(len(self.state.timers), 0)
        self.assertEqual(experiment.receipt(experiment).event, "host_released")

    def test_failed_unsubscribe_retains_inert_callback_and_failed_lifecycle(self):
        experiment = self.run_probe()
        self.state.dispose_fail = True
        self.state.fire(1); self.state.fire(2)
        result = experiment.receipt(experiment)
        self.assertFalse(result.owned_lifecycle_calls_succeeded)
        self.assertEqual(result.observer.cleanup, "unsubscribe_failed_no_automatic_retry")
        self.assertIsNone(self.invoke())

    def test_unprepared_loader_entry_is_inert_without_host_globals(self):
        entry = (ROOT / "runtime/lua/RestoVisuals_Observer_0D.lua").read_text()
        self.assertIsNone(self.lua.execute(entry))
        self.assertEqual(self.state.registered, 0)

    def test_type_diagnostic_never_registers_callback_timer_or_release(self):
        self.host.diagnostic_only = True
        experiment = self.run_probe()
        result = experiment.receipt(experiment)
        self.assertEqual(result.event, 'api_type_diagnostic_complete')
        self.assertEqual(result.required_api_types.patch_version, 'function')
        self.assertEqual(result.required_api_types.patch_build, 'function')
        self.assertEqual(result.required_api_types.post_processing, 'function')
        self.assertEqual(self.state.registered, 0)
        self.assertEqual(self.state.nextID, 0)
        self.assertIsNone(self.state.release)
        self.assertFalse(result.shader_executed)

    def test_callable_ffi_value_is_reported_without_weakening_observer_gate(self):
        self.host.ac.getPatchVersionCode = self.lua.eval("require('ffi').cast('int (*)()', function() return 3898 end)")
        experiment = self.run_probe()
        result = experiment.receipt(experiment)
        self.assertEqual(result.required_api_types.patch_build, 'cdata')
        self.assertEqual(result.observer_before_stop.reason, 'required_csp_api_missing')
        self.assertEqual(self.state.registered, 0)


class PackagePreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_root = ROOT / ".local/test-tmp"
        cls.temp_root.mkdir(parents=True, exist_ok=True)

    def test_preparation_writes_only_three_original_files_and_hash_manifest(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as directory:
            output = Path(directory) / "new-probe"
            manifest = prepare_observer_probe(output)
            self.assertEqual(manifest["target_relative_directory"], TARGET)
            self.assertEqual(set(manifest["files_sha256"]), set(FILES))
            for name, digest in manifest["files_sha256"].items():
                self.assertEqual(hashlib.sha256((output / TARGET / name).read_bytes()).hexdigest(), digest)
            entry = (output / TARGET / FILES[0]).read_text()
            self.assertIn(manifest["run_id"], entry)
            self.assertNotIn("__RESTOVISUALS_RUN_ID__", entry)
            self.assertFalse(manifest["installed"])
            self.assertEqual(manifest["reference_files_to_overwrite"], [])
            self.assertEqual(json.loads((output / "manifest.json").read_text()), manifest)
            with self.assertRaises(ValueError):
                prepare_observer_probe(output)

    def test_preparation_rejects_destination_outside_local_before_source_access(self):
        with self.assertRaises(ValueError):
            prepare_observer_probe(ROOT / "not-created")

    def test_diagnostic_package_declares_and_pins_nonregistering_mode(self):
        with tempfile.TemporaryDirectory(dir=self.temp_root) as directory:
            output = Path(directory) / 'diagnostic'
            manifest = prepare_observer_probe(output, diagnostic_only=True)
            self.assertTrue(manifest['diagnostic_only'])
            self.assertEqual(manifest['intent'], 'native_api_type_diagnostic_only')
            self.assertIn('local diagnosticOnly = true', (output / TARGET / FILES[0]).read_text())

    def test_cli_preparation_failure_is_redacted_without_installation(self):
        with patch("sys.stderr", new_callable=io.StringIO) as error:
            status = main(["prepare-observer-probe", "--output", str(ROOT / "not-created")])
            self.assertEqual(status, 2)
            self.assertNotIn(str(ROOT), error.getvalue())
