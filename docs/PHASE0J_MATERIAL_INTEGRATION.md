# Phase 0J: CSP material integration feasibility

2026-11-04. Starting verified local/remote `phase0/foundation`:
`d15d28f55d68bc5707cf8ca31686a0406653b4f8`.

**Decision: CONDITIONAL GO for a future isolated, normal-only texture assignment
to one original owned fixture using an already compatible built-in shader.**
It is not deployment authorization. Direct use of the Phase 0I moment texture,
arbitrary custom-HLSL replacement on existing objects, broad automatic material
enhancement and hot-removal rollback are **NO-GO on present evidence**.
The Phase 0E HDR/canvas-lifetime NO-GO remains unchanged.

The realistic route is original surface generation followed by a validated
shader-specific texture encoding and supported material resource assignment.
CSP's built-in shader then performs the lighting. This does **not** execute
`RV_MaterialRealism.hlsl` or `RV_TextureStability.hlsl`, preserve their BRDF exactly,
or transfer their measured performance to the game.

## Scope and evidence

This is read-only investigation outside the repository. No GUI, Content Manager,
game, native renderer, SDK code or live material API was executed. No installed
shader, asset, setting, update policy or version was changed. The existing
0G-0I implementation, tests and visual target are preserved. Only original
workspace documentation and an inert proposal are development outputs.

Evidence labels: **documented** describes public documentation or SDK annotations;
**observed locally** establishes file content/presence; **tested and validated**
is limited here to static checks and preservation. All native material behavior
is **unknown** until a controlled experiment. The decision is a proposed engineering
route, not independent architecture approval. The existing foundation documents
and AGENTS rules supply the constraints; no Studio/GDD registry or engine panel
was initialized for this bounded report.

| ID | Source and scope |
|---|---|
| S1 | Installed preview361/build3898 app SDK, `extension/internal/lua-sdk/ac_apps/lib.lua`, SHA-256 `2d83a51028663e80ff97dc9173bc26446c463628851ea64edda799a9ea27d71a`. Material/scene declarations at 9631-9689, 10083-10238, 10297-10375. |
| S2 | Same installation's track SDK, `ac_track_script/lib.lua`, SHA-256 `54e00246304725fbb93309d205e6fd22831730c5f92917ecbee2361ce9c78149`. Material setters at 9469-9511, introspection/dump at 9912-10011, reset at 10040, replacements at 10124. |
| S3 | Existing official 0.2.11 extracted reference: WeatherFX SDK SHA-256 `2e6f35c0050fdb9eb2d0016b0401a327e4df9fad0cb4e7b65e18621969dda999`; material setters 8748-8790, dump 9246, reset 9292, sharing 9312, replacements 9376, projection 9449. Archive provenance remains in [CSP0211_REFERENCE.md](CSP0211_REFERENCE.md). It was not installed/executed. |
| S4 | Installed `config/cars/common/materials_pbr.ini`, SHA-256 `ac6be23646ded081167f77845086fdec2414332ce989a271f824c05847264009`, especially 13-17, 31-47, 64-66, 103-120. Public [PBR template](https://github.com/ac-custom-shaders-patch/acc-extension-config/blob/433c5537b9e9ea0a83ab1bb1a9ccb33a486e1b17/config/cars/common/materials_pbr.ini) is pinned to config commit `433c5537b9e9ea0a83ab1bb1a9ccb33a486e1b17`. |
| S5 | Installed `materials_interior.ini`, SHA-256 `01fcb738e5c685e4d66fec067372ce6ad03792a42f7d2a43874ce922a52cb13a`, especially 217-265, 383-422; [public interior template](https://github.com/ac-custom-shaders-patch/acc-extension-config/blob/433c5537b9e9ea0a83ab1bb1a9ccb33a486e1b17/config/cars/common/materials_interior.ini). Installed `materials_carpaint.ini`, SHA-256 `57691f259a6ec066e007282ff0a73abc966c697a257d8eecd99d4988c2a28866`, especially 127, 149-151, 244-315. |
| S6 | Upstream [shader replacements](https://github.com/ac-custom-shaders-patch/acc-extension-config/wiki/General-%E2%80%93-Shader-replacements), [raw readable reference](https://raw.githubusercontent.com/wiki/ac-custom-shaders-patch/acc-extension-config/General-%E2%80%93-Shader-replacements.md), [scene queries](https://github.com/ac-custom-shaders-patch/acc-extension-config/wiki/General-%E2%80%93-Scene-queries) and [UV2](https://github.com/ac-custom-shaders-patch/acc-extension-config/wiki/General-%E2%80%93-UV2), reviewed 2026-11-04. These wiki pages are mutable and not release-specific. |
| S7 | Official [Highlands configuration example](https://github.com/ac-custom-shaders-patch/acc-extension-config/blob/433c5537b9e9ea0a83ab1bb1a9ccb33a486e1b17/config/tracks/ks_highlands.ini): shader resource assignments and dynamic material-property adjustments. A reference example, not a validated configuration for this installation. |

The installed manifest still identifies `0.3.0-preview361` / build `3898`, and
Content Manager file version remains `0.8.2913.40776`. Protected hashes also match.
The prior native build witness is retained; no observer was repeated.
Common configs can update separately from the CSP binary. Local template presence
and a current public config revision do **not** prove every referenced shader is
registered in build3898 or available on 0.2.11. The existing extracted 0.2.11
reference lacks these common-template files; that is a reference-inventory limit,
not proof that 0.2.11 cannot support them. No new minimum-version number is invented.

## Capability matrix

In the HLSL column, “config only” means original HLSL source input is **unsupported
by that documented operation**. Arbitrary source execution as an existing-object
material replacement remains **unknown**. This does not deny CSP's separate
documented shader-drawing APIs.

| Supported documented feature | Applicable CSP version/evidence | Required inputs | Reversibility/lifecycle risk | Original custom HLSL | Compatibility limit | Next safe validation |
|---|---|---|---|---|---|---|
| Static `SHADER_REPLACEMENT` with `PROP_n` or `KEY_n`/`VALUE_n` | S6 documents syntax; S1/S2 and 0.2.11 S3 declare INI replacement application. Exact key/runtime compatibility still needs a witness. | Exact scoped material/mesh; existing property types; registered shader name if changing it. | Static changes persist in the loaded scene after section removal. Mesh targeting can split shared materials. | Config only; assigning `SHADER` selects a named shader, not our `.hlsl` entry point. Arbitrary replacement-source loading is unknown. | New shader may need different slots/flags, damage, skinning or passes. | Keep the fixture's shader unchanged; later vary one known scalar with explicit baseline/reload verification. |
| `RESOURCE_FILE_n`, `RESOURCE_TEXTURE_n`, `RESOURCE_REF_n`, `RESOURCE_COLOR_n` | Documented S6; resource use corroborated by installed S4/S5 and public S7. Preview installation observed; stable parser behavior untested. | Valid existing slot; disk file, KN5 texture name, original slot reference or constant color as appropriate. | Source preservation on disk is possible, but assignment is not a live undo token. | Config only. | Slot semantics, formats, color treatment, mips and sampler behavior are shader-specific. | One disabled proposal becomes a separately reviewed normal-only owned-fixture experiment. |
| Dynamic track `MATERIAL_ADJUSTMENT` property control | S6 contrasts per-frame adjustment with static replacement; S7 demonstrates property/condition configuration. Both target versions require native verification. | Exact materials, property, condition and baseline/off behavior. | Conditions can overwrite values every frame; removal/off behavior is not assumed to restore unrelated changes. | Config only; no texture-source or arbitrary HLSL entry is established here. | Does not turn legacy gloss/specular properties into a roughness-map input. No measured cost claim. | Defer; static texture assignment is the smaller first test. |
| Built-in `fuPBR` via `Material_PBR` | S4 is locally present beside preview361 and publicly documented by its template. Shader availability on preview361 and 0.2.11 is not runtime certified. | Compatible mesh; albedo; normal `txNormal2`; RGBA `txEmAoMeRo`; matching `pbrFlags` and UV scale. | Whole shader migration changes material interpretation; protect all original slots and properties. | Configures built-in shading. Our custom BRDF/moment decoder is not installed. | Normal RG/DXT5NM flag and emissive/AO/metalness/roughness packing differ from 0I. Template describes cars; track certification is unknown. | After normal-only success, use an already-compatible owned PBR material; do not convert a production road wholesale. |
| Built-in interior/detail and car-paint families | S5 observed on preview installation; public templates corroborate. Stable version-specific availability unknown. | Authored base/detail normals, masks, detail UV scale, smoothness/reflectance/metalness or paint-layer parameters. | Shared materials, damage/skin masks and LOD variants can be affected. | Configures built-ins, not original HLSL. | Interior detail blue/alpha have other meanings; car-paint normals can be damage-gated. | Separate family-specific owned profiles after exact shader/flag inventory. |
| Scene setters, `ensureUniqueMaterials`, property/texture introspection | S1/S2 and S3 declare setters, uniqueness, slot filenames and property getters. `getTextureSlotDetails` is present in preview SDK but not the reviewed 0.2.11 SDK. | Correct supported Lua host; scoped selection; expected counts and typed values. | Setter calls return the selection, not a transactional unsubscribe. Uniqueness isolates from the rest of the scene, not between all selected meshes. | Setters/config application do not accept our material HLSL source. | Declaration is not proof of callable runtime behavior. Stable adapter must use older enumeration or omit optional details. | Read-only inventory in a future owned host; no Pure/WeatherFX host replacement. |
| `SceneReference:projectShader` | S1 and S3 explicitly declare shader-source projection while updating a texture/display/canvas. | Projection parameters, target meshes, supported drawing context and shader inputs. | Own output/caching/lifecycle needed; compilation failure can halt a script. | Supported for that projection operation; **not** a demonstrated replacement of existing object-material lighting. | It paints/draws into a texture context. It does not solve the requested material integration or HDR retirement contract. | Reject for this milestone; no new drawing framework or projection workaround. |

## Texture adaptation and minimum inputs

The Phase 0H source texture contains signed float normal XYZ and straight coating
roughness; Phase 0I stores mean signed normal XYZ and mean roughness^4. Neither
is a generic CSP normal-map layout. S4's built-in PBR normal path reads RG, with
an optional DXT5NM mode; it does not declare our mean-vector-length decoder.
Its separate packed map assigns R/G/B/A to emissive/AO/metalness/roughness.
S5's detail-normal blue and alpha can instead represent occlusion and specular
information, with additional smoothness controls. One common RGBA map is therefore
unsafe across these families. Legacy `ksSpecularEXP` is not a universal roughness
map or an established numerical conversion from our GGX parameter.

The original mathematical surface and baking logic can be reused. A future
adapter must normalize the mean direction, encode it for the exact target shader,
and convert the coating moment with a fourth root where direct roughness is needed.
Packing only normalized XY loses the stored normal variance; built-in filtering
and BRDF behavior will differ. Neither optional compensation nor our cap8 sampler
policy carries across automatically. No equivalent CSP per-material anisotropy
cap or exact mip-consumption policy was established by this investigation.

The minimum asset contract must establish:

- Exact car/track model, material identity, compatible existing shader, slot names,
  flags and typed properties. A normal slot may be a damage input rather than an
  always-on surface normal. A material name alone is insufficient.
- Geometric normals and a valid tangent basis/handedness for the target normal
  mapping path, including mirrored UVs, skinning and LODs. If a shader derives a
  basis instead, that behavior needs its own evidence. No automatic tangent repair
  is established. Our XY-plane basis is not a model's tangent basis.
- UV1 with known orientation, texel density, scale and seam behavior. Optional
  detail layers or UV2 need the specific shader's convention. S6 documents separate
  UV2 patch data and limited precision; its availability on an arbitrary asset
  must not be assumed. No UV2 file is generated here.
- A supported texture container, channel decode, normal-axis signs, image origin,
  non-color data treatment, alpha meaning, complete mip payload and runtime loading
  behavior. Conventional signed-to-encoded normal conversion is a candidate to
  validate, not a verified CSP texture-view contract. Flat and axis-ramp probes
  must resolve orientation before applying artistic detail.
- Preserved authored base normals and masks. Prefer a documented detail-normal
  layer where available; replacing sculpted normal data with generic noise erases
  information. Any composition with the original needs a validated basis and method.

Exact texture views, normal signs, GPU resource formats, compression effects,
engine-generated versus authored mips, roughness transfer and native sampler
behavior remain unmeasured. The 0I payload/timing numbers apply to its own RGBA16F
fixture, not a future packed/compressed CSP asset. DDS export or conversion is not
implemented in this read-only phase. No proprietary common texture is copied.

## Candidate materials and calibration

These are engineering hypotheses, not asset certifications or visual approvals.

| Material family | Potential benefit | Required per-asset checks / exclusions |
|---|---|---|
| Asphalt | Small-scale aggregate normals and roughness variation on opaque road materials. | Road UV density and multilayer/variation masks, authored grooves, RainFX/wetness and transitions. Do not replace multilayer shaders or change physical grip/surfaces. The current regular grooves are not approved asphalt. |
| Concrete/stone | Fine porous detail and restrained roughness on compatible static opaque surfaces. | Preserve baked AO, cracks, seams, texture direction and existing detail normals; avoid one scale across walls, kerbs and large slabs. |
| Rubber | Fine surface variation for selected trim or tyre surfaces. | Distinguish tread/sidewall/interior seals, wear/dirt masks, deformation and TyresFX or other functional shaders. The road pattern is unsuitable as a universal tyre normal. |
| Car paint | Restrained micro-normal variation or a separately calibrated paint layer. | Preserve clearcoat, flakes, metallic workflow, skin colors, damage and reflection behavior. Installed paint defaults treat normals as damage; do not assume an always-on normal path. |
| Opaque environment materials | Per-family plastic, plaster or metal detail where a compatible material exists. | Different F0/metalness, baked lighting and UVs require separate profiles. Exclude glass, mirrors, foliage, water, emissive/animated/functional materials from the generic first pass. |

Shared components can include the original procedural model, unit-normal/mip tests,
conversion rules for each validated shader adapter, ownership checks and profile
format. Per-car/per-track calibration must supply asset hashes, material identities,
UV scale, normal amplitude, coating distribution, masks, LOD/skin coverage and
interaction with existing configs. A shader family is not a semantic material
classifier. Gamma and LCS need separate visual calibration under the preserved
Pure pipeline; neither is a hardware-tier shortcut. Monitor calibration stays separate.

## Generic package identification: explicit compatibility profiles

A safe generic core can distribute original algorithms and independently calibrated
profiles, not blindly apply one texture to every material. Before enabling one
profile, require asset/model version hashes, car/track/layout/skin identity, exact
shader and flags, expected slots/properties, exact material/mesh matches and counts,
and an inventory of config includes, precedence and material sharing. Same-name
materials may be distinct objects. Texture filenames alone are also insufficient.

Documented scene queries can combine material, shader, slot and LOD predicates,
but they cannot prove UV quality, physical scale or semantic intent. Names such
as ROAD, BODY or RUBBER and broad wildcard/guessed configs are not eligibility
proof. Changed hashes, ambiguous matches, missing inputs or protected/unknown
assets must skip with a reason. An unknown mod requires a new profile, not a
fallback texture. Encrypted or inaccessible source is not permission to bypass it.
No detector, runtime host, installer or automatic profile matcher is built here.

## Preservation and restoration contract

Disk preservation and loaded-scene restoration are separate obligations. S6
explicitly says removing a static replacement section does not restore original
values already applied. `ACTIVE=0`, section deletion and script unsubscribe are
therefore not established live rollback mechanisms.

S1-S3 expose useful inspection, but do not establish a complete snapshot/restore
transaction. `dumpShaderReplacements` omits some properties and may use session-only
texture identifiers. `resetSkin` only attempts to restore associated KN5 textures;
it does not promise restoration of the selected skin, config layering, shader,
flags or every property. `clone()` copies a reference, not scene/material state.
`setMaterialsFrom()` shares matching materials and subsequent edits, rather than
capturing an independent snapshot. Reference disposal is documented for associated
resources/created nodes or loaded KN5s, not an undo token for borrowed materials.
None is accepted as a generic restoration workaround.

For a future experiment, preserve immutable original KN5/skin/config/texture inputs
and a complete effective baseline: shader, all property values/types, resource
identities, flags, sharing and matched objects. Hash every relevant file. Use
uniquely owned fixture/config/texture paths after collision checks, without editing
an existing mod or shared config include. For external textures, keep original
bindings and unrelated packed channels; original R/G/B must survive an A-only
roughness change. Do not save material changes into original KN5s.

The proposed recovery boundary is **end the owned session, restore/remove only the
owned test files, and cold-load the original asset/config state**, followed by
verification of effective values, resource bindings, appearance and protected
hashes. This is a plan, not a validated reload guarantee. Rehearse exact file
transactions and interruption recovery in the workspace first. If a fresh session
does not recover the baseline, stop and investigate; do not keep trying unreviewed
live material mutations. Existing run-bound deployment scripts are not reused.

Static config avoids a new per-frame Lua/material controller, but textures still
consume memory and built-in shader changes can alter GPU cost and batching.
Per-mesh material isolation can increase draw calls. No zero-overhead, FPS, memory
saving or Phase 0H/0I performance equivalence is claimed for this route.

## Original workspace-only proposal

[phase0j_material_proposal.ini](../examples/phase0j_material_proposal.ini) has two
disabled, exact owned-fixture selectors and no includes, shader swap, scalar
changes or HLSL deployment. The first assigns only `txNormal` to an already
compatible normal-mapped fixture. The conditional second assigns `txNormal2` and
`txEmAoMeRo` on an already-PBR fixture, preserving its other resources and flags.
No referenced DDS exists or is installed. Flags, texture encoding and baseline
recovery must be resolved before either can be enabled. Parsing this example is
not a CSP runtime test.

The alternative of converting every legacy material to `fuPBR` is rejected: it
changes shader/input semantics, can lose functional behavior and has unverified
release compatibility. Dynamic material controllers add ownership/precedence
work without solving texture decoding. Shader projection is a separate drawing
operation; it is not used as a way around the material or HDR gates.

## Next safe experiment and decision gates

1. Prepare one original owned car/track fixture with a known normal-mapped built-in
   material, authored UV/tangent data and immutable baseline. Use the same locked
   preview361 build; 0.2.11 stays a separate authorized-isolation validation target.
2. Before any deployment, establish exact ownership/install diff, config precedence,
   match count, source hashes, supported activation and session end/reload steps.
   Rehearse fault recovery in the workspace. Obtain the required specific review
   and task authorization; this read-only phase grants no launch/deployment permission.
3. In that future approved native test, first capture a baseline and a neutral
   target-encoded normal, then X/Y orientation ramps. Stop on missing/extra targets,
   unexpected slot behavior, other-material changes or recovery failure. Do not
   start artistic detail or roughness while those checks are unresolved.
4. Apply one original compact normal map at a calibrated scale. Check multiple
   views, LODs, material sharing and finite mip behavior. Compare controlled images
   against the owned baseline. Keep Pure exposure, weather, PP and HDR untouched.
5. End the owned session and demonstrate cold recovery before extending to one
   existing author-approved material. Only then test the separate PBR roughness
   route, preserving non-roughness packed channels. Validate Gamma/LCS separately
   and collect trustworthy native cost/memory measurements before performance claims.

**CONDITIONAL GO** is limited to this future isolated built-in normal-texture
experiment after its gates pass. Exact preservation of 0I moment filtering,
arbitrary original material HLSL execution, hot removal and generic deployment
remain **NO-GO**. No known-good installation was placed at risk to reach this decision.

## Validation and known-good state

All **65 targeted static checks pass**. They validate the proposal's inert sections, exact selectors,
relative owned resource paths, absence of shader/include/host deployment keys,
document links, cited declaration locations and unchanged source/installation
hashes. No repeated synthetic GPU demonstration or historical game observer is
needed for documentation-only changes. The 160-test source baseline from 0I,
including the historical 124, is preserved without claiming it was rerun here.

Private receipts are under ignored `.local/phase0j-20261104/`. The 29 protected
files, 49 selected settings, approved untracked reference and nine specifically
reviewed source files are checked before/after. No restore is required because no
game file or setting is changed. Licensing remains owner-undecided; all original
RestoVisuals enhancements remain freeware and no proprietary shader/asset is
redistributed. Continue from this report and the current handoff, without treating
the disabled example as an authorized installer.
