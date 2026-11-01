# Version-matched CSP 0.2.11 source reference

Date: 2026-11-01. A bounded request to the
[official 0.2.11 archive](https://acstuff.club/patch/?get=0.2.11) succeeded.
This resolves the earlier missing SDK inventory; runtime certification remains
blocked. No reference-game file or automatic-update setting was changed.

## Provenance and isolation

- Downloaded archive: 124,854,406 bytes, inside ignored project-local storage.
- SHA256: `0729ccaebb403a7a6d1c40516990da8116cb5f56eea4c1fe0bdd29863a5a6ffb`.
- Archive manifest: CSP **0.2.11, build 3465**.
- Extracted binary version resources: file/product version **0.2.11.0**.
- Selected PP/WeatherFX SDK and configuration files were inspected privately.
  The archived DLL was read only for version metadata, not loaded/executed.
- The archive, binary, SDK source/docs and raw inventory are not tracked or
  redistributed. This is a reference archive, not an installed/runnable game.

Version provenance is the official request plus archive hash, agreeing manifest
and binary resources. It is not a signature-based authenticity attestation or
evidence that a callback/shader runs. The stable and preview SDKs stay separate
private evidence sets; RestoVisuals still has one shared adapter codebase.

## Declared interfaces compared with preview361

| Interface/field | 0.2.11 build 3465 | Preview361 build 3898 | Interpretation |
|---|---|---|---|
| `ac.getPatchVersion`, `getPatchVersionCode` | Declared in PP/WeatherFX SDK | Declared | Exact version/build gates; runtime return still needs a game receipt |
| `ac.onPostProcessing` | Declared with the YEBIS callback contract | Declared | Candidate observer path, not proof Pure invokes it |
| `render.fullscreenPass` | Declared | Declared | Supported shader interface at source level; actual game binding/stage unknown |
| `render.getRenderTargetSize`, `ui.ExtraCanvas` | Declared | Declared | Does not establish current buffer format, lifetime or need for a new surface |
| `ac.getPerformanceCPUAndGPUTime`, `ac.getSim` | Declared | Declared | Timing units/display interval semantics still unmeasured |
| Simulation `isFSRActive`, `isTripleFSRActive` | Declared | Declared | Raw upscaling-section flags; do not identify FSR generation/algorithm |
| Simulation `isHDR` | Absent from the version-matched struct declaration | Present | Probe independently and preserve unknown on stable, rather than letting a missing FFI field hide other values |

These are **documented/observed source declarations**, not tested CSP runtime
capabilities. The original Lua adapter is exercised only with synthetic host
functions in LuaJIT; isolated D3D11 shader execution does not certify either CSP.

## Upscaler configuration difference

Stable's FSR section exposes an active switch and a **boolean**
`OLD_IMPLEMENTATION`: 0 selects the official-SDK-based spatial implementation,
1 the older spatial port. The stable source/config does not establish an exact
FSR SDK revision, FSR2/3 temporal integration or frame generation. No such mode
is enabled or advertised as certified.

Preview361 reuses the same key as a larger method enum, including FSR1, NIS,
FSR2 and FSR3 labels. Therefore interpreting stable value 2 as preview NIS would
be wrong. The read-only audit now chooses a version-specific map and reports
unknown for unsupported IDs or missing/unknown manifest versions. This is
parsing evidence, not a setting migration or live configuration change.

## Adapter changes and validation

The observer now gates stable build 3465 and preview build 3898 explicitly.
Optional simulation fields are read under independent protected calls because
FFI access to absent struct fields can raise. No missing-field failure may
discard other available flags or enable a rendering module.

All **92 tests passed** with optional LuaJIT present. Added regression coverage
checks version-scoped upscaler parsing, stable build mismatch rejection and a
synthetic stable struct that raises on `isHDR` while preserving FSR flags.
No 0.2.11 DLL or game code was executed. No binary was copied into the working
installation and no global updater/driver/application configuration changed.

Remaining gate: a properly isolated, authorized Assetto Corsa instance running
this exact build and matching Pure package, followed by a callback/format/order
receipt and identity image test. Do not satisfy it by switching the owner's
preview installation, copying a live DCC scene, launching an unisolated game,
or introducing GUI automation.
