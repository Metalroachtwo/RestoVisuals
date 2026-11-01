"""Display frame-time statistics. These functions do not capture or run a game."""

import csv
import math
import statistics
from pathlib import Path


def analyze_frame_times(samples, *, warmup_frames=0):
    values = list(samples)
    if type(warmup_frames) is not int or warmup_frames < 0 or warmup_frames >= len(values):
        raise ValueError("Warmup must leave at least one measured frame")
    if any(type(value) not in (int, float) or not math.isfinite(value) or value <= 0 for value in values):
        raise ValueError("Frame times must all be finite positive milliseconds")
    values = values[warmup_frames:]
    ordered = sorted(values)
    slow_count = max(1, math.ceil(len(values) * 0.01))

    def percentile(fraction):
        return ordered[max(0, math.ceil(len(ordered) * fraction) - 1)]

    return {
        "frames": len(values), "warmup_frames_excluded": warmup_frames,
        "average_fps": 1000 * len(values) / sum(values),
        "one_percent_low_fps": 1000 / statistics.mean(ordered[-slow_count:]),
        "p50_frame_ms": percentile(0.50), "p95_frame_ms": percentile(0.95),
        "p99_frame_ms": percentile(0.99), "worst_frame_ms": ordered[-1],
        "one_percent_low_definition": "1000 divided by arithmetic mean of slowest ceil(N*0.01) frame times",
        "percentile_definition": "nearest rank",
        "timing_source_verified": False,
        "note": "Input must be display frame intervals, not simulation/replay dt or interpolated FPS values. Short captures do not certify 1% lows.",
    }


def read_frame_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["frame_ms"]:
            raise ValueError("CSV requires exactly one frame_ms column")
        result = []
        for row in reader:
            if None in row or row.get("frame_ms") is None:
                raise ValueError("Malformed frame-time row")
            result.append(float(row["frame_ms"]))
        return result
