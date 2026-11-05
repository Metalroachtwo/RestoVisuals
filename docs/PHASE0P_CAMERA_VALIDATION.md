# Phase 0P: camera control evidence and foreground-access blocker

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
