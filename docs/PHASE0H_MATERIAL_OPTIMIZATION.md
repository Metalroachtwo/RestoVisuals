# Phase 0H: procedural versus compact material textures

2026-11-04. Starting `phase0/foundation` checkpoint:
`1e21f6a2f3d515854bc276e91f3716dad4507392`.

**Recommendation: CONTINUE the compact texture approach for this fixture.** It
preserves the tested lighting behavior closely at substantially lower measured
GPU draw cost. Use 256x256 for the original detail density; 512x512 provides a
better fidelity/storage tradeoff for the single finer-density probe. This is an
offline material result, not an asphalt asset approval, GPU compatibility promise
or in-game performance claim. Phase 0E's native HDR/lifetime NO-GO remains binding.

## Implementation and controlled inputs

[The original procedural HLSL](../shaders/RV_MaterialRealism.hlsl) is byte-for-byte
unchanged, SHA-256 `16cd16d0c183cf09666eb993bd36c1428aeea78aa6e3d0e81a6033fa4dae317f`.
The [bounded comparison driver](../restovisuals/material_optimization.py) generates
an original normal-XYZ/roughness-A map from the validated CPU `surface()` model
at texel centers. Each texel is four little-endian half floats: RGBA16F, DXGI
format 10. No color texture, external asset or image-derived normal is used.

[The texture surface fragment](../shaders/RV_MaterialTextureSurface.hlsl) replaces
only `surface()` in an assembled private copy. The lighting function, constants,
parameter layout and shader entries are identical; a regression test compares
their lighting bodies exactly. The CPU BRDF is factored into `shade_surface()`
for both references, retaining the original `shade()` behavior.

The existing D3D11 executor gains one bounded optional compact-input argument;
it remains the sole renderer. It owns a separate windowless device, immutable
texture, SRV and linear-clamp sampler. The sampler uses documented
[D3D11_FILTER_MIN_MAG_MIP_LINEAR](https://learn.microsoft.com/en-us/windows/win32/api/d3d11/ne-d3d11-d3d11_filter)
with one mip level. Interpolated normals are renormalized; normal strength is
applied through reconstructed slopes, while roughness strength interpolates from
the same 0.64 baseline. Zero strengths return the flat baseline.

All comparisons retain Phase 0G's one fullscreen triangle, synthetic coordinates,
linear RGB albedo, two light directions, material parameters and RGBA32F output.
The explicit adapter is RX 5700 XT `1002:731F`, index 0, feature level 11_0.
No window, GUI, game, CSP installation or process attachment was used.

## Measurements: quality and cost together

Each number below is a range across left/right lighting of per-draw medians from
three five-draw batches, each with two warmups. Backend order is interleaved.
Timestamps include draw/raster/shading/output writes; compilation, allocation,
upload, readback, CPU checking and PNG export are outside the GPU interval.
Raw ticks, frequency, disjoint status, payload and process-local memory samples
remain in private reports. Short batches and concurrent system/driver activity
limit generalization; there is no FPS conversion.

| Original density, 256x256 | Flat GPU ms | Procedural GPU ms | Texture GPU ms | RGB RMSE vs procedural |
|---|---:|---:|---:|---:|
| 1280x720 | 0.05382-0.05384 | 0.46969-0.46998 | 0.05901-0.05902 | 0.0003650-0.0003654 |
| 1920x1080 | 0.12064-0.12078 | 1.05714-1.05753 | 0.13294-0.13297 | 0.0003674-0.0003679 |

The freshly measured procedural increment at 1080p remains about 0.936 ms,
consistent with Phase 0G. The texture increment over its paired flat baseline is
about **0.0122 ms**, saving approximately **0.924 ms** of this isolated draw.
That is not a predicted saving inside Assetto Corsa.

Quality targets were declared before the first run: full-image linear-RGB RMSE
at most 0.002, and sampled normal-angle p95 at most 3 degrees. They are research
criteria, not universal perceptual equivalence. Original-density 256x256 passes:
normal p95 is 1.31 degrees at 720p and 1.52 at 1080p. Maximum sampled angle is
3.03 degrees, and maximum individual RGB error reaches 0.00503. The result is
close, not pixel-identical; metrics must not hide local errors.

## One material-scale probe and conditional second resolution

One controlled probe doubles the material-coordinate domain in both backends,
making features finer without changing geometry, albedo, light or strength.
This gives smaller apparent grains, but regular grooves remain. The surface
still reads as grooved stone rather than validated asphalt; aggregate structure,
physical scale, albedo variation and real reference calibration remain absent.

The 256x256 finer probe increased RGB RMSE almost threefold and visibly softened
small details. This meaningful quality/storage tradeoff justified the only second
resolution, 512x512. No third resolution or artistic tuning loop was attempted.

| Finer density | Procedural GPU ms | Texture GPU ms | RGB RMSE | Normal p95 / max, degrees |
|---|---:|---:|---:|---:|
| 256x256, 720p | 0.46834 | 0.06118-0.06128 | 0.001034-0.001041 | 2.18 / 3.33 |
| 512x512, 720p | 0.46844-0.46879 | 0.06098-0.06118 | 0.000350-0.000351 | 0.86 / 1.41 |
| 512x512, 1080p | 1.05390-1.05445 | 0.13718-0.13740 | 0.000351-0.000353 | 1.24 / 1.77 |

The 720p difference in draw time between the two texture sizes is too small to
claim a speed advantage. The larger map improves fidelity for 1.5 MiB more logical
payload. Smaller 256x256 remains preferable at the original density because its
quality already meets the declared criteria with one quarter of the storage.

## Precision, filtering and limitations

At 257 sampled texel centers, half-float quantization alone gives maximum normal
angle error 0.00523 degrees and roughness error 0.000244. Interpolation and finite
spatial resolution dominate the larger field errors. Linear filtering smooths
normal detail; renormalization restores unit length, not lost detail. Hardware
filter precision is covered by a separately declared CPU-oracle tolerance.

All color pixels are finite with alpha exactly one. Full-frame diagnostic normal
length error is below 6.9e-8, with observed roughness approximately [0.4200,0.8600]
across the probes. CPU/GPU comparisons use the analytic or half-texel bilinear
reference as appropriate: color tolerance 0.0004, normal-component tolerance
0.002. The finer 512 run's maximum color CPU error is below 0.000016 and maximum
diagnostic CPU error below 0.000168. These implementation tolerances are distinct
from quality differences against the procedural field.

Every small 32x24 gate pixel is compared to its CPU oracle, including independent
and fractional strengths. Full-resolution CPU/orientation probes use 99 positions;
finite/alpha/normal-length/range checks cover every pixel. Disabled texture output
matches the procedural flat output byte-for-byte at both lights and resolutions.
Repeated readbacks are deterministic. No identity claim extends to game images.

There is one mip level and no prefiltered normal variance. Sampling can smooth or
alias high frequencies; oblique views, minification, mip selection, seamless
tiling, motion and temporal stability remain unvalidated. Clamp boundaries are
not a demonstrated tiling contract. No GTX 1060/RTX 2060 result is inferred.

## Memory, lifetime and rollback

The additional immutable RGBA16F input is **524,288 bytes (512 KiB)** at 256x256
or **2,097,152 bytes (2 MiB)** at 512x512, plus its sampler/SRV driver objects.
Both paths retain the same output/readback payload: 29,491,200 bytes at 720p or
66,355,200 at 1080p, and the same 16-byte constant buffer. These are logical
payloads; driver alignment, object overhead and physical residency are not
measured by summing them. CPU fixture bytes and upload preparation are additional
host costs. The original 256 bake took about 439 ms; the finer 512 bake about
2425 ms on this host, outside GPU timings. This experiment rebakes at command
startup; a future packaged material should precompute its asset.

Representative process-local DXGI live samples in the original-density run are
20,905,984 bytes at 720p and 38,731,776 at 1080p. They do not distinguish the
compact input increment reliably and remain elevated after case release. Driver
caching/accounting prevents interpreting that as zero memory cost or a leak;
CPU/GPU physical peaks are unmeasured. All owned case references return to their
marks and every separate device/context is released.

Each case owns the compact texture through GPU draws and synchronous readback,
then clears only its own context and releases resources in `finally`. Partial
allocation, compilation and validation failures retain private failure evidence;
no successful viewer is produced. Existing/outside output directories are
rejected. An initial strict-compiler initialization warning was fixed with an
explicitly initialized single-return surface; warnings-as-errors stayed enabled.

No installed file or setting is changed, so no game rollback is needed. Preserve
private receipts; revert source only through a reviewed follow-up commit, never
history reset. The original procedural source and every pre-existing test remain
intact. Nine new tests and all 31 affected existing tests pass, plus one small
original-color native identity regression. The unrelated full suite/matrix was
not rerun; the 124 historical and 134 pre-session test cases are preserved.

Final checks verify 30 PNG hashes, three fixture hashes and 170 timestamp/release
receipts. All 29 protected-file hashes and 49 selected settings-file hashes match
the prior known-good receipt; the approved untracked visual-target PNG is unchanged.
No restoration was needed.

## Reproduction, images and next step

Use new ignored output directories on the verified explicit adapter:

```powershell
python -m restovisuals material-compare --adapter-index 0 --texture-size 256 --output .local/compare-original
python -m restovisuals material-compare --adapter-index 0 --texture-size 256 --domain 2 --profile 720p --output .local/compare-finer-small
python -m restovisuals material-compare --adapter-index 0 --texture-size 512 --domain 2 --output .local/compare-finer-large
```

Actual private folders are `.local/phase0h-20261104/texture-256-v2/`, `finer-256/`
and `finer-512/`. Each viewer shows original GPU-rendered flat/procedural/texture
images under both lights, with identical preview conversion and no sharpening
or contrast manipulation. Reports record all 30 PNG hashes, source/bytecode
hashes, fixture hashes, timings and quality results. No image or texture binary
is published in Git. The finer 512 fixture hash is
`67722182630666ac2f8f9563471c74b7f7eed27c1ce74aeecfef50f1ea325faa`;
its 1080p right-light texture image is
`891278601a0da23d47aa7634b01a05958ecabd37182cbe6499dd601569720d0e`.

The next bounded milestone is mip/oblique-view fidelity and seamless material
sampling, before broader hardware testing. This technique belongs with supported
material-shader normal/roughness inputs, where real surface coordinates, tangent
frames and lighting exist. It cannot infer those from finished RGB. No CSP API
was investigated or native path unblocked. Pure Gamma/LCS integration remains
separate, and freeware plus owner-controlled licensing remain unchanged.
