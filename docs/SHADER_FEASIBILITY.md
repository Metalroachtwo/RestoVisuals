# Original color-pass feasibility

Phase 0B supersedes the original compilation-only status below: both pixel
entry points have now executed in an isolated D3D11 context on the development
GPU. The initial strict identity failure was fixed with a neutral fast path;
four identity and six numerical color cases pass. Current source hash and
1788/2180-byte compilation results are in [Phase 0B](PHASE0B_RUNTIME.md).
CSP/Pure execution, visual quality and game performance remain NOT ASSESSED.
The remainder of this document preserves the Phase 0 checkpoint record.

Status: **compilation and CPU-reference contracts validated; GPU execution,
CSP integration, visual quality and performance NOT ASSESSED**.

## Artifact and dependencies

`shaders/RV_ColorPrototype.hlsl` is original project source. It combines optional
exposure compensation, a luminance-based rational highlight shoulder and
saturation adjustment in one pixel pass. This is a mathematical prototype, not a
physically based renderer, neural reconstruction, calibrated PP filter or novel
upscaler. It adds no bloom, depth, reflections, atmosphere, rain or material detail.

The prototype uses standard HLSL/SM5, no includes, vendor SDK, paid source or
external shader dependency. Intended GPU API requirement is D3D11 feature level
11_0 or higher; compilation does not certify a GPU/driver. The offline compiler
loads only System32's `d3dcompiler_47.dll` with strictness, IEEE strictness,
optimization level 3, warnings-as-errors, and no debug information. It disables
include processing and keeps bytecode in memory.

Compilation API and flags follow [Microsoft D3DCompile](https://learn.microsoft.com/en-us/windows/win32/api/d3dcompiler/nf-d3dcompiler-d3dcompile)
and [compiler constants](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/d3dcompile-constants).
The local compiler file reports 10.0.26100.9711; it was not installed or replaced.

## Contracts and color ownership

The constant buffer is 16 bytes: exposure EV, shoulder strength, saturation,
reserved. Identity parameters are `(0, 0, 1, 0)`. Proposed valid ranges are
EV [-4,4], shoulder [0,1] and saturation [0,1.5]. The host must provide finite
FP16-range RGBA inputs and valid parameters. Alpha passes through unchanged.

`PSLinear` expects already linear RGB; `PSSrgb` explicitly decodes and encodes
display sRGB, clamping display values to [0,1]. A Pure Gamma weather choice does
not prove the sampled texture contains sRGB-encoded pixels. A sampler/texture
with hardware sRGB conversion would require different binding decisions. Neither
entry point is assigned to either Pure mode until actual stage/format ownership
is measured. In HDR-output pipelines, do not substitute the sRGB entry point.

For linear RGB C, luminance Y uses standard Rec.709 weights. The exposed value
E is `max(C,0) * 2^EV`; the shoulder is `E / (1 + strength * luminance(E))`.
It preserves channel ratios with saturation 1, preserves black, and has a
monotonic grayscale response for valid parameters. RGB output is clamped to
[0,65504] for the proposed RGBA16F surface contract. This deliberately loses
negative scene values; excessive exposure/saturation or FP16 clipping can alter
highlights and hue. Identity is only guaranteed within the documented encoding
and positive finite range.

Pure retains exposure control in the intended first integration. Compensation
must not become a competing adaptation loop. Adding this shoulder after Pure's
tonemapper could double-compress highlights. Thus both default profiles keep
the pass disabled. No adaptation or weather-dependent calibration is implemented.

## Actual validation on 2026-11-01

`python -m restovisuals compile-shader shaders/RV_ColorPrototype.hlsl`

| Entry | Target | Result | Bytecode bytes |
|---|---|---|---|
| PSLinear | ps_5_0 | S_OK, warnings-as-errors | 1568 |
| PSSrgb | ps_5_0 | S_OK, warnings-as-errors | 2020 |

Source SHA256: `54d53490196acdf13d1c39d8e2bbc2d680b084a47424b32f17e7de67ece35706`.
Machine-local compile report records bytecode hashes for reproduction. Different
compiler versions may produce different bytecode. The compiler succeeds on the
source at this checkpoint; no performance improvement follows from bytecode size.

The CPU reference checks black/dim/HDR identity, EV scaling, monotonic shoulder,
channel ratios, desaturation, sRGB round trips including the breakpoint, FP16
output limits and invalid input rejection. Native tests additionally check that
broken shaders fail and includes are disabled. They do not compare shader output
against GPU readback, inspect quantization artifacts, or establish a runtime cost.

## Pending visual/performance gate and rollback

Before any deployment: validate the supported CSP entry point, input encoding,
HDR/SDR transfer, texture format, viewport, sampler, alpha semantics and Pure
ownership on an isolated installation. Start with identity parameters, compare
GPU readback against the CPU reference with an explicit FP32/FP16 tolerance, then
capture gradients and representative daylight/night/rain scenes for both modes.
Inspect banding, halos, saturated highlights, dark detail and exposure pumping.

Measure GPU pass duration and game frame-time deltas using stable native/effect
captures, and measure actual allocated output surfaces. A single proposed 1080p
RGBA16F output is 15.82 MiB, excluding CSP resources and allocator overhead.
Low-memory hardware must pass independently. There is no measured GPU duration,
VRAM allocation, image-quality improvement, or FPS result in Phase 0.

The prototype is never installed. Rollback now consists of not selecting or
deploying it; native rendering and existing configuration have not been altered.
Future integration must prove module-disable and owned-key restoration before
changing a known-good configuration.
