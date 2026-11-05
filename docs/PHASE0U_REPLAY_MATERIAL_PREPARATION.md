# Phase 0U: offline replay and concrete-material preparation

2026-11-05. Verified starting local/remote `phase0/foundation`:
`daa24375b8c00938651882f47f00417d1ccdbd7a`.

**Offline preparation is complete. CONDITIONAL GO for a future replay/baseline/
read-only material-inspection session, only after fresh owner authorization.
NO-GO for normal-map deployment or claims of reproducible playback.**
The owner explicitly ended the previous computer-use exception. No GUI provider,
desktop capture, application control, game, replay, DCC or live scene API was
initialized in this phase. Installed files were read only; no restoration was
performed. Existing sessions and owner preferences were left untouched.

Read the [disabled specification](../examples/phase0u-replay-material/experiment-spec.json),
[Phase 0T report](PHASE0T_BASELINE_VALIDATION.md),
[Phase 0R inventory](PHASE0R_REAL_MOD_VALIDATION.md) and
[Phase 0J contract limits](PHASE0J_MATERIAL_INTEGRATION.md).
Raw observations remain ignored under `.local/phase0u-20261105/`; original images,
replay and T receipts remain under `.local/phase0t-20261105/attempt2/evidence/`.
No third-party asset, raw configuration, account information or screenshot is
published. Evidence labels below distinguish source declarations from native facts.

## Preserved native baseline and recovery coverage

**Tested in Phase 0T:** the separately approved second launch rendered the original
`mm_lexus_rca` / `jd_drift_mansion/open` scene, Burnt Orange Metallic, existing
VDC 2024 track skin. Native Exit/Leave completed with code 0. Five retained
1920×1080 image hashes still match; the rear exterior image was inspected from
disk in this phase, without capturing the desktop. It does not identify which
visible mesh uses `concrete`.

The current scoped read confirms **29/29 protected files** and **48/49 selected
settings** against the T preflight. The exception is the live CM `Values.data`,
retained under the owner's keep-session-open choice. Its present bytes match the
T closeout copy. This is observation of disk contents, not inspection of CM's
current unsaved selection or a new 49/49 restoration claim.

| State file | What is now verifiable | Remaining ownership/recovery limit |
|---|---|---|
| `extension/state/lua/app/WebBrowser.ini` | Readable current bytes, SHA-256, size and modification metadata recorded privately; matches T closeout observation | No fresh pre-T2 baseline; older R contents cannot establish what T2 changed |
| `extension/state/odometers.ini` | Same present-observation coverage; matches T closeout observation | Same missing historical baseline; do not restore old mileage/state |
| CM `Values.data` | Present snapshot/hash/metadata and T closeout copy match | Live owner session can rewrite disk or hold unsaved memory state; do not overwrite or close it |

Two separated file observations found **no hash or modification-time change** in
any of these three files, with stable metadata around each read. Present hashes,
sizes, timestamps and the final comparison are retained privately. Stability
at sampled instants does not establish exclusive ownership, a stopped writer,
an atomic backup or future quiescence. A changing hash/time requires archiving
both versions and identifying owner activity before any proposed restoration.
No historical pretest hash is manufactured from these new observations.

Full user-state recovery remains unverified: T2's two historical gaps, live CM
state, previously documented unreadable auxiliary files, and any state outside
the reviewed scope. The R count of 261 readable configuration files and 194
auxiliary exclusions is historical, not a newly complete U inventory.

For a future session, freshly cover both named state files, the live CM store,
selected settings, camera/race inputs, prior logs/output and replay directory
entries **before launch**. Use the existing inventories to scope reads, capture
new files within approved runtime folders, record exclusions and never weaken
access controls. Keep the explicit CM exception. Never copy an older R/T backup
over newer owner state or claim complete rollback from protected-file hashes.

## Replay identity, metadata and playback route

**Observed locally:** the preserved private replay and its original autosave both
have **5,559,241 bytes** and SHA-256
`d447417fef436d8993c22c18a030560654215aa43bb7a9a35f98b0e8ae5c2d8f`.
The original remains in place; no rename, move or registration was performed.
The private T copy is the durable reference if the temporary autosave is later
retired by the game. Recheck the hash before any future load.

| Item | Established scope |
|---|---|
| Associated car/track/layout | T2 generated race input, exit evidence and autosave filename associate it with `mm_lexus_rca`, `jd_drift_mansion`, `open` |
| Embedded replay identity | **Unknown**; association is not an embedded metadata parse |
| Duration / recording interval / frame count | **Unknown**; neither file size nor session wall-clock duration is used as replay duration |
| Reference timestamp | **Proposed 00:10.000 only**; first verify duration, stationary interval and usable surface view; no matching frame has been established |
| Replay playback, timeline and camera persistence | **Untested**; do not substitute a fresh Practice session or different replay |

**Documented upstream, not installed-version certification:** CM's published
[file handler](https://github.com/gro-ove/actools/blob/e5e5c94b8dee7511def0b670bfd5dbb233831c11/AcManager/Tools/ArgumentsHandler.cs#L243-L248)
routes an `.acreplay` file to `StartReplayAsync`. Opening the file through that
handler is a launch action, not passive metadata inspection. It was not invoked.
Future playback must use the approved CM session and its supported replay controls;
observe their actual labels before proceeding, with no direct game executable.

The public [ReplayObject source](https://github.com/gro-ove/actools/blob/master/AcManager.Tools/Objects/ReplayObject.cs)
shows metadata loading and duration derived from frame count and recording
interval. That floating source is not version-matched to the locked installed
CM binary. This bounded review did not establish a documented installed non-GUI
metadata command, and no CM assembly, replay parser or replacement reader was run.
Duration and embedded identity therefore remain deferred to supported native
inspection. No unsupported binary/header inference or extra parsing framework.

**Comparison uncertainty:** T's configured Pure/13:06/13.5°C/8.1 km/h SSW differs
from the actual initial panel: clear/no clouds, about 13:07, air 19°C, road 30°C,
wind 0 km/h, grip 100%. Record both. Pure Gamma 3.50 remains configured; T logs
witness Dream Realism 7.3 Gamma PP loading. Replay restoration of weather, sun,
wetness, exposure adaptation, animations and CSP effects is unverified.

Use one recorded warm-up/seek history for every capture. Confirm the actual pause
control and whether weather, exposure or vegetation keeps advancing while paused.
Record timeline/frame index, target car, camera type/index, FOV, aspect/output,
HUD state, sun/clouds/wetness/wind, PP/Pure/exposure controls and settling delay.
F1 once produced T's exterior view from a Practice cockpit; it is **not** a proven
replay camera restore. Use supported pose storage/coordinates if exposed. If only
visual landmarks are available, state that limitation rather than invent a pose.

Before enhancement, obtain unchanged **baseline A/A** captures by repeating the
same seek/camera/history. Define a surface ROI only after material identification.
Measure repeatability before choosing any tolerance: encoded-image absolute
differences/RMSE are image-space measures, not radiance or HDR equivalence. Keep
full-frame witnesses to detect exposure changes. If A/A or camera recovery fails,
material inspection may still be useful, but an enhanced/restored visual comparison
remains NO-GO. No current T image is certified as that future reference frame.

## Concrete material: bounded static findings

**Observed locally, not live KN5 identity:** the two retained track authoring
sidecars both declare `MATERIAL_6`, name `concrete`, shader
`ksPerPixelNM_UVMult`, alpha blend/test 0, `txDiffuse=roughtconcrete.dds` and
`txNormal=concrete_nrm.dds`. Their current hashes match the R inventory.
Two records from source variants are not two runtime materials or a mesh count.

They agree on approximate ambient/diffuse 0.2, specular 0.6, exponent 100,
`normalMult=2` and `diffuseMult=0`. Preserve all typed values. The shipped SDK HTML
and shader metadata are unchanged from the reviewed SDK inventory; they list
`txDiffuse`, `txNormal`, texture-multiplier variables and non-alpha-tested metadata.
They do **not** document the normal decoding formula, alpha use, tangent signs,
complete UV transform or effective CSP shader substitutions. No shader binary
was decompiled, executed or copied to the public repository.

| Authoring texture copies | Standard DDS header observation | Limit |
|---|---|---|
| `concrete_nrm.dds` | Both copies identical; 512×512, 10 mips, traditional FourCC `DXT5`, 349,680 bytes | DXT5/BC3 container does not prove DXT5nm channel swizzling or native slot interpretation |
| `roughtconcrete.dds` | Both copies identical; 512×512, 10 mips, traditional FourCC `DXT1`, 174,904 bytes | No color-space inference or embedded-runtime identity proof |

Headers and hashes were read; no proprietary texture pixel payload is redistributed.
These extracted authoring resources do not prove the textures embedded in the
currently loaded KN5 or skin overrides. Phase 0P's owned `ksPerPixelNM` X-direction
result does not certify `ksPerPixelNM_UVMult`, Y orientation, mirrored UVs or scale.

Eleven specific existing configuration files were inspected, retaining repeated
`...` sections separately rather than merging them as ordinary INI duplicates:

- Track root config: 11 material-adjustment blocks; no shader-replacement block.
  The adjustment selectors target lights/windows/pool objects, not literal
  `concrete`. Their actual mesh overlap remains unknown.
- Selected VDC skin config: **three distinct** material-adjustment blocks; no
  shader-replacement block. Repeated placeholder section names are not one block.
- Nine present common-file candidates from the prior include graph and the
  selected skin's explicit include references were read. Library templates are
  not proof that a replacement is instantiated on this material.
- Five skin references — `buildings.ini`, `txemissives.ini`, `street_lights.ini`,
  `traffic_lights.ini`, `rain.ini` — were not found in the checked skin-local,
  central-track or central-car candidate locations. **Effective resolver fallback
  and precedence remain unknown**; this is not proof that CSP cannot resolve them.
- The six previously reviewed central/`loaded` car/track/layout candidate config
  paths remain absent. No config download, policy change or replacement was made.

Root RainFX rough-material names include `roughtconcrete`, which differs from
the candidate material name `concrete`. Similarity to its diffuse filename does
not prove a match. [Maintainer RainFX documentation](https://cup.acstuff.club/docs/csp/tracks/rainfx)
describes wetness-specific behavior and read-only name inspection with Objects
Inspector/Alt-click. Actual selected-skin overrides and wetness response remain
native questions. Do not infer dry behavior from a missing exact literal selector.

## Next native session: read-only checklist after new authorization

1. Obtain fresh task-specific computer-use approval, Eastern end time and cleanup
   checkpoint. Check actual day/time. Without approval, stop before GUI initialization.
2. Confirm approved application/game state without disturbing the owner CM,
   editor or unsaved work. No Steam restart, repair, software/update change or
   automatic retry is implied. Stop on launch failure and preserve the exact error.
3. Establish fresh scoped recovery copies/hashes, including the two runtime-state
   files and live CM exception above. Record replay-directory entries and all
   exact intended read/write paths. If required fresh coverage is unavailable,
   stop; archive-only observations do not authorize restoration.
4. Use the owner-approved existing CM session. Preserve Quick Drive selections.
   Verify the private replay hash and supported route before opening it; that
   opening can itself launch playback. Launch Assetto Corsa exclusively through CM.
5. Load this exact saved replay. Verify displayed car/track/layout, duration,
   recording/frame information and errors. Reject substitutions or metadata mismatch.
6. Test proposed 00:10.000 only if present and suitable. Record the actual frame,
   pause behavior, target car and repeatable camera/pose/FOV. If unsuitable, record
   one justified alternative timestamp; no prolonged camera/tuning loop.
7. Capture the unchanged baseline and A/A witness using recorded environmental
   state and warm-up history. Keep images/logs private. Preserve existing Pure,
   Dream Realism, CSP, resolution/upscaling and all material values.
8. Open only supported read-only Objects Inspector controls. Alt-click a visible
   concrete candidate; record exact originating KN5/model, mesh, material identity,
   shader, opacity/depth flags, typed properties and all texture slots/resources.
   Do not drag coefficients, edit values, reload configs or invoke setters.
9. Establish total matching material/mesh counts across active Open models and
   sharing outside the chosen surface; record resource origin, dimensions/format,
   UV density, tangent basis/handedness and mirrored UV evidence where supported.
   Record unknowns if the inspector cannot expose them. A screenshot of a slot
   name alone does not establish normal sampling or orientation.
10. Record effective root/skin/shared config provenance and unresolved includes
    without editing them. Exit normally; archive generated state, restore only
    fresh-backed proven owned changes under the reviewed policy, verify protected
    hashes and keep ambiguous/foreign changes. Preserve CM's working session.
11. Report replay/camera/A/A/material gates independently. Stop this inspection
    session; only then assess a separately authorized normal-only experiment.

The proposed first target requires **one exact selected mesh and one unique
material**, with no sharing outside that selection. Those are acceptance bounds,
not observed counts. If `concrete` is shared or broad, stop and revise the scope;
do not silently broaden a selector or clone materials. The maintainer's
[replacement reference](https://github.com/ac-custom-shaders-patch/acc-extension-config/wiki/General-%E2%80%93-Shader-replacements)
notes that mesh-targeted changes can create separate materials/draw calls.
Inspection must therefore precede any choice of selector or isolation method.

## Disabled normal-only proposal, installation and rollback

The JSON specification contains no active CSP section and no executable launch or
installer. **Actual installation diff is empty.** It proposes conventional original
normal data only; never feed the Phase 0I signed moment/roughness^4 map to this slot.
Lighting would remain the built-in shader, not RestoVisuals' custom HLSL/BRDF.

The existing candidate representation is 256×256, nine mips, uncompressed traditional
RGBA8 DDS, little-endian masks R/G/B/A `ff/ff00/ff0000/ff000000`, alpha 255,
intended non-color UNORM. This is the previously validated offline/ksEditor
representation, **not this live shader variant's certified format**. No new
conversion, compression matrix, blend, texture generation or artistic tuning was
performed. Native RGB/RG/alpha interpretation, both XY signs, V orientation,
normal normalization and actual UV/filtering behavior must pass before detail.
Do not change `normalMult`, gloss/specular or albedo to manufacture a result.

After a separate safety/authorization GO, proposed cold-load stages are original,
flat, signed X/Y diagnostics, original RestoVisuals detail, then restored original.
Diagnostics deliberately replace the normal temporarily; they do not establish
an enhancement. Authored originals remain immutable and privately preserved.
Production detail must retain authored large-scale information through a separately
reviewed shader-compatible method; generic replacement noise is not sufficient.
No composition method or redistribution right is inferred from technical access.

The complete **logical** future manifest is: one uniquely owned exact-selector
normal-assignment config, one reviewed normal DDS payload per stage, and any
registration/host-config diff needed to make that config reachable. Installed
paths/hashes and registration are deliberately unset in the draft because native
identity, precedence and supported isolation are unresolved. Thus this is **not
an install-ready manifest or transaction**. Do not choose a central/local override,
append an include to a third-party file or reuse old run-bound scripts by guess.
Future review must enumerate every exact path/hash, collision, original backup,
registration byte, file owner and recovery case before activation.

Workspace recovery must rehearse completion, failure, foreign-existing-file refusal
and interruption/resume for that fresh exact manifest. End the owned game normally
before disk recovery; remove only proven owned additions, restore only reviewed
fresh-backed files with conflict guards, and preserve unrelated/ambiguous state.
The replacement reference explicitly warns that deleting a static replacement
section does not restore live values. A cold original reload must verify shader,
all properties/resources/counts, protected hashes and matched restored imagery.
CM's live store exception and sampled runtime-state ownership still apply.

## Validation, final state and decision

**31 targeted existing tests passed, zero failures:** five DDS compatibility tests
and 26 material asset/recovery tests. They cover container/mask/payload invariants,
original normal preparation and synthetic recovery, not replay loading or native
resource removal. All 201 existing test definitions (including the original 124),
original shaders/assets and the approved untracked visual reference are preserved.
No full-suite rerun,
GPU render, image-equivalence result, native material sampling or FPS gain is claimed.

Eight closeout validation groups passed, covering private file observations,
source/hash preservation, links/privacy and the disabled-specification gates.
No installed
change needs rollback. The broad car/track/SDK inventories remain the previously
verified T checkpoint evidence; this phase rechecked only the scoped files above.

Starting live allowance: **70% five-hour / 29% weekly**, with two reset credits
reserved and no reset action. Work remained a bounded offline preparation unit;
final meters and local/remote SHA are retained in the private synchronization receipt.
Freeware, locked versions, owner-undecided licensing, unchanged main and Phase 0E
HDR NO-GO remain binding.

**Next: request fresh authorization for the replay/baseline/read-only inspection
checklist only.** Replay duration/frame/camera/A/A, effective concrete shader/resource
decode/UV/basis/sharing and effective skin/include precedence are the exact unresolved
native gates. Normal-only deployment remains NO-GO until those pass and a complete
fresh transaction receives its separate safety/owner approval.
