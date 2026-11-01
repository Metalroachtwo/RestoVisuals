# Running the Phase 0 tools

Run from the repository root with Python 3.11+. No pip installation is required.
Windows is required for `gpu`, native shader compilation, `gpu-validate`,
`gpu-demo` and their native tests. Other code uses the standard library. No command installs software or
applies game settings. JSON goes to stdout; failures use stderr with exit 2.
`guard` exits 3 for detected drift and 0 for equality in the nonempty audited set.

## Fresh checkout example

```powershell
python -m restovisuals --help
python -m restovisuals plan --config profiles/gamma.json --gpu examples/gpu-synthetic-2gb.json --adapter-index 0 --capabilities examples/capabilities-unknown.json
python -m unittest discover -s tests -v
```

The example is synthetic: Ultra Lite candidate, native rendering, no effects,
no FG, no measured performance, no settings applied. `profiles/lcs.json` uses
the same contract with separate Pure mode. Neither file is a calibrated PP filter.

## Private reference audit

Use the already confirmed installation locations supplied for the project;
paths are supplied interactively below to keep this public document machine
independent. These commands work with Windows PowerShell 5.1 or PowerShell 7;
`Out-File -Encoding utf8` avoids legacy redirection producing UTF-16 JSON.

```powershell
New-Item -ItemType Directory -Path .local -Force | Out-Null
$gameRoot = Read-Host 'Confirmed Assetto Corsa directory'
$userCfg = Read-Host 'Confirmed Assetto Corsa user cfg directory'
$cmExe = Read-Host 'Confirmed Content Manager executable'
python -m restovisuals audit --game-root $gameRoot --user-config $userCfg --cm-executable $cmExe | Out-File -Encoding utf8 .local/environment-before.json
python -m restovisuals gpu | Out-File -Encoding utf8 .local/gpu.json
python -m restovisuals capabilities .local/environment-before.json | Out-File -Encoding utf8 .local/capabilities.json
python -m restovisuals plan --config profiles/gamma.json --gpu .local/gpu.json --adapter-index 0 --capabilities .local/capabilities.json | Out-File -Encoding utf8 .local/plan-gamma.json
```

Inspect the GPU report and explicitly choose its measured adapter index. Index
0 is an example, not a rule for selecting the game's GPU. The local development
host exposes duplicate AMD identities with distinct LUIDs. Do not merge them
or infer physical hardware count. The standalone memory budget belongs to the
probe, not the game. The current audit does not establish live render mode or
buffer availability, so optional capabilities remain disabled in the plan.

The tool reads selected root/config/interface files and top-level PP INIs. It
does not inspect cars, tracks or unrelated archives. Binary version resources
are independent evidence recorded during the audit session; the Python audit
reports launcher manifest data and content hashes. An audit snapshot is not a
backup. Its JSON is ignored by Git and is not published automatically.

After development, repeat the same audit with the same path arguments:

```powershell
python -m restovisuals audit --game-root $gameRoot --user-config $userCfg --cm-executable $cmExe | Out-File -Encoding utf8 .local/environment-after.json
python -m restovisuals guard .local/environment-before.json .local/environment-after.json
```

For comparisons, missing files and additions are meaningful. Empty/malformed
inventories are rejected. Equality covers only that audited set, not the entire
installation, user state or Windows.

## Capability reports and plan output

`capabilities AUDIT.json` converts label presence to observations. Reports contain
schema version 1, context fields (CSP version, Pure mode, render mode, width and
height), a per-feature state map and an evidence ID. Unknown entries default to
unknown; arbitrary state/capability names are rejected. Optional eligibility
requires `tested_validated` and matching context. Synthetic tests exercise that
branch; no real matching runtime report has been produced.

The plan reports its candidate class, target frame-time arithmetic, optional
feature decisions, warnings, incremental surface model, input file hashes and
GPU evidence source. Class selection is provisional capacity planning after a
feature-level/software-adapter gate. It cannot certify bandwidth, performance,
drivers or total VRAM headroom. `applies_settings` and `gameplay_validated` remain
false. There is no `apply`, installer, updater, rollback executor or live adapter.

## Shader and benchmarks

```powershell
python -m restovisuals compile-shader shaders/RV_ColorPrototype.hlsl
python -m restovisuals benchmark examples/frame-times-synthetic.csv
```

Phase 0B also provides an explicit bounded GPU execution command:

```powershell
python -m restovisuals gpu-validate --adapter-index 0
```

Choose an explicitly identified hardware adapter. This creates its own D3D11
device, three small textures per case and a fullscreen triangle without a
window, swap chain or game attachment. Four strict-identity checks must pass
before six numerical color checks run. Readback handles padded rows; GPU waits
are bounded to two seconds. A numerical failure returns exit 4. The receipt
distinguishes isolated GPU execution from CSP/Pure gameplay, and records
precision tolerances, payload arithmetic and narrowly scoped GPU timestamps.
The normal suite does not run GPU draws implicitly. Optional Lua tests require
the hash-pinned local setup in the [observer guide](../runtime/lua/README.md).

## Controlled full-resolution demonstration

```powershell
python -m restovisuals gpu-demo --adapter-index 0 --profile both --output .local/my-new-demo
```

The destination must be a **new directory under this checkout's `.local/`**.
Existing directories, paths outside that root and resolved links escaping the
checkout are rejected. The command creates only original project artifacts:
24 PNGs, `report.json`, and a local `index.html` comparison viewer for `both`.
Open the viewer manually if desired; the tool does not launch a browser.
Choose `720p` or `1080p` for one profile instead of both.

The same renderer uses fixed 1280x720/1920x1080 profiles, RGBA32F/RGBA16F
textures and explicit scene-linear/sRGB-display fixtures. All identity cases
must pass byte-for-byte across the full image before any color case runs.
Color output is checked for finite values and exact alpha across the full image;
3,672 deterministic probes per production-resolution case check CPU color math.
This is sampled color equivalence, not a full-image color proof. The controlled
experiment owns exposure (+0.25 EV), shoulder (0.25) and saturation (1.0);
it does not establish Pure's real buffer encoding or exposure ownership.

Each case has one warmup draw and five timestamped draws. Timings exclude upload,
CPU validation, readback, PNG export, presentation and game work. They are a
single batch, not frame-time distributions or gameplay measurements. DXGI
memory samples describe the calling process's local segment, not texture
allocation, peak memory, game usage or system free VRAM. Owned COM-reference
counts must return to baseline; driver caching can outlive these references.
The standalone harness owns three textures including a staging readback;
it is not an installed runtime memory budget or a low-VRAM certification.

RGB8 previews declare sRGB and omit alpha, which is verified numerically.
Linear previews are converted to sRGB and display-clipped, so HDR extremes can
clip. No personal/author/application metadata is embedded. A failed identity
or numerical gate returns exit 4, retains a diagnostic JSON receipt and creates
no success viewer. Native/OS failures return exit 2 and can leave partial local
artifacts; choose another new directory after resolving the failure.

Compilation keeps bytecode in memory and dispatches no shader. See
[shader contracts](SHADER_FEASIBILITY.md) and [capture protocol](BENCHMARKING.md)
before interpreting results. The tool does not create screenshots, initialize a
creative application or capture a game. A synthetic chart does not validate
in-game appearance or artistic quality.
