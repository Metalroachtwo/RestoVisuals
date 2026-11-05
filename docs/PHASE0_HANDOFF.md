# RestoVisuals Phase 0I continuation handoff

Prepared 2026-11-04 on `phase0/foundation`, starting from verified local/remote
`e82d52ded4495196b65ffe3f655ceec3bdb9cc00`. The validated implementation checkpoint
`abf47b666d70224f6de353e76a4d8cbadb0ce477` was pushed and remotely verified before
final measurement closeout. This handoff and the [Phase 0I report](PHASE0I_TEXTURE_STABILITY.md)
record the completed result; verify the current Git tip and final private remote
receipt on continuation. Main remains `814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

**CONTINUE: 256x256 RGBA16F moment mips, wrap, 8x anisotropy cap, extra variance
compensation off.** Full chains require 699,048 bytes / 2,796,200 bytes for 256/512.
512 improves close/moderate detail; at grazing-far 1080p it costs 0.424 ms versus
256's 0.278 ms for very similar error (0.000842 / 0.000856 versus finite 4x4).
256 trilinear costs 0.189 ms but has 0.002293 RMSE. These are isolated total draw
times, not enhancement deltas or game FPS. The periodic flat reference contains
residual noise work and is unsuitable as an optimized timing baseline.

Five controlled views (0/55/78 degrees, distance 2/4/8), both sizes and full
mips pass: 52 corrected 720p cases, 31 confirmation 1080p cases and 30 deterministic
change images. Aniso8 lowers average camera/UV change residual but not every
worst-pixel UV change. The 4x4/8x8 reference differs by 0.000433 RMS; even CPU16/32
spots are not fully converged. Do not claim eliminated aliasing, pixel equivalence,
in-game temporal stability or convincing asphalt. Repetition remains visible.
The original nonperiodic shader is untouched; the periodic adapter is explicitly
separate, including the groove Y-frequency change from 1.5 to 2. New packing stores
mean normal XYZ / roughness^4 and cannot replace Phase 0H's packing implicitly.

Seventeen new automated tests and 40 affected existing tests pass. All 143
pre-session tests, including the historical 124, are preserved. Twenty-five native
numerical gates and two small legacy native regressions pass. Audit verifies 152
artifact hashes and 544 timestamp/release receipts, all owned contexts released,
56 byte-exact disabled spatial cases, finite/unit/range checks and repeat sampling.
Whole-tile translation RMSE is 4.65e-7, not exact equality. All 29 protected files,
49 selected settings and the approved untracked visual target remain unchanged.
No GUI/game, installation change, restoration or native game rendering occurred.
Native execution was limited to the separate windowless D3D11 device.

The first screen is invalid: compiled SampleLevel(-1) forced the base mip despite
a useful-looking LOD diagnostic. Disassembly, a positive boolean branch selector,
compiled-instruction test and actual implicit trilinear CPU oracle resolve it.
Do not reuse `screen/` rankings; keep its rejection receipt. Strict compiler flags
remain enabled. Source rollback is a reviewed follow-up commit, never history reset.
Cleanup uses owned contexts/resources and synchronous completion; it establishes
no CSP/Pure downstream canvas retirement guarantee. Phase 0E HDR remains NO-GO.

Dependencies: existing Windows D3D11/D3DCompiler_47, explicit RX 5700 XT adapter 0,
feature level 11_0 and Python standard library. No new installed dependency.
Accepted private evidence: `.local/phase0i-20261104/screen-v2/`, `confirm/`,
`temporal/`, `audit.json`, `preservation.json`, `previous-path-regressions.json`.
Each successful run has an original GPU-image viewer; commands in the report use
fresh ignored paths. Raw metadata and analysis remain private. Preserve receipts.

Starting live allowance: 46% five-hour / 77% weekly. Approximately 15-point review:
30% / 75%, productive bounded continuation. Last pre-reset reading: 20% / 73%.
The five-hour window replenished to 99% while confirmation completed; formal
closeout continues without expanded scope. Current closeout reading: 96% / 73%.
The former 12-point cap is revoked. Read meters anew; preserve the approximately
15% five-hour closeout reserve and independent 5% weekly hard cutoff.

**Next milestone:** an original tangent-space mesh fixture with calibrated
surface scale and a better-converged grazing reference, then a supported material
input/lifecycle plan before any separately reviewed native integration. No complete
material editor, asset library, benchmark automation or installer is implemented.
Permanent freeware, locked installations and unresolved license-owner gate persist.

---

## Historical Phase 0H continuation handoff

Prepared 2026-11-04 from verified local/remote `phase0/foundation`
`1e21f6a2f3d515854bc276e91f3716dad4507392`.
Read [PHASE0H_MATERIAL_OPTIMIZATION.md](PHASE0H_MATERIAL_OPTIMIZATION.md) for the
reproducible comparison, measured quality/cost, texture lifetime and limitations.

**Recommendation: CONTINUE compact textures for this synthetic material.** At
1080p/original density, procedural cost remains about 1.057 ms and texture cost
is 0.133 ms, about 0.0122 ms above flat rather than Phase 0G's 0.936 ms increment.
The 256x256 RGBA16F map adds 512 KiB of logical input payload; full-image RGB
RMSE is 0.000368 and sampled normal p95 is 1.52 degrees. This is close, not exact
quality equivalence, and implies no in-game FPS result.

One finer-density probe increased small-map error nearly threefold, justifying
the only second size. At 720p, 512x512 reduces its RMSE from 0.00104 to 0.000351
and normal p95 from 2.18 to 0.86 degrees, with little measured draw-time change
and 2 MiB payload. Finer 1080p also passes. Grain scale improves relative to the
large stone-like field, but regular grooves remain; asphalt realism is unvalidated.
No prolonged artistic tuning or general texture authoring system was built.

The procedural HLSL is unchanged. Only the surface-data function is replaced in
private assembled copies; lighting, parameters, geometry and output format match.
The existing renderer/compiler/exporter remain shared. All normal/finite/range,
disabled byte-equality, timestamp and resource-release gates pass. Nine new tests
and 31 affected existing tests pass; every pre-existing test is preserved,
including the historical 124 and Phase 0G's additional ten. One small original
color-path native GPU regression passed. No full unrelated suite was rerun.

Private reports, original fixture binaries and 30 labeled comparison PNGs/viewers
remain under `.local/phase0h-20261104/`. No sample is published. No GUI, game,
installation or global graphics setting was touched; Phase 0E's native HDR
NO-GO remains binding. No dependency or licensing change was made.

Starting meters were **59% five-hour and 80% weekly remaining**. The session cap
is 12 points, giving a floor of 47%; closeout began at 52% / 78%, before the
planned 51% trigger. The independent weekly hard cutoff remains 5%. Final usage,
preservation and matching local/remote SHA go in private receipts and the response.

Next: validate mip/oblique-view fidelity and seamless material sampling, then
broader physical hardware. Source rollback uses a reviewed follow-up commit;
preserve original references and receipts. No native deployment is authorized.

Final preservation passes for all 29 protected files and 49 selected settings
files; the approved untracked PNG is unchanged. All 30 image hashes, three fixture
hashes and 170 timing/resource receipts verify. No restoration was necessary.

---

## Historical Phase 0G continuation handoff

Prepared 2026-11-04 from verified local/remote `phase0/foundation`
`ca9204bc9322d5d2492d0ff39328e165050c0da2`.
Read [PHASE0G_MATERIAL_SHADER.md](PHASE0G_MATERIAL_SHADER.md) for the original
shader, equations, reproducible commands, hashes, measured costs and limitations.

**Offline result:** flat, normal-detail and normal-plus-roughness variants pass
on an explicitly verified RX 5700 XT at 720p and 1080p, under two light directions.
Geometry stays one flat fullscreen triangle; procedural inputs require no source
texture. The existing renderer/compiler/exporter are extended minimally. No
game, Content Manager, GUI application, rendering hook or Pure effect was used.

The enhanced isolated draw costs about 0.470 ms at 720p and 1.057 ms at 1080p,
approximately 0.417 / 0.936 ms above the flat variant. These are GPU batch-derived
durations, not gameplay FPS or pixel-shader-only timings. Each case retains three
five-draw batches, two warmups per batch, raw timestamps and disjoint status.
CPU discrepancy is below 6.3e-6, normal length error below 6.4e-8, and disable
readbacks are byte-exact against the synthetic baseline. All owned resources
are released. Texture payload is identical between baseline and enhancement;
sampled process-local memory is documented separately from physical allocation.

**Recommendation: REVISE before production.** Apparent relief responds to light;
roughness is subtle and the surface reads as soft grooved stone. The next bounded
milestone is a compact original normal/roughness fixture versus procedural ALU,
with material-scale refinement and the same numerical/cost gates. No older GPU
or CSP-material compatibility is inferred. Phase 0E's HDR/lifetime NO-GO remains
binding and was not reinvestigated.

Ten new tests and all 24 affected existing tests pass. One small original-color
GPU identity regression passed; the full unrelated test/hardware matrix was not
repeated. All original 124 tests and original color/fullscreen HLSL are preserved.
Raw reports, 12 labeled PNGs and viewers remain ignored under
`.local/phase0g-20261104/`; no visual sample is published in Git.

Starting meters were **74% five-hour and 82% weekly remaining**. Closeout began
at 65% five-hour / 80% weekly, reserving the 15-point session floor of 59% and
independent 5% weekly cutoff. Final usage, preservation and verified local/remote
SHA go in private receipts and the final response; read meters anew next time.
No dependency or license choice changed; RestoVisuals remains freeware.

Final preservation checks pass for all 29 protected files and 49 selected settings
files; the untracked visual target is unchanged. All 12 PNG hashes and timestamp
calculations are verified, and both resolutions used identical shader bytecode.
No installation change or restoration was necessary.

---

## Historical Phase 0F continuation handoff

Prepared 2026-11-04, America/New_York, from verified local/remote
`phase0/foundation` checkpoint `00a7d5df23d5242c9a6acfcad13a4c06bf2788af`.
Read [PHASE0F_NATIVE_BASELINE.md](PHASE0F_NATIVE_BASELINE.md) for the first native
visual/configuration receipt, precise settings and remaining benchmark limitations.

**Confirmed configuration:** 1920x1080 output; render scale 1; `FSR/ACTIVE=1`,
`OLD_IMPLEMENTATION=2` selects NVIDIA Image Scaling. No NIS-quality user override
exists, so installed `QUALITY_NIS=0.7692` applies. The stored FSR-only
`QUALITY2=0.87` is inactive for this selected method. Multiplication/rounding gives
1477x831, consistent with Phase 0D's callback size, without proving the runtime
pipeline. No observer or shader was installed or registered.

The existing Lexus `mm_lexus_rca` / `jd_drift_mansion/open` replay ran through CM.
Raw 1920x1080 captures and replay SHA are recorded; a paused witness displays
3:49 / 4:27, Camera Cockpit, car 0. The inherited view does not show the Lexus.
Exact frame/transform and live Pure weather were not established; stored replay
weather/time and camera receipts are preserved. No trustworthy frame-time capture
was available in the bounded checks, so no FPS/performance result is claimed.
No reliable CM upscaler-settings screenshot was obtained; source configuration
and the installed schema supply the method/quality evidence.

Cleanup began at 16:30:44 Eastern; the game closed normally and owned CM exited
at 16:32:25. No GUI work remains. After both exits, only the three known session
files were restored from fresh verified backups: camera settings, race settings
and CM state. Their session-written versions are preserved. All 29 protected
files and 49 settings files match preflight. Graphics/filter settings and the
untracked approved PNG are unchanged. No unrelated work or mod was modified.

Starting allowance: **86% five-hour, 84% weekly remaining**. This assignment's
15-point limit gives a five-hour floor of 71%; the independent 5% weekly cutoff
remains. Live ending meters and final verified local/remote SHA go in private
`.local/phase0f-20261104/final-sync.json` and the final response. Main stays unchanged.
The 124-test baseline is preserved; no unchanged runtime suite was rerun. All six
targeted validation groups passed, including 17 local links and the replay/three
native capture hashes. Pre-synchronization meters were 76% five-hour and 82%
weekly remaining; closeout proceeds within the 15-point cap.

**Next benchmark milestone:** establish a visible-car camera, exact replay
segment and trustworthy timing source, then a separately authorized NIS/native
comparison with fixed conditions and complete recovery. **Phase 0E's neutral-pass
NO-GO remains binding**; this task did not revisit its unresolved HDR contract.
No dependency or license decision changed; RestoVisuals remains freeware.

---

## Historical Phase 0E continuation handoff

Prepared 2026-11-04, America/New_York. Resumed from locally/remotely verified
`phase0/foundation` HEAD `3c0e40aefd958c3de923534871ce20461e050be5`.
**Current result: NO-GO for the neutral rendering pass.** The bounded contract
review is complete; no shader was installed or executed inside Assetto Corsa.

Read [PHASE0E_HDR_CONTRACT.md](PHASE0E_HDR_CONTRACT.md) for the evidence matrix,
release-specific SDK hashes/locations, rejected assumptions, alternative stage
assessment and conditional implementation plan. Installed preview361/build3898,
Content Manager 0.8.2913.40776 and Pure Gamma/LCS 3.50 were verified read-only.
No installation, version, update-policy or dependency changes were made.

## Phase 0E findings and remaining gates

- The callback substitutes HDR input **before YEBIS**. The already-bound LDR
  destination does not make this a final-image hook. The existing observer works
  and was not rebuilt or rerun.
- Actual dynamic-source format/channel precision, transfer, primaries, alpha,
  pre-exposure/scaling and source lifetime remain unknown. Owned-canvas format
  selection, readback, size/readiness and exposure overrides do not discover them.
- Callable cancellation is documented and the prior observer's stop was proved.
  Safe retirement of previously returned canvases after cancellation, during
  resize and at shutdown is still unestablished.
- Registering `ac.onResolutionChange` disables automatic reload in relevant
  hosts; its coverage of internal dynamic-resolution changes is unestablished.
  `ac.onRelease` is best effort and cannot be the only recovery guarantee.
- The documented PP redraw alternative does not provide a verified independently
  owned stage alongside Pure's occupied LDR bridge. It is rejected for this
  installation. The existing SPICE removal gap remains; no private workaround.

The single next milestone is an authoritative contract for **source representation
and returned-surface retirement on the supported versions/modes**. Seek a concrete
SDK/maintainer answer, not another observer run. No external message was sent.
Stop dependent rendering while those facts remain missing. The current agent's
critical safety assessment is NO-GO, not an independent deployment review.

If evidence resolves the gaps, prepare a fresh original design, critical review,
owned-path installation diff and bound transaction/recovery rehearsal; then use
the existing D3D11 identity harness before any native test. Old packages remain
run-bound. Native matched-image, timing, resize, auxiliary/VR, LCS/stable and other
GPU coverage are unvalidated and must remain separate gates.

## Phase 0E preservation and credit checkpoint

Starting live meters: **100% five-hour, 86% weekly remaining**. Research ended at
**91% five-hour, 85% weekly**; closeout began at that reading, well before the
75% planned closeout trigger and 70% absolute session stop. Final readings and
local/remote documentation SHA go in ignored `.local/phase0e-20261104/` receipts
and the final response; do not reuse these as a future starting budget.

The 124-test Phase 0D baseline and original 104 tests remain intact. Documentation
is the only public change; successful unchanged runtime/GPU tests were not
repeated. All six Phase 0E validation groups passed: 22 local links/anchors,
three release-specific SDK files and 27 declaration locations were checked,
alongside source/test preservation, private evidence and publication boundaries.
All 29 protected files and 49 selected settings files match preflight hashes.
The approved PNG is unchanged/untracked and the prior owned probe directory is
absent. Latest pre-synchronization meters: **89% five-hour, 84% weekly** remaining.

The last native-validated configuration remains the Phase 0D Gamma observer:
Pure PP enabled, YEBIS not bypassed, raw HDR-output flag false, 1477x831 callback
surface and 1920x1080 saved image. The raw upscaler-section flag was true; actual
algorithm/frame generation remains unknown. No Phase 0E runtime claim is added.

No GUI/game process or rendering experiment was started. There are no new live
files or settings to roll back. Exact settings/backups from the verified Phase 0D
state remain in the existing ignored receipts; no private configuration is
published. Source rollback, if needed, uses a reviewed follow-up commit, never
history reset or force-push. The branch stays `phase0/foundation`; main is not
merged. Freeware remains mandatory and repository licensing remains unresolved.

---

## Historical Phase 0D continuation handoff

Prepared 2026-11-04, America/New_York. Current work resumed from verified Phase 0C
HEAD `5fa7c42491ecb0cd049232fc70ae35d08ca21dbb`. The owner-supplied approved
reference PNG is untracked and preserved. The original 104 tests remain unchanged;
124 now pass with the declared optional LuaJIT dependency.

**Current result:** the native preview361/Gamma observer passed with 106 main
callbacks and a quiet owned-stop witness. **Neutral rendering remains BLOCKED**
on the dynamic HDR input contract and returned-canvas lifetime. No experimental
component remains installed; all owned game/CM sessions exited normally.
Latest tested/pushed code is `0cc3670968e6f6671d7934c71bd241efd2304a64`.
Final documentation HEAD and measured allowance are recorded by Git and ignored
`.local/phase0d-final-sync.json`; verify the remote rather than assuming a hash.

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

Each native attempt had a separate bound review, manifest and fault rehearsal;
all are completed and recovered. None authorizes an automatic reinstall/retry.
The original v2 attempt failed before registration, v3 established API types,
and v4 verified actual observer delivery and owned stop. No rendering review
has passed and no shader/Pure named effect was installed.

Private continuation/recovery artifacts live under `.local/phase0d-20261104/`:
`preflight.json` (29 protected files and 49 verified settings backups),
`before-game-settings.json`, `package-v2/`, `rollback-rehearsal-v2.json`,
`safety-review-v2.json` and owned CM PID/window observations. The exact-file helper
was `.local/phase0d_transaction_v2.py`; its first intent journal precedes any
game write. It preserves ambiguous output/edited files and disables only verified
owned executable source. v2/v3/v4 packages, journals and receipts remain private
for audit; retain them rather than deleting or repurposing a reviewed run.

The first reviewed observer entry loaded inside a CM-launched replay, but failed
`required_csp_api_missing` before registration. Its zero callbacks and retained
blocked pre-stop state are in `.local/phase0d-20261104/deployment-v2-output.json`.
The session and owned CM exited normally; all owned files/directories were
removed. All 29 protected hashes and 49 selected settings match their original
backups after restoring only the three session-changed files. See
`post-runtime-preservation.json` for the complete targeted rollback result.

A separate API-type-only diagnostic was staged under `package-v3/`, bound to run
`27a323d258214f688f152443151162da` and its own review/rehearsal. It registers no
callback, timer or release handler and leaves the original observer's strict gate
unchanged. Only that declaration check was reviewed for that native attempt;
it did not test callback removal. `phase0d_transaction_v3.py` and its v3 journal
remain preserved. Its native result
completed and found the build getter is `cdata` while the other three APIs are
Lua functions. Its zero-subscription session was also fully recovered with all
29/49 hashes restored; see `native-api-types-receipt.json` and
`post-api-diagnostic-preservation.json`.

The pinned SDK/Pure initialization and LuaJIT documented call semantics justify
a narrow owned-proxy closure for this single public build getter. The original
observer is unchanged and still validates protected query results and exact
version/build before registration. Noncallable data, invalid results and wrong
build are regression-tested. The separately reviewed observer v4 package was
`package-v4/`, run `2474c30f7a9b4b0abfd043c91f7885e9`, helper
`phase0d_transaction_v4.py`, separate v4 journal and rehearsal. Its native result
passed and is in `native-observer-v4-receipt.json`: actual version/build3898,
Gamma shader space, 106 main/zero auxiliary callbacks, eight bounded samples,
1477x831 callback surface, clean preserved pre-stop state and zero callbacks
after owned unsubscribe. Pure PP was enabled, YEBIS not bypassed; algorithm/FG,
input format/encoding and exact Pure fork/hotfix remain unknown. Raw timing units
are unverified and the startup samples are not a frame-time capture.

`post-observer-v4-preservation.json` verifies complete owned-file/directory
recovery, normal game/CM exit, 29 unchanged protected hashes and all 49 selected
settings matching original backups. Only camera settings, race settings and CM
state needed restoration after process exit. Screenshot/log evidence stays
private. A fresh 71-file source export passes all 124 tests; without LuaJIT,
83 execute and 41 skip. All original 104 tests remain unchanged. Rendering is
not authorized by the v4 review. Never infer a neutral
pass, game FPS, LCS support, encoding or effect-removal proof from the preparer,
observer source or 51 synthetic filesystem failure-point recoveries.

## Exact next milestone and stop conditions

Obtain version-specific authoritative metadata or a supported query for
`dynamic::pp::hdr`: actual format, transfer/primaries and pre-exposure convention.
Also establish downstream reference lifetime of a returned `ui.ExtraCanvas`,
unsubscribe-before-dispose and resize replacement. The documented callback
substitutes HDR input before YEBIS; it is not an independent final-image stage.
Size/readiness queries do not supply those missing facts. Pure named-effect
addition still has no established supported removal route. The final critical
review returned NO-GO for rendering on these concrete gaps.

Only after those contracts are supplied, prepare a fresh owned neutral-pass
design and critical review, numerical/native identity evidence, matched images
and frame captures. Reuse the proved observer and its actual dimensions; preserve
Pure's bridge/slot and weather/exposure ownership. Validate Gamma/LCS, stable CSP,
auxiliary/VR/resize and physical legacy/NVIDIA hardware separately. Do not repeat
completed Dream searches, SDK inventory or hardware runs to fill an unrelated gap.

If the input/lifetime contract remains unavailable, stop dependent rendering.
Do not replace the bridge, use internal list removal, invent texture metadata,
inject code or switch CSP/CM versions. Future GUI work needs the current task's
authorization and a fresh Eastern-time check; no persistent GUI enablement or
automation has been installed. Source rollback uses a new reviewed commit,
never reset/force-push. Historical exact-file helpers are for their bound runs,
not a general installer or an automatic instruction to deploy again.

The permanent freeware requirement remains intact. Repository license selection
is unresolved, requires owner approval, and no paid dependency was added.
Phase 0D first live weekly reading was 100%; pre-closeout reading was 87%.
Final reading goes in the receipt/response. Read the meter anew on continuation;
no new engineering/research/testing is permitted at 5% remaining.

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
