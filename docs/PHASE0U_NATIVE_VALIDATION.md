# Phase 0U native follow-up: replay loaded and live materials identified

2026-11-05. Starting verified local/remote `phase0/foundation`:
`2776389247e2c1df7ae3d9dd7a365c139d3c58de`.

**One replay launch through the existing CM session succeeded.** The original
Lexus/Drift Mansion replay rendered, paused baseline captures were collected,
and CSP Objects Inspector identified two actual track materials and resources.
Native Exit completed with **code 0 at 18:43:07 Eastern**. No normal-map comparison
was activated: the observed shader families and unresolved ownership/encoding
gates do not justify replacing an authored resource. Phase 0E HDR remains NO-GO.

This is the separately owner-authorized after-hours continuation of
[offline preparation](PHASE0U_REPLAY_MATERIAL_PREPARATION.md), not a claim that the
earlier offline run used desktop access. The permission was limited to tonight,
with credit closeout reserves; the date guard did not permit carrying access into
another day. The owned GUI helper is now disabled. No creative app was operated,
Steam restarted, reset consumed, component updated or third-party asset overwritten.

Read [sanitized observations](../examples/phase0u-native-validation/observations.json).
All 32 original captures, replay references, logs, current-state copies and receipts
remain ignored under `.local/phase0u-native-20261105/`. No screenshot, proprietary
texture, shader source, raw configuration or account label is published.

## What executed

Fresh backups covered 29 protected files, 49 selected settings, 261 previously
reviewed readable user configuration files and three runtime files. Both named
WebBrowser/odometer state files had fresh pretest hashes for **this run**. Known
car/track manifests were verified (1,265/386 files), as were 25 original sources.
Initial workspace copy recovery was rehearsed before launch. Existing owner CM,
Steam and ksEditor identities were preserved; no game was already running.
The unchanged stack is CSP **0.3.0-preview361/build3898**, CM **0.8.2913.40776**,
configured **Pure Gamma 3.50** and **Dream Realism 7.3 Gamma** PP.

The existing CM **Media → Replays** page selected the exact Phase 0T autosave.
Its hash remains
`d447417fef436d8993c22c18a030560654215aa43bb7a9a35f98b0e8ae5c2d8f`,
5,559,241 bytes, matching the original and private copies. Installed CM displayed
Lexus RC-A / Drift Mansion Open, **4 minutes 33 seconds**, version **16**, one car,
recording quality **66 Hz**, time 13:06 and **Thunderstorm (Sol)**. Displayed duration
and quality do not establish exact frame count or recording interval.

CM's native **Play** control launched the reviewed game at **18:25:46 Eastern**.
The scene loaded successfully. Native replay controls paused it; one camera-arrow
step selected **Chase 1**, displayed index **2**, car **0**. A stationary timeline
click at client `(475,997)` selected displayed **0:09** rather than the proposed
0:10. This is the actual reference; no exact frame index or numeric camera/FOV
pose was exposed or certified. F1 did not establish the replay camera selection.

At 1920×1080, move the pointer away from the controls, wait three seconds, capture
A; wait two seconds, capture B; repeat the same paused timeline click, pointer
position and three-second settling delay for the reseek witness. Close inspection
overlays and capture a final unchanged witness. No driving input, weather, exposure,
physics, material coefficient or rendering-quality setting was changed.

The native view is visibly clear despite CM's replay weather label. Configured
Pure Gamma/Dream Realism and the earlier T configured-versus-observed weather
distinction remain intact; replay weather/exposure/animation determinism is not
established by that appearance. No cold second replay launch was performed.
Startup also logged missing optional Python-app files and TrackIR warnings.
Those were preserved without repair; this is not a clean-resource certification.

## Measured baseline repeatability

The comparison decodes retained PNGs through the existing System.Drawing runtime
and measures **8-bit screenshot RGB code values**, not radiance or HDR values.
Self-comparison returns zero. No blur, crop, image adjustment or fitted tolerance.

| Compared with A | Mean absolute RGB difference | RGB RMSE | Maximum channel difference | Changed RGB pixels |
|---|---:|---:|---:|---:|
| Paused B, two seconds later | 0.337517 | 0.893661 | 68 | 879,283 |
| Same paused timeline seek repeated | 0.258196 | 0.762213 | 52 | 737,102 |
| After closing read-only inspection | 0.359040 | 0.965815 | 60 | 939,336 |

Each image has 2,073,600 pixels. **None of the paired captures is pixel-identical**;
no tolerance-equivalence threshold was specified or passed. The UI/time/camera
procedure was repeated within one load, while exact frame, numeric pose and
cross-load reproducibility remain unverified. Do not call this a deterministic
enhancement-comparison baseline yet. The measurements establish an observed
noise/difference level, not its cause or perceptual acceptability.

The window captures also contain a few nonopaque pixels: three in A, five to seven
across the compared pairs, with four to six changed-alpha pixels. Capture alpha
is therefore not certified uniformly opaque. This is not a measurement of an HDR
source texture or proof that a material shader changed alpha. No GPU draw-time,
FPS, upscaling or photorealism improvement is claimed.

Python's optional Pillow decoder was absent. Initial drawing-library references
were incomplete; explicit references to the existing drawing/runtime dependencies
resolved the analysis. A legacy PowerShell script attempt was refused by its
authorization manager and was not bypassed. No tool install, policy, unblocking
or system change was made to obtain the final measurements.

## Actual native material observations

Objects Inspector was already enabled. The supported app sidebar's **Objects**
filter exposed its Developer Apps entry; no app installation or setting enablement.
Only Alt-click selection, scene-tree expansion and read-only Details/Textures/Vars
tabs were used. No property values were dragged, edited or reloaded.

| Item | Pale ground selection | Road selection |
|---|---|---|
| Mesh | `1GRASS0_CENTRAL` | `tracksurface` |
| Material | `map_center` | `asphalt` |
| Shader | `ksMultilayer` | `ksMultilayer_fresnel_nm` |
| Origin shown in Details | `dm_land.kn5` | `jd_drift_mansion.kn5` |
| Triangles displayed | 10,144 | 14,090 |
| Resource/variable counts | 6 textures / 15 vars | 7 textures / 23 vars |
| Flags shown | Opaque, not transparent; front culling; normal depth | Same |
| Normal-related binding | No `txNormal` in the displayed six-slot list | `txDetailNM=tarmac-detail_NM.dds`; no conventional `txNormal` in the seven-slot list |

The pale ground at the first probe was **not the authored `concrete` candidate**.
The terrain's slots are diffuse/mask and detail R/G/B/A layers. Its appearance
cannot justify a normal assignment intended for `ksPerPixelNM_UVMult`.

Road variables include `detailNMMult = (30,4)`. The selected road mesh has an AABB
about **166×7.65×286 m**, and its geometry preview spans much of the track.
One selected mesh is not proof of a unique global material/resource match.
Texture Source labels identify the track KN5 model; embedded resource bytes,
native resource view format and global sharing were not independently dumped.

The bounded scene hierarchy read reached CSP's optimized chunk nodes, including
2,643 children in one branch. It was not traversed exhaustively. `concrete` was
not located or certified. Normal channel decoding, tangent/bitangent handedness,
UV scale semantics, material sharing/counts and effective root/skin/include
precedence remain unresolved. A geometric normal shown for a picked point does
not establish the normal map's tangent-space orientation.

**Normal comparison: NO-GO.** The prepared conventional normal is not a verified
drop-in for either observed family. No `RESOURCE_FILE`, shader replacement,
property adjustment, guessed packing, injector, original-normal removal or
installation transaction was attempted. There are no enhanced captures or
claims of original/enhanced/restored material validation. The final image is an
unchanged post-inspection witness, not a shader-restoration experiment.

## Recovery and final known-good state

The inspector opened by this run was closed, followed by native replay Exit.
The game exited normally, code 0. CM was returned to its original Drive page;
car/paint/track/layout/skin, Pure, 13:06, 13.5°C, Optimum, wind and original assists
remain visibly intact. CM and the owner editor remain open; Steam was not restarted.

Four changed files were restored from fresh verified backups with pre-copy hash
guards and post-copy verification: race input, CSP ImGui/inspector/taskbar state
and the two runtime logs. All generated versions were archived first. The complete
four-file workspace copy rehearsal and interrupted-copy resume passed; a synthetic
sentinel was preserved. This is not a material-transaction fault suite or an
atomic/exclusive-writer guarantee.

Two deliberate recovery limits remain:

- **48/49 selected settings match**: CM's live preference store is retained under
  the owner's keep-session-open decision, with before/after versions preserved.
- **260/261 freshly backed user configuration files match**: WebBrowser state
  changed one opaque stored value. It was not edited by the agent, and attribution
  was not established. Its current data and fresh pre/post copies were retained
  rather than overwriting uncertain state. Odometer state is unchanged.

The other 36 configuration filenames match the previously documented auxiliary
exclusion names. Their current contents were not certified; no permissions changed.
Fresh U snapshots do not retroactively close T2's historical pretest gaps. Complete
user-state rollback is not claimed.

Final hash checks pass for **29 protected files, 1,265 car files, 386 track files,
13 shared configurations, both 839-file SDK sets and 25 original sources**.
All six reviewed external configuration candidate paths remain absent.
Original/private replay hashes remain unchanged. No original mod asset, protected
binary, reference image, shader or existing test definition was modified.

## Validation, credits and continuation

Seven closeout validation groups passed, covering native replay load/normal exit,
actual inspector bindings,
decoded image comparisons, four-file recovery rehearsal/verification, preservation,
public links/privacy and Git state. The 31 targeted existing tests passed in the
immediately preceding offline U checkpoint; they were not needlessly rerun for
this native evidence/documentation change. All 201 definitions, including the
historical 124, remain unchanged. No full suite, shader deployment or game
performance benchmark was run.

Live allowance began **60% five-hour / 27% weekly**. At the productive checkpoint
it read 47%/25%; closeout was underway at 39%/24%, ahead of the 15%/10% reserves.
Final readings/SHA are retained privately. Both reserved resets remained available;
none was invoked. Main, freeware, locked versions and undecided licensing persist.

**Highest-value next milestone:** resolve the observed asphalt shader's
`txDetailNM` channel/UV contract and a method that preserves authored normal data,
using this exact native binding as evidence. Keep deployment NO-GO until that,
material sharing, config registration/precedence, a complete fresh transaction and
baseline repeatability criteria are verified. A future native session needs its
own authorization; this completed night's access is not a standing approval.
