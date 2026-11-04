# RestoVisuals Phase 0D continuation handoff

Prepared 2026-11-04, America/New_York. Current work resumed from verified Phase 0C
HEAD `5fa7c42491ecb0cd049232fc70ae35d08ca21dbb`. The owner-supplied approved
reference PNG is untracked and preserved. The original 104 tests remain unchanged;
118 now pass with the declared optional LuaJIT dependency.

Read [DREAM_WEATHER_ARCHITECTURE.md](DREAM_WEATHER_ARCHITECTURE.md) and
[PHASE0D_RUNTIME.md](PHASE0D_RUNTIME.md) for new findings and the bounded native
experiment. Initial Phase 0D code/research checkpoint
`a3b4d4f6b74d23f9831c6fdc2393dde97fe775f7` is pushed and verified. Later revisions
preserve a pre-stop fault snapshot and harden exact-file recovery before deployment.

The owner conditionally authorized a reversible live-installation experiment and
routine GUI testing only weekdays 08:00-17:00 Eastern, launching through Content
Manager exclusively. Earlier blanket Phase 0 prohibitions below are historical
for that scoped exception; version locks, protected files, lifecycle/rollback,
Pure bridge ownership and the 5% cutoff remain mandatory. No isolated host was
provisioned. The full rendering gate is not waived by GUI authorization.

Critical review permits one observer-only v2 package, not rendering. Native
acceptance requires positive main-pass callbacks, actual version/build/context,
clean preserved pre-stop state, successful disposal and a quiet stop witness.
The package is bound to run `517dbe86abfa432e8f99d6b64ad860fd`; do not substitute
the initial transaction helper/package or retry automatically after failure.

Private continuation/recovery artifacts live under `.local/phase0d-20261104/`:
`preflight.json` (29 protected files and 49 verified settings backups),
`before-game-settings.json`, `package-v2/`, `rollback-rehearsal-v2.json`,
`safety-review-v2.json` and owned CM PID/window observations. The exact-file helper
is `.local/phase0d_transaction_v2.py`; its first intent journal must precede any
game write. It preserves ambiguous output/edited files and disables only verified
owned executable source. Retain the reviewed package until recovery completes.

At this checkpoint CM alone has been opened for read-only inspection. No live
RestoVisuals file or game launch has occurred yet. Actual experiment and rollback
results must replace this pending status before closeout. Never infer a neutral
pass, game FPS, LCS support, encoding or effect-removal proof from the preparer,
observer source or 51 synthetic filesystem failure-point recoveries.

Phase 0D first live weekly reading was 100%; pre-deployment reading was 94%.
Read the meter anew rather than reusing those values as a budget.

---

## Historical Phase 0C handoff

Prepared 2026-11-01, America/New_York. **Current checkpoint is Phase 0C**;
the explicitly historical Phase 0B record below is retained to avoid repeating
completed investigations. No automation has been scheduled.

## Current repository and policy checkpoint

Repository: [Metalroachtwo/RestoVisuals](https://github.com/Metalroachtwo/RestoVisuals).
Branch: `phase0/foundation`; no automatic merge to main. Latest tested and remotely
verified code: **`d83b1f4b272f40c044fa0cfbd3ce59b4154df16f`**. The final documentation
HEAD is recorded by Git and ignored `.local/phase0c-final-sync.json` after closeout;
verify with `git rev-parse HEAD` and `git ls-remote origin refs/heads/phase0/foundation`.

Phase 0C meaningful checkpoints, each pushed and verified:

- `92088687608b34ea8e43b9d96ddc1a022ebb37cc`: mandatory first freeware checkpoint.
  README and AGENTS preserve existing restrictions and require 100% free official
  functionality, no paid tiers/trials/ad/account unlocks, and optional donations
  that never gate access. Premature open-source wording was corrected.
- `4966b1ac091beb11adfdb29d5b69336cd56db78c`: host isolation acceptance/rollback
  gate and [external dependency boundaries](FREEWARE_AND_DEPENDENCIES.md).
- `d83b1f4b272f40c044fa0cfbd3ce59b4154df16f`: full-resolution demonstration using
  the existing D3D11 renderer, memory samples, bounded draws, export safety and tests.

Repository license remains **undecided, pending owner approval**. Freeware is not
an open-source license. Assetto Corsa, Pure, CSP/CM and proprietary filter content
retain separate acquisition/distribution terms; none is bundled. Lupa/LuaJIT is
an optional private test dependency, not an end-user rendering requirement.

## Current validated results

See [Phase 0C evidence](PHASE0C_RUNTIME.md), [public original chart viewer](visuals/phase0c-demo/index.html)
and [sanitized measurements](visuals/phase0c-demo/report.json).

- **104 tests pass with no skips** using the declared optional LuaJIT setup.
  All 93 original tests remain unchanged. Without LuaJIT, 79 execute and 25 skip.
  The 11 new tests target actual full-frame checks, encoding/precision, PNG
  transfer/CRC, destination safety, failure gates and owned resource cleanup.
- A fresh 56-file tracked-source export passes both configurations without
  private game/SDK files. All 16 native 720p/1080p cases pass from that export;
  every raw readback and all 24 PNG hashes reproduce the first run exactly.
- Eight full-frame exact identities precede eight color cases across two
  resolutions, float/half and explicit scene-linear/sRGB-display. Color checks
  require finite pixels and exact alpha everywhere, plus 3,672 declared probes.
  The original four-identity/six-color small GPU regression still passes.
- RX 5700 XT, explicit adapter 0, feature-level-11_0 device; driver metadata
  32.0.21043.12001. Source and pixel bytecode hashes are unchanged. Measurements
  are single five-draw batches after one warmup, excluding upload/readback/export.
  They are not gameplay FPS or improvement claims. The published report records
  exact tolerances, per-case timing, format, dimensions and hashes.
- DXGI samples describe this process's local segment. Owned COM references
  return to baseline, while some immediate memory samples remain elevated until
  later sampling. No peak/allocation/leak/low-VRAM certification is inferred.
- Visual inspection covers original chart structure, ramps, patches and intact
  edges only. No game image, Pure calibration, physical legacy/NVIDIA board,
  gameplay frame time or artistic improvement has been validated.
- Seven previously captured protected core-file hashes and 19 unique Dream
  file/dependency states still match. This is a targeted prior-snapshot comparison,
  not a new full-installation audit. No deployment, GUI/DCC operation, game launch,
  feature/account/VM creation, application restart or driver/version change occurred.

Current private receipts: `.local/phase0c-demo-01/`,
`.local/phase0c-source-export-d83b1f4/`, `.local/phase0c-reproduction.json`,
`.local/phase0c-preservation.json`, and `.local/phase0c-small-gpu.json`.
Public files contain original code/charts and sanitized summaries only.

## Exact next milestone and blockers

**BLOCKED: isolated Assetto Corsa native loading, observer receipts and neutral
game-frame validation.** A same-user game-directory copy does not establish
configuration/cache isolation. The bounded CM source assessment identified
Windows Documents paths; no complete supported per-process redirect is established.
Read [RUNTIME_ISOLATION.md](RUNTIME_ISOLATION.md) before attempting host work.

1. Supply/authorize an independently provisioned licensed host or explicitly
   approved alternative. Verify separate resolved executable/content, Documents,
   AppData, Steam, CM, Pure/CSP, cache and output paths. No writable reference
   location or shared library/configuration may be used. Snapshot isolated state.
2. Establish the real supported CSP/Pure script-loading path for exactly stable
   0.2.11/build3465 and optional preview361/build3898. Preserve the owner's locked
   preview/CM stack, Pure bridge and active scriptable-filter slot.
3. Start the existing observer explicitly; obtain bounded real callbacks and
   successful owned unsubscribe. Verify PP/bypass flags, fork/package, ordering,
   timing units, main/auxiliary/eye behavior and actual buffer format/encoding.
4. Establish uniquely owned named-effect registration **and removal** before any
   render hook. Keep Pure exposure ownership and validate neutral game output.
   Calibrate and validate Gamma/LCS separately only after those facts are known.
5. Then test matched visual/performance and total memory on real legacy AMD/NVIDIA
   boards. Upscaling and FG remain separate runtime gates; no CSP 0.3.1 dependency.

Unknowns remain native loading, actual callback delivery/order, shader resource
access, buffer encoding, exposure stage and supported named-effect teardown.
SDK/source declarations, synthetic Lua execution and independent D3D11 output
must not be promoted into real CSP/Pure evidence. No new observer or Dream code
change was justified by this phase's evidence.

Failure symptoms: paths alias owner state, protected hashes drift, missing native
APIs/callbacks, unknown encoding, or registration with unknown cleanup. Stop
dependent work; leave uncertain callbacks inert and blocked. Do not retry via a
replacement bridge, GUI automation, injector or reference-install deployment.

Rollback: current standalone work releases only its own device/resources and
leaves ignored output; no game restore is needed. Future isolated work must stop
only owned subscriptions and restore its accepted snapshot, preserving receipts.
Never delete another mod's registration or restart an app with unsaved state.
Revert source with a reviewed new commit, preserving history and user changes.

## Phase 0C usage and continuation discipline

Owner-reported allowance was 16%; first live Phase 0C reading was **15% weekly
remaining**. Latest pre-closeout live reading was **13%**. These are account-wide
integer readings, not task-only billing. Final measured usage and synchronized
SHA belong in the final receipt/response. No need to consume the reserve while
the game-host gate is blocked. No new R&D/testing occurred at or below 5%.

For continuation, read the actual meter anew: finish the current bounded unit
and prepare closeout around 8%, prioritize synchronization at 7%, and do no new
engineering/research/testing at 5%. Never encode this session's starting reading
as a permanent budget. Reuse the code/evidence above rather than repeating GPU
runs or completed SDK/Dream research without a new change or evidence gap.

---

## Historical Phase 0B handoff (superseded where Phase 0C updates it)

Prepared 2026-11-01, America/New_York. This updates the Phase 0 handoff for the
next authorized continuation; no Wednesday automation has been scheduled.

## Known-good repository state

Repository: [Metalroachtwo/RestoVisuals](https://github.com/Metalroachtwo/RestoVisuals).
Working branch: `phase0/foundation`. Do not merge to main automatically.
The latest tested, pushed and remotely verified code checkpoint is
`9290fde1fc9793916f0382690562979cab50af4f`. Final documentation HEAD is recorded
by Git and the private `.local/phase0b-final-sync.json` receipt after closeout.
Use `git rev-parse HEAD` and `git ls-remote origin refs/heads/phase0/foundation`
to confirm the exact current synchronized revision.

Original foundation checkpoint: `c9177484c2c3fd460f3e32dc855af1db895728e1`.
Original 56-test foundation and prior audit evidence remain preserved in history.
Phase 0B checkpoints: `af61207` integration findings; `7fc4752` Lua observer;
`f4a9818` actual GPU execution/identity fix; `6c65105` Dream/Pure diagnostics;
`212d63d` official stable SDK/version-specific fixes; `9290fde` uncertain-registration failure latch. Each was pushed and
verified before the next substantial unit. Existing Git identity/history and
unrelated work were preserved; no forced push, reset or global Git change.

## Implemented and validated

- Original read-only Lua observer with explicit start/stop, exact version/build
  and Pure shader-space gates, bounded samples, raw timing/PP/upscaling flags,
  independent optional-field probes and owned unsubscribe cleanup. It returns
  nil from every callback, touches no PP parameters, and allocates no textures.
  Failed/unknown cleanup leaves the callback inert and blocks restart.
- Original windowless D3D11 GPU execution/readback harness. It owns a separate
  feature-level-11_0 device, point-sampled synthetic inputs, two floating-point
  formats, an original fullscreen triangle, timestamp/disjoint queries, bounded
  nonblocking waits and deterministic release of its own COM references.
- GPU execution found neutral saturation cancellation and sRGB round-trip drift
  in the original prototype. Exact neutral paths were added to both shader
  entry points and the CPU reference. Four identity cases now have zero channel
  differences in RGBA32F/RGBA16F; only then do six numerical color cases run.
  All six pass their declared precision tolerances; alpha is exact in all ten.
- Version-scoped upscaler parsing: stable boolean spatial selector is not the
  preview method enum. Unknown versions/IDs remain unknown. Stable struct field
  absence cannot suppress other readable flags.
- **93 tests pass, no skips with optional LuaJIT**; all original 56 are covered.
  A fresh 52-file source export passes the same 93 tests with the declared
  toolchain. All ten hardware cases also passed from the earlier source export;
  GPU/compiler/shader hashes match after the later observer-only fix. Neither
  validation reads private CSP/Pure source. The 25 Lua tests explicitly skip if the
  optional dependency is absent; 68 other tests execute on this Windows host.

The optional CPython 3.14 Windows x64 Lupa 2.8 wheel is hash-pinned in
`requirements-lua-tests-win-cp314.txt` and installed only under ignored local
test dependencies. LuaJIT 2.1.1774896198 executes original adapter code against
synthetic host APIs. It does not load CSP/Pure DLLs or certify a game runtime.
The core CLI remains standard-library-only.

## Environment and source evidence

Protected reference remains CSP 0.3.0-preview361/build 3898 and Content Manager
0.8.2913.40776. Seven targeted before/after hashes covering binaries, manifest,
Pure weather sources, Pure LDR bridge and PP SDK match. Dream INI and checked
resource/missing-file states also match. No full repeat of the Phase 0 audit,
active deployment, GUI automation, application/service restart, driver change
or update-policy change occurred. No running acs/acs_x86 process was observed.

Pure Gamma/LCS core and manifests previously report 3.50; exact hotfix package
remains unknown. Source minimums are Gamma 0.2.0/build 2639 and LCS
0.2.3p211/build 2974. Saved Gamma/Dream Realism selection and 1920x1080/MSAA8,
Extra FX, NIS method ID 2 are configuration observations, not running-game proof.
The prior 101-PP-filter inventory and historical ReShade status remain in
[ENVIRONMENT.md](ENVIRONMENT.md); they were not broadly rediscovered.

The official 0.2.11 archive is now obtained privately. Manifest build **3465**
and binary file/product **0.2.11.0** resources agree. Archive SHA256 is
`0729ccaebb403a7a6d1c40516990da8116cb5f56eea4c1fe0bdd29863a5a6ffb`.
Selected version-matched SDK/config files were inspected; the DLL was never
installed or executed. PP/WeatherFX SDK declares version, simulation, timing,
post-processing callback, fullscreen pass, render-target size and extra canvas
interfaces. Stable lacks the preview `isHDR` field and uses a boolean old/new
spatial-upscaler selector. FSR2/3/FG are not established on stable. This resolves
the source-inventory blocker, **not runtime certification**.

The development RX 5700 XT exposes 8,546,471,936 dedicated bytes and previously
measured maximum D3D11 feature level 12_1. The validation deliberately creates
an 11_0 device. Windows driver metadata was 32.0.21043.12001; physical legacy
boards and NVIDIA hardware remain untested. Duplicate AMD DXGI identities have
different LUIDs; explicitly choose a measured adapter and do not infer two cards.
External process budgets are not game usage or system-free VRAM.

## Rendering evidence and limits

Current color-source SHA256:
`f762d3e4e98295b257b2fd46452023857e3b8d972c753d268835061dcf6fce88`.
Pixel bytecode sizes: 1788/2180 bytes. Original Phase 0 source/hash/compile-only
results remain historical records. GPU fixture resolution is 63x31 (1953 pixels),
with padded-row readback, controlled encoding, positive HDR/small-channel stress
and sRGB transfer breakpoints. Nonidentity error thresholds are in the Phase 0B
report; half-float results are not exact CPU equivalence.

The first successful run had non-disjoint single-draw GPU timestamps of
0.00160-0.00224 ms. These include pipeline overhead on a tiny synthetic workload;
they are not an FPS gain, 1080p estimate, stable throughput benchmark or in-game
cost. Three-texture payload arithmetic was 93,744/46,872 bytes for float/half;
driver allocation, placement and total game VRAM were not measured.

No shader or observer was deployed to CSP/Pure. No callback has been observed
in the game. No image-quality, physical low-VRAM compatibility, stable game
frame-time, HDR/VR, rain/night or reflection improvement is claimed. Compile,
Lua contract execution, actual isolated GPU execution and actual game execution
remain distinct evidence classes. Native resolution/default effects stay safe.

## Dream Realism and safer integration direction

Authorized read-only investigation found the 7.3 Gamma INI but no matching Lua
or encrypted companion in loader-resolved candidate locations, and no referenced
grading LUT at the PP-filter-relative path. Pure's loader/source predicts default
script fallback; actual loading/resource resolution still needs a runtime receipt.
No installation repair, decryption, proprietary implementation copying or asset
publication occurred. Available settings configure existing engine/Pure effects;
they do not establish a Dream-specific renderer or LCS implementation.

The related Pure SDK exposes read-only PP/YEBIS-bypass queries and named SPICE
HDR/LDR effect registration functions. This is a candidate route preserving
Pure's LDR bridge. Unregister/rollback and the exact supported shader/lifecycle
contract are not yet established, so the observer only records API presence and
never registers, forces YEBIS, changes exposure or replaces the bridge.

Keep one shared engine with independent Gamma/LCS calibrations, vendor-neutral
capability gates and conservative memory ceilings. Pure retains exposure/weather
ownership. No custom injector/upscaler, FSR4/RTX requirement, proprietary dependency
redistribution or replay MCP is introduced.

## Exact next task and prerequisites

Remaining Phase 0B gate: **isolated game-host observation and identity validation**.

1. Supply an authorized Assetto Corsa host with verified isolation of user config,
   caches and mod state from the owner's working install. Stable reference source
   is available; a safe running 0.2.11 game environment is not. Do not switch the
   reference CSP, launch an unisolated copy or use GUI automation to fill this gap.
2. Establish a supported native script-loading path exposing CSP and Pure SDK
   namespaces. Import the original observer in that isolated context, start it
   explicitly, collect bounded real callback receipts and remove only its own
   subscription. Preserve the existing Pure LDR bridge/filter slot.
3. Verify version/build, actual weather fork/package, PP and YEBIS bypass state,
   callback ordering, main/auxiliary/eye flags, timing units, render format and
   input/output encoding. SDK symbols/flags do not prove temporal buffers or FG.
4. Verify a supported owned named-effect registration/removal path before any
   neutral render hook. Compare actual game identity output/images and use
   engine-owned surfaces where possible; preserve Pure exposure ownership.
5. Only after that gate introduce bounded visual changes and repeat matched
   native/effect timing, game-memory and visual tests across both modes and real
   low-memory AMD/NVIDIA hardware. Do not infer improvement from this checkpoint.

If the host/loading path is unavailable, report BLOCKED for dependent game
validation and stop that work. No DCC gateway probing, GUI fallback, application
restart, replacement replay MCP or reference-install deployment is authorized.
Independent permitted work is already preserved; further unsupported rendering
integration is not justified merely to consume the remaining account allowance.

## Resume, files and rollback

Read AGENTS, [PHASE0B_RUNTIME.md](PHASE0B_RUNTIME.md),
[CSP0211_REFERENCE.md](CSP0211_REFERENCE.md), [DREAM_REALISM_REFERENCE.md](DREAM_REALISM_REFERENCE.md),
[ARCHITECTURE.md](ARCHITECTURE.md), [COMPATIBILITY.md](COMPATIBILITY.md) and
[VALIDATION.md](VALIDATION.md). Reuse confirmed paths from the private original
machine context; do not scan unrelated game assets or repeat completed research.
The official archive, SDK, binary, Dream analysis, dependency wheel, GPU receipts,
source exports and targeted integrity snapshots remain ignored under `.local/`.
No third-party source/assets or private machine paths were committed.

Phase 0B added ten tracked artifacts: the runtime report; Lua module/guide;
hash-pinned optional test requirement; Lua tests; D3D11 harness, validation vertex
shader and tests; Dream reference report; stable SDK report. It modified original
shader/reference/compiler/CLI/audit code and relevant tests/docs. Full diffs are
available from the Phase 0 commit to current HEAD. Final closeout reports clean
tracked status and exact remote SHA; private receipts are intentionally untracked.

Run the suite with the optional dependency per the observer guide, and run GPU
validation explicitly only when required. Do not repeat hardware runs without a
new code change or unresolved concern. Nothing is installed, so no game rollback
is needed. Future owned subscription stop must not touch another mod's state;
failed cleanup remains inert/blocked with no automatic retry or restart. A future
render/apply path needs verified ownership, backups, drift checks and an exercised
restore procedure before changing known-good state. Revert source through a new
reviewed commit, preserving history/user work; never reset or force-push.

## Account usage

First actual Phase 0B weekly reading: **22% remaining**. Latest pre-closeout
reading: **17% remaining**. These are exposed account-wide integer percentages;
the difference is not exact task-only billing. The final reading and synchronized
SHA go in the closeout receipt and final response. Phase 0B bounds: finish bounded
work at 9-7%, synchronize at 7-5%, and no new research/engineering/testing at 5%.
No reset credit, purchase or GUI meter access was used. Every meaningful work
unit was pushed well before the reserve; no new major game milestone starts here.
