# Phase 0N: traditional DDS header compatibility

2026-11-05. Verified starting local/remote `phase0/foundation`:
`5350ca3d34cc806026c1e0fa7f453606a5213f03`.

**The Phase 0M format/dimension symptom is resolved at the editor metadata layer.**
With unchanged pixels, ksEditor reports the DX10 control as `LUM (0), 0x0` and
the traditional-header candidate as `ARGB, 256x256`, with nine mips in Texture
Review. Both files independently decode to the same original RGBA pixels outside
the editor. This isolates header representation as the cause of the different
metadata reports; it does **not** establish that the original DX10 texture failed
GPU loading, or that the candidate is sampled correctly by the material shader.

**KN5 export and the next native milestone remain NO-GO.** The reviewed interfaces
did not provide positive resource-pixel/shader-sampling evidence, and the viewport
remained inconclusive. No KN5 save, game launch or material deployment was attempted.

## Exact original and candidate representation

The control is the unchanged original Phase 0K
[flat DDS](../examples/phase0k-normal-probe/textures/flat.dds).
The only new experiment file is
[flat-legacy-rgba8.dds](../examples/phase0n-dds-compatibility/flat-legacy-rgba8.dds).
[comparison.json](../examples/phase0n-dds-compatibility/comparison.json) contains
independent header, pixel, per-mip and decoder receipts.

| Field | Original control | One traditional-header candidate |
|---|---|---|
| Dimensions / levels | 256x256 / nine through 1x1 | Identical |
| Header bytes, including DDS magic | 148 | 128 |
| DDS header / pixel-format structure sizes | 124 / 32 | Identical |
| Header flags / pitch / caps | `0x0002100f` / 1024 / `0x00401008` | Identical |
| Pixel-format flags | `DDPF_FOURCC = 0x04` | `DDPF_RGB \| DDPF_ALPHAPIXELS = 0x41` |
| FourCC / RGB bit count | `DX10` / 0 (format supplied by extension) | 0 / 32 |
| Format | DXGI 28, `R8G8B8A8_UNORM` | Legacy `A8B8G8R8` word layout, RGBA byte order |
| DX10 extension | Format 28, dimension 3, misc 0, array size 1, alpha-mode field 0 | Absent |
| Channel masks R/G/B/A | Defined by DXGI 28 | `0x000000ff / 0x0000ff00 / 0x00ff0000 / 0xff000000` |
| Compression | None | None |
| Pixel payload | 349,524 bytes; 87,381 texels | Byte-identical |
| File bytes | 349,672 | 349,652 |
| SHA-256 | `ce82d560691c9fcd58ca30ba22f725e48b293048547e0f4c1a77f1ac360393d1` | `1ead2f733f73ab1abff72f48267acdf794efbc1291165468df875081055e1460` |

Only the 32-byte pixel-format structure at file offsets 76..107 changes, and the
20-byte DX10 extension at offsets 128..147 is removed. All other retained header
bytes and every mip byte are unchanged. No row, face, pixel or channel is reordered.

All integer fields and pixel words are little endian. Byte order is **R, G, B, A**;
the corresponding 32-bit word is `0xAABBGGRR`. This is **not BGRA** and must not be
relabeled as `A8R8G8B8` while retaining these masks. ksEditor's generic `ARGB` UI
label does not override the measured file layout. Microsoft's
[DDS pixel-format specification](https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dds-pixelformat)
defines these fields, and its
[DirectXTex loader mapping](https://github.com/microsoft/DirectXTex/blob/main/DDSTextureLoader/DDSTextureLoader11.cpp)
maps these exact masks to `R8G8B8A8_UNORM`. The
[DDS guide](https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide)
recommends traditional headers for broadly compatible uncompressed RGB storage;
that recommendation alone is not proof of ksEditor shader behavior.

Each texel remains `(128,128,255,255)`, including every mip. Alpha is opaque; no
premultiplication, normalization, gamma conversion or compression occurs. Intended
treatment remains linear/non-color normal data. The original explicitly declares
UNORM rather than sRGB; the traditional header has no explicit transfer-function
field. Native view/decode behavior still requires verification. Phase 0K's
0.317755-degree flat-normal quantization bias is preserved, not corrected or
misrepresented as exact neutrality.

## Independent offline inspection and original implementation

[dds_compatibility.py](../restovisuals/dds_compatibility.py) is one small pure
container adapter. It first uses the existing strict reader to require the
original opaque 256x256/nine-mip DXGI-28 contract, substitutes the traditional
pixel-format structure and retains the original pixels. It accepts no installation
path and implements no general texture authoring system or KN5 writing.

Five new [tests](../tests/test_dds_compatibility.py) independently check exact
header offsets/masks, all nine mip payloads and every decoded texel, rejection
of changed/sRGB/array/truncated/non-opaque sources, and reproducible output bytes.
An asymmetric in-memory channel canary detects an R/B swap; it creates no second
experiment file or format. Existing source files are never overwritten.

A separate inspection script reads fields and decodes mask bits independently of
the adapter. The already available **Pillow 13.0.0** decoder also opened both real
files as RGBA 256x256 and decoded every base-level pixel identically to the manual
reader. Pillow base-level decoding is not presented as a nine-mip API or as an
editor/GPU test; the separate mask reader checked all nine mips. No library was
installed or added as a RestoVisuals runtime dependency.

Reproduce the candidate into a fresh owned workspace file:

```python
from pathlib import Path
from restovisuals.dds_compatibility import legacy_rgba8_dds

source = Path('examples/phase0k-normal-probe/textures/flat.dds').read_bytes()
output = Path('.local/flat-legacy-new.dds')
with output.open('xb') as stream:
    stream.write(legacy_rgba8_dds(source))
```

Validation commands:

```powershell
python -m unittest discover -s tests -p test_dds_compatibility.py -v
python -m unittest discover -s tests -p test_material_assets.py -v
```

All **five new tests and 26 affected existing tests passed**. The original 196
test definitions, including the historical 124-test baseline, remain unchanged;
there are now 201 definitions. Unchanged GPU demonstrations and full historical
suites were not unnecessarily repeated.

## Controlled editor comparison

The owner explicitly authorized today's pre-08:00 GUI access through 17:00 Eastern,
with cleanup by 16:30. Actual Eastern time was checked using timezone conversion;
the initial preflight was 06:39. A host-view guard found no existing Blender or
ksEditor session. Blender was not needed: the unchanged, previously validated
original FBX/Blend/OBJ and their receipts were reused without re-exporting them.

Fresh verified backups cover 29 protected files, 49 selected settings files, the
original DDS/source packages, raw FBX/Blend/persistence, SDK config/log and reference.
A fresh private SDK mirror contained 839 byte-verified files. Only its canonical
ksEditor executable was launched; no alternate editor or new tool was installed.
Private GUI guards enforced today's date, cleanup-only operations from 16:30 and
no computer control at/after 17:00. The protected game/graphics stack stayed intact.

The original FBX SHA-256 remained
`49e1dc29e3e2ff976995d67e0bceaaca038e57443885814c72ea48e65ab2b474`.
Its verified geometry, UVs and basis receipt from Phase 0M is preserved. The
supported Open FBX/persistence workflow restored `RV0L_NORMAL_TEST`,
`ksPerPixelNM`, `txNormal` slot 1, opaque flags, one material and 12 properties.
The SDK-required singular `texture` folder held the unchanged control, original
diffuse PNG and the one new candidate.

| Observation | Test A: DX10 control | Test B: traditional header |
|---|---|---|
| Normal resource | `flat.dds` | `flat-legacy-rgba8.dds` |
| Material panel format | `LUM (0)` | `ARGB` |
| Material panel dimensions | `0x0` | `256x256` |
| Size label | `349 Kb` | `349 Kb` |
| Supported R reload | Texture reloaded message | Same message |
| Texture Review header list | Mip count 0 / dimensions unrecognized | 256x256, nine mips, 349,652 bytes |
| Viewport | Low-contrast grayscale; inconclusive | Low-contrast grayscale; inconclusive |
| Confirmed material sampling | Unknown | Unknown |

Complete A/B persistence snapshots were saved. Excluding header date/checksum,
the **only persisted difference is the normal resource filename**. Geometry flags,
shader, all property channels, other resources, lighting and camera parameters
were not changed to conceal a failed test. The scalar baseline remains ambient
0.2, diffuse 0.6, specular 0, exponent 10, emissive zero; additional zero-valued
properties and complete typed channels are retained in the existing Phase 0M
receipt and private A/B snapshots.

The supported **Utilities > Texture Review** tool explicitly says its review is
based on the saved FBX INI. Its used/unused list and mip fields are file/header
evidence, **not a resident GPU-resource query**. No pixel preview/readback was
established in the reviewed controls. Focusing the viewport did not produce an
identifiable material test view. Captures contain low-contrast gray levels;
neither their differences nor apparent similarity proves correct shader sampling
or a pixel-identical rendered result.

The manual-recommended Data Editor dialog was inspected without saving. It showed
default selections `1_heavy_fog` / `b&w`, and the camera panel exposed lens/exposure
values. These are observed UI values, not proof of active weather/PP processing or
the cause of the gray viewport. No values were edited and Save Data was not used.
The copied 22,600-byte error log remained byte-identical to the pre-existing log;
it supplies no new render-failure evidence. A separate preview/workflow issue
remains possible and unproven.

[editor-observations.json](../examples/phase0n-dds-compatibility/editor-observations.json)
records the sanitized observations, exact state comparison and review. Raw
screenshots, original exports, complete snapshots and inspection scripts remain
under ignored `.local/phase0n-20261105/`.

## Specific export-safety review: NO-GO

This is a documented gate review for a workspace KN5 export, not deployment or
an independent peer review. No additional model/delegated review was invoked.

| Gate | Decision / evidence |
|---|---|
| Original ownership, immutable inputs, fresh backups | Pass |
| Known geometry/units/UV/basis | Preserved supported FBX validation and unchanged hash |
| Exact shader, material count, properties and slots | Pass for persisted editor state |
| Original/candidate pixel identity and independent decoding | Pass offline |
| Candidate header/dimensions/nine mips recognized | Pass in editor metadata |
| Positive supported resource-pixel/material sampling proof | **Not established** |
| Informative controlled material view | **Inconclusive** |
| Collision-free proposed output | Fresh owned empty `kn5-export` directory |
| Supported exported-KN5 validation route | Not established; prior Open KN5 uncertainty persists |
| Final KN5 export decision | **NO-GO; Save KN5 not invoked** |

The precise confirmed cause is DX10-header incompatibility in the observed
metadata/reporting path. No pixel/channel encoding error was found. Whether the
original texture was actually GPU-loadable, whether the candidate is sampled
correctly, and why the preview is inconclusive remain unknown. This is not a claim
that all DX10 DDS loading in ksEditor/CSP fails, or that the legacy candidate is
native-compatible. No extra format/compression matrix or undocumented workaround
was attempted.

The highest-value next prerequisite is a supported, informative editor
preview/resource-pixel validation baseline using these same two files. Resolve
that gate without speculative shader/property changes or additional DDS variants,
then obtain a fresh explicit export GO. Any later KN5 must be a real supported
save to a new owned path, with a hash and an honestly labeled output-validation
status. In-game testing still requires its own reviewed experiment.

## Cleanup, preservation and credit review

The owned editor closed normally with parent-process exit code 0 at **07:08:44
Eastern**, before both cleanup and hard deadlines. No force termination occurred.
The Data Editor dialog closed without Save Data. A/B evidence was retained and
only the owned working-project INI was restored byte for byte to its backed-up
input after closure. This workspace restoration is not a live-game material
rollback demonstration.

All **127 closeout checks pass**. All 29 protected hashes, 49 selected settings,
23 scoped original inputs/reference
and all 839 installed SDK files match fresh preflight. The original flat DDS,
FBX, Blend, OBJ, packages, shaders, source tests and untracked visual reference are
unchanged. No game/CM launch, material package enablement, third-party modification,
version change or persistent GUI enablement occurred. The known-good installation
is preserved; the candidate remains experimental.

The private SDK copy includes six pre-existing axis/sphere KN5 resources. They
match the copied SDK baseline and are not original-fixture exports. No such
resource is used as the authored fixture or published; the owned export directory
is empty.

Starting live allowance was **99% five-hour / 59% weekly**. At the approximately
15-point review it was **83% / 57%**: the header comparison had advanced, the
sampling gate had not passed, and work moved to formal closeout. Final meter
readings and local/remote verification are recorded in ignored run receipts;
the 5% weekly hard cutoff remains binding. This session does not create a permanent
budget or GUI exception. The commit-ready closeout snapshot was **76% five-hour /
56% weekly**, representing 23 five-hour points consumed to that stage. The final
through-push readings are retained in `.local/phase0n-20261105/evidence/final-receipt.json`.

Phase 0E HDR NO-GO, Phase 0J cold-load recovery requirements, the permanent 100%
freeware policy and the owner-undecided repository license are unchanged.
