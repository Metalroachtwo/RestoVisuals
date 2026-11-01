# RestoVisuals architecture, Phase 0

## Decision and current implementation

Use one vendor-neutral engine with capability adapters and separate Pure
calibrations. Begin with an offline control plane and supported CSP/Pure
integration research. Do not build an injector, custom upscaler or replay MCP.

The implemented control plane is Python 3.11+ standard library. It has no package
downloads, installation hooks, telemetry service or game-setting writer.
Windows-only GPU detection uses system DXGI/D3D11 through ctypes; the planner,
schema validator, file audit and frame-time mathematics are independently usable.
A future CSP Lua bridge will supply runtime evidence and apply approved graphics
operations through existing supported interfaces. That bridge is not implemented.

```mermaid
flowchart LR
    Files[Explicit graphics paths] --> Audit[Read-only audit and hashes]
    DXGI[System DXGI and D3D11] --> GPU[Measured adapter capabilities]
    Profiles[Gamma or LCS plan configuration] --> Planner[Shared offline planner]
    Audit --> Claims[Evidence states and context]
    Claims --> Planner
    GPU --> Planner
    Planner --> Plan[JSON candidate plan]
    CSV[Previously captured frame_ms CSV] --> Stats[Frame-time analysis]
    Stats --> Review[Engineering review]
    Plan --> Review
    Review -. future approved integration .-> CSP[CSP capability adapter]
    CSP -. separate calibration .-> Pure[Pure Gamma or LCS]
```

## Module contracts

| Module | Inputs and output | Implemented boundary |
|---|---|---|
| Environment audit | explicit roots -> sanitized observations and relative IDs/hashes | Selected files and top-level PP INIs only; no recursive asset inventory |
| GPU capability engine | DXGI adapters + temporary D3D11 devices -> vendor/device, software flag, dedicated bytes, actual feature level | No swap chain, process attachment, game adapter guess or vendor SDK |
| Configuration | JSON profile -> strict validated fields | Schema version 1; reject unknown/missing fields, types, invalid ranges and unauthorized CSP tracks |
| Capability adapters | context + per-capability evidence states -> feature eligibility | Observed labels stay observations. Optional eligibility requires tested evidence for matching CSP, Pure mode, render mode and resolution |
| Performance planner | config + explicit adapter + capability report -> candidate JSON | Proposed memory class and resource ceiling; no setting writes, FPS prediction or runtime certification |
| Benchmark analysis | display interval CSV -> average FPS, 1% low and percentiles | Duration-based average, documented slowest-frame definition, explicit warmup; no capture source certification |
| Rendering integration | stage/format/ownership + approved operations | Future CSP/Pure runtime bridge; no active game module in Phase 0 |
| Replay integration | versioned capture intent and visual profile ID | Future external MCP; no camera/replay implementation in Phase 0 |

## CSP and evidence model

Only `0.2.11` and `0.3.0-preview361` are accepted target tracks. Track recognition
does not imply runtime compatibility. No version comparison automatically enables
a newer feature. Runtime capability states are `unknown`, `documented`,
`observed_locally`, `tested_validated`, `proposed` or `unavailable`.

Installed labels produce `observed_locally`. Capability reports carry a reviewable
evidence ID and exact context. The planner requires all context fields to match
before permitting optional features. Tests use synthetic evidence reports to
exercise gates; these are not measurements from the game. A future runtime
collector must verify symbols, loaded libraries, prerequisites and buffer
availability, record source/hashes/driver/context, and invalidate evidence after
changes. Until that exists, do not hand-edit an observation into runtime proof.

Temporal FSR requires independent evidence for its integration plus depth,
motion, jitter and history resets. FSR3 upscaling does not enable frame generation.
Native remains selectable. Extra FX, post-processing, render-mode restrictions,
payload availability and original motion blur belong in the integration probe's
validated claim; the offline planner does not inspect or alter their live state.

## Pure ownership and visual processing

Gamma and LCS use separate profile documents with identical engine contracts.
They have equal hardware standing. Their current documents describe proposed
plan inputs, not visually calibrated PP presets. The saved active Gamma selection
does not establish LCS behavior.

Pure should retain exposure/weather ownership initially. Future RestoVisuals
processing must explicitly identify input/output color encoding and bind at a
verified supported stage. Avoid two exposure controllers, repeated tonemapping,
duplicated bloom or multiple sharpeners. Start with no extra render targets and
one optional fused color pass only after numerical, compile, runtime and visual
gates. Night, rain, fog, sun/headlights and reflections require both calibrations.
Existing CSP control adjustments must be labeled as configuration operations.
Only original shader source may be called a RestoVisuals rendering effect.

## Low-memory policy

| Candidate class | Nominal target | Proposed incremental effect ceiling |
|---|---|---|
| Ultra Lite | 2 GB | 24 MiB |
| Optimized | 3-4 GB | 48 MiB |
| Balanced | 6 GB | 96 MiB |
| Enhanced | 8 GB | 128 MiB |

These are design ceilings, not profiled budgets or minimum hardware guarantees.
Capacity boundaries tolerate reserved adapter memory: 2.5, 5.5 and 7.5 GiB
separate the proposed classes; below 1792 MiB is outside the initial targets.
Software adapters and unmeasured/below-11_0 feature levels cannot receive an
eligible class. Unvalidated vendors get only a conservative exploratory class.
AMD/NVIDIA receive the same policy. A requested class cannot raise the capacity
ceiling. Bandwidth, driver behavior and displayed frame times remain required
before recommending deployment on any card.

One proposed full-resolution RGBA16F output costs `width * height * 8` bytes
without MSAA, mips, array layers or history. At 1080p that is 15.82 MiB; at 4K,
63.28 MiB. The planner disables this pass above its tier ceiling. Current default
plans request no effect surface. CSP's own resources and FSR working sets are
unknown and excluded, so this arithmetic cannot certify total VRAM headroom.
Prefer CSP-owned targets, pass fusion, reuse and reduced resolution over extra
history buffers. Do not confuse dedicated capacity with available memory.

## Measurement and future adaptation

The user-supplied target FPS defaults to 60 in examples; it is an input, not a
measured result or guaranteed target. A frame-time budget is `1000 / target_fps`.
Average FPS uses total displayed frames divided by elapsed display time. The
1% low is reciprocal mean of the slowest ceil(N*0.01) frame intervals. Percentiles
use nearest rank. Require longer consistent captures for certification and report
sample count, warmup, source, driver, settings, resolution and native baseline.

CSP exposes candidate performance APIs but their units and wall-clock behavior
need runtime validation. Simulation dt is replay/pause dependent. DXGI budget in
a helper is not the game's usage. In-process timing and memory collection are
future work. No real-time adaptation is implemented. When added, use hysteresis,
minimum dwell, bounded setting deltas and restore-on-error behavior; never
automatically change an upscaler requiring a restart.

## Reversibility, packaging and tradeoffs

No apply operation exists in this checkpoint. Later application must snapshot
only owned keys, hash the baseline, present a concrete diff, check drift, apply
through supported interfaces, and verify rollback before touching known-good
configuration. Preserve other mods and enable one module at a time. Runtime
errors must disable the optional module and retain native rendering.

Python keeps the initial tools inspectable and dependency-free; it is not the
planned per-frame runtime or end-user installer. Lua is the expected thin CSP
adapter, HLSL the optional effect language. Native C++ is deferred until a measured
integration requirement exists. ReShade would add hook/order/compatibility risk
and is not an initial dependency. Public repository licensing remains undecided;
no third-party source, paid Pure assets or binaries are vendored.
