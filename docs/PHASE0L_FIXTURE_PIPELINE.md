# Phase 0L: original material fixture authoring pipeline

2026-11-04. Starting verified local/remote `phase0/foundation`:
`c1e03094a42f3a7ca54d7dfe88651938b3428d76`.

**Native test NO-GO.** A documented candidate path and original source inputs now
exist: original OBJ/MTL -> authorized DCC import -> installed legacy FBX exporter
-> ksEditor Open FBX / Save KN5. No DCC import, FBX export, ksEditor operation,
KN5 export or game load was performed. The documented final conversion is
interactive; no supported headless KN5 interface was identified in this bounded
review. This phase stops at prepared source, as required by its offline limits.

## Read-only tool verification

The inventory was limited to the known Assetto Corsa SDK, installed-authoring
registration/expected paths, the registered MCP tool metadata and selected
exporter files. No executable was invoked for help/version/export, no live DCC
gateway was contacted, and no authoring application, scene or service was started/restarted.
Static file/version evidence is not a working-runtime witness.

| Tool / evidence | Verified availability | Limit |
|---|---|---|
| SDK `editor/ksEditor.exe` | Present, 512,000 bytes, file version `1.0.0.0`, product ksEditor; SHA-256 `820a1c5de8b64074e3d32cdf1a377238da3a3e0480d03070ffa35ba98e6c122e`. | Not launched; exact runtime/import/export behavior untested. |
| SDK FBX runtime | `fbxsdk-2014.1.dll`, 6,741,832 bytes, `2014.1 RC (212161)`; SHA-256 `bd80cab92b6078f24d137e1758de0a73dc68e4e86a5371f2480840742f98e822`. | Presence does not certify every newer exporter option or file. |
| Kunos pipeline manual | `sdk/dev/car_pipeline_2.0rev/AC_Pipeline_PUB_Rev2.0.pdf`, 76 pages; SHA-256 `dacca0748b712c7d0d9057db80362c00b20d2421386968c001de3a1970b16ecf`. Pages 3-6 and 66-70 inspected; editor instructions/screenshots reviewed. | This is a car/authoring guide, not a complete minimal-track packaging contract. No manual/image is redistributed. |
| Installed Blender | Executable present, 108,686,296 bytes, file version `5.1`; uninstall registration identifies `5.1.1`; SHA-256 `b952b58cafe44050ae016bda94c91de0968b028b1c7082a824d7087985619642`. | Not launched; registration and file metadata do not prove a reachable DCC session. A leftover 4.5 directory was not mistaken for the active binary. |
| Blender legacy FBX exporter | Installed `io_scene_fbx` source declares `export_scene.fbx`, selection export, axis controls and `use_tspace`; `fbx_utils.py:25` declares `FBX_VERSION = 7400`. | Operator registration/execution and ksEditor roundtrip are untested. No replacement FBX writer is introduced. |
| Authoring integrations | Blender MCP provider is configured; DCC/MCP CLI executable is present. Tool metadata exposes Blender operations. | No live health/scene probe was performed. No ksEditor MCP/export API was established. Maya/3ds Max registry entries are not evidence of a selected, verified exporter integration. |
| Alternate editor executables | Additional `(2)` and `At` executables exist with different bytes/hashes. | Not authenticated, selected, launched or treated as a supported unattended converter. |

Installed exporter source hashes: `__init__.py`
`b7a2c06c11267ff9baaeb30ebc6add17b044d27f754340f17345dc78d74db336`;
`fbx_utils.py` `66a15d79d5eaf490176b439f22fb01963efcd46e06702eff224a84135e636fb3`;
`export_fbx_bin.py` `8fd324e4ee0d25cc89cd53507b0f93c057b17b699601ac90f81085d5be09e44a`.
The installed tangent-space option explicitly covers triangle/quad meshes and is
off by default. Its source is inspected, not copied into RestoVisuals.

The local SDK manual states an FBX 2014/2015-era export target for its documented
XSI/3ds Max workflow, warns against its 2016 exporter path, requires one UV set and
unique object names per exported model, and describes supported normals and mesh
data (page 3). It also stresses correct system units before authoring/export
(page 4). Blender's observed 7400 writer is a concrete candidate to test; version
numbers alone do not validate a modern Blender-to-ksEditor pipeline.

The same manual documents an interactive editor, Open FBX, Save KN5 and persistence
operations (pages 67-70). The installed `ksEditor.bat` only starts the editor;
its config specifies .NET Framework 4.5 and saved UI settings. Neither establishes
headless conversion. No documented export command was found in the checked
launcher, config, SDK changelog or manual. A visible Batch tab is not a documented
command-line contract. No guessed flags, `--help` launch, PDB inspection,
binary decompilation, import bypass or third-party converter was used.

## Original source assets and exact geometry

[The source package](../examples/phase0l-fixture-source/README.md) contains only
original geometry, original preview-material data, an original neutral diffuse
texture, a byte-identical copy of the original Phase 0K flat normal, a contract
and a hash manifest. No Kunos sample geometry, shader binary, third-party vehicle,
track or paid texture is reused. The existing visual target is untouched.

| Source | Content / validation |
|---|---|
| [pad.obj](../examples/phase0l-fixture-source/pad.obj) | One `RV0L_TEST_PAD` object, four vertices, one planar quad, one UV set, one +Y normal; no cameras, empty nodes, animation or tangents. |
| [pad.mtl](../examples/phase0l-fixture-source/pad.mtl) | One `RV0L_NORMAL_TEST` material with relative diffuse-image reference and zero preview specular. This is a DCC-preview material, not a CSP/ksEditor shader binding. |
| [source-contract.json](../examples/phase0l-fixture-source/source-contract.json) | Exact coordinates, UVs, basis, proposed shader inputs, camera/spawn requirements and false export/native eligibility flags. |
| [neutral diffuse](../examples/phase0l-fixture-source/textures/neutral_diffuse.png) | Original 32x32 constant RGB8 128/128/128 PNG, with sRGB intent metadata; all chunks/CRCs and pixel bytes checked. Native color handling remains unverified. |
| [flat normal](../examples/phase0l-fixture-source/textures/flat.dds) | Unchanged Phase 0K 256x256/nine-mip experimental DXGI 28 DDS; SHA-256 `ce82d560691c9fcd58ca30ba22f725e48b293048547e0f4c1a77f1ac360393d1`. |
| [manifest](../examples/phase0l-fixture-source/manifest.json) | Exact byte counts and SHA-256 for all six payload files. Scoped Git attributes preserve their bytes. |

The intended pad is 12x12 metres: vertices `(-6,0,6), (6,0,6), (6,0,-6), (-6,0,-6)`.
UVs are `(0,0), (6,0), (6,6), (0,6)`, giving an intended two metres per repeat.
The source is a quad, matching the SDK preference to avoid unnecessary authoring
triangulation. Either planar diagonal yields two positive-facing triangles and
144 square source units of area. Units are an explicit authoring intention;
OBJ itself does not carry a verified metre conversion into the game.

Analytic UV derivatives are `dP/du=(2,0,0)` and `dP/dv=(0,0,-2)`.
The unit basis is T=+X, B=-Z, N=+Y, with `T cross B=N`. Positive tangent Y therefore
points toward asset-local -Z. These calculations validate the source data, not
exported FBX tangent attributes or the game's normal-map convention. Exporter
axis conversion, handedness and import must preserve the measured result.

OBJ is an intermediate source, not an input format claimed for ksEditor.
Blender's [OBJ reference](https://docs.blender.org/manual/en/4.1/files/import_export/obj.html)
describes its basic geometry/material support and lack of cameras/empty objects;
the [format overview](https://docs.blender.org/manual/en/4.4/files/import_export/index.html)
lists OBJ/FBX authoring routes. These references corroborate the source choice,
not this installed version's unexecuted import. The local version-matched exporter
files supply stronger evidence for the proposed FBX settings.

## Shader/material baseline to confirm before export

For this new owned source, the candidate is **ksPerPixelNM**, whose SDK shader
artifact is present (14,582 bytes; SHA-256
`72482e8729e6577d566a582a88a51befc5dc9bb580a15bf886a952f6e1b9dab6`).
It is a proposed simpler normal-mapped candidate, not a runtime compatibility
finding inferred from its filename. Its binary was not disassembled or modified.
This is a new source profile: Phase 0K's disabled `ksPerPixelMultiMap` selector
and `RV0K_OWNED_SURFACE` name do not match it and must not be enabled/reused.

The exact **expected baseline**, recorded as unverified in the source contract, is:

| Entry | Proposed expected value |
|---|---|
| Material / shader | `RV0L_NORMAL_TEST` / `ksPerPixelNM` |
| `txDiffuse` | `textures/neutral_diffuse.png` |
| `txNormal` | `textures/flat.dds` |
| `ksAmbient`, `ksDiffuse` | scalar 0.2, 0.6 |
| `ksSpecular`, `ksSpecularEXP` | scalar 0.0, 10.0 |
| `ksEmissive` | RGB `(0,0,0)` |
| Render state | opaque, no alpha test/transparency, front-face rendering, cast shadows |

This is an exact proposal to check against the selected material in ksEditor,
not a verified exhaustive shader declaration. Stop if any expected slot, property,
type, normal use or render flag differs; record all additional effective values
instead of silently inventing a mapping or changing to another shader. The SDK
manual itself requires selecting a matching shader and filling slots manually
(page 69), and warns that persistence alone does not transfer every transparency/
shadow setting onto a new export (page 70).

The baseline normal is the same quantized 128/128/255 candidate described in Phase
0K, including its 0.317755-degree bias under the offline decoder. Its alpha, RGB
interpretation, DDS loading and mip/sampler behavior remain native gates. The
diffuse PNG's sRGB tag is appropriate to its intended color role, separate from
normal data. An initial test expectation omitted that tag; it was corrected to
validate the actual metadata explicitly, without changing the image texels.

## Future authorized authoring/export sequence

These are future operator steps, not commands executed by this phase:

1. Review the exact tools/hashes and authoring permissions. Preserve SDK/editor
   preferences, outputs and logs that an application launch might change; define
   verified backups and rollback before launching. Keep all project, FBX,
   persistence and KN5 outputs in an owned workspace directory. Do not choose an
   alternate editor binary or change any installed version/update policy.
2. Through an approved DCC/MCP integration, inspect the existing session safely,
   preserve unrelated unsaved work and create an isolated owned scene/collection.
   Import the OBJ or author the same declared coordinates. Confirm one unique
   object/material, 12m intended span, planar normal, UVs and T/B/N. OBJ import and
   material preview are not a successful FBX export.
3. Verify the actual installed exporter/operator and selected scene context. Use
   selected-only legacy FBX export, the verified units/axis conversion, tangent
   space enabled and no animation. The installed operator exposes selection,
   unit/axis and `use_tspace` controls; it writes version 7400. Record every chosen
   setting and output hash, and restore the previous DCC context. Do not invoke
   an unreviewed converter if the source/exporter cannot meet the SDK constraints.
4. In a separately authorized interactive ksEditor operation, use **File > Open
   FBX** on that exact output. Check orientation, dimensions, unique names,
   UV/normal appearance and material inventory. Select/verify the candidate,
   explicitly assign both proposed textures and confirm all effective values,
   transparency and shadow flags. Stop on any import/texture/schema mismatch.
5. Save owned persistence and a complete material/object baseline. Use **File >
   Save KN5** to an owned workspace output. Only a successful actual operation,
   nonempty output and receipt may establish exported status. Reopen the result
   through the supported editor and verify names, material state and bindings;
   do not treat persistence loading alone as a full material-state comparison.
6. Freeze the original source, FBX, persistence, KN5, texture and configuration
   hashes. Establish the supported original track/container registration,
   collision and spawn metadata before preparing any game-load package. A lone
   model is not a complete track or a proven loadable fixture.

The existing policy makes creative applications DCC/MCP-only. ksEditor is an
authoring application; ordinary Content Manager/game GUI authorization is not
automatic permission for its GUI. Owner-operated interactive export is one
possible future path. If Friday is to operate it, a specific policy exception/
authorization or supported approved integration is required. No such operation
is attempted here. Any future approved computer control must check actual
America/New_York time and remain within Monday-Friday 08:00-17:00, with enough
time for recovery; a scheduling window does not override the DCC restriction.

## Minimal future scene and native validation sequence

The source contract proposes a parked-car spawn at `(-3,0.5,0)` and observation
target `(2,0,0)`. Near-normal/moderate/grazing camera proposals are `(2,6,0)`,
`(2,3,4)` and `(2,1,4.7)`. Up vectors are defined and nonparallel to the sightlines.
These are asset-local pose requirements, not a generated `cameras.ini` or native
spawn. Proposed `AC_PIT_0` / `AC_START_0` names, transforms, required track files,
collision/surface conventions and car ground clearance still require supported
track-specific verification. The car SDK manual is not used to invent that
contract. OBJ cannot contain those empty nodes; no track/vehicle is built here.

Once those prerequisites, exact file ownership, complete baseline, a new recovery
rehearsal, safety review and separate authorization exist, the native sequence is:

1. Cold-load the original fixture without an enhancement. Launch Assetto Corsa
   through Content Manager exclusively. Capture all effective material state and
   controlled baseline images before changing anything.
2. Use a fresh, uniquely owned disabled-by-default configuration for this exact
   model/material/shader. Verify collision-free paths, include precedence and
   exactly one material/mesh match. Preserve every unrelated property/resource.
3. Assign the same reviewed neutral normal DDS and compare controlled captures.
   Verify slot compatibility, alpha use and unchanged original material behavior;
   do not call it pixel-identical from appearance alone.
4. Test +X/-X and +Y/-Y separately against the exported tangent basis and light
   directions. Resolve orientation, normalization, DDS/mip behavior and any
   automatic conversion before using artistic detail. Stop on unexpected effects.
5. Test the original detail candidate only after all orientation gates pass.
   Retain the original Pure/PP/weather pipeline, separate Gamma/LCS calibration
   and the existing HDR NO-GO. No rendering bridge or HDR pipeline change is needed.
6. End the owned session, remove/restore only reviewed owned test resources and
   cold-load the immutable original asset/configuration. Verify shader, all typed
   properties, texture identities, flags, images and protected hashes against the
   original baseline. Static section removal alone is not recovery.

No part of this native sequence is performed. There is no current in-game
comparison, visual/material approval, FPS result or loaded-state restoration proof.

## Validation, preservation and decision

Ten new source tests pass: object/material identities, index validity, exact
positions/UVs, area/planarity/winding, analytic tangent basis/scale, preview material,
normal DDS identity, PNG chunks/CRCs/pixels, nondegenerate camera proposals, source
hashes and false export/native flags. These tests validate original data only,
not DCC import or a native shader. No old runtime implementation/test was modified;
the previous 186 test definitions are retained, with ten additions (196 total).
All 140 closeout checks pass, covering preservation, source payloads, evidence
flags, documentation links, privacy boundaries and the retained handoff history.
Unchanged prior GPU demonstrations and full historical suites are not rerun.

Private evidence is under ignored `.local/phase0l-20261104/`: preflight,
`tool-inventory.json`, SDK text/page extracts, final source tests and preservation/
Git receipts. Thirteen specifically inventoried tool/document/exporter artifacts
are hashed before/after, in addition to the previous nine reviewed sources,
29 protected files, 49 settings and approved untracked visual target. No authoring application
was launched and no installed input was modified, so no installed-state rollback
is needed. Preserve all original sources and use reviewed follow-up commits for
repository rollback. The freeware policy and owner-undecided license are unchanged.

**NO-GO for a separately authorized native test at this checkpoint.** The exact
blocking export operation is the unexecuted supported ksEditor import/material/
Save KN5 workflow, whose documented route requires interactive authoring currently
prohibited. A verified DCC/FBX roundtrip, complete material/track-load baseline and
fresh native safety authorization are also outstanding. No headless workaround is
invented. Next: obtain the specific authoring permission/integration and execute
the documented owned FBX -> ksEditor -> KN5 roundtrip, then reassess native readiness.
