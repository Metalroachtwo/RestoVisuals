# Phase 0M: supported FBX export and ksEditor material gate

2026-11-04 evening run. Original Phase 0L source checkpoint:
`4eb90d9b9962e607fb334750497d68b376863807`; resumed from verified
`cf80bda61467c574bf1c5c12e6495128c5539876` on `phase0/foundation`.

**FBX export and supported Blender reimport passed. KN5 remains NO-GO.**
The real installed Blender exporter produced the original fixture, and ksEditor
imported its geometry and exposed the intended normal-mapped material controls.
The original normal DDS still displayed `LUM (0), 0x0` after supported binding and
reload. This does not establish a successfully decoded normal resource. No KN5
export was attempted or claimed. No Assetto Corsa launch/native test occurred.

[The sanitized export receipt](../examples/phase0m-export-evidence/export-receipt.json)
records actual settings, before/after numerical data, hashes, material values
and limitations. The unchanged [Phase 0L source](../examples/phase0l-fixture-source/README.md)
is still the source of truth; its source-only flags remain historical and unchanged.

## Access, isolation and preservation

The initial preflight at 22:22 America/New_York stopped at the scheduling gate.
The owner subsequently answered **Authorize this export tonight**; the resumed
preflight at 22:37 confirmed the task-specific authoring and after-hours exceptions.
They are recorded in [AGENTS.md](../AGENTS.md). No unrelated DCC or application
access was granted. The GUI exception ended with this run's owned-session cleanup.

One original Blender MCP request could not connect. An ordinary restricted-shell
process inventory also returned no processes; later evidence showed that this
shell cannot see the authorized desktop process namespace. It must not be used
to prove host-wide process absence. The authorized desktop launch guard checked
for existing Blender/ksEditor processes before creating the owned sessions.
There were no existing sessions to replace. No gateway restart or installation
change was attempted. GUI control used the two recorded owned process IDs only.

Blender 5.1.1 ran visibly with documented `--factory-startup` and
`--disable-autoexec`, with its user-config path redirected into the ignored run
folder. Original preferences were backed up and verified. The settings were not
saved over the original user configuration. These switches are documented in the
[Blender 5.1 command-line reference](https://docs.blender.org/manual/de/5.1/advanced/command_line/arguments.html).
No background authoring/export process was substituted for the approved GUI path.

The canonical SDK editor and dependencies were copied privately: 839 files,
144,326,531 bytes, every copied file byte-verified before launch. The selected
ksEditor executable retained SHA-256
`820a1c5de8b64074e3d32cdf1a377238da3a3e0480d03070ffa35ba98e6c122e`.
This local mirror isolated editor preferences, placeholder textures and logs
from the installed game. Alternate editor binaries were not executed. No SDK
binary, shader, manual, configuration or copied error log is published.

## Actual original authoring/export results

The owned new Blender session imported the original OBJ using source forward
-Z/up Y. World-space coordinates became the expected Blender Z-up pad:
`(-6,-6,0), (6,-6,0), (6,6,0), (-6,6,0)`. Checks passed for one quad, four vertices,
one UV set spanning 0..6, material `RV0L_NORMAL_TEST` and mesh `RV0L_TEST_PAD`.
The measured world-space basis was T=+X, B=+Y, N=+Z, corresponding to the source
T=+X, B=-Z, N=+Y convention. Metric unit scale was 1.

The installed legacy `export_scene.fbx` operator executed successfully. Relevant
settings were selected mesh only, scale 1, unit scaling, forward -Z/up Y,
`use_tspace=True`, no animation, no embedded textures and no custom properties.
The complete actual settings are in the receipt. The output is binary FBX 7400:

| Output | Bytes | SHA-256 |
|---|---:|---|
| `original_pad.fbx` | 19,260 | `49e1dc29e3e2ff976995d67e0bceaaca038e57443885814c72ea48e65ab2b474` |
| `original_pad.blend` | 98,472 | `b7244f1347b30ded51545b49dc3a9f353950aaf685101663756d2896bf97a124` |

Blender's supported FBX importer reloaded the unchanged FBX. The same positions,
UVs, basis and exact material name passed. The first inspection failed its name
assertion because deleted objects left orphan mesh data holding the old material;
Blender gave the reimported material a `.001` suffix. Removing only orphan data
in this owned session and reimporting the **same hashed FBX** resolved that name
collision. The exported file was not rewritten or renamed to bypass the check.

Tangent checks calculate the basis from supported imported mesh/UV data. They do
not prove that serialized FBX tangents survive every downstream importer unchanged.
The raw Blend/FBX remain private under
`.local/phase0m-20261104/resumed-export/exports/`: the FBX contains an absolute
workspace texture path. No binary path-stripping or unreviewed rewriting was used.

## ksEditor observations and exact blocker

The documented **File > Open FBX** operation succeeded. The legacy Windows file
dialog required backslashes; a forward-slash filename was rejected before import.
The imported geometry had the expected name/material, two triangles, scale
`1,1,1` and radius `8.485281`, consistent with the original 12x12 pad. These are
editor observations, not a KN5 or in-game measurement. The viewport remained gray;
no visual-fidelity or normal-orientation approval is claimed.

Selecting the exact **ksPerPixelNM** entry exposed these persisted values:

| Property | Final value |
|---|---|
| Depth / blend | `eDepthNormal` / `eOpaque`; alpha blend/test flags both 0 |
| `ksAmbient`, `ksDiffuse`, `ksSpecular`, `ksSpecularEXP` | 0.2, 0.6, 0, 10 |
| `ksEmissive` | RGB 0,0,0 |
| `ksAlphaRef`, `fresnelC`, `fresnelEXP`, `nmObjectSpace`, `isAdditive`, `fresnelMaxLevel` | 0 |
| `boh` | zero-valued persisted channels; semantics unknown |
| `txDiffuse`, slot 0 | `neutral_diffuse.png` |
| `txNormal`, slot 1 | `flat.dds` |

The receipt retains all four persisted value channels for each of the 12
properties, without inventing uniform types or undocumented meanings. The editor
initially selected other list entries during GUI navigation; none was exported
or treated as a reviewed substitute. The final exact shader/property state is
confirmed by supported **Save Persistence**, including one material, opaque flags,
renderability and cast shadows. The private persistence is an incomplete editor
checkpoint, not a deployable package or proven material-recovery contract.

The texture picker explicitly supports PNG/DDS. The SDK project-folder section
requires a singular **texture** directory beside the FBX; the original source's
**textures** directory is not that editor resource directory. Copies of the same
original image bytes were placed in the documented directory. The supported R
reload then reported the diffuse as **32x32**. Its rounded size display remained
0 Kb; dimensions and the actual 108-byte source are recorded separately.

The unchanged Phase 0K flat DDS was assigned to txNormal. It reported filename,
349 Kb payload and **LUM (0), 0x0** before and after supported R reload, despite a
Texture reloaded message. The original file is the existing 256x256/nine-mip,
DX10/DXGI-28 candidate. This is a failed validation gate: a success message and
filename/payload alone do not prove decode or compatibility. A legacy metadata
widget limitation versus an actual loader failure remains **unknown**. No claim
that DX10 DDS is categorically unsupported follows from this display alone.
No alternate encoding, converter, shader or KN5 writer was tried.

The inspected error log contained render exceptions, but its 22,600 bytes and
hash matched the pre-existing installed log copied before launch. An initial
suspicion of new exceptions was rejected; this log is not evidence of a new
render fault. The gray viewport's cause remains unestablished.

The observed installed File menu exposed Open FBX and Save KN5, but no Open KN5
entry. The manual's screenshot is not sufficient to establish that reopening
route in this executable. No import-filter bypass or alternate editor was used.
A supported exported-asset verification route remains a future gate.

## Recovery, validation and next milestone

Both owned applications closed normally, each with exit code 0. The original
saved Blend was retained; transient reimport changes were discarded on normal
exit. Original Blender settings, installed editor config/log, locked stack,
protected files, selected settings and visual reference are checked unchanged.
There was no game/CM launch, installed mod/configuration change, force kill,
persistent GUI enablement or restoration of unchanged settings. Private tools,
backups, copied SDK files, raw exports and screenshots remain ignored.

The existing 196 test definitions, original source manifest, all prior runtime
code, shaders, tests and references are preserved. Actual Blender assertions and
169 scoped closeout checks validate this checkpoint; unchanged historical GPU/tests
are not unnecessarily rerun. This phase adds original evidence data and
engineering documentation, not another rendering/authoring framework.

Initial allowance: 37% five-hour / 64% weekly; resumed allowance: 33% / 63%.
Formal closeout began at 18% five-hour; applications were closed at 16%, preserving
approximately the requested 15 points for recovery, evidence, documentation and
Git synchronization. Ending readings and final local/remote SHA are in
`.local/phase0m-20261104/resumed-export/evidence/final-receipt.json`.
The 5% weekly hard cutoff remains binding.

**Next milestone:** establish whether the normal DDS display represents a loader
failure or only legacy UI metadata, then review a version-compatible original
normal representation if needed. Verify a decoded normal and visible original
surface before Save KN5 and supported output verification. Do not invent that
contract or change protected software to advance. Current KN5/native readiness
is **NO-GO**; game testing is outside this authorization. Phase 0E HDR NO-GO,
Phase 0J cold-recovery restrictions, freeware and unresolved licensing remain.
