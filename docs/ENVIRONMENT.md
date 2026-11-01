# Reference environment observations

Audit date: 2026-11-01, America/New_York. Installed files were read only. No
game, Content Manager, DCC application, installer, or GUI automation was launched.

## Observed locally

| Component | Evidence | Result and limit |
|---|---|---|
| CSP | `dwrite.dll` product/file versions; `extension/config/data_manifest.ini` | 0.3.0-preview361, file 0.3.0.361, manifest build 3898. Binary and manifest agree. |
| Content Manager | executable version resource | 0.8.2913.40776; protected version retained. |
| Pure Gamma | `extension/weather/pure/manifest.ini`, `weather.lua` | Both report 3.50; exact hotfix inventory not established. |
| Pure LCS | `extension/weather/Pure LCS/manifest.ini`, `weather.lua` | Both report 3.50; not runtime tested. |
| Pure source version guards | each fork's `weather.lua` | Gamma declares minimum CSP 0.2.0/build 2639; LCS declares 0.2.3p211/build 2974. These are observed code guards, not exercised support guarantees or exact package hotfix requirements. |
| Saved weather selection | user `extension/weather_fx.ini` | `BASIC/IMPLEMENTATION=pure`, corresponding to Pure Gamma; saved state only. |
| Saved video | user `video.ini` | 1920x1080, MSAA 8, PP active, PP filter `Dream Realism 7.3 Gamma`, 75 Hz and VSync enabled. These settings are not project performance targets. |
| Saved upscaler | merged default/user `graphics_adjustments.ini` | FSR section active, method ID 2 = NVIDIA Image Scaling. FSR section name does not identify the selected algorithm. |
| Extra FX | default/user `extra_fx.ini` | User enables Extra FX; SSLR tracing quality 3 and SSGI enabled are present in overrides. No FPS or cost inferred. |
| PP inventory | top-level `system/cfg/ppfilters/*.ini` | 101 files, including pure, pureCandy, pureHDR, pureLinear, pureSIMPLE, pureVR, NOVA_LCS, Ocular 1.0 LCS, SEDREALISM variants, and Dream Realism variants. No filters copied or replaced. |
| ReShade history | first line of `ReShade.log1` | Historical initialization of 6.5.1.2008 through a root dxgi.dll. Neither root dxgi.dll nor d3d11.dll exists at audit time. Current installation/activation unknown; log presence does not establish active injection. |
| Display driver | Windows display-class registry | AMD Radeon RX 5700 XT, driver 32.0.21043.12001 dated 2026-05-29. A Parsec virtual display adapter also appears. Registry identity does not establish the GPU used by the game. |
| GPU capabilities | Windowless native DXGI enumeration and D3D11 device creation | RX 5700 XT: 8,546,471,936 dedicated bytes, measured feature level 12_1. Two DXGI adapter entries have distinct LUIDs but the same AMD identity; physical GPU count and game-selected adapter are not inferred. Software Basic Render Driver is excluded. |

The CSP install log reports version/build zero from a custom ZIP installation.
It is weaker version evidence than the agreeing binary and launcher manifest.
Driver package naming in Radeon Software was not inferred from the Windows
driver number. The WMI/CIM graphics query was unavailable in the sandbox;
display-class registry metadata remained readable.

The native probe loaded system DLLs with the Windows System32 search flag,
created no window/swap chain, and released its own COM/device objects. A
7,741,161,472-byte DXGI budget and zero current usage were returned for the
**probe process**. They do not measure the game's budget or system free VRAM.
No shader was dispatched and no adapter/driver configuration was changed.

## Rendering interfaces observed

Installed PP-context SDK declares `ac.getPatchVersion()`,
`ac.getPatchVersionCode()`, `ac.isModuleActive()`,
`ac.getPerformanceCPUAndGPUTime()`, `render.fullscreenPass()`, and
`ui.ExtraCanvas()`. Simulation fields include `fps`, `fpsCapped`, `cpuTime`,
and replay/simulation `dt`. The generated README incompletely describes the
performance function; its Lua declaration lists two returns. Units, sampling
latency, and their meaning must be measured before using it as telemetry.
Simulation dt is affected by pause/replay speed and is unsuitable as a display
frame-time substitute.

Pure's installed SDK declares configuration access and exposure APIs, including
CBE controls, bypass, limits, sensitivity, target and adaptation speeds. This
shows integration candidates, not a tested permission to take exposure ownership
from Pure or a RestoVisuals profile. Pure source and SDK are not redistributed.

Preview configuration labels include FSR 1.0.2, FSR 2.2.1, and FSR 3.1.2.
The installed hints require Extra FX and post-processing for the temporal
methods, exclude original motion blur, and describe single/triple screen support.
Some methods can trigger downloads. This project has not selected them, fetched
their libraries, or validated loaded DLLs, VR behavior, buffers, or frame generation.
No standalone frame-generation capability has been established.

## Preservation and reproduction

`python -m restovisuals audit --help` describes the bounded read-only collector.
Supply game and user configuration paths explicitly; use the optional CM path
to include its executable in preservation checks. The collector publishes only
selected metadata and relative logical file IDs; raw reports stay local.

The initial snapshot `.local/environment-before.json` covers 112 entries:
11 fixed graphics/application files and 101 top-level PP filters. The snapshot
includes missing expected files as explicit missing values. Compare with a new
snapshot using `python -m restovisuals guard BEFORE.json AFTER.json`. Hash
equality proves preservation only for the audited set. It is not a whole-system
attestation, a backup, or a gameplay validation.

No runtime visual, frame-time, GPU-memory-under-game-load, or low-VRAM hardware
results are available. The development GPU cannot validate 2-4 GB targets.
