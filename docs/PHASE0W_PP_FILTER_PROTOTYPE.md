# Phase 0W: original offline photographic PP prototype

Starting verified checkpoint: `c32d657ca0067af98edc68724aaa2fa5f3b3a642`,
`phase0/foundation`. **Working offline CPU/HLSL processing, three presets and
original GPU-rendered previews are delivered. Native CSP/Pure operation remains
unverified and deployment is NO-GO.** No GUI/game/CM launch or installed write.

Open [the before/after viewer](../examples/phase0w-pp/index.html),
[GPU evidence](../examples/phase0w-pp/report.json),
[presets](../presets/photographic.json), and
[disabled installation proposal](../examples/phase0w-pp/disabled-installation.json).
The chart is original synthetic input, **not Assetto Corsa/Pure output** or proof
of superiority over Dream Realism. No proprietary source, LUT or capture is reused.

## Implemented source and mathematical contract

[photographic.py](../restovisuals/photographic.py) and
[RV_Photographic.hlsl](../shaders/RV_Photographic.hlsl) implement the same original
pipeline: exposure in stops; linear RGB white-balance gains normalized for neutral
luminance; contrast around 0.18; bounded shadow response; saturation; a continuous
maximum-channel highlight knee; effect-intensity interpolation. Alpha is preserved.
Disabled, zero-intensity and neutral settings bypass processing exactly.

The independent reference accepts finite nonnegative linear Rec.709 RGB through
65504, straight alpha in [0,1], or explicitly declared sRGB/Rec.709 RGB in [0,1].
Unknown encodings, invalid settings, bool-as-number, NaN/Inf and invalid alpha are
rejected. Negative/wide-gamut values are outside this prototype contract. This
contract describes our fixtures, **not CSP's unresolved HDR input**.

The knee starts at maximum RGB 0.72; above it, distance d maps to
`d/(1 + highlight*d/0.28)`. Full highlight response approaches 1 continuously,
preserving highlight ordering without hard clipping. Lower response or partial
intensity can retain values above 1; the preview encoder then clips for display.
No process recovers information already clipped in an input image. RGB gains are
an original modest white-point treatment, not a calibrated chromatic-adaptation
transform or a Kelvin-to-RGB model. No spatial sharpening/bloom stage is added.

`transition()` provides bounded exponential parameter settling; split-step and
single-step behavior is tested. `controlled()` resolves common controls against
each preset, preserving preset defaults and bounding effective values. HLSL is
specialized from validated settings at compilation time; dynamic game control
buffer updates are not implemented or claimed.

| Preset | Original treatment |
|---|---|
| Balanced Photorealism — Default | Neutral gains, contrast 1.03, saturation 0.99, shadow response 0.15 |
| Warm Photorealism | Subtle red/blue gains 1.025/0.975, restrained saturation/contrast |
| Cool / High Contrast | Blue/red gains 1.03/0.975, contrast 1.10 with shadow response 0.20 |

## Verified configuration surface and isolated runtime gates

Read-only evidence comes from the installed Kunos `system/cfg/ppfilters/default.ini`
and Pure Gamma 3.50's shipped SDK declarations. The three original candidate INIs
use only observed `[YEBIS]`, `[AUTO_EXPOSURE]`, `[TONEMAPPING]` and `[COLOR]` keys.
Function ID 2 is the previously documented Sensitometric engine control. All
key/section pairs are checked against that local reference; source hashes remain
private under `.local/phase0w-validation/source-evidence.json`.

These are **candidate engine configurations**, not an implementation of our HLSL
inside the game. Their saturation/contrast settings are independent calibration
seeds; all temperature/white-balance values stay neutral pending verified native
semantics. Sparse-INI defaults, Pure overrides, complete minimal schema, actual
selection and exposure behavior remain unverified. No claim that the three native
appearances match the offline presets. Existing Pure default-script fallback is
the documented candidate route; its exact native behavior still needs validation.

The proposed uniquely owned paths are `system/cfg/ppfilters/RestoVisuals.ini`,
`RestoVisuals_Warm.ini` and `RestoVisuals_Cool.ini` in that same directory. Current
collision checks pass; the disabled manifest records exact source hashes. No
auto-discovered `pure_scripts` companion, scriptable-filter slot, custom HDR
callback or effect registration is supplied. The existing Pure LDR bridge remains
untouched. No installer is built.

[The Lua control module](../runtime/lua/restovisuals_pp_controls.lua) uses the
version-matched documented `pure.script.ui.addSliderInteger(name,value,min,max,tooltip)`,
`addSliderFloat(name,value,min,max,tooltip)` and `getValue(name)` signatures.
It exposes preset, intensity, EV, highlights, shadows, saturation and contrast.
Import/construction is inert; an explicitly reviewed host must call initialization.
It rejects unsupported capability metadata or missing APIs, catches read failures,
and latches partial creation failures against automatic retry. Control state is
tested against the CPU preset resolver. **`rendering_connected` remains false.**
No exposure setter or rendering callback is called. A native host, metadata
verification, UI teardown and attachment to a safe rendering stage are unresolved.
There is no verified UI removal mechanism; partial registration cannot be claimed
reversible in-game. The module is therefore not installed or auto-loaded.

## Actual validation and measurements

**29 targeted tests pass, zero failures**: 11 photographic, seven LuaJIT control
fixtures, plus 11 existing color/compiler checks. All original 201 definitions
remain unchanged; there are now 219 definitions. Full-suite rerun was unnecessary
because existing implementations are unchanged. Lua tests use the already present
isolated optional dependency in `.local/devdeps`; nothing was installed.

Eight SM5 pixel programs compile with strict warnings-as-errors: neutral and three
presets, each linear and sRGB entry. Four linear RGBA32F GPU cases execute through
the **existing windowless D3D11 renderer**, at 512×128, then compare every channel
with the CPU oracle. No window/swap chain, second renderer or game integration.

| GPU case | Maximum absolute CPU/GPU error | Float pixels with RGB peak ≥1 |
|---|---:|---:|
| Neutral | 0; input/output bytes identical | 18,144 |
| Balanced | 2.42e-7 | 0 |
| Warm | 3.42e-7 | 0 |
| Cool | 3.16e-7 | 0 |

Alpha is exact in all four cases; owned dispatch and device resources are released.
The clipping count is a **linear-value threshold before display encoding**, not a
claim of lossless 8-bit quantization or native highlight recovery. Synthetic shadow
and HDR grey ramps remain ordered, positive shadows survive, and black stays zero.
The sRGB entries compile and CPU encoding paths are checked; sRGB GPU dispatch is
not newly validated here.

Single-draw timestamp observations were 0.00280–0.00284 ms, excluding generation,
upload, readback and export. They have no warm-up/repetition basis for a performance
ranking; no game FPS, Dream comparison or production speedup is inferred.

An initial shader-compiler warning was fixed by making the positive power domain
explicit. Two first demo attempts reported device removal because the new caller
passed bytecode instead of owned shader objects. The caller now creates/checks
native shader handles; the corrected four-case run passed. No driver restart,
software change or usage reset was used. Failed private output directories remain
preserved; they are not success evidence.

## Reproduction, recovery and exact continuation

From the repository root, run `python -m restovisuals.pp_demo --output .local/new-pp-run`.
The destination must be a new owned workspace folder. Run numerical/compiler tests
with `python -m unittest discover -s tests -p test_photographic.py`. For Lua fixtures,
prepend the existing `.local/devdeps` to Python's module path as in prior Lua tests.
The viewer and all five PNGs are original GPU outputs with only standard image
chunks; raw memory samples/device timestamps remain private.

Native deployment stays **NO-GO** until complete INI/default/exposure behavior,
Pure fallback ownership and a supported removable controller/render host are
established. Do not try the blocked HDR callback. Future review must recheck all
collisions/hashes and fresh settings backups, define exact registration/selection,
rehearse failure/interruption recovery, then compare original/enhanced/restored
controlled captures. End the owned game normally, restore the previous filter
and exact changed settings, remove only hash-matched owned additions, cold-load
the original and verify protected files. Old run-bound transactions are not reused.

No installed recovery is required for this phase. Original shaders/material work,
the approved untracked visual target, locked versions, freeware and undecided
licensing are preserved. Starting live allowance was **26% five-hour / 22% weekly**;
final readings and verified Git SHA are retained privately. Both resets remain
reserved and unused. Next: review the standard PP-only package/default inheritance
and the safe host/processing connection; keep this tested offline core as the oracle.
