# Original material-pad source

Source-only checkpoint: one 12-by-12 metre intended pad, one quad, one UV set,
one material. No FBX, KN5, Blender scene, native track package or exporter is
included. No DCC or exporter application was launched to prepare these files.

`pad.obj` / `pad.mtl` are original geometry and DCC-preview material inputs.
`source-contract.json` gives the exact proposed basis, shader expectations,
camera/spawn requirements and unresolved gates. OBJ contains no tangents,
cameras or empty nodes. The native shader binding is not carried by the MTL.

`textures/neutral_diffuse.png` is original constant RGB8 source data.
`textures/flat.dds` is an unchanged copy of the original Phase 0K flat candidate.
Its native decode is unverified; it is not an exactly neutral signed vector
under the declared offline decoder. There are no enhancement settings to enable.

The installed legacy FBX exporter and ksEditor provide a documented candidate
route. Actual DCC import, FBX export, ksEditor import/Save KN5 and game load are
all pending. Follow docs/PHASE0L_FIXTURE_PIPELINE.md in the repository. Do not
launch tools or substitute conversion utilities from this source package.

All geometry and texture inputs here are original RestoVisuals assets. No SDK
binary, manual, shader source, third-party car/track or paid texture is included.
RestoVisuals remains freeware; repository licensing is unresolved.
