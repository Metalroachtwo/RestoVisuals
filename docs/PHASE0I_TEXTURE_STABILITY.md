# Phase 0I: texture filtering and oblique-view stability

2026-11-04. This initial engineering checkpoint extends the existing windowless
D3D11 executor; it does not launch a GUI/game or modify the installed stack.
The original procedural HLSL and prior test files are unchanged.

## Validated fixture checkpoint

- Proper pinhole rays intersect an infinite flat XY plane. FOV is 18 degrees,
  aspect 16:9; views are 0, 55 and 78 degrees from the geometric normal and
  distances 2, 4 and 8 synthetic units. World-space lighting and view vectors
  share the normal's coordinate space. This is an analytic geometric fixture,
  not a UV-only stretch or another renderer.
- The old field is not periodic. A separately labeled periodic adapter wraps
  lattice indices and changes the oblique groove's Y frequency from 1.5 to 2.
  Original-repeat images remain a visual reference; periodic textures are
  compared numerically against their declared periodic procedural reference.
- RGBA16F mips retain **mean unnormalized normal XYZ** and **mean roughness^4**.
  Averaging does not renormalize each level. Direction variance is
  `1 - dot(meanNormal, meanNormal)` before decoding. Adding this variance to the
  GGX alpha-squared parameter is an explicit approximation, under investigation.
- Full chains: 256x256 has 9 levels / 699,048 bytes; 512x512 has 10 levels /
  2,796,200 bytes. These are logical payloads, not measured physical allocation.
- Seventeen new tests and 40 affected existing tests pass. Twenty-five native
  gates pass, including projection, explicit and implicit mip CPU oracles,
  normal/range/finite checks and byte-exact disabled output. Small original
  color and Phase 0H texture-path native regressions also pass.

## Correctness finding before accepting filter measurements

The first screen is invalid for filter ranking. The installed HLSL compiler's
negative preprocessor comparison selected `SampleLevel(-1)`, forcing base-mip
sampling despite a separate diagnostic reporting valid LOD estimates. Compiled
shader disassembly established the exact instruction. A positive boolean macro,
a compiled-instruction regression and an implicit trilinear CPU/GPU oracle fix
and cover that failure. Raw invalid evidence is preserved and labeled privately.

The corrected 720p screen is in progress under ignored
`.local/phase0i-20261104/screen-v2/`. No preferred filter, compensation policy or
synthetic temporal-stability conclusion is accepted at this checkpoint. Final
results will replace this provisional report after controlled comparisons.

Reproduce the validated gate with a fresh private destination:

```powershell
python -m restovisuals texture-stability --adapter-index 0 --stage smoke --output .local/stability-smoke
```

The Phase 0E native HDR/lifetime NO-GO and freeware/license-owner boundaries remain
binding. No native deployment or broader GPU compatibility is claimed.
