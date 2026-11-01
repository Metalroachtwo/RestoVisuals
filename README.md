# RestoVisuals
Freeware graphics-enhancement project for Assetto Corsa. Modern visuals on legacy AMD & NVIDIA GPUs, with adaptive optimization, low-VRAM support, and Pure LCS/Gamma compatibility as development targets.

# RestoVisuals

### Modern visuals. Legacy hardware.

**RestoVisuals** is a graphics enhancement and optimization project designed to bring modern, photorealistic visuals to older AMD Radeon and NVIDIA GeForce GPUs.

Our first target is **Assetto Corsa**, with support planned for Custom Shaders Patch (CSP), Pure LCS, and Pure Gamma.

The mission is simple:

**Beautiful graphics shouldn't require a $1,000 GPU.**

---

## 🎯 Project Goals

RestoVisuals aims to improve visual realism while respecting the performance and memory limitations of older hardware.

Rather than relying on proprietary AI hardware, RestoVisuals will prioritize efficient rendering techniques, intelligent graphics configuration, and GPU-adaptive optimization.

### Core Objectives

- **Cross-vendor compatibility:** Support older NVIDIA GeForce GTX and AMD Radeon graphics cards.
- **Low-VRAM optimization:** Target GPUs with as little as 2–4 GB of VRAM where technically feasible.
- **Photorealistic rendering:** Improve lighting, exposure, color reproduction, material appearance, and visual depth.
- **Pure compatibility:** Support both Pure LCS and Pure Gamma rendering pipelines.
- **Adaptive optimization:** Recommend graphics settings based on GPU capabilities, available VRAM, and measured performance.
- **Upscaling integration:** Investigate FSR 1, FSR 2, and FSR 3 support through compatible CSP integrations.
- **Cinematic capture:** Provide enhanced graphics presets for replay recording, photography, and video production.
- **Modular design:** Allow players to enable or disable individual visual enhancements.

## 🖥️ Target Hardware

RestoVisuals is intended for a broad range of legacy GPUs.

| GPU Class | Example Hardware | Target Profile |
|---|---|---|
| 2 GB VRAM | GTX 950, GTX 1050, RX 460 | Ultra Lite |
| 3–4 GB VRAM | GTX 970, GTX 1060 3GB, RX 570 | Optimized |
| 6 GB VRAM | GTX 1060 6GB, GTX 1660, RX 5600 XT | Balanced |
| 8 GB VRAM | GTX 1070, RX 580 8GB, RX 5700 XT | Enhanced |

These are proposed development targets, not confirmed hardware requirements or compatibility guarantees.

Supported effects will depend on GPU architecture, graphics APIs, driver capabilities, available memory, and the installed Assetto Corsa rendering stack.

## ✨ Planned Features

### Adaptive Visual Enhancement

- Natural color reproduction and cinematic tonemapping
- Dynamic exposure and improved highlight handling
- Optimized bloom, glare, and optical effects
- Improved perceived surface and material detail
- Performance-aware reflection and ambient-effect configuration
- Separate tuning for daylight, sunset, nighttime, and wet-weather conditions

### Intelligent Performance Optimization

- GPU identification and capability detection
- VRAM-aware graphics profiles
- Frame-time monitoring and performance benchmarking
- Automatic quality recommendations
- Optional upscaling and sharpening
- Configurable visual quality versus performance targets

### Pure LCS & Gamma Integration

RestoVisuals will investigate and support both rendering pipelines through documented, compatible interfaces.

Separate configurations will account for differences in lighting, exposure, color response, and post-processing behavior.

### Cinematic & Replay Tools

Future integration is planned with automated Assetto Corsa replay and camera-control workflows.

Potential capabilities include cinematic profiles, consistent capture settings, advanced replay rendering, and optional offline video enhancement.

## 🧠 Rendering Philosophy

RestoVisuals is not intended to reproduce NVIDIA DLSS 5 or require neural-rendering hardware.

Instead, the project aims to achieve a more modern visual aesthetic using techniques that remain practical on older GPUs.

Our priorities are:

1. Image quality
2. Consistent frame times
3. Efficient VRAM usage
4. Broad hardware compatibility
5. Reversible, user-controlled configuration

Visual enhancements must justify their performance cost.

## 🏗️ Development Roadmap

- [ ] **Phase 0 — Research & Architecture:** Audit CSP/Pure integration points, establish hardware targets, and document the rendering architecture.
- [ ] **Phase 1 — Visual Foundation:** Develop initial LCS/Gamma-compatible visual presets.
- [ ] **Phase 2 — GPU Optimization:** Implement hardware detection, performance profiling, and VRAM-aware quality presets.
- [ ] **Phase 3 — Shader Enhancements:** Develop original, efficient graphics effects where existing integrations are insufficient.
- [ ] **Phase 4 — Adaptive Rendering:** Explore dynamic quality control and supported upscaling integrations.
- [ ] **Phase 5 — Cinematic Studio:** Integrate replay capture and optional offline enhancement.
- [ ] **Phase 6 — Public Testing:** Validate performance and compatibility across AMD and NVIDIA GPU generations.

## 🚧 Current Status

**Pre-Alpha — Phase 0B: Isolated Runtime Engineering**

The repository now contains a tested offline control plane: a bounded graphics
audit, windowless DXGI/D3D11 GPU detection, strict profile validation, conservative
capability planning, frame-time analysis and context-checked capture comparisons.
An original Lua observer is contract-tested under LuaJIT. The original HLSL
color prototype now executes in an isolated D3D11 device: both entry points
preserve neutral test pixels exactly in RGBA32F/RGBA16F, with additional color cases
checked against the CPU reference.

In-game CSP/Pure integration, visual calibration, certified legacy-GPU support,
and gameplay performance improvement remain unvalidated. No adapter or shader
has been deployed into the reference installation.

Hardware compatibility, installation instructions, benchmarks, and download releases will be published after successful testing.

## 🔧 Planned Technology Stack

The following technologies are being evaluated:

- Python 3.11+ standard-library offline engineering tools (implemented)
- Windows DXGI/D3D11 capability probing and system HLSL compilation (implemented)
- Assetto Corsa
- Custom Shaders Patch (CSP)
- Pure LCS / Pure Gamma
- CSP Lua scripting and configuration interfaces
- ReShade FX and documented add-on interfaces (deferred; not a foundation dependency)
- C++ and HLSL shader development where justified
- AMD FidelityFX Super Resolution integrations
- Performance benchmarking and diagnostics

Final implementation choices will be based on verified compatibility, licensing, and performance testing.

## 🤝 Contributing

Development and contribution guidelines will be established as the initial architecture matures.

Future contributions may include hardware benchmarking, graphics research, shader optimization, bug reports, and compatibility testing.

## 📜 License

### Permanent freeware policy

RestoVisuals will remain **100% free for end users**. All RestoVisuals-developed
graphics enhancements, shaders, presets and optimization profiles in official
releases must be freely available. There will be no purchase price, subscription,
premium packages, paid feature tiers, trial limits, advertisement unlocks, or
account requirement for local rendering. Free functionality must never be reduced
to create a commercial upgrade. Optional donations or community sponsorship may
be considered later and must never be required for feature access.

Freeware describes the project's end-user pricing policy; it does not select an
open-source license. Public repository visibility alone does not grant broad
redistribution or modification rights. A repository license requires the project
owner's approval. Third-party software/content keeps its own license and may have
separate acquisition costs; RestoVisuals does not redistribute commercial game,
Pure, CSP preview, or proprietary filter content.

A project license has not yet been selected.

Until a license is added, the repository should not be assumed to grant permission to copy, modify, or redistribute its code.

Third-party components will retain their respective licenses.

---

**RestoVisuals — Modern visuals. Legacy hardware.**

*Restore the visuals. Not the hardware.*

## Run the Phase 0 tools

From the repository root, with Python 3.11+ and no package installation:

```powershell
python -m unittest discover -s tests -v
python -m restovisuals plan --config profiles/gamma.json --gpu examples/gpu-synthetic-2gb.json --adapter-index 0 --capabilities examples/capabilities-unknown.json
```

The example uses synthetic hardware data and applies no settings. Native GPU
probing and shader compilation require Windows. The reference installation
remains read-only; CSP 0.3.0-preview361 and Content Manager 0.8.2913.40776 are
locked. CSP 0.2.11 is the minimum target, with runtime validation still pending.
No other CSP track is authorized.

The current suite passes 104 tests with the optional hash-pinned LuaJIT
dependency. Without that dependency, 25 Lua contract tests explicitly skip;
the other 79 tests run on the Windows development host. The original 93 tests
are preserved. See the
[observer contract](runtime/lua/README.md) for the isolated test setup.
Run `python -m restovisuals gpu-validate --adapter-index 0` explicitly for bounded
hardware identity/readback validation; select the intended measured adapter.
Phase 0C adds `python -m restovisuals gpu-demo --adapter-index 0 --profile both --output .local/my-new-demo`
for original 720p/1080p calibration charts, GPU readback PNGs and a local
comparison viewer. This is isolated D3D11 evidence, not an in-game demonstration.
See the [host isolation gate](docs/RUNTIME_ISOLATION.md) and
[freeware/dependency boundaries](docs/FREEWARE_AND_DEPENDENCIES.md).

The [Phase 0B report](docs/PHASE0B_RUNTIME.md) records the GPU-discovered identity
defect and fix, the [official 0.2.11 reference](docs/CSP0211_REFERENCE.md) records
version-matched SDK evidence, and the [Dream Realism analysis](docs/DREAM_REALISM_REFERENCE.md)
records missing local companion resources and a Pure-owned extension candidate.

Read the [CLI guide](docs/CLI.md), [architecture](docs/ARCHITECTURE.md),
[compatibility matrix](docs/COMPATIBILITY.md), [environment audit](docs/ENVIRONMENT.md),
[research ledger](docs/RESEARCH.md), [shader feasibility](docs/SHADER_FEASIBILITY.md),
[benchmark protocol](docs/BENCHMARKING.md), [validation evidence](docs/VALIDATION.md),
[roadmap](docs/ROADMAP.md), and [continuation handoff](docs/PHASE0_HANDOFF.md).
Development follows [repository instructions](AGENTS.md) and the
[Phase 0 execution plan](docs/PHASE0_PLAN.md).
