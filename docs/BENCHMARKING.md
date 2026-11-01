# Capture and comparison contract

Phase 0 implements analysis of existing CSV files. It does not capture a game,
run benchmark loops, certify timing sources, or change settings.

## Reproduce the software checks

From the repository root, with Python 3.11+:

```powershell
python -m unittest discover -s tests -v
python -m restovisuals benchmark examples/frame-times-synthetic.csv
python -m restovisuals compare examples/frame-times-synthetic.csv examples/capture-synthetic-baseline.json examples/frame-times-synthetic.csv examples/capture-synthetic-candidate.json
```

All example inputs are labeled synthetic. The ten-frame CSV has nine 10 ms
intervals and one 50 ms interval: 71.428571 average FPS and 20 FPS 1% low by the
defined formula. Comparing it against itself under separately named treatments
produces zero deltas. Neither result measures Assetto Corsa performance.

## Input data

CSV has exactly one header, `frame_ms`, followed by finite positive displayed
frame intervals in milliseconds. No FPS smoothing, simulation/replay dt,
automatically interpolated samples or silently dropped invalid intervals.
The current parser rejects bad headers, extra columns, invalid numerics and
nonpositive/nonfinite samples. An explicit warmup count must leave measured
frames. Preserve the original capture privately; convert through an inspectable
script when adapting an external capture format.

Sidecar JSON follows `schemas/capture.schema.json`. Its context fixes scene ID,
CSP version, Pure version/mode, GPU ID, driver, render mode, resolution, VSync
and frame cap (0 means uncapped). The scene ID must refer to an independently
preserved local scenario record containing car/track/replay hashes, camera,
time, weather, session/traffic seed, graphics snapshot and capture settings.
Do not publish protected assets, private roots, telemetry identifying a person,
or third-party configuration dumps. The tool compares declared metadata; it
cannot establish that the capture actually followed it.

Name the baseline/candidate treatments separately and keep a change manifest
so a reviewer can identify which module, upscaler or setting changed. Compare
one variable at a time. Any context difference, capture-source difference or
generated-frame classification difference refuses a combined comparison.
Treat FG display throughput separately from rendered simulation throughput and
input latency. Both runs may be analyzed independently if the comparison fails.

## Output definitions and proposed protocol

- Average FPS = `1000 * number_of_frames / sum(frame_ms)`.
- 1% low FPS = `1000 / mean(slowest ceil(N*0.01) frame_ms)`.
- P50/P95/P99 use nearest-rank frame times; higher values indicate slower frames.
- Percent change is `(candidate/baseline - 1) * 100`. A positive FPS delta and a
  negative frame-time delta are favorable numerically; neither proves a gain
  outside the captured workload or preserved visual quality.
- Input file SHA256s bind CLI comparisons to the exact CSV and JSON files.
  A comparison does not automatically emit a performance-improvement verdict.

For the future runtime gate, use at least 3000 measured frames and 30 seconds
per run after a declared warmup, then repeat matched trials to report variation.
Those are proposed starting sample floors, not a statistically proven protocol;
the tool warns below either. VSync/caps and CPU-bound workloads can mask GPU
differences. Preserve worst stalls rather than trimming inconvenient samples.

Pair each performance comparison with matching visual captures for Gamma and
LCS, native and optional reconstruction, including disocclusion, wheel/fence
detail, mirrors/HUD, lights, rain, fog and exposure transitions. Measure actual
game-process memory and incremental render surfaces. External probe-process
memory does not establish game memory pressure.

No game capture or physical legacy-GPU benchmark has been performed in Phase 0.
The next milestone must use authorized native integrations or independently
supplied captures; it must not initialize computer-use or alter locked software.
