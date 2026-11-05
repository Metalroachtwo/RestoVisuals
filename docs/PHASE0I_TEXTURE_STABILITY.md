# Phase 0I: texture filtering and oblique-view stability

2026-11-04. Starting verified local/remote `phase0/foundation`:
`e82d52ded4495196b65ffe3f655ceec3bdb9cc00`.

**CONTINUE: 256x256, complete moment mips, wrap sampling and an 8x anisotropy cap
are the preferred balanced strategy for this synthetic material.** Use 512x512
as a close-view quality option. Leave the tested extra variance compensation off.
This is a measured offline recommendation, not production asphalt approval,
proof of flicker-free motion or an Assetto Corsa performance improvement.
The Phase 0E native HDR/lifetime **NO-GO** remains binding.

## Controlled geometry and reference preservation

The existing windowless D3D11 renderer now evaluates pinhole rays intersecting
an infinite flat XY plane: vertical FOV 18 degrees, aspect 16:9, fixed world-space
light, albedo and strengths. The camera looks at the origin from
`(0,-d*sin(angle),d*cos(angle))`. Normals, lighting and actual per-pixel view
vectors share world coordinates. The fullscreen triangle transports these rays;
this is a geometric perspective fixture, not merely stretched UVs or a new renderer.
All rays in the bounded fixtures remain below the horizon.

| Fixture | Angle from geometric normal | Distance, synthetic units |
|---|---:|---:|
| front-near | 0 degrees | 2 |
| front-far | 0 degrees | 8 |
| moderate | 55 degrees | 4 |
| grazing-near | 78 degrees | 2 |
| grazing-far | 78 degrees | 8 |

[The original procedural shader](../shaders/RV_MaterialRealism.hlsl) is byte-for-byte
unchanged, SHA-256 `16cd16d0c183cf09666eb993bd36c1428aeea78aa6e3d0e81a6033fa4dae317f`.
Its field is not seamless when repeated. A separately labeled periodic adapter
wraps lattice corners at the existing noise frequencies 10/32/90 and roughness
frequency 7, and changes the groove's Y frequency from 1.5 to 2. Weights and
lighting equations remain consistent. Original-repeat images remain a reference;
their field difference is explicitly excluded from texture-filter rankings.

The periodic analytic reference uses the original GGX BRDF with the actual view
vector. Its raw single sample can itself alias. Texture quality therefore uses
regular 4x4 subpixel integration of periodic procedural shading as a separately
labeled finite reference. It is not exact pixel integration. An 8x8 image and
4/8/16/32 CPU spot integration assess convergence without assuming ground truth.

## Mip mathematics, encoding and memory

[The generator](../restovisuals/material_mips.py) evaluates unit normals and coating
roughness at texel centers. Each little-endian RGBA16F texel stores **mean normal
XYZ and mean roughness^4**. This is a separate encoding from Phase 0H's straight
roughness channel; the corresponding shader fragments must not be interchanged.
Coarser levels average four children in double precision before upload quantization.
Normals are deliberately not renormalized during mip construction.

For unit input normals `n` with mean `m`, direction variance is exactly
`E[||n-m||^2] = 1-dot(m,m)`. Renormalizing each level would discard this statistic.
Both final 1x1 levels have mean length about 0.994900 and variance about 0.010174.
Generator statistics precede half-float quantization. At sampling, slope-based
normal strength is applied and the final normal is normalized. Coating roughness
decodes as `mean(roughness^4)^(1/4)` because this BRDF uses GGX alpha-squared =
roughness^4. Preserving parameter moments is not exact nonlinear BRDF integration.

The optional compensation experiment adds
`normalStrength^2 * max(0,1-dot(m,m))` to coating roughness^4, takes its fourth root
and caps roughness at 0.98. The variance identity is exact before quantization;
adding it to GGX alpha-squared is a heuristic, not an exact GGX convolution.
Half-float length error also perturbs small variance estimates. On this broad,
rough material, compensation slightly worsens the measured match: far-grazing
256/aniso8 RMSE rises from 0.0009506 to 0.0009833; 512 rises from 0.0009462 to
0.0009791. This does not establish that compensation is unnecessary for smoother,
stronger-normal or differently lit materials.

| Base size | Levels through 1x1 | Base bytes | Full-chain bytes | Mip overhead bytes |
|---|---:|---:|---:|---:|
| 256x256 | 9 | 524,288 | 699,048 | 174,760 |
| 512x512 | 10 | 2,097,152 | 2,796,200 | 699,048 |

The larger chain adds exactly 2 MiB. These are declared logical payloads, not
physical VRAM allocation measurements. Alignment, driver objects, caches and
residency are additional. Shared RGBA32F output/staging payload is 29,491,200 bytes
at 720p or 66,355,200 at 1080p, with a 32-byte fixture constant buffer. There is
no temporal history or extra filtering target. CPU generation in the accepted
screen took about 740 ms / 2,957 ms respectively, outside GPU draw timing. Future
assets should be precomputed. Process-local DXGI samples are retained privately;
post-release caching prevents treating their deltas as exact input allocation or
leak measurements.

## Filtering and measurement method

All native work uses an explicitly selected RX 5700 XT `1002:731F`, feature level
11_0, on a separate owned device with no window, swapchain or process attachment.
RGBA16F sampling/mip support and all selected sampler creations succeed locally;
this does not certify the other target GPUs.

The [D3D11 filter enumeration](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/ne-d3d11-d3d11_filter)
defines the implemented modes: point spatial/mip sampling; bilinear spatial with
point mip selection; trilinear spatial/mip interpolation; and anisotropic sampling.
The [sampler descriptor](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/ns-d3d11-d3d11_sampler_desc)
uses anisotropy caps 2/4/8/16, wrap addressing, zero bias and the full mip range.
A cap is not a guaranteed tap count. GPU
[CalculateLevelOfDetail](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-to-calculate-lod)
readback is diagnostic; an independent CPU/GPU interpolation oracle validates the
actual trilinear path. Anisotropic tap selection remains driver dependent.

Costs below are per-draw medians of three five-draw timestamp batches, with two
warmups per batch. The finite reference uses one batch. Raw ticks, frequency and
non-disjoint status are retained. Allocation, upload, CPU generation, readback,
quality checking and PNG export are outside the GPU interval. Geometry, light,
albedo, strengths and RGBA32F output stay consistent. Short batches and background
system/driver activity limit generalization; there is no game-FPS conversion.
The procedural flat image is a correctness reference, not an optimized timing
baseline: its periodic roughness noise is still evaluated before multiplication
by zero. No enhancement cost is inferred by subtracting that timing. Phase 0H's
0.936 ms procedural increment belongs to a different orthographic fixture.

## Accepted GPU costs and spatial fidelity

Linear-RGB RMSE below is against finite 4x4 periodic shading at the same output
resolution. A no-mips control uses bilinear base-level sampling. The screen has
52 cases at 720p; confirmation has 31 cases at 1080p. No sampler is unavailable.

| 720p, grazing-far | 256 GPU ms | 256 RMSE | 512 GPU ms | 512 RMSE |
|---|---:|---:|---:|---:|
| No mips | 0.08434 | 0.001721 | 0.09525 | 0.001779 |
| Point + mips | 0.08398 | 0.002852 | 0.08402 | 0.002850 |
| Bilinear + mips | 0.08404 | 0.002643 | 0.08399 | 0.002649 |
| Trilinear | 0.08414 | 0.002571 | 0.08408 | 0.002578 |
| Aniso 2 | 0.08454 | 0.001803 | 0.08435 | 0.001810 |
| Aniso 4 | 0.09624 | 0.001252 | 0.12275 | 0.001251 |
| Aniso 8 | 0.14873 | 0.000951 | 0.20036 | 0.000946 |
| Aniso 16 | 0.18938 | 0.000866 | 0.24485 | 0.000860 |

| 1080p fixture | 256 trilinear ms / RMSE | 256 aniso8 ms / RMSE | 512 trilinear ms / RMSE | 512 aniso8 ms / RMSE |
|---|---:|---:|---:|---:|
| front-near | 0.18895 / 0.000382 | not repeated | 0.18864 / 0.000118 | not repeated |
| front-far | 0.18903 / 0.000316 | not repeated | 0.18959 / 0.000129 | not repeated |
| moderate | 0.18883 / 0.000271 | 0.18887 / 0.000271 | 0.18914 / 0.000133 | 0.18911 / 0.000076 |
| grazing-near | 0.18919 / 0.001250 | 0.20011 / 0.000650 | 0.18930 / 0.001245 | 0.23623 / 0.000603 |
| grazing-far | 0.18911 / 0.002293 | 0.27775 / 0.000856 | 0.18924 / 0.002301 | 0.42400 / 0.000842 |

Raw periodic shading costs about 0.564 ms at 720p and 1.268-1.270 ms at 1080p;
4x4 reference shading costs about 3.46 / 7.76 ms. These are isolated total draw
costs. They establish no in-game speedup.

At near-normal 720p, 512 reduces texture RMSE from 0.000377 to 0.000112 at nearly
identical 0.084 ms cost. It also improves moderate and near-grazing fidelity.
At distant grazing views both sizes converge on similar filtered error; 256 then
has the better memory/cost balance. Aniso8's extra cost over trilinear is meaningful
at grazing-far: +0.0646 ms at 720p and +0.0886 ms at 1080p for 256, while moderate
cost differences are negligible on this adapter.

Row-centered distant detail standard deviation, relative to the finite reference,
is about 1.29 for raw procedural and 1.27-1.29 for unmipped textures: excessive
contrast accompanies aliasing. Trilinear falls to 0.50; aniso4 to 0.81; aniso8 to
0.93; aniso16 to 0.97. More contrast is not automatically more fidelity. Aniso16
adds roughly 0.04 ms at 720p over aniso8 for only about 0.000085 lower RMSE, smaller
than the measured reference-convergence difference. It is not established as the
best quality/cost default.

## Deterministic change probes and reference uncertainty

The final 720p/256 probe uses three UV phases (0, 0.25/256, 0.5/256) at the grazing
camera, and three camera distances (7.8, 8, 8.2). Each frame has its own procedural
reference. The metric is RMS of `(currentTexture-previousTexture) -
(currentReference-previousReference)` across RGB. It removes constant bias but is
not optical-flow reprojection, perceptual flicker measurement or game motion.

| Filter | UV-step residual RMS range | Camera-step residual RMS range |
|---|---:|---:|
| Point | 0.001138-0.001139 | 0.003934-0.003947 |
| Bilinear | 0.0003604-0.0003607 | 0.003594-0.003616 |
| Trilinear | 0.0003432-0.0003433 | 0.003489-0.003512 |
| Aniso8 | 0.0001842-0.0001864 | 0.0011168-0.0011171 |

Aniso8 has the lowest average residual, but the UV-step maximum individual RGB
residual reaches 0.01431 versus trilinear's 0.00996. Worst-pixel change is not
uniformly improved. Camera-step maxima improve to 0.01293 versus 0.02269.

Full-image 4x4 versus 8x8 reference difference is **0.0004332 RMS / 0.006991 max**.
At five CPU spots, GPU4/GPU8 match their corresponding CPU integrations within
8.94e-7 / 6.23e-7. However, CPU16 versus CPU32 still differs by up to 0.0004127 at
these spots. The grazing reference is therefore not fully converged. Small filter
rankings and subpixel residuals cannot be treated as exact error to an ideal image.
This bounds the conclusion to improved aggregate synthetic behavior, not eliminated
aliasing or actual in-game temporal stability. No longer tuning loop was attempted.

## Seams, normal checks and visual limitations

Analytic opposite boundaries match. CPU wrap sampling at 65 positions per axis
on every mip has zero opposite-boundary component mismatch for both sizes.
Across a 0.000002-coordinate span crossing a repeat, maximum component change is
0.00004992 / 0.00005203. Opposite texel centers are adjacent positions, not the
same point; they need not match and were not artificially copied or blurred.
A whole-tile GPU UV translation gives RGB RMSE 4.65e-7 / max 3.86e-5. Finite
coordinate/filter precision prevents claiming byte identity across translated UVs.

Across both spatial matrices, normal length error is below 6.6e-8; observed
roughness is [0.43408,0.85854]. Color pixels are finite with alpha exactly one.
Repeated identical inputs give byte-identical readbacks. All 56 spatial texture
cases give byte-exact disabled output against the corresponding procedural flat
image. Unit-normal validity does not prove temporal angular stability.

Visual inspection shows trilinear's lost distant detail and anisotropy's improved
retention, while regular grooves and tile repetition remain evident. Seamless
boundaries do not make repetition invisible or validate convincing asphalt.
There is no seam-hiding post-process blur. Float linear RGB drives metrics;
RGB8 sRGB PNG previews can conceal small differences. Physical scale, aggregate
structure, albedo variation, real tangent bases, depth, motion/history and different
roughness/light distributions remain unvalidated. The technique fits material
shading with surface coordinates; a full-screen image cannot supply these inputs
or repair original material lighting by itself.

## Tests, failure evidence and rollback

Seventeen new automated tests and 40 affected existing tests pass. All 143
pre-session test cases, including the historical 124, and the original shader are
preserved. The unrelated full historical suite was not unnecessarily rerun.
Twenty-five native gates cover geometric CPU oracles, original/periodic lighting,
explicit base/mid/last mips with compensation on/off, actual implicit trilinear
interpolation, finite/unit/range and disable checks. Two small original-color and
Phase 0H default texture native regressions pass. Accepted runs contain 113 image
cases and one additional 8x8 reference image. Final audit verifies **152 artifact
hashes and 544 serialized timestamp/release receipts**, with all owned contexts
released. Reports include no disjoint timing or cleanup failure.

The first filter screen is invalid and excluded from every table. The installed
HLSL compiler selected `SampleLevel(-1)` under a negative-macro comparison,
effectively forcing base mip sampling. Identical base/trilinear hashes prompted
disassembly, which proved that instruction. A positive boolean selector plus a
compiled-instruction regression and actual implicit-mip CPU/GPU oracle fix and
cover it. Earlier strict compilation also caught a possibly negative power input;
a positive guard fixes the valid roughness power domain. Warnings remain errors.
Failed/invalid evidence is retained privately rather than represented as successful.

Each case owns its immutable texture, sampler and views through draw completion
and synchronous readback. `finally` clears only its separate owned context and
releases case references back to their mark; normal Python unwinding also covers
partial creation or interruption. Abrupt process termination cannot provide a
completed cleanup receipt. Existing/outside output destinations are rejected.
This owned-device lifecycle does not resolve CSP/Pure's canvas retirement contract.
No GUI/game or installed-stack change occurred. All 29 protected-file hashes and
49 selected-settings hashes match the previous known-good receipt; the approved
untracked visual target is unchanged. No restoration or game rollback was needed.
Keep private receipts; use a reviewed follow-up commit for source rollback rather
than history reset. Freeware and unresolved license-owner boundaries are preserved.

## Reproduce, inspect and continue

Use fresh ignored destinations on the explicitly verified adapter. GPU stages
must run sequentially so they do not contaminate each other's timings:

```powershell
python -m restovisuals texture-stability --adapter-index 0 --stage smoke --output .local/stability-smoke
python -m restovisuals texture-stability --adapter-index 0 --stage screen --output .local/stability-screen
python -m restovisuals texture-stability --adapter-index 0 --stage confirm --candidate aniso8 --compensation 0 --output .local/stability-confirm
python -m restovisuals texture-stability --adapter-index 0 --stage temporal --candidate aniso8 --compensation 0 --size 256 --output .local/stability-temporal
python -m unittest discover -s tests -p test_texture_stability.py
```

Successful runs include `index.html`, original GPU PNGs and `report.json` with
quality, timestamps, hashes, logical payloads, CPU wall times and release receipts.
Spatial runs also write packed mip levels. No browser is launched. Accepted local
evidence is under ignored `.local/phase0i-20261104/screen-v2/`, `confirm/` and
`temporal/`; `screen/ASSESSMENT.json` explicitly rejects the first screen. Raw
machine metadata, proprietary assets and private analysis are not published.

Prefer **256 + complete moment mips + wrap + cap8 anisotropy + compensation off**
for the balanced synthetic profile. Keep 512 as a close-view option; cap4 is a
measured lower-cost compromise with less grazing detail, not equivalent quality.
Do not promote cap16 or variance compensation to defaults from this evidence.

The highest-value next material milestone is an original tangent-space mesh
fixture with calibrated surface scale and a better-converged grazing reference,
followed by a documented supported material-interface/lifecycle plan. This can
validate material inputs and approximation limits before any reviewed integration.
Native HDR rendering remains NO-GO; no CSP deployment is authorized by these tests.
