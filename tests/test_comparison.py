import copy
import json
import unittest
from pathlib import Path

from restovisuals.benchmark import compare_captures
from restovisuals.validation import validate_document


def metadata(name):
    path = Path(__file__).resolve().parents[1] / f"examples/capture-synthetic-{name}.json"
    return json.loads(path.read_text())


class ComparisonTests(unittest.TestCase):
    def test_hand_computed_deltas_and_synthetic_label(self):
        result = compare_captures([10] * 100, [20] * 100, metadata("baseline"), metadata("candidate"))
        self.assertEqual(result["percent_change"]["average_fps"], -50)
        self.assertEqual(result["percent_change"]["one_percent_low_fps"], -50)
        self.assertEqual(result["percent_change"]["p95_frame_ms"], 100)
        self.assertEqual(result["timing_source"], "synthetic_fixture")
        self.assertIsNone(result["performance_gain_claim"])
        self.assertFalse(result["visual_quality_assessed"])
        self.assertTrue(any("Short capture" in warning for warning in result["warnings"]))

    def test_each_environment_axis_blocks_comparison_on_drift(self):
        first = metadata("baseline")
        for key, value in (("scene_id", "other_scene"), ("csp_version", "0.2.11"), ("pure_mode", "lcs"),
                           ("pure_version", "other"), ("gpu_id", "other_gpu"), ("driver_version", "other_driver"),
                           ("render_mode", "vr"), ("width", 1280), ("height", 720), ("vsync", True), ("frame_cap_fps", 60)):
            second = metadata("candidate")
            second["context"][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "comparison refused"):
                compare_captures([10], [20], first, second)

    def test_generated_frames_cannot_be_mixed_with_rendered_only(self):
        first, second = metadata("baseline"), metadata("candidate")
        second["includes_generated_frames"] = True
        with self.assertRaisesRegex(ValueError, "comparison refused"):
            compare_captures([10], [20], first, second)
        first["includes_generated_frames"] = True
        result = compare_captures([10], [20], first, second)
        self.assertTrue(any("not simulation throughput" in warning for warning in result["warnings"]))

    def test_timing_sources_cannot_be_mixed(self):
        first, second = metadata("baseline"), metadata("candidate")
        second["timing_source"] = "display_intervals_external"
        with self.assertRaisesRegex(ValueError, "comparison refused"):
            compare_captures([10], [20], first, second)

    def test_identical_treatment_ids_rejected(self):
        first = metadata("baseline")
        with self.assertRaises(ValueError):
            compare_captures([10], [20], first, first)

    def test_invalid_metadata_and_unknown_fields_fail_closed(self):
        for change in ("missing", "unknown", "empty", "bad_type", "new_version"):
            second = metadata("candidate")
            if change == "missing":
                del second["context"]["gpu_id"]
            elif change == "unknown":
                second["context"]["made_up"] = 1
            elif change == "empty":
                second["context"]["scene_id"] = " "
            elif change == "bad_type":
                second["context"]["width"] = True
            else:
                second["context"]["csp_version"] = "0.3.1"
            with self.subTest(change=change), self.assertRaises(ValueError):
                compare_captures([10], [20], metadata("baseline"), second)

    def test_metadata_is_not_mutated(self):
        first, second = metadata("baseline"), metadata("candidate")
        original = copy.deepcopy((first, second))
        compare_captures([10], [20], first, second)
        self.assertEqual((first, second), original)

    def test_unsupported_schema_keyword_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_document("value", {"type": "string", "pattern": "value"})
