"""Display frame-time statistics. These functions do not capture or run a game."""

import csv
import json
import math
import statistics
from pathlib import Path

from .validation import validate_document


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
        "sampled_duration_ms": sum(values),
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


def compare_captures(baseline, candidate, baseline_metadata, candidate_metadata):
    """Compare only matching declared contexts and timing semantics.

    Metadata is a reproducibility contract, not independently attested capture
    provenance. No automatic performance or visual-quality verdict is issued.
    """
    schema = json.loads((Path(__file__).resolve().parents[1] / "schemas/capture.schema.json").read_text())
    for metadata in (baseline_metadata, candidate_metadata):
        validate_document(metadata, schema)
    for key in ("context", "timing_source", "includes_generated_frames"):
        if baseline_metadata[key] != candidate_metadata[key]:
            raise ValueError("Capture context or timing semantics differ; comparison refused")
    if baseline_metadata["treatment_id"] == candidate_metadata["treatment_id"]:
        raise ValueError("Treatments must be identified separately")
    first = analyze_frame_times(baseline, warmup_frames=baseline_metadata["warmup_frames"])
    second = analyze_frame_times(candidate, warmup_frames=candidate_metadata["warmup_frames"])
    warnings = ["Metadata and timing source have not been independently verified; repeat matched captures and inspect visual quality before claiming a gain"]
    if min(first["frames"], second["frames"]) < 3000 or min(first["sampled_duration_ms"], second["sampled_duration_ms"]) < 30000:
        warnings.append("Short capture: proposed minimum of 3000 measured frames and 30 seconds per run is not met")
    if baseline_metadata["timing_source"] == "synthetic_fixture":
        warnings.append("Synthetic fixtures: results are software validation only, not game performance")
    if baseline_metadata["includes_generated_frames"]:
        warnings.append("Displayed FPS includes generated frames and is not simulation throughput or a latency measurement")
    return {
        "schema_version": 1, "comparison": "matching_declared_context_only",
        "baseline_evidence_id": baseline_metadata["evidence_id"], "candidate_evidence_id": candidate_metadata["evidence_id"],
        "timing_source": baseline_metadata["timing_source"], "baseline": first, "candidate": second,
        "percent_change": {key: 100 * (second[key] / first[key] - 1) for key in ("average_fps", "one_percent_low_fps", "p95_frame_ms", "p99_frame_ms")},
        "performance_gain_claim": None, "visual_quality_assessed": False, "warnings": warnings,
    }
