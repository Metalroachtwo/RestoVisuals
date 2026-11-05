# Phase 0K: normal texture preparation and recovery rehearsal

2026-11-04. Starting verified local/remote `phase0/foundation`:
`24d1ef8c3a2d110950af95a81ca49717a7d6fa42`.

**Offline preparation passes; future native experiment is NO-GO.** Six original,
numerically validated normal-only DDS candidates and a disabled owned package are
ready for review. A suitable original KN5 fixture, supported authoring/export/load
workflow and verified material decode are still missing. Filesystem recovery does
not establish loaded-material recovery. The Phase 0E HDR NO-GO remains binding.

No GUI, Content Manager, Assetto Corsa, DCC, graphics device or renderer was
launched. Installed files/settings were read only. An already-installed D3DX
library parsed DDS metadata without allocating a GPU texture or creating a device.
No experimental shader-replacement section was enabled or proprietary asset copied.

## Original fixture contract and ownership

No original game fixture is registered/tracked in the project or established by
the Phase 0J handoff. The existing D3D11 infinite-plane fixture is not a KN5 or a
demonstrated game authoring workflow. No third-party car/track was modified to
fill this gap, and no handwritten KN5 writer or alternate renderer was built.

The original [fixture contract](../examples/phase0k-normal-probe/fixture-contract.json)
specifies one proposed `RV0K_OWNED_PLANE` mesh and `RV0K_OWNED_SURFACE` material,
with no damage, transparency, skinning, LOD variants or shared materials outside
the test. Its candidate is the existing built-in `ksPerPixelMultiMap` normal slot
`txNormal`; it is not a claim that this shader/slot has been verified on a fixture.
The required material match and mesh match counts are both exactly one.

Proposed asset-local quad vertices are `(-1,0,1), (1,0,1), (1,0,-1), (-1,0,-1)`;
UV1 is `(0,0), (1,0), (1,1), (0,1)`, with triangles `012` and `023`.
Tangent is +X, bitangent -Z, normal +Y; `T cross B = N`. Thus a positive texture-Y
normal points toward asset-local -Z. This is a mathematically defined proposal,
not an exported mesh. Exporter transforms, winding and tangent handedness must be
verified against the actual game material rather than assumed from these vectors.

Prerequisites remain original editable source, a supported export to KN5 and
supported loading route, immutable source/KN5/config hashes, authenticated original
texture bindings and all effective properties/flags, known UV/tangent data and
verified always-on normal interpretation. Preserve albedo and every unrelated
texture/property. An original KN5's existence, exportability and loadability are
not inferred from texture-file preparation. No authoring or loading is attempted.

## Selected shader and experimental texture contract

[Phase 0J](PHASE0J_MATERIAL_INTEGRATION.md) supplies the bounded CSP evidence.
The upstream [shader-replacement reference](https://github.com/ac-custom-shaders-patch/acc-extension-config/wiki/General-%E2%80%93-Shader-replacements)
documents disk texture-resource assignment and a flat normal filler around
`127,127,255`; it does not establish this shader's complete byte decode, tangent
signs, alpha use, runtime view format or DDS-loader behavior. The new candidates
therefore remain **experimental, not native-compatible assets**. They configure
built-in shading if eventually validated; they do not execute our original HLSL.

The offline file contract is precise:

- One 256x256 two-dimensional surface, nine levels through 1x1, no array/cubemap,
  no compression, no roughness or other packed material data.
- DDS magic, a 124-byte header and 20-byte DX10 extension; explicit DXGI
  `R8G8B8A8_UNORM` (28), not `_SRGB` (29). Each mip has tightly packed RGBA bytes.
- RGB is `round_half_up(255 * (normalize(n) * 0.5 + 0.5))`; rows are written in
  increasing array Y. The offline decoder is `normalize(2*RGB/255-1)`.
  Every A byte is 255. No gamma/monitor transform or premultiplication is applied.
- DDS alpha-mode metadata is zero despite the known opaque bytes. Microsoft's
  [DX10 header documentation](https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dds-header-dxt10)
  warns that legacy D3DX loaders reject nonzero values. This avoids a documented
  incompatibility; it does not certify CSP loading or alpha semantics.

The layout follows Microsoft's [DDS guide](https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide)
and [header specification](https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dds-header).
The [DXGI enumeration](https://learn.microsoft.com/en-us/windows/win32/api/dxgiformat/ne-dxgiformat-dxgi_format)
distinguishes the declared UNORM and sRGB formats. File metadata expresses intended
non-color data; whether CSP overrides its view/decode remains unknown. RGB versus
RG reconstruction, normal sign, V orientation, alpha meaning, DDS support, mip use
and sampler behavior must be established on the selected shader in the future test.
No DXT5NM, BC compressor, roughness packing or extra format matrix is added here.

## Generation, mip filtering and numerical results

[material_assets.py](../restovisuals/material_assets.py) reuses the existing
`build_mips(256)` hierarchy for the detail candidate. Only its mean normal XYZ is
read; the moment alpha is discarded. The original Phase 0I generator, moment-map
encoding and every prior shader remain unchanged. Each output direction is
normalized and quantized to RGB8 after reduction. The signed RGBA16F moment map
is never substituted into a conventional normal slot.

Diagnostics start with double-precision unit normals. A ramp has one signed
component `+/- 0.6*(i+0.5)/256`, the other tangent component zero and positive
`z=sqrt(1-component^2)`. X ramps advance across columns; Y ramps across rows.
These ramps intentionally expose orientation and are not seamless production
patterns. The detail field is the original periodic Phase 0I surface, including
its previously documented groove-frequency adaptation.

Mip reduction averages unnormalized vector means. It does not renormalize child
means before further reduction. Only each final stored direction is normalized.
A targeted unequal-variance grid test distinguishes this method from recursively
normalizing parents, which biases the coarse direction. The detail source retains
Phase 0I's half-float intermediate precision; diagnostics use unquantized double
means. RGB8 output loses the mean-vector magnitude/variance statistic. It cannot
reproduce the original shader's moment decoder or establish identical filtering.

All 54 mip levels, comprising 524,286 texels, have finite reconstructed normals
and alpha exactly 255. Offline normalization error is below 1e-12. Component
quantization error against the normalized source is at most `1/255` (0.003922).
Maximum angular error is 0.36510 degrees for the orientation diagnostics and
0.33807 degrees for the detail conversion across its mips. These are CPU numerical
results under the declared decoder, not observations of CSP's shader.

The flat asset is `(128,128,255,255)` throughout. Eight-bit UNORM cannot represent
encoded 0.5 exactly: its decoded X and Y are each `1/255` before normalization.
Its angular bias is **0.317755 degrees**, not an exactly neutral vector. CSP's
documented 127 filler has the opposite signed bias under this assumed decoder;
neither proves the native convention. No pixel-identical native neutrality claim
is made. The original future fixture baseline must define its actual normal asset.

An independent comparison of all 65,536 detail-base texels against the original
double-precision analytic field gives maximum/RMS angular error
**0.337558 / 0.183761 degrees**. The final 1x1 direction differs by 0.316703 degrees
from the normalized analytic full-image mean. The numerical source tolerance and
native compatibility question are kept separate.

The existing Windows `D3DX11GetImageInfoFromMemory` metadata reader independently
accepts all six files with HRESULT 0, dimensions 256x256, array size 1, nine mips,
DXGI 28 and 2D dimension 3. Its [documented API](https://learn.microsoft.com/en-us/windows/win32/direct3d11/d3dx11getimageinfofrommemory)
requires no device for metadata inspection. This deprecated library is only an
already-present local validation aid, not a new RestoVisuals dependency, pixel
decoder validation, GPU upload or evidence that Assetto Corsa consumes the files.

## Original candidates, hashes and exact payload

The [disabled package](../examples/phase0k-normal-probe/README.txt) contains six
original DDS files, `disabled.ini`, the fixture requirements, README and manifest.
The disabled selector targets only the proposed original material/shader/slot and
defaults to **flat**. It has no shader swap, includes, scalar edits or HLSL source.
Changing candidate selection requires a fresh reviewed run-bound package; no
command enables it. The [manifest](../examples/phase0k-normal-probe/manifest.json)
hashes each payload and keeps `native_ready` and `native_compatible` false.

| Candidate | DDS SHA-256 |
|---|---|
| [flat](../examples/phase0k-normal-probe/textures/flat.dds) | `ce82d560691c9fcd58ca30ba22f725e48b293048547e0f4c1a77f1ac360393d1` |
| [positive X](../examples/phase0k-normal-probe/textures/x-positive.dds) | `6795dc027948c66054d9abe4b65101cc486018a2812971bfffa80e51282301e6` |
| [negative X](../examples/phase0k-normal-probe/textures/x-negative.dds) | `c00831f1fefb5e76b0f7d6c5a1bfb66d1a9a65b6378e48e7b5bcbd2d29550a7e` |
| [positive Y](../examples/phase0k-normal-probe/textures/y-positive.dds) | `54a9f730c24cafe907664ef9fd9350299746af2d283a11ad8c20e5b8b518a704` |
| [negative Y](../examples/phase0k-normal-probe/textures/y-negative.dds) | `f565389f97b6d4582446e8e8697a38ca0f955807bf3f052302366e3b3e9eff6a` |
| [original detail](../examples/phase0k-normal-probe/textures/detail.dds) | `34b93be3c4077d4ca50e1a90619e595bf0382c202a38c2915e449307bf36c3da` |

| Mip width | Pixel bytes per candidate |
|---|---:|
| 256 | 262,144 |
| 128 | 65,536 |
| 64 | 16,384 |
| 32 | 4,096 |
| 16 | 1,024 |
| 8 | 256 |
| 4 | 64 |
| 2 | 16 |
| 1 | 4 |

Each full chain is **349,524 bytes**, plus a 148-byte file header = **349,672 bytes**.
All six chains total **2,097,144 pixel bytes**; DDS files total **2,098,032 bytes**.
The complete ten-file package is **2,102,109 bytes**, including text/manifest data.
A proposed test assigns one candidate at a time; it does not require all six to
be resident. These are exact logical/file payloads, not physical VRAM, driver
alignment, CPU peak, loading time or in-game performance measurements.

Regeneration on the validated host produces identical bytes and hashes, including the package manifest.
The public package is byte-equal to the final generated package. A scoped Git
attribute disables line-ending conversion inside it so config/JSON hashes survive
checkout; this does not change unrelated source-file attributes. No timestamps,
private paths, author/tool/model fields or third-party source appear in the package.

## Workspace-only transaction and recovery rehearsal

[material_recovery.py](../restovisuals/material_recovery.py) has no game installation
target. Its only destinations are fresh directories inside this checkout's
ignored `.local/`. Package input is limited to a generated workspace package or
the reviewed original example. Links/reparse points, unexpected package files,
modified hashes, native-ready claims and changed disabled configuration are rejected.
This is a closed rehearsal, not a reusable native installer.

Each simulated transaction creates an immutable **synthetic** two-file baseline,
records a nonce and hashes, stages the exact owned component under an ownership
marker, writes each file through an exclusive temporary file and atomically
renames the complete directory to its simulated activation path. Recovery reads
the on-disk journal and content rather than depending on the interrupted call's
in-memory state. Source and destination paths are checked inside the owned workspace.

All **45 fault/complete cases pass**: before allocation; an empty stage; ownership
creation; open-empty, partial-write, renamed-before-journal-update and completed
copy for each of ten files; directory commit before journal update; and a completed
transaction. Repeated recovery is idempotent. Every case retains its original
baseline and leaves the simulated active component absent.

Recovery atomically retires the owned directory inside the scenario as private
evidence, rather than recursively deleting it. Four additional guards verify:
an existing component is not overwritten; managed-file drift is preserved and
refused; an unexpected file is preserved; and interruption after retirement can
be recovered by a fresh invocation. Eight negative synthetic material descriptors
reject missing/extra matches, external sharing, wrong shader/slot, damage-only
normal use or unknown basis. These are descriptor tests, not scene discovery or
proof that real material selection is collision-free.

Unit tests additionally reject missing ownership/baseline receipts, redirected
package paths and reparse attributes. An uncertain orphan `.journal-next` blocks
continuation before changing the component and is retained for review. The
rehearsal is not a claim of arbitrary I/O-error, real power-loss, cross-process
race or filesystem durability coverage. It uses journal/data flushes but cannot
certify hardware durability. Original immutable inputs and manual review remain
necessary when metadata or files drift.

Most importantly, none of this restores material state inside a running game.
Static shader replacements can persist after config removal. A future native
transaction must end the owned session, restore/remove only its reviewed files,
cold-load the original asset/config state and compare shader, properties, bindings,
flags, appearance and protected hashes. Script removal or filesystem equality
alone cannot pass that gate. No existing Phase 0D deployment transaction is reused.

## Native readiness decision

| Required gate | Current evidence |
|---|---|
| Original/authorized fixture | **Missing:** exact proposed geometry/ownership exists as requirements, not KN5. |
| Verified compatible material/shader | **Unknown:** candidate only; no fixture/material execution. |
| Defined texture encoding | **Pass offline**, with declared quantization; native decode remains unknown. |
| Immutable original material baseline | **Missing natively**; package inputs and synthetic baselines are hashed. |
| Collision-free files/config and precedence | **Pass in workspace simulation**; native paths, effective includes and scene counts unverified. |
| Successful workspace recovery | **Pass:** 45 cases, additional guards and targeted tests. |
| Cold-load recovery plan | **Documented**, not executed. |
| Separate authorization and safety review | **Not granted/performed for deployment by this offline assignment.** |

**NO-GO for a native experiment now.** The next action is to obtain or author an
independently owned fixture through an established supported export/load workflow,
then verify the candidate material's actual contract and prepare a fresh reviewed
transaction. Start with the baseline/flat asset and X/Y diagnostics, not detail or
roughness. Keep locked CSP/CM, Pure, weather, PP and HDR unchanged. Do not use a
third-party car/track, injector, GUI fallback or additional renderer to bypass the
missing fixture. This does not reopen Phase 0E HDR rendering.

## Reproduction, tests and known-good state

The new standard-library-only commands refuse an existing output directory and
accept no installation or enabling operation:

```powershell
python -m restovisuals prepare-material-textures --output .local/normal-assets-new
python -m restovisuals rehearse-material-recovery --package .local/normal-assets-new/package --output .local/normal-recovery-new
python -m restovisuals rehearse-material-recovery --package examples/phase0k-normal-probe --output .local/reviewed-normal-recovery-new
python -m unittest discover -s tests -p test_material_assets.py
python -m unittest discover -s tests -p test_cli.py
python -m unittest discover -s tests -p test_texture_stability.py
```

All **37 final static/preservation checks**, **26 new tests**, five existing CLI regressions and 17 existing Phase 0I tests
pass: **48 automated tests**. Coverage includes independent DDS header offsets,
truncation/format/alpha rejection, exact regeneration, analytic orientation,
unequal-variance mip filtering, full decoded-vector checks, fixture basis,
selection/collision/drift safeguards, interrupted recovery and CLI routing.
The original 160 test definitions are unchanged; 26 additions bring the source
inventory to 186. The historical 124 are preserved without claiming a full suite
rerun. No prior shaders or moment generator implementation were edited.

Final known-good evidence is under ignored `.local/phase0k-20261104/`: final
`assets-b/`, `recovery-b/`, targeted/CLI/moment test logs, independent DDS metadata,
analytic cross-validation, preflight and final Git/preservation receipts.
`assets-a/`/`recovery-a/` retain the earlier disabled detail-selection package for
audit; they are superseded, not automatically reusable run-bound packages.
All 29 protected files, 49 selected settings, nine reviewed sources and the
approved untracked visual reference remain unchanged. No game restoration was
needed. Preserve receipts and use reviewed follow-up commits for source rollback.
All original assets remain freeware; repository licensing stays owner-undecided.
