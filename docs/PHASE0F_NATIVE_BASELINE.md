# Phase 0F: native visual baseline and upscaling audit

2026-11-04, America/New_York. Starting checkpoint:
`00a7d5df23d5242c9a6acfcad13a4c06bf2788af`, branch `phase0/foundation`.

**Result:** one native replay ran through Content Manager with the existing
graphics stack. Unedited output/configuration receipts were collected. The
configured upscaler is **NVIDIA Image Scaling**, despite its `FSR` section name.
This is a visual/configuration baseline, not a measured performance baseline or
a validated pixel-matched benchmark. The [Phase 0E shader NO-GO](PHASE0E_HDR_CONTRACT.md)
remains binding; no rendering component or hook was installed or registered.

## Confirmed configuration

Evidence is read-only local configuration, the installed preview361 configuration
schema, CM's selected-replay UI and native screenshots. Full files, exact paths,
backups and receipts remain ignored under `.local/phase0f-20261104/`.

| Setting | Observed value and qualification |
|---|---|
| Output | `VIDEO/WIDTH=1920`, `HEIGHT=1080`, `FULLSCREEN=1`, `REFRESH=144`; captured native window is 1920x1080 |
| Pacing | `VSYNC=1`, `FPS_CAP_MS=13.3333333333333`; configured cap only, not measured FPS |
| Render scale | User `RENDER_SCALE` section has no overrides; installed defaults: `SCALE=1`, `SCREENSHOTS_SCALE=1`, `QUALITY=1` (sharp bicubic). Screenshot scale concerns the documented special screenshot path, not this desktop-window capture. |
| Upscaler enabled | User `FSR/ACTIVE=1` |
| Method | User `FSR/OLD_IMPLEMENTATION=2`; installed preview361 schema maps 2 to NVIDIA Image Scaling v1.0.3, described there as usable on any GPU. This is configuration evidence, not a traced execution of the upscaler. |
| Active method's quality | No user `QUALITY_NIS` override; installed `FSR/QUALITY_NIS=0.7692`, labeled Ultra Quality (77%). `SHARPEN_NIS=0.05` is also inherited. |
| Inactive quality value | User `FSR/QUALITY2=0.87` belongs to method 0's FSR path; it is not the selected NIS quality setting. |
| Screenshot behavior | Installed `FSR/DISABLE_FOR_SCREENSHOTS=1`; these unedited foreground-window captures did not invoke the game's special screenshot command. No claim about that command's internal pipeline is made. |
| PP resolution | User WeatherFX `PP_TWEAKS/FULL_RESOLUTION=1`; this flag alone does not establish the callback's input size or encoding. |
| Dynamic resolution | No separate active dynamic-resolution control was identified in the reviewed render-scale/upscaler sections. Internal behavior is not independently established. |
| PP filter | `POST_PROCESS/ENABLED=1`, `FILTER=Dream Realism 7.3 Gamma`, `QUALITY=5`; unchanged |
| Other graphics | MSAA `AASAMPLES=8`, anisotropic 16, shadow-map size 2048, world detail 5, reflection cube size 2048 / six faces per frame; unchanged |
| Pure | Gamma implementation `pure`, controller `pureCtrl static`; installed Gamma/LCS manifests remain 3.50. LCS was not tested. |
| Locked stack | CSP 0.3.0-preview361/build3898; Content Manager 0.8.2913.40776; protected hashes match the preceding checkpoint |

The schema defining method and quality labels is the installed
`extension/config/graphics_adjustments.ini`, especially its `FSR` entries at
lines 26, 28 and 29. User overrides select the method; the absent NIS-quality
override leaves the installed default applicable. No method, quality, resolution,
PP filter, weather or update policy was changed for this investigation.

## Interpretation of the previous callback dimensions

At the configured NIS factor, `1920 * 0.7692 = 1476.864` and
`1080 * 0.7692 = 830.736`. Rounding gives **1477x831**, exactly the dimensions
reported by the earlier Phase 0D observer. The independent render scale is 1.

This resolves the apparent discrepancy at the **configuration/arithmetic** level:
the `FSR` namespace is enabled, but its selected method is NIS at approximately
77% linear resolution. Mathematical consistency does not prove pipeline order,
actual allocation dimensions, a particular rounding implementation or callback
origin. No observer was reinstalled or rerun to manufacture that proof. A 1080p
final screenshot does not establish a 1080p internal render surface.

## Replay, camera and capture receipt

| Item | Evidence |
|---|---|
| Car | `mm_lexus_rca`, MM - Lexus Rocket Bunny RC-A; installed UI metadata reports v2.0 |
| Track/layout | `jd_drift_mansion` / `open`; installed UI metadata reports 1.0 |
| Replay | `AC_021126-192502_O_mm_lexus_rca_jd_drift_mansion_open.acreplay`, SHA-256 `57e39b11a89bcee6bab0ba98143783304a732f42d140cb6711bf98d64bab3baa` |
| Replay metadata | Format version 16; CM displays 66 Hz recording quality, duration 4:27, time of day 13:06 and Squalls (Sol). Recording Hz is not game rendering FPS. |
| Weather qualification | Stored weather is `sol_44_squalls`; the selected Pure static controller is recorded above. Live weather type was not independently sampled; the captured view has predominantly clear blue sky. Do not equate replay metadata with a verified live Pure state. |
| Camera | Inherited view; no camera-selection action. Native replay controls display Camera Cockpit and car 0. Session persistence changed `LAST_CAMERA/MODE` from 2 to 0; the original file was restored. |
| Fixed visible position | Paused using the existing replay control at displayed 3:49 / 4:27. Subsecond/frame index and world camera transform were not established. |
| Adapter inventory | RX 5700 XT, driver 32.0.21043.12001; a Parsec Virtual Display Adapter is also present. Enumeration does not independently map the game's active D3D adapter. |
| Initial native capture | `native-baseline.png`, 1920x1080, SHA-256 `5d3ac5b53290d73e3af48665eb09553cb0d100d5adb4acf763a487198a6c8dde`; game process age about 122 seconds, not a verified warmup interval |
| Paused capture | `native-paused-baseline.png`, 1920x1080, SHA-256 `378468a86f300287ce74b5c663b71a3caf7141aa5fd19813fe730f4416a503f6` |
| Position/camera witness | `native-paused-controls.png`, SHA-256 `bf9e829094f395121ac5d520b058e59b4f602dc2ba1bb4e1ed61570279407a77` |

The existing selected Lexus/Drift Mansion replay and dependencies were available.
The CM replay list did not expose a Sakura-named candidate; no missing content was
downloaded and no alternate replay was tried. The native view shows grass, road,
trees and sky, without the Lexus in frame despite the displayed Cockpit label.
This limits car/material comparisons and requires a camera check before a future
benchmark. Captures are unedited screen copies of the verified owned foreground
window, visually inspected and retained privately. They are not exported engine
buffers, color-managed reference images or evidence of pixel equivalence.

## Performance and UI limitations

No verified usable frame-time capture tool was found in the bounded PATH and
known CapFrameX/PresentMon location checks. No tool was installed. **No frame-time,
FPS, GPU-time or performance-improvement measurement is reported.** Replay Hz,
configured refresh/cap, historical CM statistics and process age are not substitutes.

CM startup/window restoration is asynchronous. Immediate window-handle probes
could not inspect its main UI; after native exit its process also exposed a tiny
helper window. No reliable CM upscaler-settings screenshot was obtained. The
method/quality finding comes from exact configuration and installed schema, not
a claimed GUI confirmation. The original recorded CM main window was closed
normally through its own window-close interface; no force termination occurred.

## Recovery and verification

Fresh copies of all **29 protected files and 49 settings files** were hashed and
verified before CM opened; all matched the preceding checkpoint. Native cleanup
began at **16:30:44 Eastern**, with normal game exit verified. Owned CM exited
normally at **16:32:25**. All GUI work ended before the 16:35 cleanup target and
16:45 hard task deadline. No unrelated application was controlled.

Only `camera_manager.ini`, `race.ini` and CM `Values.data` changed during the
owned session. Camera mode changed as noted; parsed race settings were equivalent
despite byte-level rewriting. The three files' changed versions were preserved
privately, then fresh originals were restored after both processes exited.
Backup/current hashes and intervening-edit guards preceded each restoration.
All **29 protected hashes and all 49 selected settings hashes now match preflight**,
including original graphics and PP-filter settings. No ambiguous change was
overwritten. The approved untracked visual-target PNG is unchanged.

No RestoVisuals file, shader, canvas, SPICE effect or hook was deployed. Pure's
bridge, locked binaries and existing assets remain intact. The existing 124-test
baseline is retained; unchanged implementation tests were not rerun for this
documentation-only checkpoint. All six targeted validation groups passed,
including configuration arithmetic, replay/three capture hashes, 17 local links,
source/test preservation, recovery receipts and publication boundaries.

## Next benchmark experiment

In a fresh authorized window, first establish a visible-car camera and exact
repeatable replay segment with a trustworthy already-available timing source.
Then compare unchanged NIS 0.7692 against native resolution as a separately
backed-up, authorized A/B experiment, with identical replay/camera/weather/filter,
warmup and capture duration, followed by full restoration. Do not change these
settings automatically or claim a benefit from the current captures. Rendering
integration remains gated separately by Phase 0E; its HDR research was not reopened.
