# Phase 0Q: original KN5 render-load and runtime readiness

2026-11-05. Starting local/remote `phase0/foundation`:
`e9cbf60d1707028add4c1e62bab930e441ab7a0d`.

**Content Manager accepted and rendered the original Track-exported KN5 through
its non-game viewer.** The original quad was visible and the viewer reported two
triangles. This resolves the absence of any demonstrated KN5 loading path after
Phase 0P. Detailed serialized material/texture auditing remains incomplete, and
**an in-game experiment is NO-GO** until the original track container and complete
installation/recovery gates are established. No driving session was launched.

Read [observations](../examples/phase0q-kn5-validation/observations.json),
[runtime readiness](../examples/phase0q-kn5-validation/runtime-readiness.json) and
[source references](../examples/phase0q-kn5-validation/source-references.json).
Raw screenshots, application state and receipts remain ignored under
`.local/phase0q-20261105/`. No KN5 or third-party source is published.

## Immutable export and actual loading route

Original source:
`.local/phase0p-20261105/resume-1014/kn5-export/rv0p_original_pad.kn5`.
Its **350,981 bytes** match SHA-256
`cc4285989205597824750c9871c44f7eeace384b02ef026dbf472fc9ea4d28fd`.
The preflight backup, inspection copy and viewer copy match the same hash, before
and after loading. The original was never opened for writing or re-exported.

The actual viewer input was a new copy under
`.local/phase0q-20261105/viewer-input/rv0q_kn5_only_fixture/`.
That folder basename was checked against installed car IDs and did not collide.
No existing car or track container was registered, replaced or used as a wrapper.

| Existing interface | Evidence and outcome |
|---|---|
| ksEditor 1.0.0.0 GUI | Phase 0P's reviewed menu provides FBX input and KN5 export; a KN5 reopen route was not established. No repeated FBX/editor experiment occurred. |
| SDK AcTools.dll 1.0.1.21 | Managed-library metadata/hash confirmed. The maintainer publishes a generic KN5 reader, but the direct legacy-host assembly load returned `0x80131515`; both installed/mirror files retain ZoneId 3. The local public KN5 type was not invoked. No unblocking, policy switch, settings change or byte-loading workaround was used. |
| Installed CM 0.8.2913.40776, plain KN5 file argument | **Tested and validated at geometry/render-load level.** Opens an internal Lite Showroom window for the reviewed copy outside a car container. No developer option, conversion utility or tool installation was required. |

The maintainer's [file handler](https://github.com/gro-ove/actools/blob/e5e5c94b8dee7511def0b670bfd5dbb233831c11/AcManager/Tools/ArgumentsHandler.cs#L288-L310)
routes a plain KN5 to the custom showroom; Alt/Shift with developer mode selects
a different conversion branch. No modifiers were held and developer settings
were not changed. The [wrapper](https://github.com/gro-ove/actools/blob/e5e5c94b8dee7511def0b670bfd5dbb233831c11/AcManager/CustomShowroom/CustomShowroomWrapper.cs#L62-L134)
has a nullable-car fallback that creates a renderer directly from the KN5 path.
This was identified before testing, rather than assuming a car showroom accepts
standalone track files. Source is an implementation reference; the installed
version's observed behavior is the local compatibility evidence.

Reproduction requires valid task/time authorization, fresh backups, a reviewed
copy/hash and no pre-existing CM viewer session. Use the existing pinned CM
executable with the copy's absolute filename as its sole argument:

```powershell
Start-Process -FilePath $reviewedCmExe -ArgumentList ('"' + $ownedKn5Copy + '"') `
  -WorkingDirectory $ownedWorkFolder -WindowStyle Normal
```

Do not use a replay, archive, folder, game-launch URI or modifier-based conversion
route. Do not enable missing developer/rendering features. If dependencies or
updates are requested, stop without accepting them. This command documents the
tested viewer entry point; it grants no standing GUI or game authorization.

## What the load actually validates

The owned window was **Lite Showroom**, with a visibly rendered quad and
`Triangles: 2`. Source [renderer information](https://github.com/gro-ove/actools/blob/e5e5c94b8dee7511def0b670bfd5dbb233831c11/AcTools.Render/Kn5SpecificForward/ForwardKn5ObjectRenderer.cs#L705-L715)
associates the triangle counter with the loaded model. There was no visible load
error dialog, and the owned process closed normally with exit **0**.

| Validation level | Phase 0Q result |
|---|---|
| Exact selected file identity | PASS: original/copies all retain the expected size/hash |
| KN5 acceptance by compatible non-game loader | PASS: plain-file route opened the renderer |
| Visible model geometry | PASS: quad rendered; two triangles reported |
| Serialized mesh name/count, vertices, UVs, tangent arrays | Not inspected by the bare viewer; Phase 0P source evidence remains separate |
| Serialized `RV0L_NORMAL_TEST` / `ksPerPixelNM` identity | Not exposed/verified here; these remain the expected Phase 0P source bindings |
| Named texture slots and exact embedded payloads | Not exposed/compared; lit surface appearance alone does not establish them |
| Resource errors | No visible error dialog; a complete resource-error log was not obtained in the bounded inspection |
| Game load, collision, spawn and driving behavior | Not tested; NO-GO |

The overlay's **SimpleNoPCSS** is CM's renderer shader set, not evidence of the
serialized material's shader name. Its HDR effects label is unrelated to the
Phase 0E dynamic-HDR contract. The displayed capped viewer FPS is not a measured
draw cost or Assetto Corsa performance result. No RestoVisuals custom HLSL was
executed in the game. No Phase 0P camera, DDS-header or signed-X experiment was
repeated, and complete normal-channel orientation remains unverified.

Private capture: `evidence/cm-window-1641214.png`; its hash is in the observation
receipt. Only the owned viewer window was inspected. The owner's existing
installed ksEditor session was left untouched.

## Original track container and proposed footprint

**No installable package or complete installation diff is approved.** The native
game addition list for this phase is empty. A candidate identity,
`rv0q_material_fixture`, was checked: its game track directory and matching
`extension/config/tracks/loaded/` config did not exist. These are scoped collision
checks, not a substitute for fresh complete precedence/collision checks later.

The installed SDK inventory and the previously inspected Kunos manual cover the
car/FBX/editor pipeline, not a complete minimum-track contract. Phase 0L's pit/start
marker names and poses remain proposals; this phase does not promote them to
version-verified requirements or invent physics/UI values.

The following is a **blocked candidate footprint**, relative to
`{AC_ROOT}/content/tracks/rv0q_material_fixture/`, not a ready installation manifest:

| Candidate path | Current readiness |
|---|---|
| `rv0p_original_pad.kn5` | Known original, hash above; proposed visible model only |
| `models.ini` | Explicit model registration proposed; exact contract/precedence must be established |
| `rv0q_fixture_support.kn5` | Missing: separately authored original support geometry and reviewed pit/start/collision requirements |
| `data/surfaces.ini` | Missing: version-supported surface keys, collision association and values |
| `ui/ui_track.json` | Missing: verified CM schema, selected-mode requirements and pit metadata |
| `ui/preview.png`, `ui/outline.png` | Proposed original UI images; necessity and content not yet established |

Additional AI, timing, map and camera requirements must be determined for the
chosen test mode rather than treated as universally mandatory. Original pad
FBX/Blend/OBJ/KN5 must remain immutable; author any support asset separately through
the supported pipeline. No CSP material-replacement config is proposed or enabled.

## Runtime safety decision and recovery rehearsal

**NO-GO for separately authorized runtime testing at this checkpoint.** Required
gates remain: authoritative track-specific requirements; original support/marker/
collision assets; complete file/hash/ownership manifest; full payload rehearsal;
material/resource questions appropriate to the test; and explicit owner approval
before game staging or launch. Today's development GUI permission does not supply
that approval. No installer or old run-bound transaction package was reused.

A bounded workspace-only rehearsal exercised the **one currently known KN5**:

- A pre-existing namespace was refused without changing its sentinel.
- An interrupted partial copy was recovered without leaving the owned directory.
- A verified copy was rolled back, preserving unrelated synthetic content and
  the immutable input hash.

All three cases passed. They validate ownership/recovery for that known-file subset,
**not** a complete track payload, game resource removal or cold-load behavior.

After a complete future manifest and review, the proposed sequence is: fresh
protected/settings baselines and collision checks; explicitly authorized additive
staging; launch through Content Manager exclusively; cold-load the reviewed
fixture; verify model registration, resource errors, physical surface, car
clearance, marker placement and material state. Record exact test car/weather/
graphics choices and preserve Pure/CSP/Dream/CM versions and ownership.

On failure, end owned sessions normally, preserve evidence and stop speculative
retries. Remove only manifest-owned additions whose hashes still match receipts;
preserve foreign/ambiguous changes. Restore only verified owned settings changes,
then cold-load the known-good baseline and recheck protected hashes. Removing a
SHADER_REPLACEMENT section is not treated as live material recovery. Exact staging
and rollback commands await a complete manifest; none are authorized here.

## Preservation, checks and closeout

The owned CM viewer closed normally at **12:27:17 America/New_York**, exit 0,
without force termination. All KN5 copies/originals remain unchanged. One CM
preferences file changed during normal viewer use; its post-run bytes were retained
privately. With CM quiescent and its exact post-run hash checked, only that file
was restored from the fresh verified backup.

All **29 protected files**, **49 selected settings**, **25 original/backup pairs**
and **839 files in each installed/mirror SDK location** match baseline. The legacy
DLL origin markers remain unchanged. No software version/update policy, game
asset, Pure bridge, original shader or approved untracked visual reference changed.
No game engine process was launched and no installed test files were added.

Ten affected fixture-source regressions pass, zero failures. All 201 existing
test definitions, including the historical 124 baseline, remain unchanged; the
full suite was not rerun. The three workspace recovery cases are reported
separately from those regressions and from actual game validation.

Live allowances began at **100% five-hour / 46% weekly**, after the five-hour
reset. The checkpoint read 87%/44% with the renderer open; formal closeout began
at **82%/44%** after normal closure. Research then stopped. Final balances and
Git synchronization are retained in the ignored receipt. No model escalation or
delegation occurred; the independent 5% weekly cutoff remains binding.

Next: establish the authoritative minimum-track contract and review original
support/marker/collision assets plus a complete installation/recovery manifest.
The demonstrated CM render-load route can be reused without repeating Phase 0P.
RestoVisuals remains freeware; repository licensing is owner-undecided. Main,
Phase 0E HDR NO-GO and Phase 0J cold-reload restrictions remain unchanged.
