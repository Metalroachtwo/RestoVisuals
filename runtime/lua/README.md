# Read-only CSP/Pure observer contract

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
