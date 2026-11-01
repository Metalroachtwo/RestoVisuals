import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-m", "restovisuals", *map(str, args)], cwd=ROOT,
                              capture_output=True, text=True, timeout=20)

    def test_clean_checkout_synthetic_plan_is_usable(self):
        result = self.run_cli("plan", "--config", "profiles/gamma.json", "--gpu", "examples/gpu-synthetic-2gb.json",
                              "--adapter-index", "0", "--capabilities", "examples/capabilities-unknown.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual(plan["candidate_profile"], "ultra_lite")
        self.assertEqual(plan["input_gpu_source"], "synthetic_fixture")
        self.assertEqual(plan["upscaler"], "native")
        self.assertFalse(plan["applies_settings"])
        self.assertEqual(set(plan["input_files_sha256"]), {"config", "gpu", "capabilities"})

    def test_cli_benchmark_hand_computed(self):
        result = self.run_cli("benchmark", "examples/frame-times-synthetic.csv")
        self.assertEqual(result.returncode, 0, result.stderr)
        stats = json.loads(result.stdout)
        self.assertEqual(stats["frames"], 10)
        self.assertAlmostEqual(stats["average_fps"], 10000 / 140)
        self.assertEqual(stats["one_percent_low_fps"], 20)

    def test_comparison_reports_synthetic_identity_without_gain_claim(self):
        result = self.run_cli("compare", "examples/frame-times-synthetic.csv", "examples/capture-synthetic-baseline.json",
                              "examples/frame-times-synthetic.csv", "examples/capture-synthetic-candidate.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["percent_change"]["average_fps"], 0)
        self.assertIsNone(report["performance_gain_claim"])

    def test_invalid_input_is_redacted_and_returns_two(self):
        temp_root = ROOT / ".local/test-tmp"
        temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as directory:
            path = Path(directory) / "bad.json"
            for text in ("null", "[]", "not json", '{"pure": []}', '{"protected_files": {}}'):
                path.write_text(text)
                command = ("guard", path, path) if "protected_files" in text else ("capabilities", path)
                result = self.run_cli(*command)
                self.assertEqual(result.returncode, 2)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn(str(path), result.stderr)
                self.assertIn("error", json.loads(result.stderr))

    def test_guard_detects_drift_with_exit_three(self):
        temp_root = ROOT / ".local/test-tmp"
        temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as directory:
            before, after = Path(directory) / "before.json", Path(directory) / "after.json"
            before.write_text(json.dumps({"protected_files": {"logical/file": {"exists": True, "sha256": "a" * 64}}}))
            after.write_text(json.dumps({"protected_files": {"logical/file": {"exists": True, "sha256": "b" * 64}}}))
            result = self.run_cli("guard", before, after)
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertFalse(json.loads(result.stdout)["protected_files_unchanged"])
            self.assertEqual(json.loads(result.stdout)["changed"], ["logical/file"])
