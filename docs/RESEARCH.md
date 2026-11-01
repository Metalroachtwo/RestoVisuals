# Phase 0 research ledger

Phase 0B update: the official CSP 0.2.11 archive and version-matched SDK were
obtained privately and identify build 3465. The historical missing-inventory
note below is superseded by [the stable reference](CSP0211_REFERENCE.md).
Actual isolated GPU execution and the read-only Lua observer are recorded in
[Phase 0B](PHASE0B_RUNTIME.md). No CSP/Pure game runtime has been certified.
See [Dream Realism reference analysis](DREAM_REALISM_REFERENCE.md) for the
additional authorized research; protected code/assets were not redistributed.

Evidence date: 2026-11-01. Separate an upstream algorithm's requirements, CSP's
integration, file presence, and actual runtime validation.

## Primary references and implications

| Reference | Established scope | RestoVisuals decision |
|---|---|---|
| [AMD FSR 1](https://gpuopen.com/fidelityfx-superresolution/) | Spatial upscaling; supports DirectX 11; MIT-licensed upstream. | Prefer CSP's existing spatial implementation where verified. Do not add a custom port in Phase 0. |
| [AMD FSR 2.2.1 source/documentation](https://github.com/GPUOpen-Effects/FidelityFX-FSR2/blob/master/README.md) | Temporal inputs include color, depth, motion and jitter; upstream backends are DX12/Vulkan. Working-set and persistent allocations depend on resolution. | An available algorithm is not proof of a DX11/CSP port. Let CSP own temporal integration and verify the exact build. |
| [AMD FSR 3 announcement](https://gpuopen.com/news/fsr3-announce/) | Upscaling and frame generation have different hardware guidance. The original FG guidance starts above several legacy targets. | Gate FG independently; never require it or infer it from FSR3 upscaling. No FSR4 dependency. |
| [Microsoft D3D11CreateDevice](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/nf-d3d11-d3d11createdevice) | Explicit adapter/device creation returns an actual feature level; an explicit adapter uses UNKNOWN driver type. | Probe actual adapters, including software flags; do not classify by name or VRAM alone. |
| [Microsoft QueryVideoMemoryInfo](https://learn.microsoft.com/en-us/windows/win32/api/dxgi1_4/nf-dxgi1_4-idxgiadapter3-queryvideomemoryinfo) | Reports calling-process usage/budget, not total free VRAM or another process's consumption. | Never use a standalone diagnostic's usage as Assetto Corsa usage. Native in-process telemetry is a later integration requirement. |
| [CSP Lua SDK](https://github.com/ac-custom-shaders-patch/acc-lua-sdk) | Public upstream source under MIT; current main can differ from pinned CSP builds. | Installed preview SDK is stronger evidence for the reference machine. Pin a revision before adopting dependencies; no vendored code this phase. |
| [Pure publisher](https://www.patreon.com/cw/peterboese/home) | Release information belongs to the original publisher; package/hotfix labels can differ from core version. | Do not infer a hotfix number from core 3.50 or redistribute paid sources. |

## Bounded local findings

See [environment evidence](ENVIRONMENT.md) for paths relative to known roots,
exact versions, saved settings, interface candidates and preservation scope.
Metadata/SDK inspection is **observed locally**. Offline synthetic tests are
**tested and validated** only for the tested software contracts. Architecture
and tier budgets are **proposed**. Unmeasured runtime capabilities are **unknown**.

The official CSP patch landing page returned a redirect loop through the web
reader. A trustworthy build-specific 0.2.11 interface inventory was not obtained.
Community mirrors, reposted preview binaries and generic current API pages were
not accepted as proof of the stable build. Do not repeat broad searches or
change the reference install to resolve this gap. Obtain a legally supplied,
isolated 0.2.11 environment and its matching SDK during the next validation gate.

## FSR investigation conclusions

| Technique | Integration and inputs | Cost/artifact risks | Phase 0 status |
|---|---|---|---|
| Native | No upscaler dependency | Baseline aliasing depends on AA; required comparison | Always offered by planner; game result unknown |
| FSR 1 | Spatial; does not require temporal motion/history | Fine-detail loss and sharpening halos; output surface and bandwidth cost | Preview label observed; baseline CSP integration unknown |
| FSR 2 | Requires correct temporal inputs and resets, including depth/motion/jitter | History memory, ghosting/disocclusion, transparency and wheel artifacts | Preview 2.2.1 label observed; no runtime proof |
| FSR 3 upscaling | Temporal reconstruction; separate from FG | Similar temporal validation burden; integration-specific allocations | Preview 3.1.2 label observed; no runtime proof |
| FSR 3 FG | Requires separate timing/presentation and latency handling | Generated frames are not simulation throughput; latency, HUD, pacing | No callable CSP integration verified; disabled |

No numeric CSP memory or speed claim follows from AMD's upstream tables. A
working set measured in a different API, build or GPU is not a measurement of
this installation. Do not promise FPS, FSR2/3 on 0.2.11, or support on every
legacy board. Newer FSR SDK versions are outside the chosen dependency path.

## Pending measurements

- Pure Gamma/LCS: assign exposure/tonemap ownership, verify linear/gamma stage,
  color transfer, highlight rolloff, dark adaptation, fog, solar/headlight glare,
  reflections, wet surfaces, SDR/HDR output and VR separately.
- For each CSP track, probe actual symbols, modules, render format and resolution,
  available buffers, temporal resets, and loaded upscaler payload before enabling.
- Establish a fixed car/track/replay/time/weather/camera/driver/resolution baseline,
  then collect displayed frame-time samples and visual captures with native and
  one optional effect/upscaler at a time. No Phase 0 automated benchmark loop.
- Hardware matrix: actual 2 GB, 3-4 GB, 6 GB and 8 GB AMD/NVIDIA cards; memory
  bandwidth and driver support need independent evidence. The local RX 5700 XT
  is a development host, not a stand-in for low-memory boards.
- ReShade is optional research only; no dependency, injection, or add-on loading
  is needed for the foundation. Keep it outside the initial runtime architecture.
