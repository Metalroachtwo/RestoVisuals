# Compatibility matrix

Evidence date: 2026-11-01. **No CSP/Pure gameplay combination is runtime validated
by Phase 0.** `tested and validated` below applies only to stated offline contracts.

| Area | CSP 0.2.11 baseline | CSP 0.3.0-preview361 development | Enablement rule |
|---|---|---|---|
| Track detection | Proposed target; no isolated install available | Observed locally: binary, manifest and build 3898 agree | Target enum is not proof of compatibility |
| Basic graphics/PP controls | Unknown build-specific inventory; native/no extra pass is the design fallback | Observed default/user configuration and PP-context SDK | Read first; do not modify reference stack |
| Shader/fullscreen interface | Unknown for this exact build | Observed SDK declares fullscreen pass and extra canvas | Probe callable entry point, context and buffer format in isolation |
| Pure Gamma | Mandatory design target; Pure minimum needs independent confirmation | Observed 3.50 manifests/core; saved selection Gamma | Separate exposure/color calibration and visual gate |
| Pure LCS | Mandatory design target; same runtime gap | Observed 3.50 manifests/core and linear-space manifest hint | Separate calibration; no tier hierarchy |
| FSR 1 spatial | Upstream DX11 algorithm documented; exact CSP integration unknown | Observed 1.0.2 label, not selected or tested | Require matching validated integration before optional selection |
| FSR 2 temporal | Unknown; not assumed | Observed 2.2.1 label and prerequisite hints | Validate integration, depth/motion/jitter/resets, screen mode and payload |
| FSR 3 upscaling | Unknown; not assumed | Observed 3.1.2 label; not FG evidence | Same temporal gate; actual allocations/performance unknown |
| Frame generation | Unknown | No supported callable integration verified | Separately tested claim required; otherwise disabled |
| GPU memory pressure | Unknown in-game | External DXGI probe reports its own process budget only | No inference of game consumption or system free VRAM |
| Frame timing | Unknown exact-build semantics | Observed candidate API and simulation fields; units unverified | Use validated displayed intervals before optimization claims |
| Rain/wet/night/reflections | Proposed visual goals, unknown runtime compatibility | Existing configuration observed; no visual test | Validate both Pure modes with fixed scenes |
| Preview-only features | Never inherited by version assumption | Optional only after capability evidence | Fail closed when report/context is missing or different |
| 0.3.1 or other CSP builds | Outside authorized scope | Outside authorized scope | Configuration validation rejects them |

## Offline tests versus supported hardware

The planner exercises hypothetical 2/3/4/6/8 GB AMD and NVIDIA data, software
adapter rejection, feature-level requirements, evidence/context gating and
resource arithmetic. These are **tested and validated software contracts**,
not certified GPUs, measured frame rates or proven stable CSP compatibility.

The local RX 5700 XT has measured D3D11 device feature level 12_1 and approximately
8 GB dedicated capacity. No game GPU workload was captured. Older GTX 950/1050,
GTX 970/1060, RX 460/570 and other targets still need physical hardware testing.
No driver minimum is invented. FSR4, Tensor/RTX requirements, neural reconstruction
and proprietary vendor accelerators are not foundation dependencies.

## Pending release gates

1. Obtain an authorized isolated 0.2.11 installation and matching API inventory;
   never switch, install or downgrade the owner's reference CSP.
2. Establish each installed Pure fork's exact minimum CSP requirement and package
   hotfix revision; distinguish source gates from exercised runtime behavior.
3. Validate a read-only runtime probe and shader stage on each permitted track.
4. Compare Gamma/LCS visual captures in daylight, dusk, night, headlights, fog,
   wet/rain and high-contrast scenes; validate SDR/HDR and VR separately.
5. Measure native/effect/upscaler frame times and game-process memory on physical
   low-VRAM AMD/NVIDIA hardware. Check wheels, fences, transparent objects,
   disocclusion, HUD/mirrors and replay temporal resets.
6. Test installation ownership, config drift, crash/failure disablement and
   rollback before any active deployment is authorized.

See [research](RESEARCH.md) for primary references and the bounded stable-build
documentation gap. See [environment](ENVIRONMENT.md) for local evidence.
