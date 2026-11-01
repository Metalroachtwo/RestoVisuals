import tempfile
import unittest
from pathlib import Path

from restovisuals.benchmark import analyze_frame_times, read_frame_csv


class BenchmarkTests(unittest.TestCase):
    def test_duration_based_fps_not_average_instantaneous_fps(self):
        result = analyze_frame_times([10, 30])
        self.assertEqual(result["average_fps"], 50)

    def test_spike_and_percentiles_have_hand_computed_results(self):
        result = analyze_frame_times([10] * 99 + [50])
        self.assertAlmostEqual(result["average_fps"], 100000 / 1040)
        self.assertEqual(result["one_percent_low_fps"], 20)
        self.assertEqual(result["p99_frame_ms"], 10)
        self.assertEqual(result["worst_frame_ms"], 50)
        self.assertFalse(result["timing_source_verified"])

    def test_slowest_one_percent_mean_uses_ceiling(self):
        result = analyze_frame_times([10] * 199 + [40, 60])
        self.assertAlmostEqual(result["one_percent_low_fps"], 1000 / ((10 + 40 + 60) / 3))

    def test_explicit_warmup_exclusion(self):
        result = analyze_frame_times([1000, 10, 10], warmup_frames=1)
        self.assertEqual(result["average_fps"], 100)
        self.assertEqual(result["warmup_frames_excluded"], 1)
        self.assertEqual(result["frames"], 2)

    def test_invalid_samples_are_rejected_not_silently_removed(self):
        for samples in ([], [0], [-1], [float("nan")], [float("inf")], [False], ["10"]):
            with self.subTest(samples=samples), self.assertRaises(ValueError):
                analyze_frame_times(samples)

    def test_invalid_warmup(self):
        for warmup in (-1, 1, 2, True, 0.5):
            with self.subTest(warmup=warmup), self.assertRaises(ValueError):
                analyze_frame_times([10], warmup_frames=warmup)

    def test_csv_contract(self):
        root = Path(__file__).resolve().parents[1] / ".local/test-tmp"
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as directory:
            path = Path(directory) / "synthetic.csv"
            path.write_text("frame_ms\n10\n20\n", encoding="utf-8-sig")
            self.assertEqual(read_frame_csv(path), [10, 20])
            for text in ("fps\n60\n", "frame_ms\n10,extra\n", "frame_ms\ninvalid\n"):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    read_frame_csv(path)
