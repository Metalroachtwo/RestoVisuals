import copy
import json
import unittest
from pathlib import Path

from restovisuals.planning import CAPABILITIES, capabilities_from_audit, make_plan, validate_config


def config():
    return json.loads((Path(__file__).resolve().parents[1] / "profiles/gamma.json").read_text())


def adapter(gib=2, vendor=0x10DE, level="11_0", software=False):
    return {"dedicated_video_memory_bytes": int(gib * 1024**3), "is_software": software,
            "vendor_id": vendor, "feature_level": level}


def evidence(profile, state="unknown"):
    return {"schema_version": 1, "context": {key: profile[key] for key in ("csp_version", "pure_mode", "render_mode", "width", "height")},
            "capabilities": dict.fromkeys(CAPABILITIES, state), "evidence_id": "synthetic_test_fixture"}


class ConfigurationTests(unittest.TestCase):
    def test_profiles_validate_and_preserve_modes(self):
        for name in ("gamma", "lcs"):
            path = Path(__file__).resolve().parents[1] / f"profiles/{name}.json"
            self.assertEqual(validate_config(json.loads(path.read_text()))["pure_mode"], name)

    def test_unknown_missing_and_wrong_types_rejected(self):
        bad_values = [dict(config(), invented=True), {k: v for k, v in config().items() if k != "pure_mode"},
                      dict(config(), width=True), dict(config(), frame_generation=1), dict(config(), target_fps=float("nan")),
                      dict(config(), target_fps=float("inf")), dict(config(), target_fps=10**1000),
                      dict(config(), width=32000), dict(config(), profile="ultra"), dict(config(), target_fps=0)]
        for value in bad_values:
            with self.subTest(value=str(value)[:100]), self.assertRaises(ValueError):
                validate_config(value)

    def test_only_authorized_csp_tracks(self):
        for version in ("0.3.1", "0.3.0-preview362", "0.3.0", "0.2.10"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                validate_config(dict(config(), csp_version=version))
        validate_config(dict(config(), csp_version="0.2.11"))


class PlannerTests(unittest.TestCase):
    def test_no_integration_claim_from_labels(self):
        audit = {"csp": {"manifest_version": "0.3.0-preview361"}, "pure": {"configured_weather_implementation": "pure"},
                 "interfaces": {"upscaler_labels_present": {"fsr1": True, "fsr2": True, "fsr3": True}}}
        report = capabilities_from_audit(audit)
        cfg = dict(config(), upscaler="fsr3", frame_generation=True, color_transform=True)
        plan = make_plan(cfg, adapter(8), report)
        self.assertEqual(plan["upscaler"], "native")
        self.assertFalse(plan["frame_generation"])
        self.assertFalse(plan["color_transform"])
        self.assertFalse(plan["applies_settings"])
        self.assertFalse(plan["gameplay_validated"])

    def test_vendors_have_equivalent_capacity_classes(self):
        for gib, expected in ((2, "ultra_lite"), (3, "optimized"), (4, "optimized"), (6, "balanced"), (8, "enhanced")):
            for vendor in (0x1002, 0x10DE):
                cfg = config()
                result = make_plan(cfg, adapter(gib, vendor), evidence(cfg))
                self.assertEqual(result["candidate_profile"], expected)
                self.assertIsNone(result["performance_prediction"])

    def test_capacity_does_not_override_feature_level_or_software(self):
        cfg = dict(config(), upscaler="fsr2", frame_generation=True, color_transform=True)
        for gpu in (adapter(8, level="10_1"), adapter(8, software=True), adapter(8, level=None),
                    adapter(8, level="99_9"), adapter(8, level="11_9"), adapter(1)):
            with self.subTest(gpu=gpu):
                result = make_plan(cfg, gpu, evidence(cfg, "tested_validated"))
                self.assertIsNone(result["candidate_profile"])
                self.assertEqual(result["status"], "unsupported_or_unmeasured")
                self.assertEqual(result["upscaler"], "native")
                self.assertFalse(result["frame_generation"])
                self.assertFalse(result["color_transform"])

    def test_requested_tier_cannot_exceed_hardware_class(self):
        cfg = dict(config(), profile="enhanced")
        self.assertEqual(make_plan(cfg, adapter(2), evidence(cfg))["candidate_profile"], "ultra_lite")
        cfg["profile"] = "ultra_lite"
        self.assertEqual(make_plan(cfg, adapter(8), evidence(cfg))["candidate_profile"], "ultra_lite")

    def test_documented_observed_and_proposed_never_enable_features(self):
        cfg = dict(config(), upscaler="fsr1")
        for state in ("unknown", "documented", "observed_locally", "proposed", "unavailable"):
            with self.subTest(state=state):
                self.assertEqual(make_plan(cfg, adapter(), evidence(cfg, state))["upscaler"], "native")

    def test_each_context_dimension_invalidates_proof(self):
        cfg = dict(config(), upscaler="fsr2", frame_generation=True, color_transform=True)
        for key, value in (("csp_version", "0.2.11"), ("pure_mode", "lcs"), ("render_mode", "vr"), ("width", 1280), ("height", 720)):
            report = evidence(cfg, "tested_validated")
            report["context"][key] = value
            result = make_plan(cfg, adapter(8), report)
            self.assertEqual(result["upscaler"], "native")
            self.assertFalse(result["color_transform"])
            self.assertFalse(result["frame_generation"])

    def test_temporal_requires_each_buffer_and_reset(self):
        cfg = dict(config(), upscaler="fsr2")
        for missing in ("fsr2", "depth", "motion", "jitter", "history_reset"):
            report = evidence(cfg, "tested_validated")
            report["capabilities"][missing] = "unknown"
            self.assertEqual(make_plan(cfg, adapter(), report)["upscaler"], "native")

    def test_fsr3_upscaling_does_not_enable_frame_generation(self):
        cfg = dict(config(), upscaler="fsr3", frame_generation=True)
        report = evidence(cfg, "tested_validated")
        report["capabilities"]["frame_generation"] = "unknown"
        result = make_plan(cfg, adapter(8), report)
        self.assertEqual(result["upscaler"], "fsr3")
        self.assertFalse(result["frame_generation"])

    def test_memory_model_disables_over_budget_surface(self):
        cfg = dict(config(), color_transform=True, width=3840, height=2160)
        result = make_plan(cfg, adapter(2), evidence(cfg, "tested_validated"))
        self.assertFalse(result["color_transform"])
        self.assertEqual(result["effect_surface_model"]["additional_bytes"], 0)
        self.assertIsNone(result["effect_surface_model"]["fsr_working_set_bytes"])
        result = make_plan(cfg, adapter(8), evidence(cfg, "tested_validated"))
        self.assertTrue(result["color_transform"])
        self.assertEqual(result["effect_surface_model"]["additional_bytes"], 3840 * 2160 * 8)

    def test_stable_track_does_not_inherit_preview_observations(self):
        cfg = dict(config(), csp_version="0.2.11", upscaler="fsr1")
        report = evidence(cfg)
        report["context"]["csp_version"] = "0.3.0-preview361"
        report["capabilities"]["fsr1"] = "observed_locally"
        result = make_plan(cfg, adapter(4), report)
        self.assertEqual(result["csp_track"], "stable_baseline")
        self.assertEqual(result["upscaler"], "native")

    def test_unknown_states_and_capabilities_fail(self):
        cfg = config()
        for key, value in (("fsr1", "available"), ("invented", "tested_validated")):
            report = evidence(cfg)
            report["capabilities"][key] = value
            with self.assertRaises(ValueError):
                make_plan(cfg, adapter(), report)

    def test_input_objects_unchanged(self):
        cfg, gpu = config(), adapter()
        report = evidence(cfg)
        original = copy.deepcopy((cfg, gpu, report))
        make_plan(cfg, gpu, report)
        self.assertEqual((cfg, gpu, report), original)
