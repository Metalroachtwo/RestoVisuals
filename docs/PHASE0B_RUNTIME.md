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
