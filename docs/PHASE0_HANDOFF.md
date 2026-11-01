# Phase 0 continuation handoff

Prepared 2026-11-01 for the next Wednesday continuation, 2026-11-04
(America/New_York). This is a durable handoff, not a scheduled automation.

## Known-good repository state

- Repository: [Metalroachtwo/RestoVisuals](https://github.com/Metalroachtwo/RestoVisuals).
- Branch: `phase0/foundation`; original `main` history was preserved.
- Most recent verified code checkpoint:
  `0e5628e5e594061ee69313419ed37c6349012caa`.
- Early upload: `c558f6d9a3051ae6ed268f8a61a62c00b6cda473`.
- Verified audit, planning, shader and capture-framework checkpoints:
  `7532280`, `bf80f1f`, `81bc380`, `ace85b7` respectively.
- The final documentation revision is discoverable from this branch's HEAD;
  a document cannot contain its own commit hash. Confirm its exact current SHA
  using `git rev-parse HEAD` and `git ls-remote origin refs/heads/phase0/foundation`.
- Existing Git identity was retained. No force push, history reset, global Git
  configuration change, proprietary asset publication or credential exposure.

At code closeout the tracked worktree was clean and its SHA matched the remote.
Final synchronization also verifies the documentation commit before reporting
completion. A private `.local/final-sync.json` receipt records the final exact
SHA and observed usage; the repository and remote refs are the durable source
of truth on another machine.

## Delivered work and files

The original README was updated in place. Added artifacts are:

- `.gitignore`, `.gitattributes`, and `AGENTS.md` with the full access policy,
  version locks, evidence, compatibility, credit and Git requirements.
- `restovisuals/`: CLI, bounded audit and preservation checks, native DXGI/D3D11
  GPU probe, shared schema validation, capability/profile planning, frame-time
  analysis/comparison, original color reference, and isolated shader compilation.
- `schemas/profile.schema.json`, `schemas/capture.schema.json`; separate
  `profiles/gamma.json` and `profiles/lcs.json` plan inputs.
- `shaders/RV_ColorPrototype.hlsl`, fully preserved original source.
- `examples/`: explicitly synthetic GPU, unknown capabilities, timing CSV and
  baseline/candidate capture sidecars usable on a fresh checkout.
- `tests/`: eight files, 56 meaningful unit/native/CLI tests.
- `docs/PHASE0_PLAN.md`, `ENVIRONMENT.md`, `RESEARCH.md`, `ARCHITECTURE.md`,
  `COMPATIBILITY.md`, `SHADER_FEASIBILITY.md`, `BENCHMARKING.md`, `CLI.md`,
  `ROADMAP.md`, `VALIDATION.md`, and this handoff.

Private `.local/` holds observations, before/after hashes, compiler receipts,
native GPU report, shell checks and an independently tested tracked-source
export. These are intentionally untracked; they are not missing public source.
No shipping release, installer, preconfigured game filter or runtime bridge exists.

## Verified findings and decisions

Reference binaries: CSP 0.3.0-preview361/build 3898 and Content Manager
0.8.2913.40776. Both Pure forks' manifests and core scripts report 3.50; package
hotfix revision unknown. Source minimums differ: Gamma 0.2.0/build 2639;
LCS 0.2.3p211/build 2974. Runtime compatibility remains untested.

Saved settings select Pure Gamma, Dream Realism 7.3 Gamma, 1920x1080, MSAA 8,
Extra FX enabled and NVIDIA Image Scaling (FSR section method ID 2). There are
101 top-level PP INIs. Preview labels advertise FSR 1.0.2, FSR 2.2.1 and FSR
3.1.2; availability, loaded payloads and frame generation have not been exercised.
Historical ReShade 6.5.1.2008 log exists; root dxgi/d3d11 loaders are absent and
current activation is unknown.

RX 5700 XT native capability measured: 8,546,471,936 dedicated bytes, D3D11 FL
12_1. Display-class registry driver 32.0.21043.12001, dated 2026-05-29. Two AMD
DXGI entries have distinct LUIDs; do not infer two physical cards or auto-select
the game's adapter. Probe-process memory is not game memory. No low-VRAM target
board, FPS gain or visual improvement has been certified.

Keep one shared engine, strict target tracks and evidence-gated adapters. Prefer
CSP/Pure interfaces; retain Pure exposure ownership. Gamma/LCS calibrations
are separate and uncalibrated. Native stays available. No injector, custom FSR
port, neural dependency or ReShade dependency is justified by this foundation.
GPU class/extra-surface ceilings are proposed policy, not profiled guarantees.
Future capture/replay integration consumes versioned profile/capture contracts;
do not develop the separate replay MCP here.

Validation: 56 tests passed both in the working checkout and an independent
39-file source export. Two SM5 pixel entry points compiled at 1568/2020 bytes.
PowerShell 5.1 inline and 7.6.5 JSON pipelines passed. All 112 selected reference
entries matched before/after. No shader was dispatched or installed, no app or
driver version changed, and no GUI/DCC application was initialized.

## Outstanding blockers and exact next milestone

Begin **Phase 0B: read-only integration evidence**, as specified in
[ROADMAP.md](ROADMAP.md). First obtain an authorized isolated CSP 0.2.11 instance
with matching SDK and a supported native integration. No safe isolated instance
or runtime game connector was established during Phase 0. Do not alter the
owner's reference installation to fill that gap or repeat broad searches.

Establish Gamma/LCS stage encoding, formats, exposure ownership, callable APIs,
timing units, pause/replay semantics, Extra FX prerequisites, buffer/reset/payload
availability and exact package versions. Generate a genuine capability receipt
with matching context. Expected result: compatibility matrix entries backed by
reproducible runtime evidence, or explicit unknown/blocked entries. Optional
features stay disabled without it. The official patch web reader hit a redirect
loop; unverified community reposts were not accepted as baseline evidence.

Then validate an identity pass and GPU readback against the CPU reference in
isolation before artistic tuning. Require visual captures/review and repeated
native/effect timing and game-memory measurements on physical legacy hardware
before claiming support or improvement. HDR, VR, night, fog, headlights, wet
surfaces, wheel/fence detail and temporal artifacts are pending. Compilation is
not visual or performance validation.

## Resume validation and rollback

1. Verify branch, status, remote destination and exact SHA; preserve any new work.
2. Read AGENTS and the evidence/architecture documents. Run the 56-test suite
   and synthetic example from [CLI.md](CLI.md), requiring Windows for native tests.
3. Re-read usage and recheck only drift-prone installed facts. Existing private
   roots are already known on the original machine; do not rescan unrelated assets.
4. Compare an explicit current audit against the prior snapshot when available.
   Do not overwrite an earlier baseline or treat missing local receipts as proof
   that files remained unchanged.
5. Satisfy Phase 0B prerequisites before runtime tests. If an authorized gateway
   is unavailable, use only the bounded read-only assessment and safe validated
   recovery allowed by policy; no GUI fallback, restarts or copied live scenes.
6. Commit/push/verify useful evidence units and preserve the synchronization reserve.

Nothing is installed by this checkpoint, so no game rollback is needed. Disable
or omit proposed modules and retain the original stack. Do not delete or reset
the repository for rollback. If source changes must be undone, review a new
revert commit, preserve user changes, and use normal non-forced synchronization.
Any later apply operation needs owned-key backups, drift detection, approval
for concrete changes and a tested restore path; no apply/restore executor exists.

## Usage accounting and policy boundaries

Owner estimate at authorization: approximately 27% weekly remaining. First
observable account reading: 26%. Latest pre-documentation reading: 22% remaining,
an exposed-meter difference of 4 percentage points. These are account-wide
integer readings, not an exact attribution of task consumption. The final
reading is recorded in the closeout receipt and final response after remote
verification. The 3-5 percentage-point reserve was intact at every observed gate;
no reset credit or purchase was used. Starting 27% is session context, not a
permanent budget rule.

The offline Phase 0 work units are complete and independently recoverable.
Remaining runtime/visual gates need the isolated environment and integration
above; they are not resolved by further unbounded offline research. Do not
automatically start character testing, a new major runtime build, an installer,
or Wednesday automation. Keep computer-use providers disabled by default; no
provider was initialized/enabled and no persistent tool permissions were changed.
