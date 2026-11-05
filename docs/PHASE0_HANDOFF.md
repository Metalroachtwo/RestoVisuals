# RestoVisuals Phase 0T handoff — original native baseline captured

Prepared 2026-11-05 from verified local/remote
`4f7ba0530c8ab4724fa0d9af0fc624978343c716` on `phase0/foundation`. Read
[PHASE0T_BASELINE_VALIDATION.md](PHASE0T_BASELINE_VALIDATION.md) and
[observations](../examples/phase0t-baseline/observations.json). Previous handoffs
remain below. Main stays `814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

**The separately owner-authorized second attempt rendered the as-installed
Lexus/Drift Mansion scene and exited normally with code 0 at 17:18:22 Eastern.**
Private 1920×1080 cockpit/exterior images and one matching replay candidate were
preserved and hashed. The replay was not load-validated. No RestoVisuals material,
shader, HDR hook, physics or graphics setting was deployed or changed.

The first T attempt failed Steam API initialization. The game was already gone
before agent cleanup input; its exit code remains unknown. The owner confirmed a
manual Steam-only restart, then explicitly authorized one fresh baseline attempt.
No automatic retry, agent Steam restart, repair or usage reset occurred. Live
Steam/CM/game contexts matched user/session and Medium integrity on both attempts.
Successful loading after the owner's restart does not uniquely establish root
cause. Normal launch readiness is now witnessed for this session only.

CM retains the original car/skin, track/layout/skin and Practice/Pits selections.
The game's initial panel reported clear/no clouds, approximately 13:07, air 19°C,
road 30°C, wind 0 km/h and grip 100%, differing from CM's Pure/13:06/13.5°C/
8.1 km/h SSW configuration. Do not equate configured and effective conditions.
Native logs witness Dream Realism 7.3 Gamma PP loading; Pure Gamma 3.50 remains
configured. Existing missing-model/app-icon warnings were retained, not repaired.

Camera evidence records Drive, F1 once from cockpit, then two exterior captures
without driving input. Simulation time advanced; exact camera/world pose,
exposure, replay frame and internal render resolution were not certified. No
image-equivalence test, live material inventory or trustworthy performance
measurement was performed. Material integration and Phase 0E HDR remain **NO-GO**.

Recovery restored nine fresh-backed file versions after the first attempt and
five after the second, with scoped workspace rehearsals and hash guards. The
owner explicitly chose **Keep CM open; preserve working session**. Accordingly,
**48/49 selected settings match the T baseline**; the live CM preference store
is the declared exception, with both versions preserved. CM and the owner's
existing ksEditor remain open. No owned game process remains.

Two additional runtime-state files, `extension/state/lua/app/WebBrowser.ini` and
`extension/state/odometers.ini`, differ from an older R receipt but lack fresh T2
pretest hashes. Their current data was archived and retained. Do not overwrite
them from the old receipt or claim full user-state rollback/change attribution.
Fresh final checks verify 29 protected files, 1,265 car files, 386 track files,
13 shared configs, both 839-file SDK baseline sets and 25 original sources.
The approved untracked reference and all 201 test definitions, including the
historical 124, remain unchanged. Unit suite not rerun for this evidence/docs-only
change; nine targeted receipt, recovery, preservation and publication validation
groups passed.

Last GUI evidence was collected at 17:26:47 Eastern, before the owner's final
18:00 cleanup checkpoint and 18:15 hard stop. No further GUI work is planned.
Initial allowance was 20% five-hour / 34% weekly, then 17%/33% while timing was
pending; a replenished window was observed at 99%/33% without a reset action.
Closeout began at 78%/30%; final meters/SHA are in private synchronization receipts.
Both reset credits remain reserved for explicit owner instructions. No persistent
access exception, model escalation or new deployment permission was created.

**Next:** establish one controlled replay/camera baseline and read-only native
inventory of a single opaque normal-mapped material, with fresh runtime-state
coverage, exact match/slot counts, UV/basis, original resources and config
precedence. Require separate authorization/safety review before enhancement.
Preserve locked versions, freeware, owner-undecided licensing, existing source,
Phase 0J cold-reload recovery and the Phase 0E HDR NO-GO.

---

## Historical Phase 0S handoff — read-only Steam evidence; cause unresolved

Prepared 2026-11-05 from verified local/remote
`a98d1cb0fcc722e44719882a07d70e9c1d8a9523` on `phase0/foundation`. Read
[PHASE0S_STEAM_READINESS.md](PHASE0S_STEAM_READINESS.md) and
[findings](../examples/phase0s-steam-readiness/findings.json). Previous handoffs
remain below. Main stays `814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

**Root cause remains unconfirmed; no launch/repair GO.** The same Steam client
process predates Phase 0R's failure, and Steam's own log tracks the reviewed game
process under correct App ID 244210 at 14:33:50, then removes it at 14:35:38.
The configured library manifest resolves to the reviewed game installation and
present executable; the existing App ID file contains 244210. Nothing was changed.
This does not prove successful API initialization or active-account entitlement.

Current Steam client/UI and diagnostic process share Windows user/session and
Medium integrity, not elevated. No checked RUNASADMIN compatibility entries were
present. Historical CM/game tokens and actual working directory were not captured
in 0R and remain unknown. Windows denied the scoped Security-log read; supporting
Sysmon/Application evidence was not obtained. No auditing or privilege change.

Privacy-safe exact UI label queries exposed no sign-in/online indicator. No
account labels, IDs, credentials, cookies, login stores or licensing records were
retrieved; no raw Steam logs were copied. Absence of a label is not proof of
offline/signed-out state. CM/game remain closed; owner ksEditor is untouched;
Steam remains running. No activation, screenshot, menu, restart, repair, verify,
update, AppID/DLL/manifest/launch-option edit or game test occurred.

Fresh SHA checks pass for 29 protected files and 49 settings. Reuse Phase 0R's
1,265-car/386-track/13-shared/both-839-SDK inventories rather than repeat them.
Original shaders/code, 201 test definitions and the untracked reference are
preserved. Private receipts stay ignored under `.local/phase0s-20261105/`.
Unit suite not rerun for read-only/documentation work. No restoration is needed.

Allowances began 31% five-hour / 36% weekly; bounded investigation ended and
closeout began at 25%/35%. Final meters/SHA are in private synchronization
receipts. No delegation/escalation of model reasoning occurred. Preserve freeware,
owner-undecided licensing, locked versions and Phase 0R material/0E HDR NO-GO.
Next: owner verification of visible Steam readiness without sharing identifiers,
then only a separately reviewed baseline with live process-context evidence.
No automatic retry or repair. Check actual time before GUI; today's deadline
remains 17:00 Eastern with cleanup by 16:30.

---

## Historical Phase 0R handoff — Steam-init launch blocker; recovery verified

Resumed 2026-11-05 from verified local/remote
`bb0033bea42c093043474a7232da128e275ffa89` on `phase0/foundation` after the
owner answered "Allow CM cleanup restart if needed". Read
[PHASE0R_REAL_MOD_VALIDATION.md](PHASE0R_REAL_MOD_VALIDATION.md),
[observations](../examples/phase0r-real-mod-validation/observations.json) and
[failure evidence](../examples/phase0r-real-mod-validation/failure-evidence.json).
The earlier preflight handoff and prior milestones follow below.

**The single unmodified CM baseline attempt failed before scene loading.** At
14:33:50 Eastern, the existing CM Quick Drive Go control started the reviewed
game process for `mm_lexus_rca` / `jd_drift_mansion/open`, Burnt Orange Metallic
and the existing VDC 2024 track skin. Logs identify CSP preview361/build3898,
then report Steam API initialization failure. The native offer to restart Steam
and retry was declined. No Steam/account repair or second launch was attempted.
This does not identify the underlying cause or establish mod incompatibility.

No scene, replay baseline, Objects Inspector data, live material/texture
compatibility, custom-HLSL execution, comparison image or game-performance result
was obtained. **Native material testing and Phase 0E HDR remain NO-GO.** The
pre-existing missing-model warning is unrelated evidence and was not reached in
this attempt. Existing shader/UV/normal/sharing/precedence gates remain pending.

The game process exited after No; its exit code is unknown, not zero. CM's
cancellation dialog closed, and CM exited normally with code 0. Five original
files (race input, CM preferences, two logs and one prior output) were restored
from fresh backups; post-run versions were preserved privately. Four full-plan
workspace recovery cases and a Windows copy rehearsal passed. One native atomic
log replacement failed; the fallback encountered a non-terminating PowerShell
hash/sharing error, so its precheck did not prevent the copy. Final shared-read
hashes verify restoration; no concurrency/atomicity guarantee is claimed. Details
and guard limitations are documented. No lock owner or access controls changed.

CM reopened with the original unsaved selection visibly intact. Because startup
rewrote its preference store, it closed normally again, code 0, at **14:49:39
Eastern** and the exact preflight preference bytes were restored. **CM is left
closed**; the existing owner ksEditor remains open/untouched. Owned crash and
recovery-temp files were archived privately and removed. No persistent GUI
permission or running helper remains. All GUI work ended before the deadline.

Final scoped checks pass: 29 protected files, 49 settings, 25 original/backup
pairs, 1,265 car files, 386 track files, 13 shared configs and both 839-file SDK
inventories match baseline. Additional readable settings/logs/outputs match;
194 inaccessible auxiliary files retain size/time only. All 201 test definitions
and original shaders/code/reference remain unchanged. Unit suite not rerun.
Private evidence is ignored under `.local/phase0r-20261105/`; public receipts
contain no mod assets, proprietary shaders, machine paths or private configs.

Original allowance 70% five-hour / 42% weekly; resumed 52%/39%; native failure
ended testing and recovery/closeout continued at 41%/37%. Final meters/SHA are in
private synchronization receipts. Main stays
`814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`; freeware and licensing remain unchanged.
**Next:** owner-established normal Steam/CM launch readiness, then a fresh reviewed
unmodified baseline run. Do not automatically repair or retry. Recheck actual
Eastern time and meters; today's GUI authorization ends at 17:00, cleanup by 16:30.

---

## Historical Phase 0R preflight handoff — runtime pending at that checkpoint

Prepared 2026-11-05 from verified local/remote
`f58b95ca72791f0174a36115b01db616058f9bd3` on `phase0/foundation`.
Read [PHASE0R_REAL_MOD_VALIDATION.md](PHASE0R_REAL_MOD_VALIDATION.md),
[observations](../examples/phase0r-real-mod-validation/observations.json) and
[ownership manifest](../examples/phase0r-real-mod-validation/ownership-manifest.json).
The owner's Phase 0R authorization permits controlled reversible testing on the
selected real mods; building a complete original track is no longer prerequisite.
Main remains `814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

**Preflight validated; the primary runtime objective remains pending.** Existing
CM displays the requested MM Lexus RC-A, Burnt Orange Metallic and Drift Mansion
Open. Installed metadata and existing CM-generated race settings identify
`mm_lexus_rca`, `jd_drift_mansion`, layout `open`, skin `Burnt_Orange Metallic`.
Existing track skin `vdc2024` is preserved. Fresh immutable baselines cover 1,265
car files, 386 track files and 13 shared configs. No original KN5/config was edited.
The Open list references missing `dm_layout_pits.kn5`, also warned about during
successful Phase 0D initialization; no repair or clean-dependency claim is made.

Current configured stack remains CSP preview361/build3898, CM 0.8.2913.40776,
Pure Gamma 3.50, Dream Realism 7.3 Gamma PP. CM shows 13:06, Pure, 13.5°C,
Optimum, 8.1 km/h SSW, Practice/Pits. Configured output is 1920×1080 with existing
FSR active/QUALITY2 0.87; effective runtime rendering is not newly witnessed.
No weather, exposure, camera, physics or graphics setting was changed.

Twelve existing authoring sidecars contain 1,137 records across source variants;
these are not a runtime material count. Opaque normal-mapped trim/concrete are
potential targets only. Actual shader/bindings, normal orientation, UV scale,
sharing/match count and effective config precedence still need live inspection.
Objects Inspector is enabled in the installed GUI default, not yet opened here.
No generic replacement, roughness, family migration or custom HLSL was staged.

**Baseline launch is HOLD pending the existing CM cleanup choice.** The existing
CM session contains an unsaved preset. Its current files and visible selection
are preserved, and the owner was asked whether CM may be closed/reopened only if
needed for exact recovery. No answer is assumed. The installed owner ksEditor
remains untouched. Do not launch a dependent game test before resolving safe
recovery; if normal loading fails, stop without speculative mod repairs.

All 29 protected files, 49 selected settings, 25 original/backup pairs and both
839-file SDK inventories are backed up/verified. The new owner CM preference
state since Phase 0Q is the current baseline; never restore the older Q bytes.
Additional readable state backups and exact inaccessible auxiliary-file exclusions
are recorded privately. No access controls, versions or update policies changed.
No game session, native material activation, enhanced/restored image comparison
or game performance measurement occurred in Phase 0R. Actual installation diff
is empty; enhancement and Phase 0E HDR remain NO-GO. Prior code/tests/reference
and Phase 0P/Q evidence are preserved; private receipts stay under ignored
`.local/phase0r-20261105/`.

The preflight preservation validation passes for all scoped readable files; the
194 inaccessible auxiliary files retain size/time only. All 201 old test
definitions remain byte-unchanged; no unit suite was rerun. No setting restore
was needed, no owned application remains open and the original CM/editor sessions
remain alive. At the approximately 15-point review, research stopped and this
checkpoint entered synchronization while the required cleanup choice was pending.

Allowances started 70% five-hour / 42% weekly; first checkpoint 64%/41%,
checkpoint closeout 55%/39%.
Read fresh meters/final private receipts before resuming. GUI cleanup must begin
by 16:30 and all computer-use finish before 17:00 Eastern today. Next: resolve
CM recovery permission, capture one unmodified stationary baseline through CM
and read one live material in Objects Inspector. Prepare no material transaction
until every exact-target gate passes. Freeware and unresolved licensing persist.

---

## Historical Phase 0Q handoff — original KN5 render-load validated

Prepared 2026-11-05 from verified local/remote
`e9cbf60d1707028add4c1e62bab930e441ab7a0d` on `phase0/foundation`.
Read [PHASE0Q_KN5_LOAD_VALIDATION.md](PHASE0Q_KN5_LOAD_VALIDATION.md),
[observations](../examples/phase0q-kn5-validation/observations.json) and
[runtime readiness](../examples/phase0q-kn5-validation/runtime-readiness.json).
Main remains `814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`; Git and ignored final
receipts identify the synchronized checkpoint. The prior handoff follows below.

**Non-game geometry/render-load passes.** Installed CM 0.8.2913.40776 accepted
the original Track KN5 through its plain-filename Lite Showroom route, outside
any installed car/track container. The original quad rendered and the viewer
reported two triangles. The selected 350,981-byte file and all owned copies retain
SHA-256 `cc4285989205597824750c9871c44f7eeace384b02ef026dbf472fc9ea4d28fd`.
The original remains private and immutable. No FBX, DDS-header, camera or signed-X
experiment was repeated; the owner's existing installed editor was untouched.

**Serialized material/texture auditing remains incomplete.** The bare viewer
did not expose mesh identity/count, material name, shader binding or embedded
texture payloads. Its SimpleNoPCSS overlay is the viewer renderer shader set,
not proof of serialized ksPerPixelNM. Phase 0P's source/editor sampling evidence
remains separate. The older SDK AcTools library candidate was blocked by its
legacy-host load error; its existing origin marker was preserved, with no
unblocking or policy change. Maintainer source references and observed CM
behavior establish the successful route without a custom parser or new tool.

**In-game testing remains NO-GO.** No installation, game launch, material
replacement or custom-HLSL execution occurred. The candidate original track
namespace is absent, but the minimum supported track contract, original support/
marker/collision assets and complete file/hash/recovery manifest are not ready.
Three workspace-only recovery cases passed for the one known KN5: collision
refusal, interrupted-copy cleanup and owned rollback preserving an unrelated
sentinel. This is not complete track rollback or game cold-load validation.
Separate owner approval is required before any future game staging or launch.

The owned CM viewer closed normally, exit 0, at 12:27:17 America/New_York.
One CM preferences file changed during normal use; its changed bytes were
preserved privately and the verified preflight backup restored with CM closed
and exact hash guards. All 29 protected files, 49 selected settings, 25 original/
backup pairs and 839 files in each installed/mirror SDK location match baseline.
The original untracked visual reference is preserved. Ten affected fixture-source
regressions pass, zero failures; all 201 existing test definitions, including the
historical 124 baseline, remain unchanged. No full-suite rerun was needed.

Allowances began at 100% five-hour / 46% weekly following replenishment. Formal
closeout began at 82%/44%, after native work finished; documentation checkpoint
73%/42%. Read final private receipts and fresh meters before resuming. No model
escalation or delegation occurred. Raw evidence remains ignored under
`.local/phase0q-20261105/`. The temporary GUI exception ends at 17:00 Eastern,
cleanup by 16:30. No further GUI operations are required for this checkpoint.

Next: establish the authoritative minimum-track contract and prepare separately
owned support assets plus a complete installation/recovery manifest. Preserve
the demonstrated CM load route, locked stack, freeware policy, owner-undecided
license, Phase 0E HDR NO-GO and Phase 0J cold-reload requirements.

---

## Historical Phase 0P resumed handoff — camera and sampling validated

Prepared 2026-11-05 from verified `cecd6448dd0920ea2aaf9d8afed18546f820b8b5`
on `phase0/foundation`. Read the current
[PHASE0P_CAMERA_VALIDATION.md](PHASE0P_CAMERA_VALIDATION.md),
[resumed receipt](../examples/phase0p-camera-validation/resumed-observations.json)
and [native comparisons](../examples/phase0p-camera-validation/native-sampling.json).
The prior blocked attempt is preserved below. Main remains
`814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`; final tip/verification are in Git
and ignored receipts.

**Primary gate passes; native normal-texture sampling is confirmed.** Two fresh
owned sessions reused the verified SDK mirror and unchanged original FBX. At FOV
60, Ctrl+Page Up held 120 ms followed by vertical left-drags +90 and +60 pixels
produced the same full-pad view, position label `(0,30,0)`. The captured viewport
interiors match exactly in display RGB. Verify pose when repeating elsewhere;
timed input is not guaranteed frame-independent. Actual mesh identity, two
triangles, position/scale/bounds and original material values were checked.

Original +X/-X DDS inputs were represented in the existing legacy container only
after that repeat passed. All original pixels/nine mips and channel masks are
preserved. Fixed-state captures show distinct six-repeat shading; persistence
changes only the normal filename. Returned flat restores all material/mesh values
and exactly matches baseline display RGB. This confirms native ksPerPixelNM
texture consumption and X-consistent response, not complete RGB-to-TBN calibration,
green-axis sign, absolute world-light direction or native resource precision.
No artistic detail map or custom HLSL was deployed.

**One original Track KN5 was exported**, after a fresh file-only safety GO, through
File > Save KN5 > Track and native Save As. Private `rv0p_original_pad.kn5`:
350,981 bytes; SHA `cc4285989205597824750c9871c44f7eeace384b02ef026dbf472fc9ea4d28fd`.
Its backup matches. It is **exported, not load-validated**; serialized contents
were not independently inspected. No game launch/deployment occurred. Native-game
integration remains NO-GO pending supported KN5 load validation and a separately
reviewed original container/spawn/collision/cold-load plan. Phase 0E HDR NO-GO persists.

Programmatic focus refusals were resolved with a validated owned-title-bar click:
date/executable/PID guards, two ownership hit tests, no held modifiers and final
foreground verification. No unrelated app received input, no input-routing bypass
or persistent provider permission was added. The owner's installed editor was
left open/untouched. Only the two owned resumed sessions closed, both exit 0;
the last closure was verified at 10:54:23 Eastern. Original preview selections
were reloaded and working persistence restored. Editor restoration is not a game
loaded-material recovery test.

All 29 protected files, 49 settings, 25 source/backup pairs and 839 SDK files in
each installed/reused-mirror location pass fresh hashes. Four original working
inputs are restored. The SDK-created NULL.dds and private KN5/screenshots remain
ignored under `.local/phase0p-20261105/resume-1014/`; no proprietary asset is
published. The approved reference remains unchanged/untracked. Fifteen targeted
tests pass, zero failures; all 201 old definitions/historical 124 baseline remain
unchanged. No full-suite rerun, model escalation or delegation occurred.

Resumed meters began 41% five-hour / 50% weekly. After sampling, 30%/48% supported
one bounded file-only export; formal closeout began at 23%/47% with all native work
finished. Read final receipts/fresh balances before resuming, reserve closeout
allowance and retain the weekly 5% cutoff. Today's GUI/DCC exception ends at 17:00
Eastern, cleanup by 16:30. Recheck actual time. Next: supported KN5 load validation
under a separately reviewed isolated fixture plan. Keep locked stack, freeware,
unresolved licensing, Phase 0J cold-reload requirements and main unchanged.

---

## Historical Phase 0P initial handoff — foreground blocked

Prepared 2026-11-05 on `phase0/foundation` from verified local/remote
`d7e3c1707ecf32e6964583ba0095f5c74e9de50f`. Read
[PHASE0P_CAMERA_VALIDATION.md](PHASE0P_CAMERA_VALIDATION.md) and the
[sanitized observation receipt](../examples/phase0p-camera-validation/observations.json).
Current Git tip and ignored final receipts identify synchronization. Remote main
remains `814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

**BLOCKED at foreground access; primary camera gate incomplete.** One fresh owned
ksEditor session reused the verified existing Phase 0O SDK mirror and unchanged
original FBX/legacy-flat DDS. Clear/default Load buttons restored the colored sky.
One Page Up down/up pair, held 600 ms, changed the position label from zero to
`0.000000; 0.150000; 0.000000` and View to `0.000000; -0.150000; 0.000000`.
A narrow surface edge appeared at the bottom; full silhouette, live mesh identity,
visible face and diffuse sampling were not jointly established. FOV stayed 60.
This is one label displacement, not a measured continuous movement speed.

The next Ctrl+Page Up/left-drag operation was rejected by foreground verification
before any input was delivered. An unrelated app was foreground; ordinary owned
activation/restore did not acquire it. A direct accessibility focus request found
the top-level target could not receive focus, and the owned viewport did not
advertise keyboard focusability. No unrelated-app input or input-routing bypass
was used. The underlying activation failure remains UNKNOWN. A manual foreground
request remained unanswered, and the bounded run then closed the owned editor.
That earlier request no longer refers to a live window.

Left-drag/arrows/Page Down/Shift/Ctrl/wheel behavior remains UNTESTED, not failed.
There was no second session/repeatability test, no tree double-click, geometry/
winding/shader/coefficient/light change, Blender/export repeat or DDS conversion.
One read-only source/persistence inspection retained +Y plane orientation, expected
bounds/basis/UVs, material slots/properties and visible/renderable flags. Do not
promote the narrow edge to confirmed diffuse/normal sampling. KN5/native NO-GO
and Phase 0E HDR NO-GO remain binding.

The owned editor closed normally, parent-witness exit 0, verified at 09:49:59
America/New_York. No Save Data or force termination was used; the in-memory preview
session ended. All 29 protected files, 49 settings, 25 original/backup pairs,
839 installed SDK files and 839 reused-mirror files match fresh baselines. Four
owned project inputs are restored/verified; persistence has no value delta and
the exception log is unchanged. No KN5, game launch, deployment or installed
rollback occurred. This is not a game material cold-reload test.

Ten affected fixture-source regressions pass. All 201 existing test definitions,
including the historical 124 baseline, remain unchanged; the full suite was not
rerun for this evidence/documentation change. Raw screenshots, unrelated desktop
diagnostics, settings and backups remain ignored in `.local/phase0p-20261105/`.
The approved visual target remains unchanged and untracked.

Live meters started at 52% five-hour / 52% weekly, read 47% / 51% at interruption
and 45% / 51% at formal closeout. Access failure ended investigation before the
approximately 15-point review. Final balances are in the ignored receipt; preserve
the approximately 15-point closeout reserve and weekly 5% cutoff. No model
escalation or delegation occurred.

Next: fresh owned editor with confirmed foreground access, then short controlled
vertical/left-drag movements to frame the unchanged pad from its +Y side and
reproduce an equivalent view in another fresh session. Only then compare original
flat/+X/-X normals and review one KN5 export. Do not investigate more DDS formats,
change source geometry or repeat exporter work to address this desktop blocker.
Recheck time/allowances: today's GUI/DCC exception ends at 17:00 Eastern, cleanup
by 16:30. All owned applications are closed. Keep locked versions, Phase 0J
cold-load requirements, freeware policy, unresolved licensing and main unchanged.

---

## Historical Phase 0O continuation handoff

Prepared 2026-11-05 on `phase0/foundation` from verified local/remote
`092625e2669f0f10a6afbdb8c8f15c2934c39a06`. Read
[PHASE0O_EDITOR_RENDER_VALIDATION.md](PHASE0O_EDITOR_RENDER_VALIDATION.md),
[editor observations](../examples/phase0o-editor-preview/editor-observations.json)
and [capture receipts](../examples/phase0o-editor-preview/capture-receipts.json).
The synchronized tip is recorded in Git and ignored final receipts; main remains
`814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

**Preview partially recovered; material sampling and KN5 remain NO-GO.**
In one fresh isolated SDK mirror, loading `3_clear` through Illumination >
Load Weather recovered sky/cloud structure while `b&w` stayed monochrome.
Loading `default` through Load PPfx then recovered color. Merely selecting a
combo entry was recorded separately from pressing Load. Data Editor's original
default selections were inspected without Save Data. Actual game/Pure/Dream
weather or PP settings were untouched.

The pad/diffuse surface was still not identifiable. Double-clicking its scene-tree
mesh leaf produced a black view; the gesture's framing semantics and actual camera
pose were not established. Reloading weather did not recover that transient view.
View/Pos labels displayed zero triples, but were not proven live camera telemetry
or supported setters. Do not diagnose a zero camera, a DDS failure or hidden mesh
from these labels/blackness. No speculative navigation/settings loop followed.

Before/after Save Persistence differs only in header DATE/MD5_HASH. The exact
`ksPerPixelNM` material, 12 properties, diffuse/legacy-flat slots and mesh flags
remain unchanged. Phase 0M's original FBX (19,260 bytes, SHA
`49e1dc29e3e2ff976995d67e0bceaaca038e57443885814c72ea48e65ab2b474`)
was reused without Blender/export. Phase 0N's legacy flat DDS is unchanged.
No new DDS, directional sampling, KN5 save, game launch or deployment occurred.
Diffuse/normal shader sampling and native tangent/channel decode remain UNKNOWN.

Original `1_heavy_fog`/`b&w` preview values were reloaded. That restored the
illumination grid, not the original preview pixels; no visual camera rollback
is claimed. The owned editor closed normally with exit 0, verified at 08:48:13
America/New_York. Its working persistence was restored byte-for-byte. All 29
protected files, 49 settings, 25 original/backup pairs and 839 SDK files in each
of the installed, prior-mirror and current-mirror locations pass fresh hashes.
No SDK file was added/modified; the pre-existing exception log is unchanged.
No installed rollback is needed. This is not a game material cold-reload test.

Ten affected fixture-source tests pass, zero failures. All 201 existing test
definitions and original implementations/assets remain intact, including the
historical 124-test baseline; the entire 201-test suite was not rerun for this
documentation/evidence milestone. Private screenshots, settings, raw exports,
backups and receipts remain ignored under `.local/phase0o-20261105/`. The approved
visual reference remains unchanged and untracked.

Live meters started at 69% five-hour / 55% weekly. Formal closeout was already
underway at 56% / 53%, before the approximately 15-point review, because the
bounded preview gate had failed. The 15-point review read 54% / 52%; all 58 closeout
checks passed and only synchronization remained. Final live readings are in the ignored receipt.
No model escalation or delegation occurred. Preserve synchronization allowance
and the independent 5% weekly cutoff; obtain fresh readings on resumption.

Next: establish a documented repeatable ksEditor camera/framing operation above
the unchanged +Y-facing pad, with identifiable silhouette and diffuse material.
Reuse clear-weather/default-PP Load buttons and existing FBX/flat DDS. Only after
that succeeds may fixed-camera/light flat/+X/-X sampling begin, followed by a
fresh export review. Do not repeat header research, re-export Blender, generate
more formats or alter shader coefficients/geometry to conceal visibility failure.
Any future game experiment still requires its original container/markers and a
separate reviewed authorization/cold-load plan.

Today's temporary GUI/DCC exception ends at 17:00 America/New_York, cleanup by
16:30; check actual time before any new GUI use. All owned applications are closed.
Preserve Phase 0E HDR NO-GO, Phase 0J cold-reload requirements, locked versions,
freeware policy, unresolved repository licensing and unchanged main.

---

## Historical Phase 0N continuation handoff

Prepared 2026-11-05 on `phase0/foundation` from verified local/remote
`5350ca3d34cc806026c1e0fa7f453606a5213f03`. Read
[PHASE0N_DDS_COMPATIBILITY.md](PHASE0N_DDS_COMPATIBILITY.md), the
[offline DDS comparison](../examples/phase0n-dds-compatibility/comparison.json) and
[editor observations/review](../examples/phase0n-dds-compatibility/editor-observations.json).
Current tip and ignored final receipts identify synchronization; main remains
`814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

One original traditional-header candidate now reproduces all nine mip payloads
of the unchanged Phase 0K DX10 flat DDS. It retains RGBA bytes/opaque alpha with
little-endian R/G/B/A masks 0x000000ff/0x0000ff00/0x00ff0000/0xff000000.
This is A8B8G8R8 word layout, not BGRA. No compression/gamma/pixel change occurs.
Files are 349,672 / 349,652 bytes; the 349,524-byte pixel payload is identical.
Candidate SHA-256:
`1ead2f733f73ab1abff72f48267acdf794efbc1291165468df875081055e1460`.
Independent mask decoding checks all mips; existing Pillow 13.0.0 independently
checks both complete base images. Five new tests and 26 affected regressions pass;
all 196 old definitions remain unchanged (201 now). The historical 124 baseline,
original implementations and all original packages remain intact.

ksEditor's metadata recognition changes from LUM (0), 0x0 to ARGB, 256x256 and
nine mips. The generic ARGB UI label does not redefine the actual RGBA byte order.
Saved A/B state differs only in the normal filename after ignoring header date/
checksum; the same mesh/material/shader, 12 properties, slots and flags are retained.
No lighting, camera, geometry or texture-coordinate change concealed the result.

**KN5/native NO-GO.** This confirms header sensitivity in the editor's reporting
path, not a categorical DX10 GPU-loader failure. Texture Review explicitly reads
saved INI/file metadata; it is not proof of resident-resource or shader sampling.
No supported pixel/readback evidence was established and the viewport stayed
inconclusive. No KN5 save or game launch occurred. The export-safety review is
explicitly NO-GO until actual resource/material compatibility is evidenced.

Read-only preference inspection showed default weather/PPfx UI selections and
camera lens/exposure values, but their active state and the preview's cause remain
unknown. They were not changed/saved. The pre-existing copied exception log stayed
unchanged; do not call it a new render fault. No alternate format was generated.

Today only, task-specific GUI authorization runs from the owner's approval until
17:00 America/New_York, overriding the 08:00 start and DCC GUI restriction in scope.
Start GUI cleanup by 16:30. Recheck actual time before any later operation; neither
this handoff nor a staging package extends the deadline or authorizes game testing.
Private time guards enforce the window. No Blender session was needed or launched.
One fresh owned editor session closed normally with exit 0 at 07:08:44 Eastern.
A/B evidence is preserved; the owned project INI was restored to its input bytes.

All 29 protected files, 49 settings, 23 scoped originals/reference and 839 installed
SDK files match fresh preflight; 127 closeout checks pass. Original source packages
and raw FBX/Blend remain
unchanged; the visual reference remains untracked. No installed rollback is needed.
Private backups, raw exports, screenshots and final receipts are under
`.local/phase0n-20261105/`. Public artifacts contain original data/receipts only.

Starting live meters were 99% five-hour / 59% weekly; the near-15-point review
read 83% / 57%. Work then moved to closeout; the commit-ready reading was 76% / 56%.
Read fresh meters on resumption,
reserve verification/documentation/Git allowance and retain the 5% weekly cutoff.
No model escalation or delegation occurred.

Next: establish a supported informative editor preview/resource-pixel validation
baseline with the same DDS pair, then review export readiness anew. Preserve
KN5/native NO-GO, Phase 0E HDR NO-GO, Phase 0J cold-load restrictions, locked stack,
freeware policy and unresolved repository licensing. Do not enable old J/K
replacement packages, build a converter matrix or bypass the missing proof.

---

## Historical Phase 0M continuation handoff

Prepared 2026-11-04 evening on `phase0/foundation`, resumed from verified
`cf80bda61467c574bf1c5c12e6495128c5539876`. Original Phase 0L source checkpoint:
`4eb90d9b9962e607fb334750497d68b376863807`. Read
[PHASE0M_EXPORT_STATUS.md](PHASE0M_EXPORT_STATUS.md) and the
[sanitized numerical receipt](../examples/phase0m-export-evidence/export-receipt.json).
Current tip and ignored final receipts identify synchronization. Main remains
`814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

Actual original FBX export and supported Blender reimport passed. Blender 5.1.1
used the installed legacy FBX 7400 exporter, selected mesh, metric unit scale 1,
-Z/Y export axes and tangent-space output. Four positions, one quad/UV set,
UV-derived T/B/N and exact material name passed before/after import. The initial
material-name check hit an orphan-data alias; cleaning only the owned orphan
mesh/material data and reimporting the same unchanged FBX resolved it.

FBX: 19,260 bytes, SHA-256
`49e1dc29e3e2ff976995d67e0bceaaca038e57443885814c72ea48e65ab2b474`.
Original Blend: 98,472 bytes, SHA-256
`b7244f1347b30ded51545b49dc3a9f353950aaf685101663756d2896bf97a124`.
Raw exports stay in `.local/phase0m-20261104/resumed-export/exports/` because
the FBX embeds an absolute workspace path. Do not publish or rewrite it casually.
The unchanged Phase 0L source package retains its historical source-only flags.

ksEditor imported the FBX and reported two triangles, unit scale and radius
8.485281. The exact ksPerPixelNM panel and saved persistence confirm one material,
two slots, 12 properties, opaque flags and owned mesh state. Extra properties
and all persisted channels are recorded without inventing their semantics.
The required resource folder is singular `texture`, documented by the SDK.
Copying the original PNG there and reloading made it report 32x32.

**KN5/native NO-GO.** The original DX10/DXGI-28 flat normal DDS reported
`LUM (0), 0x0`, 349 Kb before/after supported reload. A reloaded message does not
validate decode. UI metadata limitation versus actual loader failure is unknown;
do not assert categorical DX10 incompatibility. The viewport stayed gray, so
visual appearance/orientation is not approved. No KN5 export was attempted.
An Open KN5 menu entry was not observed; supported output verification is pending.
The copied render-exception log was unchanged from the original and is not a
new runtime failure witness. No alternative converter/shader/writer was tried.

The owner explicitly approved the after-hours export and cleanup. Two owned GUI
sessions ran with private configuration/SDK mirror and verified backups. Both
closed normally with exit 0; original preferences and installation inputs are
unchanged. No existing session, unrelated app, game/CM, mod or protected stack
was changed. The temporary after-hours scope ended with cleanup. Future operations
must follow the retained task scope and independently applicable time rules.
The restricted-shell process inventory cannot prove host-wide absence; use the
authorized host view when actually permitted. Do not repeat the failed gateway probe.

Initial allowance was 37% five-hour / 64% weekly; resumed start was 33% / 63%.
Closeout began at 18%, sessions closed at 16%; reserve remains for verification,
documentation and Git. Read both meters anew on continuation, retain sufficient
closeout allowance and keep the 5% weekly hard cutoff. All 196 tests and prior
source/runtime artifacts are preserved; 169 closeout checks pass. No model
escalation/delegation was used. Resumed-run final receipts are under
`.local/phase0m-20261104/resumed-export/evidence/`.

Next: resolve the normal-resource decode/display gate through supported evidence,
then review any required compatible original DDS representation and output
verification route before another owned export attempt. Do not launch games,
automatically deploy the incomplete persistence, change locked versions or
bypass a failed exporter. Preserve Phase 0E HDR NO-GO, Phase 0J cold recovery,
100% freeware, references and unresolved repository licensing.

---

## Historical Phase 0L continuation handoff

Prepared 2026-11-04 on `phase0/foundation` from verified local/remote
`c1e03094a42f3a7ca54d7dfe88651938b3428d76`. Read
[PHASE0L_FIXTURE_PIPELINE.md](PHASE0L_FIXTURE_PIPELINE.md) for exact inventory,
source assets, future operator steps and native gates. Current tip plus final
private Git receipt identify closeout. Main stays
`814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

**Native test NO-GO.** The genuine candidate path is now documented: original
OBJ/MTL -> authorized isolated DCC scene -> installed legacy FBX exporter ->
ksEditor Open FBX / Save KN5. No DCC import, FBX export, editor operation, KN5 or
game load was performed. No supported headless KN5 export was identified in the
bounded installed references. Do not guess flags, launch help, use a variant
editor or construct a conversion workaround. Stop at prepared source.

The SDK contains ksEditor.exe (file 1.0.0.0), its FBX SDK 2014.1 runtime and the
76-page Kunos pipeline manual. The launcher only starts the GUI. The manual
requires its documented older FBX workflow, one UV set and unique object names;
it documents Open FBX, Save KN5 and partial persistence behavior. Blender's real
installed binary is 5.1 (registry 5.1.1), with a bundled legacy exporter declaring
version 7400, selected export and tangent-space controls. This is static evidence,
not a verified toolchain roundtrip. Version/hashes are in the report/private receipt.
Blender MCP registration and DCC/MCP CLI exist; no live gateway/scene probe occurred.
No ksEditor MCP interface was established. Alternate editor files were not chosen.

The original [source package](../examples/phase0l-fixture-source/README.md) has
one 12x12 intended-metre quad, one material and one UV set (0..6), at two intended
metres per repeat. Basis is T=+X, B=-Z, N=+Y. Source counts/indices, area, winding,
UV derivatives, PNG pixels/metadata and manifest hashes pass ten new tests. OBJ
does not store tangent attributes, cameras or empty nodes; actual FBX conversion
must preserve/recompute and verify them. No FBX, KN5 or native track is fabricated.

This source uses `RV0L_TEST_PAD` / `RV0L_NORMAL_TEST` and candidate ksPerPixelNM
(SDK artifact present), with exact expected txDiffuse/txNormal and scalar/RGB
properties recorded as **unverified**. The MTL is preview material, not a native
shader assignment. Its diffuse is original RGB8 128 PNG with sRGB intent; its flat
DDS is an unchanged original Phase 0K candidate. All source/native/export flags
remain false. Phase 0K's old ksPerPixelMultiMap/RV0K selector does not match this
source and must not be enabled or automatically reused.

The source contract gives spawn/camera proposals, but track/container files,
collision conventions, native marker names and complete baseline are pending.
A KN5 alone is not a driveable track. Before native testing, establish a supported
original load container, verify ground clearance, source/FBX/exported hashes,
material inputs and exact owned configuration/precedence. Future validation must
cold-load the original, capture baseline, test neutral and +/-X/Y separately,
then detail only after orientation succeeds; end the owned session, remove only
reviewed resources and verify a fresh original load restores complete material
state. Section deletion/persistence/file equality alone is not loaded-state recovery.

The existing DCC/MCP-only policy still applies to authoring. Current offline
authorization prohibits application launches and GUI. A future owner-operated
interactive export or specific approved authoring integration/GUI policy exception
is required; ordinary CM/game GUI authorization is insufficient. Any approved
computer control must check actual weekday 08:00-17:00 America/New_York and allow
recovery time. This checkpoint grants no such permission and initiates no tool.

Previous 186 test definitions and all runtime code, shaders, Phase 0K assets and
existing reports are preserved. Ten additions give 196 definitions; 140 closeout
checks pass. Prior successful
GPU/historical suites were not unnecessarily repeated. All 29 protected files,
49 settings, nine previously reviewed sources, 13 inventory artifacts and the
approved untracked visual reference are checked unchanged. No installed rollback
is needed. Preserve original freeware assets; repository licensing stays unresolved.

Private evidence is under `.local/phase0l-20261104/`: preflight, tool-inventory,
SDK text/static-page extracts, final source tests and validation/Git receipts.
No proprietary SDK manual, screenshot, shader or binary is published. Source
manifest hashes and scoped Git attributes preserve exact original payload bytes.

Starting live allowance was 60% five-hour / 67% weekly. The checkpoint near
15 points read 46% / 65%: original source preparation is validated, remaining
export is authorization-blocked, and documentation/synchronization closeout
continues without research expansion. Read both meters anew on continuation,
retain milestone reviews and synchronization reserves, and keep the 5% weekly
hard cutoff. No deeper model or delegated review was used.

**Next action:** obtain the specific authoring authorization/integration, execute
the documented original source -> legacy FBX -> ksEditor -> KN5 roundtrip with
verified units/basis/material state, then reassess native readiness. Preserve
locked CSP/CM/Pure/Dream and Phase 0E HDR NO-GO throughout. Do not install new tools,
launch DCC/GUI or deploy this source automatically on continuation.

---

## Historical Phase 0K continuation handoff

Prepared 2026-11-04 on `phase0/foundation` from verified local/remote
`24d1ef8c3a2d110950af95a81ca49717a7d6fa42`. Read
[PHASE0K_MATERIAL_FIXTURE.md](PHASE0K_MATERIAL_FIXTURE.md) for the exact texture,
fixture, package and recovery contracts. The current tip plus final private Git
receipt identify closeout. Main remains `814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

**Native experiment NO-GO.** No original KN5 fixture or supported authoring/export/
loading workflow is established. `ksPerPixelMultiMap` / `txNormal` remains a
candidate, not a verified always-on normal material. The proposed original quad,
UVs and right-handed T/B/N are recorded in the package; they are not an exported
mesh. Native signs, alpha, mip/sampler behavior, effective baseline and cold-load
recovery remain unvalidated. No third-party asset or new KN5 writer fills the gap.

**Offline candidate/package readiness passes.** Six original 256x256 DX10 DDS
files contain nine mips each: flat, +/-X, +/-Y and periodic detail. Format is
R8G8B8A8_UNORM (28), signed normal encoded in RGB, every A byte 255, no roughness,
no sRGB transform. Alpha-mode metadata is zero for documented legacy D3DX
compatibility. Flat 128/128/255 has 0.317755-degree bias under the declared CPU
decoder. Max source quantization angle is 0.36510 degrees; direct analytic detail
base comparison is max/RMS 0.337558/0.183761 degrees. Unit normalization is offline,
not proof of native shader decoding. The Phase 0I moment generator/shaders are
unchanged; normalizing/packing loses their variance statistic.

Each texture chain is 349,524 pixel bytes plus 148 header bytes. Six DDS files
total 2,098,032 bytes; the ten-file public package totals 2,102,109 bytes. Logical
payloads are not physical VRAM or performance measurements. Independent existing
D3DX metadata parsing accepts all six with 256x256, nine levels and DXGI 28;
it creates no device, uploads no texture and establishes no CSP compatibility.

The original package is [examples/phase0k-normal-probe](../examples/phase0k-normal-probe/README.txt).
Its manifest SHA-256 is `1073f5b093d912eec82f15bf54227c918ba9ecdc43d743ac6db20aa8682026a4`.
All files match regeneration; scoped Git attributes preserve exact package
bytes. `disabled.ini` remains ACTIVE=0 with exact owned material/shader/slot
selection and flat as default. It has no shader swap, include or enabling command.
Changing a candidate needs a fresh reviewed run-bound package. Native eligibility
flags remain false. This is not an installer and grants no launch/deployment permission.

The new recovery command only writes fresh `.local/` simulations. Forty-five
file/commit interruption cases recover idempotently, preserving synthetic
baselines and retiring owned data as private evidence. Four additional guards
cover collisions, drift, unexpected content and interrupted retirement; eight
negative synthetic selections are rejected. Unknown files, links, wrong ownership,
missing baseline receipts and orphan journal updates stop automatic recovery.
No recursive deletion or live installation target is exposed. Filesystem recovery
is not material-state recovery: end an owned native session and verify a fresh
load against full original bindings/properties/flags before any native success claim.

All 26 new tests, five existing CLI tests and 17 existing moment/filter tests pass
(48 total). Original 160 test definitions, including the historical 124, remain
unchanged; the source inventory is now 186. No old shader/moment implementation
was modified. All 37 final static/preservation checks pass. All 29 protected files, 49 settings, nine reviewed sources and the
approved untracked reference are unchanged. No GUI, CM/game launch, DCC, graphics
device, rendering or installed-file modification occurred; no game restore is needed.

Reproduce with fresh ignored paths using `prepare-material-textures` then
`rehearse-material-recovery`; the report provides commands. Final private evidence
is `.local/phase0k-20261104/assets-b/`, `recovery-b/`,
`targeted-tests-final-v2.txt`, `cli-regressions.txt`, `moment-regressions.txt`,
`independent-dds-metadata.json`, `asset-cross-validation.json`, preflight and final
preservation/Git receipts. Superseded `assets-a/`/`recovery-a/` are retained only
for audit and must not be reused automatically. No broad CSP research is pending.

Live starting allowance was 81% five-hour / 70% weekly. The approximately
15-point review read 66% / 68%: the bounded implementation is productive and
complete, so formal closeout proceeds without scope expansion. Read meters anew
on continuation. Keep milestone reviews and synchronization reserves; the independent
5% weekly hard cutoff remains binding. No deeper model or delegated review was used.

**Next action:** establish a supported original fixture authoring/export/load
workflow or obtain an independently owned fixture with complete source/baseline
data, then verify its actual normal-slot contract. Prepare a fresh transaction
and obtain separate safety review/task authorization before any native flat/ramp
test. Do not bypass the fixture, use GUI fallback, enable this package or change
locked CSP/CM/Pure/Dream installations. Phase 0E HDR NO-GO, freeware and the
owner-undecided repository license remain intact.

---

## Historical Phase 0J continuation handoff

Prepared 2026-11-04 on `phase0/foundation` from verified local/remote
`d15d28f55d68bc5707cf8ca31686a0406653b4f8`.
Read [PHASE0J_MATERIAL_INTEGRATION.md](PHASE0J_MATERIAL_INTEGRATION.md) for the
capability/version matrix, evidence, inert example and cold-recovery gates.
The current Git tip plus the final private remote receipt identify closeout;
`main` remains `814f34e18f3f03fb5f03e11b43cabf78eb0ef4f1`.

**CONDITIONAL GO:** a future isolated normal-only texture assignment to one
original owned fixture with an already compatible built-in material shader.
This report grants no deployment/launch permission. Static material resource
assignment is documented; it does not execute our HLSL. Direct Phase 0I moment
packing, arbitrary original existing-object material HLSL, broad generic
application and hot-removal rollback remain NO-GO on present evidence.
Phase 0E HDR/canvas retirement NO-GO remains binding; Pure is untouched.

Installed app/track SDK declarations support material setters, uniqueness and
inspection. The 0.2.11 extracted WeatherFX SDK declares the older core methods;
its reviewed declarations lack preview's getTextureSlotDetails. Keep optional
metadata behind an adapter. Installed fuPBR templates expose normal RG/DXT5NM
and separate emissive/AO/metalness/roughness packing, but template presence does
not certify shader availability in build3898 or 0.2.11. Common configs can evolve
independently of the binary. Exact decoding, normals, mips and runtime costs
require native validation on each target release in authorized isolation.

Phase 0I signed normal moments / mean roughness^4 are not target-ready material
maps. Reuse the original surface model, then validate a target-specific encoding.
Normalizing/packing XY loses mean-vector variance; native filtering/BRDF and
anisotropy are not equivalent to the offline shader. No automatic roughness to
legacy specular-exponent conversion or per-material cap8 control is established.
No converter or second renderer was implemented. All 0G-0I source and 160 existing
test definitions, including the historical 124, are preserved.

Removal of SHADER_REPLACEMENT does not restore loaded values. Material dumps are
incomplete and can contain session-only texture IDs. resetSkin is not full
restoration; clone copies a reference; setMaterialsFrom shares state. Do not use
these as an undo transaction. Future testing needs exact owned paths, complete
effective baselines, collision/precedence checks, a workspace fault rehearsal,
then a separately approved session with cold-reload recovery verified before
expanding to one author-approved existing asset.

The original [configuration proposal](../examples/phase0j_material_proposal.ini)
has two ACTIVE=0 sections, exact future fixture selectors, no shader swap or
include and no supplied DDS files. It is not an installer. Production selection
must use reviewed asset profiles with hashes, material/shader/slot/flag checks,
match counts, UV/tangent validation, LOD/skin handling and skip-on-ambiguity.
Road/paint/rubber names are not eligibility proof. Gamma/LCS visual calibration
remains separate; no universal texture or in-game improvement is claimed.

This phase is documentation/static inspection only: no GUI, CM/game launch,
native renderer, material mutation or installed-file change. Targeted checks
cover disabled config, path/selector safety, declared evidence, local links and
preservation. All 29 protected files, 49 settings, nine reviewed sources and the
approved untracked reference match their receipts. No restore is required.
Private evidence: `.local/phase0j-20261104/preflight.json`,
`declaration-evidence.json`, `validation.json` and final Git/usage receipt.
Do not rerun the unchanged 0I GPU demonstrations to validate this report.

Starting live allowance: 93% five-hour / 72% weekly. Closeout reading: 84% / 71%.
The former 12-point cap remains revoked. Read meters anew, review after about
15 five-hour points of future work, and retain synchronization reserves and the
independent 5% weekly hard cutoff. No deeper model or delegated review was used.

**Next milestone:** prepare the original owned fixture's exact material/encoding
contract and a workspace-only recovery rehearsal, then obtain review/authorization
for the bounded native normal-orientation and cold-reload experiment. Preserve
locked CSP preview361/build3898 and CM 0.8.2913.40776, original assets, freeware
policy, unresolved repository license and all Phase 0E constraints.

---

## Historical Phase 0I continuation handoff

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
