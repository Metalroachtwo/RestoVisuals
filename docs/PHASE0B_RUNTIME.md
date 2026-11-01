# Phase 0B runtime integration record

Session resumed from `c9177484c2c3fd460f3e32dc855af1db895728e1` on
`phase0/foundation`; local/remote SHA matched and all original 56 tests passed.
The first actual weekly reading was 22% remaining. Phase 0B begins bounded
closeout at 9-7%, enters synchronization at 7-5%, and stops all new research,
engineering and testing at 5%. No reference-game deployment is authorized.

## Supported interface investigation

The installed preview361 PP-context SDK includes `script.update(dt)` and
`render.fullscreenPass()`. A documented scriptable-filter direct pass can read
`dynamic::screen`. `ac.setFilterActive()` controls the scriptable filter, but
this is not a global RestoVisuals enable/disable permission.

The saved scriptable-filter implementation is **pure**, whose installed manifest
describes a Pure LDR bridge. It reads Pure's shared PP state and commands. This
is a real ownership constraint: replacing that slot with a RestoVisuals filter
could remove Pure processing. Do not install a separate filter into that slot.

Another documented candidate is `ac.onPostProcessing(callback)`, present in the
installed PP and WeatherFX contexts. Its signature supplies parameters, exposure,
main-pass/update-exposure flags and render size; the callback returns a disposable
subscription. Returning nil leaves the YEBIS flow intact; true suppresses YEBIS;
returning a canvas replaces its HDR input. Phase 0B will use a nil-returning
observer contract only, with no parameter writes, canvas or exposure controller.
Actual invocation under Pure's YEBIS replacement still needs a game receipt.

Both installed Pure SDK mappings expose `pure.system.isCSP_LCS()`, aliasing a
CSP linear-space state. This is evidence for the current shader color-space
mode when exposed in the proper Pure script context; it does not prove the
weather implementation's fork identity, texture encoding, version or that the
Pure namespace exists in an unrelated CSP script. Unknown remains unknown.

Public primary source:
[CSP PP-script context](https://github.com/ac-custom-shaders-patch/acc-lua-sdk/blob/main/ac_pp_filters.lua),
[post-processing callback](https://github.com/ac-custom-shaders-patch/acc-lua-sdk/blob/main/wfx_impl/ac_postprocessing.lua).
Current upstream source is not a version-matched 0.2.11 SDK and cannot certify
that build. The installed preview SDK and protected version resources provide
the preview source-level evidence; neither constitutes successful runtime/GPU
execution in CSP.

## Validation path and current limits

The working game stays read-only. A seven-file targeted integrity snapshot
protects the locked binaries, CSP manifest, Pure weather sources, LDR bridge and
PP SDK; no repeat of the full Phase 0 installation discovery is needed.

Next bounded units are an original read-only Lua observer with explicit context
gates and isolated Lua contract tests, followed by native windowless D3D11
execution/readback of the existing identity shader. The latter can validate GPU
math on the development adapter without starting Assetto Corsa, creating a
window/swap chain, or claiming CSP/Pure integration success.

CSP 0.2.11 runtime certification is BLOCKED pending an authorized isolated
installation and matching SDK. Preview361 in-game callback/pipeline validation
is BLOCKED pending an authorized isolated game host/loading path. No connected
Assetto Corsa runtime tool is exposed in this session. These blockers do not
prevent source-contract and isolated GPU validation. No DCC gateway or GUI
provider is initialized as a substitute.

## Read-only observer implementation checkpoint

Implemented `runtime/lua/restovisuals_observer.lua` as a module with explicit
start/stop and injected native namespaces. It has no import-time registration,
filter replacement, shader dispatch, exposure/settings writes or texture access.
It gates exact CSP version/build and requested Pure shader-space profile, records
bounded callback samples and resize events, and keeps timing units unknown.
Every callback returns nil; only its own function unsubscribe handle is invoked.
Cleanup failure leaves an inert callback and blocks restart without retries.

All original tests plus 19 LuaJIT contract tests passed: **75 total, no skips**
with the optional project-local dependency. Tests exercise the original Lua
source under LuaJIT 2.1.1774896198/Lupa 2.8, including missing APIs, version and
mode mismatch, main/auxiliary/second-eye callbacks, frozen PP parameters,
bounded sampling, resize, registration errors and cleanup failures. These are
executed Lua contracts with synthetic host functions, not CSP game execution.
See [observer host contract](../runtime/lua/README.md).

## Isolated D3D11 execution and identity defect

Executed the original pixel shaders on the RX 5700 XT in a separate, explicit
adapter-0 D3D11 device at requested feature level 11_0. No game, window, swap
chain, injector, proprietary renderer or application configuration was involved.
The harness uses original fullscreen-triangle source, system D3D11/DXGI/compiler
DLLs, format support queries, three owned textures, bounded nonblocking readback,
GPU timestamp/disjoint queries and deterministic resource release. COM ABI/slots
were checked against installed Windows SDK 10.0.26100.0 `d3d11.h`.

The first identity run found an actual defect in the Phase 0 prototype. For 1953
synthetic pixels per case (63x31), neutral parameters changed 610/4375 channels
in RGBA32F linear/sRGB and 366/3785 in RGBA16F. Linear saturation interpolation
lost small channels beside HDR values through cancellation; sRGB decode/encode
round trips also changed neutral output. The gate correctly skipped all color
cases when identity failed. No claim of an in-game defect or visible difference
is inferred from those synthetic pixels.

Added an exact neutral path to both original shader entry points and the CPU
reference. The second GPU run passed all four identity cases with **zero channel
differences**, including exact alpha, across RGBA32F and RGBA16F. Only then did
six nonidentity cases execute. All matched the CPU reference within the declared
precision tolerances; alpha remained exact in every case.

| Validation | RGBA32F result | RGBA16F result |
|---|---|---|
| Linear identity | exact, max error 0 | exact, max error 0 |
| sRGB identity | exact, max error 0 | exact, max error 0 |
| Linear exposure/shoulder | max absolute error 0.00000190735 | max absolute error 0.015625 |
| Linear desaturation/shoulder | max absolute error 0.000000476837 | max absolute error 0.00390625 |
| sRGB transform | max absolute error 0.000000363216 | max absolute error 0.00048828125 |

Nonidentity thresholds are per-channel `3e-5 + 5e-6*abs(reference)` for RGBA32F
and `0.002 + 0.002*abs(reference)` for RGBA16F. Half precision has larger HDR
quantization steps; its absolute errors above must not be described as zero or
as exact CPU/GPU equivalence. Identity and alpha use exact equality, not those
nonidentity tolerances. Inputs and expected outputs are quantized to the tested
format before comparison. Odd-width rows exercise GPU row padding correctly.

GPU timestamps were non-disjoint for all ten draws. Single-draw durations in the
successful 63x31 run ranged from **0.00160 to 0.00224 ms**, including pipeline
overhead. This tiny synthetic workload is not a stable throughput benchmark,
1080p cost estimate, FPS gain or CSP/Pure timing result. No scaling extrapolation
is made. Declared texture payloads were 93,744 bytes for the three RGBA32F
textures and 46,872 bytes for RGBA16F; driver allocation/VRAM placement was not
measured. The staging texture is a readback resource, not a claimed game target.

Current color source SHA256:
`f762d3e4e98295b257b2fd46452023857e3b8d972c753d268835061dcf6fce88`.
Both PS entry points compile at 1788/2180 bytecode bytes using the same system
compiler. Original source/history and the first failing receipt are preserved;
machine-local raw reports remain ignored. There are now **86 passing tests**
with LuaJIT enabled, including precision regression, identity-before-color gate,
native resource ABI, input-size bounds and two-second query timeout tests.

Run explicitly with `python -m restovisuals gpu-validate --adapter-index 0`.
Numerical failures return exit 4. The normal test suite does not silently start
GPU draws; this command is the separate hardware-execution gate. CSP callback
composition, actual game buffer encoding/lifetime, physical legacy GPU support
and visual quality remain unvalidated. The observer still cannot dispatch this
shader in the reference game and no planner capability is promoted by the test.

## Subsequent source evidence

The [official 0.2.11 reference](CSP0211_REFERENCE.md) now resolves the missing
version-matched SDK. Its manifest/build and binary version resources were
inspected without installation/execution. The earlier source-inventory blocker
is superseded; isolated stable/preview **game runtime validation remains BLOCKED**.
Version-specific parsing and optional-field handling are covered by **92 passing
tests** with LuaJIT enabled. Dream Realism reference findings and the related
Pure extension route are recorded in [the bounded analysis](DREAM_REALISM_REFERENCE.md).
