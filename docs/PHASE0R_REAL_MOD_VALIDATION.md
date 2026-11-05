# Phase 0R: real-mod baseline blocked at Steam initialization; recovery verified

2026-11-05. Starting local/remote `phase0/foundation`:
`f58b95ca72791f0174a36115b01db616058f9bd3`.

**One unmodified baseline attempt failed at Steam API initialization before scene
loading.** The game process was started through CM; no baseline scene, live
material inspection or enhancement was obtained. The owner resolved the prior
CM cleanup gate with "Allow CM cleanup restart if needed". The reviewed attempt
then ran from checkpoint `bb0033bea42c093043474a7232da128e275ffa89`.
Recovery is verified, including the original unsaved CM selection. CM is left
closed to retain exact preflight preference bytes; the owner editor is untouched.

Read the [sanitized observations](../examples/phase0r-real-mod-validation/observations.json)
and [ownership manifest](../examples/phase0r-real-mod-validation/ownership-manifest.json).

The owner authorizes this selected real-mod environment, superseding the earlier
original-track prerequisite. Phase 0E HDR NO-GO remains unchanged. An enhancement
is **NO-GO**, first pending a normally loading baseline and then the exact live
material, resource interpretation, sharing/count, configuration precedence and
complete rehearsed transaction gates. The primary runtime objective remains unmet.

## Target identification and immutable baseline

CM's existing Quick Drive page displays the requested vehicle, track and paint.
Those labels match installed UI metadata; the existing CM-generated `race.ini`
independently records the same car/track/layout and case-insensitive skin ID.
No guessed directory or new selection was applied.

| Target | Identified installation-relative identity |
|---|---|
| MM - Lexus Rocket Bunny RC-A | `content/cars/mm_lexus_rca`, UI version `v2.0` |
| Burnt Orange Metallic | `skins/Burnt_Orange Metallic`; existing race ID `burnt_orange metallic` |
| JD Drift Mansion - Open | `content/tracks/jd_drift_mansion`, layout `open`, UI version `1.0` |
| Existing track skin | CM displays VDC 2024; installed folder `skins/cm_skins/vdc2024` |

Fresh SHA-256 inventories cover **1,265 car files / 1,274,975,377 bytes** and
**386 track files / 1,314,645,660 bytes**. These include existing backups,
unpacked authoring sidecars, layouts and skins; they are not runtime resource or
material counts. Original KN5 files remain immutable. The complete private
manifest records every scoped file and existing path; no mod asset is published.

| Original file | Bytes | SHA-256 |
|---|---:|---|
| Car `mm_lexus_rca.kn5` | 86,636,062 | `d1084750eff45996f559df48c99c2dc7beaa591c72c7ea7e4006920a075f9b78` |
| Car `extension/ext_config.ini` | 11,433 | `af05c31cb695e35514e0e0349ef45e498975349098665f863eaa9ffef511a008` |
| Paint `ext_config.ini` | 2,074 | `fc1490b130bfc01298e27c2e58f85157f0f708ea47f42b62d38e6fd298cd3d61` |
| Track `models_open.ini` | 464 | `3eec1fbf80845d0b95c2d7187b2bf2fe0b8c93ff9310c8eda8cf9a3b4a7d5d38` |
| Track `jd_drift_mansion.kn5` | 157,244,712 | `f016ab05c097628a15e59cb38903b503a77133bbf76172e37f8e6db279e50a55` |
| Track `extension/ext_config.ini` | 12,019 | `0b2a4abaf84e70f733b9f4cd3d56b0acd840f2d6e283e1b88085c4ce00c9b744` |

The car's LOD declaration references the present `mm_lexus_rca.kn5` from 0 to
9999; its declared `MMRaceDriver.kn5` dependency is present and hashed privately.
The Open model list references six present KN5 files and missing
`dm_layout_pits.kn5`. Successful Phase 0D logs already report this missing/empty
model and continue through normal initialization/shutdown. This is a **known
pre-existing warning**, not a clean-dependency certification or a repair target.
If the unmodified game fails to load normally, stop and preserve evidence.

## Configured baseline, not a new runtime witness

The existing CM page matches 13:06, Pure, 13.5°C, Optimum, 8.1 km/h SSW, Practice
from Pits, Pro assists, tyre blankets enabled, extended physics enabled, zero
ballast and zero restrictor. Real/ideal conditions are unchecked. These existing
choices were captured without changing them. VDC 2024 is preserved even though
its own metadata labels a VDC layout; no track-skin correction is attempted.

| Component/option | Read-only evidence |
|---|---|
| CSP | Manifest `0.3.0-preview361`, build `3898`; protected hash unchanged |
| CM | Locked `0.8.2913.40776`; protected executable hash unchanged |
| Pure | Gamma manifest `3.50`; configured `IMPLEMENTATION=pure`, controller `pureCtrl static` |
| PP filter | Configured `Dream Realism 7.3 Gamma`, PP enabled |
| Output | Configured 1920×1080, fullscreen, VSync, 8× MSAA, anisotropy 16 |
| Upscaling | Existing FSR section `ACTIVE=1`, `QUALITY2=0.87`, `OLD_IMPLEMENTATION=2`; effective runtime dimensions/algorithm not newly witnessed |
| Pure bridge | Existing scriptable filter `pure`, enabled; no bridge/filter/shader replacement |

Configured weather is not promoted to a runtime observation. The failed attempt
never reached a scene in which Pure, exposure or rendering could be verified.
No camera, exposure, resolution, weather or visual setting was tuned. CM's
displayed UI FPS is not game performance.

## Material inventory and rejected shortcuts

Twelve existing third-party `.fbx.ini` sidecars contain **1,137 material records**,
including repeated source variants. They were read, not re-exported. Their shader
histogram and exact slots/properties remain private. The records are **authoring
evidence only**, not proof of current KN5 contents, effective CSP replacements,
unique materials, mesh counts, UV scale or normal orientation.

| Source candidate | Declared shader/normal slot | Eligibility still required |
|---|---|---|
| Car `plastic_rgh_001_#010101FF` | `ksPerPixelNM_UVMult`, `txNormal=plastic_normals.dds`; opaque flags | Live identity, nonfunctional trim, exact sharing/count, UV multiplier and preserved authored normals |
| Track `concrete` | `ksPerPixelNM_UVMult`, `txNormal=concrete_nrm.dds`; opaque flags | Live model/mesh match, UV density/basis, wetness interaction and local resource decode |
| Track `warehouse_floor` | `ksPerPixelMultiMap_NMDetail`, authored base/detail maps | More complex slot semantics; deferred as first target |
| Paint, glass, wheels/tyres, lamps and displays | Existing functional/PBR/clearcoat configurations | Excluded from the first experiment |

No candidate is selected for activation yet. Replacing an authored normal with
generic noise would erase information; a normal-slot name alone cannot justify
it. Phase 0P signed-X sampling does not certify this shader variant, complete Y
orientation, tangent basis or texture scale. No roughness packing, shader-family
migration or original custom HLSL execution is claimed.

The installed GUI default enables Objects Inspector. The maintainer's
[RainFX documentation](https://cup.acstuff.club/docs/csp/tracks/rainfx) describes
Alt-click inspection of scene material/mesh names; the
[0.3.0 release notes](https://acstuff.club/patch/?info=0.3.0) also warn that dragging
1D values can alter them temporarily. Planned inspection therefore reads names,
flags and bindings only, with no coefficient drags or edits. Its actual runtime
availability still needs observation.

## Includes, precedence and ownership

Car-local and selected skin configs already include car-paint/glass/self-lighting
templates and dashboard/display integrations. The track has lighting, water,
GrassFX, RainFX and material adjustments. **Thirteen shared configuration files**
were resolved as present, hashed and backed up; their use by other assets makes
them read-only. The simple inventory did not resolve `android_auto/config.ini`;
this is not proof that every CSP resolver fallback is unavailable.

The six scoped car/track/layout candidate files in central and `loaded` config
folders are absent. Native local/skin override precedence and the exact effective
include graph remain unverified. The maintainer's
[configuration README](https://github.com/ac-custom-shaders-patch/acc-extension-config/blob/433c5537b9e9ea0a83ab1bb1a9ccb33a486e1b17/README.md)
notes that CM may fetch configs automatically; no update policy is changed.
Post-run checks must distinguish any generated/downloaded file from an owned
RestoVisuals addition. No guessed precedence or broad wildcard replacement is used.

**Actual material installation diff: empty.** No RestoVisuals material files were
added to the game; no inventoried mod files changed, and no replacement section
or enhancement asset was activated.
All RestoVisuals receipts/backups/captures are confined to ignored
`.local/phase0r-20261105/`. A future normal-only test needs a fresh exact
material/mesh/slot selector, expected count, immutable inputs, collision checks,
complete file/hash manifest and full workspace recovery rehearsal before GO.

## Actual baseline attempt and stop decision

At **14:33:50 Eastern**, CM's existing Quick Drive Go control was invoked through
UI Automation after the run-specific unmodified-baseline GO and fresh preservation
checks. It started the expected game executable. Startup logs identify CSP
preview361/build3898, then report **`ERROR: Steam init failed`** and **Steam API
failed to initialize**. A native error dialog offered to restart Steam and retry.
That offer was declined using **No**; there was no retry, Steam restart, account
investigation, installation repair or graphics/mod change.

The attempt's generated race file confirms the requested car/track/layout/skin.
It contains ambient/road temperatures 14/14, weather ID `sol_06_overcast`, sun
angle 1.78 and time multiplier 1.0. These are **generated launch inputs**, not
observed world conditions: the scene, Pure/PP execution, exposure, actual output
surface and upscaling never became available for validation.

The game process was confirmed gone at **14:35:36 Eastern**. Its exit code was
not recoverable from the retained process object and is reported as unknown,
not zero. CM showed **Cancelled**. No game-scene baseline, replay frame, live
Objects Inspector data, normal-map sampling, image comparison or performance
measurement was obtained. This failure does not establish a broken target mod
or identify the underlying Steam/account/process cause. The earlier missing-model
warning was not reached or diagnosed anew. **NO-GO for another native attempt or
enhancement at this checkpoint.**

## Executed recovery and preservation limits

Fresh backups preserve the 29 protected files, 49 selected settings, 25 original
source/backup pairs and both 839-file SDK inventories. One CM preference file had
changed through owner use since Phase 0Q; its **new preflight state** is the
baseline, not the older Phase 0Q backup. Restoring old settings would lose owner
changes and is prohibited.

Additional backups cover 261 readable user configuration files, 34 readable
previous logs and three output files. Temporary replay and CSP installation-state
folders contain no files. Thirty-six auxiliary configuration files and 158 old
logs cannot be read; their size/attributes/time were recorded, no access controls
changed, and they are excluded from modification/restoration. Active mandatory
settings are readable; the inaccessible LUT is disabled in its active config.
These exclusions prevent a claim of complete archival backup of every user file.

The cancellation dialog was dismissed, and CM closed normally at 14:37:40,
exit **0**, under the owner's cleanup authorization. No process was force-killed.
An exact post-attempt audit found **no mod/protected/shared-config drift**. Five
unique original files needed restoration: `race.ini`, the CM preference store,
two runtime logs and the removed previous `race_out.json`. Every changed version
was archived privately before restoration; the removed output's preflight backup
was retained. One new crash archive was positively linked to this attempt's log.

The complete five-file recovery and owned-crash-archive removal passed **four
workspace cases**: completion, foreign-existing-file refusal, refusal of a foreign
file at the missing-output path, and interrupted recovery/resume. An unrelated
synthetic sentinel survived each case. These are recovery tests for this failed
launch, not static-material unload or scene cold-load validation.

Native atomic replacement of `log.txt` was denied by Windows. A rehearsed native
copy fallback restored it. PowerShell's hash reader encountered a sharing error;
because that error was non-terminating, the copy was not prevented by that failed
precheck. Verification then stopped. The original shared-read SHA-256 reader
confirmed the restored bytes and the remaining recovery completed. This is a
recorded guard limitation, not an atomicity/concurrency guarantee: an intervening
writer at that instant cannot be independently excluded. The lock owner was not
identified; no other process handle, ACL or permission was changed. Subsequent
PowerShell recovery commands used terminating-error handling. Both file versions
and the recovery receipts remain private. A verified temporary file left by the
failed atomic step and the archived owned crash report were removed.

CM was reopened under the same pinned executable. The original unsaved preset,
vehicle/paint/track/skin, time, weather and other visible choices were verified.
Normal startup rewrote its preference store. CM therefore closed normally again
at **14:49:39 Eastern**, exit **0**, and the exact fresh preflight preference file
was restored. **CM is left closed** to retain exact disk hashes; its restored
selection is backed up and was visibly verified. The existing owner ksEditor
remains open and untouched. All GUI operations finished before the deadline.

The five-file restore, startup preference restore and all post-run bytes are
documented under ignored `.local/phase0r-20261105/`. No material replacement was
installed or removed. This recovery does not prove live material restoration;
a future enhancement still needs original/enhanced/restored cold loads.

## Final verification and next prerequisite

The final scoped preservation check passes: **1,265 car files, 386 track files,
13 shared configs, 29 protected files, 49 selected settings, 25 original/backup
pairs and both 839-file SDK inventories** match their fresh baselines. All 261
additional readable configuration files, 34 readable logs and three output files
match baseline after recovery. The 194 excluded auxiliary files retain recorded
size/time; their contents are not hash-certified. The approved untracked visual
reference and all original sources remain unchanged.

All **201 existing test definitions** are byte-unchanged, including the historical
124 baseline. The unit suite was not rerun: project shader/code/asset bytes did
not change. Four recovery cases and the Windows copy rehearsal passed; the native
launch failed as recorded above. New checks cover preservation, manifest/hash consistency,
policy/history preservation, public links and privacy; these pass and do not
constitute native shader or image validation.

Fresh allowance began **70% five-hour / 42% weekly**. At the approximately
15-point preflight review it read **55%/39%**. After the owner replied, resumed
work began at **52%/39%**. The native failure ended testing; recovery/closeout
continued at **41%/37%**. Final meters/SHA are in the ignored synchronization
receipt. No delegation, model escalation, software update or licensing decision
occurred. Main, freeware and Phase 0E HDR NO-GO remain unchanged.

**Next prerequisite:** owner-established normal Steam/CM launch readiness, then
a freshly reviewed, unmodified CM baseline run. Do not automatically retry or
repair it. Only a normally loading scene can establish the exact live material,
normal orientation/scale, sharing/match counts and config precedence required
for the first normal-only transaction. The primary Phase 0R baseline/material
objective remains unfulfilled; no visual improvement or game FPS claim is made.
