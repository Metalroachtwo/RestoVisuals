# Phase 0O: ksEditor preview recovery and sampling gate

2026-11-05. Starting local and remote `phase0/foundation`:
`092625e2669f0f10a6afbdb8c8f15c2934c39a06`.

**Partial preview recovery is confirmed; material sampling and KN5 remain NO-GO.**
Loading `3_clear` through the Illumination tab recovered recognizable sky/cloud
structure. Loading `default` PPfx then recovered color. The original test pad and
its diffuse texture were still not identifiable. A bounded scene-tree interaction
subsequently produced a black preview. No directional-normal experiment, new DDS,
KN5 save, game launch or installed material change followed the failed preview gate.

This advances the blocker beyond Phase 0N: the owned editor does render a colored
sky, and its weather/PP load controls affect the preview. It does not establish a
usable camera view of the imported surface or correct `txNormal` sampling.

## Inputs and scope

The existing original Phase 0M FBX was reused, without opening Blender or exporting
again. Its 19,260 bytes retain SHA-256
`49e1dc29e3e2ff976995d67e0bceaaca038e57443885814c72ea48e65ab2b474`.
The original Blend/OBJ, Phase 0K package, original DX10 DDS and Phase 0N candidate
remain unchanged. Phase 0N's header investigation was not repeated.

The normal input was the existing
[legacy flat DDS](../examples/phase0n-dds-compatibility/flat-legacy-rgba8.dds),
349,652 bytes, SHA-256
`1ead2f733f73ab1abff72f48267acdf794efbc1291165468df875081055e1460`.
Its earlier metadata recognition remains the result recorded in
[Phase 0N](PHASE0N_DDS_COMPATIBILITY.md); this phase does not promote that result
to resource-decoding or shader-sampling validation.

One new owned SDK mirror was copied from the verified Phase 0N mirror after
checking all 839 files. The installed editor, prior mirror and current mirror
all retain the reviewed bytes. The executable is the existing 512,000-byte
ksEditor 1.0.0.0, SHA-256
`820a1c5de8b64074e3d32cdf1a377238da3a3e0480d03070ffa35ba98e6c122e`.
The current mirror was launched in one isolated owned session. No other Blender
or ksEditor session was active at launch; no other application was operated.

The Kunos SDK pipeline manual remains the source for the `texture` project folder,
FBX import and Save Persistence/Save KN5 workflow. The preview controls and results
below are **observed locally**, rather than inferred from that general manual.
No undocumented exporter, custom shader, binary patch or replacement tool was used.

## Controlled preview sequence

Raw screenshots remain under the ignored
`.local/phase0o-20261105/evidence/` directory. Public
[capture receipts](../examples/phase0o-editor-preview/capture-receipts.json)
record their filenames, hashes and bounded display-image measurements;
[editor observations](../examples/phase0o-editor-preview/editor-observations.json)
record the decision and preserved state. No application screenshot or private
configuration is published.

| Step | UI action and state | Visible result / evidence filename |
|---|---|---|
| Baseline | Load the unchanged FBX and prior verified material persistence | Uninformative gray viewport; `00-original-material-viewport.png` |
| Inspect defaults | Utilities > Data Editor: default weather `1_heavy_fog`, default PP `b&w`; close without Save Data | Defaults inspected only; `00-data-editor-defaults.png` |
| Inspect preview | Illumination tab: weather `1_heavy_fog`, PPfx `b&w` selected | Original illumination grid captured; `00-illumination-panel.png` |
| Select clear | Select supported `3_clear` in Illumination, before Load Weather | Preview remains monochrome; `01-clear-selected-not-loaded.png` |
| Apply clear | Press **Load Weather**, leaving PP `b&w` | Recognizable monochrome sky/clouds and changed illumination values; `02-clear-weather-loaded.png` |
| Select PP | Select supported `default`, before Load PPfx | Still monochrome; `03-default-pp-selected-not-loaded.png` |
| Apply PP | Press **Load PPfx**, retaining loaded `3_clear` | Blue sky/colored clouds; no identifiable pad; `04-default-pp-loaded.png` |
| Bounded framing check | Select Scene tab and double-click the actual `RV0L_TEST_PAD` mesh leaf | Black viewport; gesture's camera/framing semantics unverified; `05-selected-pad-framing.png` |
| Recovery check | Reload the same clear weather without changing material values | View remains black; `06-preview-after-weather-restore.png` |
| Cleanup | Reload original `b&w` PP and `1_heavy_fog` weather, then close the owned editor normally | Original illumination values/selectors restored; black viewport persists until close; `08-preview-settings-restored.png` |

Selecting an item is not treated as applying it. The explicit **Load Weather**
and **Load PPfx** buttons provide the active-change witnesses. Data Editor's
default selectors were not edited/saved. The copied `cfg/race.ini` named
`5_light_clouds`, while these UI selectors initially named `1_heavy_fog`; the
file alone did not establish active illumination. Neither source game weather
nor Pure/PP configuration was changed.

For the display-only viewport interior `(352,62)..(1869,758)` in 1936x1048 captures,
the fraction of pixels with `max(abs(R-G), abs(G-B)) > 2` was 0 before loading the
default PP and **0.88418233** afterward. The post-tree-interaction interior was
all RGB zero. Dialog-overlapped captures are excluded from this measurement.
This corroborates visible chroma/blackness, not correct material rendering.
Cloud animation/capture time were not controlled, so these are not pixel-matched
neutral-pass images or a quantitative exposure/normal comparison.

## Effective illumination and camera evidence

These are displayed values after the relevant Load button, not a newly inferred
lighting/color-space contract. Selecting `3_clear` does not mean cloud cover zero.

| Illumination property | Original / restored | After loading `3_clear` |
|---|---|---|
| AmbientHigh | 5.929412, 6.352942, 6.564706 | 4.529412, 4.529412, 4.529412 |
| AmbientLow | 6.27451, 5.882353, 5.490196 | 8.752942, 8.752942, 8.752942 |
| Angle | 40 | 40 |
| CloudColor / CloudCover / CloudCutoff / CloudOffset | 0.3 / 0 / 0.69 / 0 | 0.7 / 0.9 / 0.5 / 0 |
| FogBlend / FogLinear | 1 / 2000 | 0.85 / 9000 |
| FogColor | 4.25, 4.25, 4.25 | 1.8, 2.37, 3.42 |
| HorizonHigh | 2.572549, 2.572549, 2.572549 | 2.058824, 2.333333, 3.019608 |
| HorizonLow | 2.250981, 2.250981, 2.250981 | 1.9, 1.028235, 0.253333 |
| SkyHigh | 2.250981, 2.250981, 2.250981 | 0.3529412, 0.8588236, 1.964706 |

The separate angle-slider label stayed 50; zenith and azimuth sliders stayed in
their initial positions and the three Shadow Bias fields stayed zero. No light
direction, material coefficient, exposure, geometry or UV edit was attempted.
The loaded PP changed visible color without changing the displayed weather grid.

The viewport FOV display was 60. `View` and `Pos` displayed
`0.000000;0.000000;0.000000` throughout the inspected states. A narrow UI inspection
of those two fields returned Pane elements with no ValuePattern setter. This
does **not** prove that the actual camera was at the origin or had a zero direction;
their telemetry semantics/update behavior remain unknown. No verified numeric
camera pose or reproducible supported framing operation was established.

The View menu exposed Display Axis, Scene/Material/Tools on Form and TopMost Forms;
it supplied no camera-reset command in the inspected menu. The bounded investigation
stopped without speculative key sequences, render-setting changes or material edits.
The black view after the tree double-click is an observation, not a diagnosis of
an engine fault, hidden mesh, backface issue or texture-decoding failure.

## Material compatibility and export decision

The before/after supported Save Persistence files have identical section sets
and all values except header DATE/MD5_HASH. In particular:

- One `RV0L_NORMAL_TEST` material retains `ksPerPixelNM`, `eDepthNormal`, opaque
  rendering, alpha blend/test 0 and all 12 property records.
- `ksAmbient=0.2`, `ksDiffuse=0.6`, `ksSpecular=0`, `ksSpecularEXP=10`,
  `ksEmissive=0,0,0`; the prior remaining zero-valued channels are unchanged.
- `txDiffuse` slot 0 remains `neutral_diffuse.png` (reported 32x32), and `txNormal`
  slot 1 remains `flat-legacy-rgba8.dds` (reported ARGB, 256x256).
- Existing mesh ACTIVE/VISIBLE/RENDERABLE/CAST_SHADOWS flags and all other
  persisted values remain unchanged. Earlier Phase 0M geometry, scale, UV and
  analytic tangent findings are preserved, not re-exported or revalidated in DCC.

Diffuse sampling is **UNKNOWN**: neither the pad silhouette nor its texture was
positively identified. Normal sampling, native channel decode/orientation and
tangent behavior are also **UNKNOWN**. Successful metadata reporting and the
colored sky do not answer these material questions.

**NO-GO for directional sampling, KN5 export and the next in-game material test.**
The prerequisite informative material preview failed. No +X/-X conversion was
performed, no matched diagnostic set was fabricated, no second illumination
direction was tried, and no export review GO was issued. There is no new fixture
KN5 or output hash. The six existing axis/sphere KN5 files in the SDK mirror are
unchanged SDK tool resources, not fixture exports.

Rejected hypotheses/claims: weather/PP selectors alone prove active state;
header recognition proves shader sampling; restoring sky/color necessarily makes
the pad visible; a scene-tree double-click supplies a verified camera pose;
black output proves DDS failure. The evidence supports none of those claims.

## Recovery, checks and known-good state

Original weather/PP selectors and displayed illumination values were restored
through their Load buttons. This did not recover the pre-framing sky pixels;
no visual camera rollback is claimed. The failed transient session was then
closed normally, with launch-parent exit code **0**, verified closed at
**08:48:13 America/New_York**, well before the 16:30 cleanup/17:00 deadline.
No force termination or preference Save Data action was used.

The owned final persistence was retained privately as evidence, then the working
INI was restored byte-for-byte from its fresh backup. Fresh post-close checks:

| Preservation check | Result |
|---|---|
| Protected files / selected settings | 29/29 and 49/49 unchanged |
| Scoped original files and their fresh backups | 25/25 pairs verified |
| Installed SDK / prior Phase 0N mirror / current owned mirror | 839/839 each, exact inventory and hashes |
| Owned SDK additions or modifications | Zero |
| Private pre-existing exception log | 22,600 bytes, unchanged hash; no new fault witness |
| Original FBX / owned flat DDS / diffuse / visual reference | Retained unchanged |
| Working persistence | Restored to immutable input |
| Game launch / native material change / fixture KN5 | None |

The known-good installation, locked CSP/CM versions and Pure/Dream assets remain
unchanged. This editor cleanup is not an Assetto Corsa material cold-reload test.
The next editor session must establish framing independently; the current result
does not make this preview production-ready.

Ten affected `test_fixture_source.py` regressions pass with zero failures. All
201 existing test definitions and code/assets remain unchanged, including the
historical 124-test baseline. Those 201 tests were not all rerun; no rendering
implementation changed. All 58 closeout checks pass, covering policy/history retention, receipt
hashes, false readiness flags, links, privacy, ignored evidence and Git whitespace.

Live allowance began at **69% five-hour / 55% weekly**. Formal closeout was already
underway at **56% / 53%**, before the approximately 15-point progress checkpoint;
the evidence had reached the bounded preview gate. At the 15-point progress review,
the live meters read **54% / 52%**; investigation was complete and all 58 closeout
checks had passed, so only synchronization remained. Final live balances and Git
verification are retained in the ignored final receipt. No model escalation or
delegation occurred; the independent 5% weekly hard cutoff remains binding.

## Single next milestone

Establish a documented, repeatable ksEditor camera/framing operation that visibly
shows the unchanged +Y-facing pad from above, with its silhouette and diffuse
material identifiable. Reuse the verified clear-weather/default-PP Load sequence
and original FBX/flat DDS. Until that camera/visibility prerequisite passes,
retain the sampling/export NO-GO and do not generate more DDS formats or change
material coefficients/source geometry. Once it passes, compare the original
flat/+X/-X normals under fixed camera/light/material and review export again.

Any future game load additionally needs a reviewed original fixture/container,
native markers/collision requirements, separate authorization and Phase 0J's
cold-load restoration plan. Phase 0E HDR NO-GO, permanent freeware policy and
owner-undecided repository licensing remain unchanged.
