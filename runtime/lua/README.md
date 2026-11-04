# Read-only CSP/Pure observer contract

## Phase 0D finite host experiment

`prepare-observer-probe --output .local/new-probe` stages three original Lua
files and a hash/run-ID manifest under a new workspace directory. It does not
install files, modify settings or launch a game. The unprepared loader is inert.
The candidate target is the uniquely owned
`extension/config-ext/PureLdrEffects/RestoVisuals_Observer_0D/` directory;
the installed Pure global loader remains unmodified.

The prepared entry requires the existing Pure weather context and pins the
owner's preview361/Gamma experiment. It reuses the observer unchanged, returns
no rendering override, registers no Pure named effect and writes only its own
`runtime-receipt.json`. Import/re-entry has a uniquely owned lifetime guard.
The new host probe arranges a ten-second script-timer stop, invokes the returned
unsubscribe and checks for later native callbacks over another one-second
script-timer interval. Timer intervals are not guaranteed wall-clock durations
when the host does not update. Receipt failures and unknown handles block start
or stop the owned observation; there is no automatic retry. `onRelease` remains
best effort, with explicit stop handling required as well.

The two timers and release handle are owned by this experiment. A late callback
fails the cleanup witness while the observer itself stays inert. Zero callbacks
remain zero and do not validate the PP stage. Neither this probe nor synthetic
tests determine texture encoding, render a neutral pass, or certify named-effect
removal. Actual file rollback requires a verified manifest, no active game,
unchanged owned source hashes and handling only declared owned output; do not
recursively remove an unverified directory.

The wrapper retains `observer_before_stop`, since the original observer's normal
stop state must not hide a prior mode/API fault. A blocked pre-stop snapshot
fails the terminal experiment even when callback removal subsequently succeeds.

Deployment is conditional on the Phase 0D gates and critical review, even though
the owner has authorized the task. No foreign file, shared test-ground script,
existing Pure LDR bridge or active filter slot may be overwritten. The package
and Lua contract tests alone are not native loading/unloading validation.

`restovisuals_observer.lua` is original module source, not an installed PP filter.
Import has no registration side effect. No manifest or installer is supplied:
the working Pure scriptable-filter slot must remain owned by Pure.

## Host contract

An authorized isolated host must expose the real CSP `ac` namespace and the
Pure SDK namespace in that script context. `new(host, config)` accepts exactly
`csp_version`, `pure_mode` and optional `max_samples` (1-64, default 8).
`start()` verifies exact track/version, stable build 3465 or preview build 3898, required callable
APIs and Pure's linear-space signal before registering the read-only callback.
`stop()` invokes only its own returned unsubscribe function. Calling start/stop
again is idempotent while cleanup succeeds.

The returned `receipt()` is a copied Lua table. A host can serialize it through
an independently validated JSON sink. Record `execution_scope` truthfully as
`csp_runtime_unverified` for a future real game-host test; automated tests use
`lua_contract_fixture`. A claimed host scope is not attestation and this receipt
does not automatically promote planner capabilities to tested/validated.

Every callback returns nil, ignores the post-processing parameter structure,
does not allocate/render a texture, and does not write exposure/settings.
Auxiliary/second-eye callbacks do not run adaptation. Mode changes, invalid
callback data and missing APIs disable observation. Sample history is bounded.
Resize changes are recorded, not handled by creating buffers. Raw CPU/GPU timing
values retain unknown units and must not be converted into FPS.

Optional read-only queries record Pure PP enabled/YEBIS bypass state and the
presence of named SPICE HDR/LDR registration APIs. Registration APIs are never
called. Raw simulation flags `isFSRActive`, `isTripleFSRActive` and `isHDR` remain
raw booleans; they do not identify an upscaler algorithm, frame generation or
texture encoding. Missing/failed queries preserve unknown values.

If registration throws, unsubscription fails or registration returns an unexpected handle, the
callback stays locally inert, restart is blocked, and cleanup remains unknown.
There is no automatic retry, application restart, foreign subscription removal
or claim that native cleanup succeeded. Host reload/recovery needs the existing
authorization and access policy. Lua pcall cannot promise recovery from fatal
native/C++ exceptions; no rendering operation is performed by this observer.

## Pure semantics and unsupported stages

`pure.system.isCSP_LCS()` reports the shader linear-space state according to
the installed SDK mappings. It does not identify the weather fork, exact Pure
hotfix, sampled texture encoding, SDR/HDR output transfer, or a PP callback's
ordering against Pure's replacement renderer. Receipts preserve those unknowns.
The observer claims neither HDR/depth access nor a GPU shader dispatch.

`ac.onPostProcessing()` is the documented YEBIS callback candidate; Pure may
replace/bypass that flow. Registration alone does not prove callback invocation
or harmless composition with another renderer. That requires an isolated game
receipt and image-preservation test. No such game execution occurred here.

## Isolated contract tests

Only the optional tests need [Lupa](https://pypi.org/project/lupa/). Its native
LuaJIT 2.1 runtime executes the original Lua module with synthetic CSP/Pure
functions. The CPython 3.14 Windows x64 wheel is hash-pinned and installed into
ignored project-local dependencies, never the game or global Python environment.

```powershell
python -m pip --isolated install --no-deps --only-binary=:all: --require-hashes --target .local/devdeps -r requirements-lua-tests-win-cp314.txt
$env:PYTHONPATH = (Join-Path (Get-Location) '.local/devdeps')
python -m unittest discover -s tests -v
```

Different Python/platform wheels need their own reviewed hash; do not remove
hash enforcement. Without optional LuaJIT, these tests explicitly skip and the
original 56 tests still run. The Phase 0B full run used Lupa 2.8 and LuaJIT
2.1.1774896198. No CSP/Pure DLL, FFI export or proprietary module was loaded.
