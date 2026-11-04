# Phase 0G: original synthetic material shader

2026-11-04. Starting `phase0/foundation` HEAD:
`ca9204bc9322d5d2492d0ff39328e165050c0da2`.

**Recommendation: REVISE before production.** The original GPU experiment proves
apparent relief and roughness-dependent lighting on unchanged flat geometry.
Numerical, disable and cleanup gates pass at 720p and 1080p on the RX 5700 XT.
The current procedural field is relatively expensive and reads as soft grooved
stone, rather than calibrated asphalt. Retain this reproducible proof; refine its
cost and material scale before proposing integration. No in-game improvement,
legacy-GPU performance or photorealism-target match is claimed.

## Architecture and exact synthetic inputs

- [Original HLSL](../shaders/RV_MaterialRealism.hlsl): two pixel entries, shaded
  material and diagnostic normal/roughness. The original fullscreen vertex shader
  and color prototype are unchanged.
- [CPU mathematical oracle](../restovisuals/material_reference.py): double-precision
  height, analytic gradient, normal and material response.
- [Demonstration driver](../restovisuals/material_demo.py): uses the existing
  `D3D11Session`, `execute_texture`, compiler and PNG exporter. It is not a second
  renderer. The shared executor adds only two explicitly permitted procedural
  entries, no-input allocation and raw timestamp fields.
- Separate windowless D3D11 device, explicit adapter 0, verified AMD vendor/device
  `1002:731F` / RX 5700 XT, feature level 11_0, reported dedicated capacity
  8,546,471,936 bytes. This is not the game's device.
- One unchanged fullscreen triangle: three generated vertices, no vertex-buffer
  mesh, tessellation, displacement, extra polygons or geometry modifications.
- Synthetic plane XY, positive Z normal/view direction, fixed orthographic
  UV-to-image projection. World/tangent axes coincide; normalized UV spans the
  same surface domain at both resolutions. No texture or screenshot is sampled.
- Fixed linear RGB albedo `(0.13,0.135,0.14)`, defined for sRGB/Rec.709 primaries
  and D65 previews; dielectric normal-incidence reflectance 0.04. This encoding is
  chosen for this fixture and says nothing about CSP input encoding.
- Two normalized light directions from `(0.85*side,0.25,0.65)`, side -1/+1;
  view `(0,0,1)`, direct-light multiplier 1.8 and ambient multiplier 0.12. All
  other inputs and geometry remain identical within each comparison row.
- Three parameter pairs: flat `(0,0)`, normals `(1,0)`, normals plus roughness
  `(1,1)`. A separate normal-off/roughness-on small test proves independent
  controls. Returning both controls to zero is tested after enhancement.

## Mathematical model

An original deterministic integer lattice is interpolated with cubic smoothstep.
Its analytic derivatives define three height bands with frequencies 10, 32 and
90 and height weights `0.12/10`, `0.10/32`, `0.055/90`. A low-amplitude oblique
sinusoidal groove adds directional detail. The shading normal is
`normalize((-amount*dh/dx, -amount*dh/dy, 1))`; finite differences of the scalar
CPU height independently test the derivatives. Height is never applied to mesh
positions. These are shading cues, not true cavities, silhouette changes,
parallax, cast shadows or macro-scale occlusion.

Perceptual roughness is `0.64 + amount*0.44*(noise(uv*7)-0.5)`, theoretically
bounded to [0.42,0.86]. Lighting combines Lambert diffuse with a single-scattering
GGX specular distribution, separable Smith masking and Schlick Fresnel. Diffuse
is weighted by `1-F`. This is a physically inspired approximation without
multiscattering or an environment-light integral, not a complete energy/appearance
validation. The public [Filament material-model discussion](https://google.github.io/filament/main/filament.html#materialsystem)
documents the general BRDF concepts; our implementation is original and uses
separable rather than Filament's correlated visibility formulation. No source
implementation or third-party asset was copied.

## Reproduction and artifacts

Run on the approved RX 5700 XT with explicit adapter identity. Each destination
must be a **new** directory inside this checkout's ignored `.local/`:

```powershell
python -m restovisuals material-demo --adapter-index 0 --profile 720p --output .local/material-reproduction-720p
python -m restovisuals material-demo --adapter-index 0 --profile 1080p --output .local/material-reproduction-1080p
```

The command intentionally rejects other adapter identities for this bounded
experiment. Supporting another physical GPU requires a separately scoped change
and validation; no GTX 1060 or RTX 2060 measurement is invented.

Actual outputs remain private under `.local/phase0g-20261104/material-720p/` and
`material-1080p/`. Each contains six labeled PNGs, a static comparison viewer and
`report.json`. PNGs are original synthetic GPU readback, encoded to RGB8 sRGB
through the existing exporter, with alpha checked separately. There is no
contrast enhancement, sharpening, image-generation substitution or identifying
author/tool metadata. Viewers label variants and lighting; no GUI was launched.
All 12 PNG hashes and raw numerical/timestamp receipts are retained privately.

Representative SHA-256 output identifiers:

| 1080p right-light image | SHA-256 |
|---|---|
| Flat | `00d01778d8b746a7b04d084f3b3cf9dbddaaa830f376f8ec0cdcd7c4a349a0a1` |
| Normal detail | `6f7e4cecb99018983eb6b52cd7a61419159ecadb375afffe2d05ecf43f5f5792` |
| Normals and roughness | `18d53e2ca061f42427051f77302d1af30904bd52f8f4f9a2968af63320ac453a` |

Visual inspection found relief clearly distinguishable from the flat baseline,
and the bright/dark response changes with the opposite light. Roughness is
subtler: approximately 58% of preview pixels change from the normal-only image,
with maximum channel changes of 5-6/255. It is not presented as a dramatic extra
depth effect. Sampled red-channel normal-detail response across opposing lights
has correlation about -0.88; roughness-only incremental RMS is about 0.00125 in
linear units. Constant albedo and analytic normals rule out painted-on shading
as the mechanism, while the oracle verifies the actual GPU calculation.

## GPU measurements and numerical validation

Each variant/light has three independently recorded five-draw batches, each
preceded by two warmup draws. Below are ranges of **per-draw medians across the
two light cases**, in milliseconds, on this RX 5700 XT:

| Resolution | Flat | Normal detail | Normals + roughness | Enhanced minus flat |
|---|---:|---:|---:|---:|
| 1280x720 | 0.05367-0.05385 | 0.36847-0.36858 | 0.47012-0.47039 | 0.4163-0.4167 |
| 1920x1080 | 0.12070-0.12077 | 0.82982-0.83024 | 1.05706-1.05734 | 0.9363-0.9366 |

These timestamps cover the existing draw/raster/shading/output-write batch, not
pixel-shader ALU alone. Compilation, allocation, upload, query polling, readback,
CPU oracle and PNG export are outside the timestamp interval. Host wall times
for dispatch/synchronization/readback, CPU checking and export are recorded
separately; the first is not pure CPU execution time. Raw start/end ticks,
frequency and disjoint status are retained; all reported timing batches are
non-disjoint. Short warmup/sample counts and uncontrolled concurrent system load
limit generalization. There is no Assetto Corsa FPS inference.

- All output pixels are finite and color alpha is exactly 1. All diagnostic
  normals are checked: maximum length error below `6.4e-8`. Observed roughness
  spans approximately [0.43408,0.85824].
- CPU/GPU maximum absolute discrepancy is below `6.3e-6`, against a declared
  `4e-4` tolerance. Full-resolution color/oracle comparisons use 99 positions;
  finite/alpha/normal-length checks cover every pixel. The final 1080p run's
  prerequisite 64x48 gates compare every pixel to the CPU oracle; the earlier
  720p small gates used the 99-position grid.
- Repeated identical GPU readbacks are byte-exact. Disabling both controls after
  the enhanced draws restores the baseline byte-for-byte at both resolutions
  and both lights. This equality concerns this synthetic fixture only.
- Ten new regression tests pass, including finite-difference gradients, bounds,
  independent controls, corruption detection, no-input allocation failure,
  fail-closed export, CLI failure status and cleanup. All 24 affected existing
  tests pass; the original 124 test cases and their source files remain intact. The unrelated
  full suite and old hardware matrix were not rerun.
- One small original-color-path native identity regression passed after the
  shared executor change; it did not repeat the old full GPU matrix.
- Initial strict compilation rejected signed integer modulus as a performance
  warning. Changing the nonnegative lattice to unsigned arithmetic resolved it;
  warnings remain errors. No artistic/architecture retry loop was performed.

## Resource and failure contract

There are **no source textures or samplers** in the material path. Each draw case
allocates an RGBA32F output plus staging readback and a 16-byte immutable constant
buffer, with existing raster/query objects. Declared texture payload is
29,491,200 bytes at 720p or 66,355,200 at 1080p. Flat and enhanced variants have
the same resources, so **incremental candidate texture payload is zero**. These
are logical payload sizes, not measured driver allocation or total VRAM demand.

DXGI process-local-segment samples are available: the representative before
sample is 3,866,624 bytes; live samples are 19,857,408 (720p) and 37,683,200
(1080p). Those samples remain elevated after case reference release. Staging
residency, driver caching and deferred accounting mean that these counters
cannot be equated to declared payload, a leak, a peak or physical-memory release.
CPU RAM peak is unmeasured. All owned COM counts return to their marks, and both
separate device/context sessions are fully released.

Final preservation checks match all 29 protected-file hashes and all 49 selected
settings-file hashes against the prior known-good receipt. The untracked approved
reference PNG is unchanged. No restoration or installation cleanup was needed.

Numerical and disable gates run before large draws. Invalid/disjoint timings
abort measurement rather than becoming zero-duration successes. Partial
allocation and callback-free executor failures clear only the owned context and
release resources in `finally`; a failed run retains its private report and
does not publish a successful viewer. Existing destinations/outside paths are
rejected before native access. Readback/query waits and draw counts retain the
existing bounds. Original game files and global graphics state are never touched.

## Integration boundaries and next milestone

Future material integration needs real surface coordinates/tangent frames,
geometric normals, material roughness/albedo and consistent light/view data.
Normal and roughness maps belong in material shading; using supported CSP
material inputs where available would avoid an extra full-screen PP reconstruction.
Their exact version-specific API and ownership still need separate validation.
This session did not search SDKs or claim a working CSP material route.

Image-only PP cannot recover the fixture's true normals, roughness or material
identity from finished RGB. The present result therefore does not unblock the
HDR callback or returned-canvas lifecycle NO-GO. Pure Gamma/LCS remain separate
integration/calibration targets. Temporal stability, oblique views, normal-map
filtering, material scale and legacy/NVIDIA hardware costs remain unvalidated.

The next engineering milestone is a compact, original precomputed normal/roughness
fixture evaluated by the same oracle and renderer, to compare texture-fetch cost
against this procedural ALU cost while refining stone/asphalt scale. It needs a
fresh explicit allocation/cleanup contract and actual measurements; no speedup is
promised. Photo Studio and the complete UI remain deferred. Freeware and the
unresolved owner-controlled licensing decision are unchanged.
