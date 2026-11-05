# Phase 0P: repeatable camera, native normal sampling and original KN5

## Resumed result — 2026-11-05

Resumed from local/remote `cecd6448dd0920ea2aaf9d8afed18546f820b8b5` after the
owner's foreground-readiness reply. **The visible-pad gate now passes.** Two fresh
owned editor sessions reproduced the full original pad from above. Signed-X
normal inputs produced distinct shading through `ksPerPixelNM`, and returning
the flat input restored the captured viewport exactly. One original Track KN5
was exported after a fresh file-only safety GO. **It is not load-validated.**

Read the [resumed receipt](../examples/phase0p-camera-validation/resumed-observations.json),
[native image comparisons](../examples/phase0p-camera-validation/native-sampling.json)
and [directional DDS checks](../examples/phase0p-camera-validation/directional-dds.json).
The earlier blocked attempt is retained below as history, not current status.

### Repeatable camera and visible material

The owner had opened the installed SDK editor. That session was left untouched;
the tests used the existing verified isolated SDK mirror and a new working copy
of the same hashed FBX. No Blender export, source geometry edit or stack change
was performed. The actual `RV0L_TEST_PAD` mesh was identified by single selection:
two triangles, position 0,0,0, scale 1,1,1, radius 8.485281, and the original
`RV0L_NORMAL_TEST` material. Selecting the scene root clears its pink highlight.

At the tested 1936x1048 editor window, the repeatable sequence was:

1. Open the unchanged FBX; Load Weather `3_clear`, then Load PPfx `default`.
2. Keep FOV 60 and the initial mouse-speed control unchanged. Click empty viewport.
3. Send one Ctrl+Page Up down/up pair held 120 ms.
4. Left-drag vertically +90 pixels, from window-relative `(1100,400)` in ten steps.
5. Select Scene Root without double-clicking the mesh; left-drag another +60 pixels
   from `(1100,400)`, again in ten steps.
6. Verify full pad framing and the resulting position label `(0,30,0)`; the View
   label was `(0,-18.648300,-23.499810)` in both sessions.

The complete pad silhouette and neutral material are distinct from the background.
The camera is above the unchanged +Y-facing source plane. Display labels are
reported as observed; their complete matrix/direction semantics are not inferred.
Timed key motion can depend on rendering/input timing: verify the resulting pose
on another host rather than promising frame-independent movement distances.

The two independent viewport interiors `(352,62)..(1869,758)` are exactly equal in
captured 8-bit RGB: all difference-channel extrema are zero. These are display
screenshots, not native floating-point readbacks or in-game stability measurements.
Private captures: `s2-final-camera.png`, `s3-final-camera.png`.

Programmatic foreground activation was still unreliable. A scoped fallback was
validated: raise only the owned window without activation, verify its title-bar
hit-test belongs to the owned PID twice, click that title bar, then verify foreground
ownership before any further input. It checks the owned executable, date/window
and held modifiers; it sends no input to other apps and grants no persistent
provider permissions. Raw diagnostics stay private. No repeated focus investigation
is needed when this already validated task-scoped route is applicable.

### Native sampling and restoration

Only after the fresh-session repeat passed, the existing adapter represented the
original Phase 0K +X/-X DDS files in the already validated legacy container. Each
349,652-byte output preserves every original RGBA texel across all nine mips;
independent per-word mask decoding passed. R/G/B/A masks remain
`ff/ff00/ff0000/ff000000`, little-endian word `0xAABBGGRR`; no compression,
channel reorder, gamma conversion or normal-vector change occurs.

Flat, +X, -X and returned-flat captures used the same camera, geometry, UVs,
lighting, diffuse texture and all 12 material properties. Persistence confirms
the only non-header change was the `txNormal` resource filename. Reload opens an
information dialog; it must be dismissed before capturing. The initial dialog-
occluded frame was retained privately and excluded from all image comparisons.

| Input | Mean display RGB, pad interior | RGB MAE from flat | Maximum channel difference |
|---|---|---|---|
| Flat | 244.438, 240.250, 232.365 | 0 | 0 |
| +X | 248.875, 245.905, 239.894 | 5.874 | 11 |
| -X | 221.289, 214.526, 203.742 | 25.832 | 84 |
| Returned flat | Same as flat | 0 | 0 |

The 49,844 interior pixels exclude the fixed axis overlay. Signed inputs produce
distinct shading across the six source U repeats, consistent with the expected
U/+X basis. This is positive **native normal-texture sampling evidence**, beyond
metadata or reload messages. Absolute world-light direction, green-axis sign and
complete RGB-to-TBN decode calibration remain unverified; no full tangent-handedness
or radiometric correctness claim is made. No artistic detail map was applied.

The returned-flat **entire viewport interior** exactly matches the baseline RGB,
and all original material/mesh values were restored. Private matched captures are
`s3-final-camera.png`, `matched-x-positive.png`, `matched-x-negative.png` and
`matched-flat-return.png`. Their hashes and numerical scope are in the receipts.

### Original KN5 export and remaining gates

The fresh review checked original ownership/hashes, live source counts and
transforms, supported authoring/basis evidence, shader/slots, sampling, flat
restoration, backups and an unused output destination. Its **GO covers one private
file save only**. File > Save KN5 offers Car, Car (No Textures), Track and Car
(Experimental); the ordinary **Track** route was used. Menu navigation needed
an explicit path into the submenu; early navigation/control-name checks did not
invoke an exporter or create files. No alternate exporter was tried.

The native Save As dialog saved `rv0p_original_pad.kn5` to the reviewed ignored
`kn5-export/` directory and reported success. The actual file is **350,981 bytes**,
SHA-256 `cc4285989205597824750c9871c44f7eeace384b02ef026dbf472fc9ea4d28fd`.
A separate private backup is byte-identical. No KN5 writer, patcher or parser was
constructed. The serialized mesh/texture counts were not independently inspected;
source counts and the successful save do not establish load/runtime compatibility.
No reviewed KN5 reopen method was available through the inspected editor menu.

**In-game integration remains NO-GO.** The fixture still needs supported KN5 load
validation and a separately reviewed original container/spawn/collision/cold-load
plan. The existing Phase 0E HDR NO-GO is unchanged. ksEditor used a built-in shader
with original texture inputs; no RestoVisuals HLSL or CSP replacement was deployed.

### Closeout

Both resumed owned sessions closed normally with exit 0, the last at **10:54:23
America/New_York**. Original heavy-fog/b&w preview values were reloaded, and the
working persistence was restored to its immutable input. The owner's installed
editor remains open and untouched. No game launch or installation change occurred.

All **29 protected files**, **49 settings**, **25 original/backup pairs**, **839
installed SDK files** and **839 reused-mirror files** match fresh baselines. All
four original working inputs are restored/verified. The SDK generated a 136-byte
`NULL.dds` placeholder only in the owned project; it and all raw exports/screenshots
remain private. No SDK/proprietary asset is added to Git.

**15 affected tests pass** (five DDS adapter, ten fixture-source), zero failures.
All 201 existing test definitions, including the historical 124 baseline, remain
unchanged; the full suite was not rerun. The two new public diagnostic files are
original RestoVisuals data with lossless container changes, not new shader code.

Resumed live meters started at **41% five-hour / 50% weekly**. The camera repeat
checkpoint read 36%/49%; after sampling, 30%/48% supported the bounded file-only
export. Formal closeout began at **23%/47%** with all native work finished. Final
balances/synchronization are recorded privately. No model escalation/delegation
occurred; the approximate 15-point closeout reserve and weekly 5% cutoff remain.

Next: **supported KN5 load validation under a separately reviewed isolated fixture
plan**, retaining the remaining channel-orientation and game-container gates.
Freeware policy, unresolved licensing, locked stack and unchanged main persist.

---

## Initial attempt — historical foreground-access blocker

2026-11-05. Starting local/remote `phase0/foundation`:
`d7e3c1707ecf32e6964583ba0095f5c74e9de50f`.

**BLOCKED before a repeatable full-pad view.** After viewport focus and one
delivered Page Up key event, the displayed camera position changed from `(0,0,0)`
to `(0,0.15,0)` and a narrow surface edge was visible at the bottom. Subsequent camera input
was withheld because the owned editor could not obtain foreground ownership.
The primary acceptance gate is incomplete; normal sampling and KN5 remain NO-GO.
This is an access/routing blocker, not evidence that the other camera controls,
geometry or normal texture failed.

## Preserved inputs and fresh session

One fresh owned ksEditor process reused the existing verified Phase 0O SDK
mirror. No SDK copy, Blender launch, FBX export or DDS conversion was performed.
The original FBX was copied into a new owned project directory, retaining all
19,260 bytes and SHA-256
`49e1dc29e3e2ff976995d67e0bceaaca038e57443885814c72ea48e65ab2b474`.
The unchanged legacy flat DDS retains SHA-256
`1ead2f733f73ab1abff72f48267acdf794efbc1291165468df875081055e1460`.

Fresh scoped backups and hashes covered 29 protected files, 49 settings, 25
original/backup pairs and the four owned project inputs. Installed and reused
SDK inventories each matched all 839 reviewed files before launch. No existing
Blender/ksEditor/game session was active during the initial host check.

## Recorded operations and actual controls

Raw captures and operation receipts remain under the ignored
`.local/phase0p-20261105/evidence/` directory. The sanitized
[result receipt](../examples/phase0p-camera-validation/observations.json) records
capture hashes and gate states. No screenshots, application titles from unrelated
programs, private configurations or raw exports are published.

| Delivered operation | Result / private evidence |
|---|---|
| File > Open FBX, using the unchanged original working copy | Fresh scene, FOV 60; `s1-00-fbx-loaded.png` |
| Illumination: select `3_clear`, press Load Weather; select `default`, press Load PPfx | Colored sky as established in Phase 0O; `s1-01-clear-default.png` |
| Click empty viewport to focus, then deliver one Page Up down/up pair, held for 600 ms | Position label becomes `0.000000; 0.150000; 0.000000`; View becomes `0.000000; -0.150000; 0.000000`; narrow surface edge appears; `s1-02-pageup.png` and `s1-02-pageup-state.json` |

The original FOV remained **60**. The single injected key-down did not generate
a stream of keyboard-repeat events. The measured result is one 0.15-unit label
change, not a validated movement speed in metres/second. The physical meaning of
every View-label component is still unverified; a direction/target contract is
not inferred from these strings.

The proposed next operation was Ctrl+Page Up followed by a bounded left-drag.
Foreground verification rejected it **before key or mouse input was sent**.
Consequently left-drag rotation, arrows, Page Down, Shift precision, Ctrl speed
and wheel/FOV behavior remain **untested**, rather than disproven. No scene-tree
double-click was used. No second session or equivalent-view reproduction occurred.

The cached installed Kunos pipeline guide documents Illumination, project layout
and persistence, but the inspected editor section did not establish these key
bindings. Its linked [official editor thread](https://www.assettocorsa.net/forum/index.php?threads/ac-editor.10964/)
returned the forum index during this bounded lookup, not usable control
documentation. The supplied Phase 0P controls were treated as test instructions;
only the delivered Page Up behavior is validated locally. No broad SDK research
or alternative navigation system followed.

## Exact interruption and bounded inspection

After the first camera result, an unrelated application was foreground. Normal
owned-window activation did not grant foreground ownership. An owned-window
restore request also returned no foreground ownership. A direct accessibility
focus call reported that the top-level target could not receive focus; the
specific owned viewport did not advertise keyboard focusability, so no focus
action was invoked on it. No keys/mouse actions were sent to the unrelated app,
and no input-routing bypass, process termination or system setting was used.
The underlying reason Windows refused activation was not established.

A request to bring the existing owned editor forward remained unanswered during
the run. Further focus troubleshooting stopped. The editor has since been closed;
that foreground request no longer refers to a live window.

One bounded read-only inspection confirmed the unchanged source plane spans
X/Z -6..6 at Y=0, with geometric N=+Y, tangent +X, bitangent -Z and UVs 0..6.
The prior imported two-triangle/bounds findings were reused, not re-exported.
Persistence retains the one `RV0L_NORMAL_TEST` material, `ksPerPixelNM`, its
12 properties, `txDiffuse` slot 0 and legacy-flat `txNormal` slot 1. Mesh
ACTIVE/VISIBLE/RENDERABLE/CAST_SHADOWS remain 1. No source winding, geometry,
UVs, shader, material coefficients or light direction was changed.

The edge is consistent with the original surface becoming visible after vertical
movement, but its full silhouette, live mesh identity, visible face and diffuse
sampling were not jointly established. It is not sufficient for the visible-pad
gate or a native orientation claim. Flat/+X/-X captures were not attempted and
no additional DDS was generated. No export-safety GO, KN5 save, game launch or
material deployment occurred.

## Recovery and verification

The owned editor received a normal close request and its launch-parent witness
reported **exit code 0**; closure was verified at **09:49:59 America/New_York**.
The unrelated foreground application was untouched. No forced termination or
Save Data operation was used. The in-memory preview/camera session ended; no
visual camera rollback or fresh-session reproduction is claimed.

Post-close verification found:

- All **29 protected files** and **49 settings** unchanged, with fresh backups intact.
- All **25 original/backup pairs** verified, including source assets and visual target.
- All **839 installed SDK files** and **839 reused-mirror files** unchanged, with
  exact inventories; the pre-existing exception log also remained unchanged.
- All **four owned project inputs** restored/verified. Final persistence had no
  value differences from its input, including its header. No fixture KN5 exists.
- **10 affected fixture-source regressions passed**, zero failures. All 201
  existing test definitions, including the historical 124 baseline, are preserved;
  the entire suite was not rerun for this evidence/documentation change.

Live allowance started at **52% five-hour / 52% weekly**, read **47% / 51%** at
the interrupted-work checkpoint and **45% / 51%** at formal closeout. The run
stopped well before the approximately 15-point review because access remained
blocked. Final balances and local/remote synchronization are recorded privately.
The approximately 15-point closeout reserve and weekly 5% cutoff were preserved.
No model escalation or delegation occurred.

## Next prerequisite

**Resume camera recovery in a fresh owned editor with confirmed foreground access.**
Reuse the existing SDK mirror, unchanged FBX/flat DDS and clear/default Load
sequence. Starting at FOV 60, verify short vertical and left-drag movements, frame
the pad's +Y-facing side and reproduce an equivalent view in another fresh owned
session. Only then proceed to fixed-state flat/+X/-X normal sampling and a fresh
export review. Obtain fresh allowance/time checks; today's GUI exception still
ends at 17:00, with cleanup by 16:30.

Game deployment remains separately gated. Phase 0E HDR NO-GO, Phase 0J cold-load
restrictions, locked versions, permanent freeware and owner-undecided repository
licensing remain unchanged. No texture-format or export rework is justified by
this foreground-access failure.
