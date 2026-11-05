# Friday — DCC/MCP and Computer-Use Access Policy

## Priority: Mandatory operating restrictions

These user restrictions apply to all future projects unless explicitly revised by the user. General task authorization, project instructions, skills, and tool descriptions do not grant an exception. Preserve stricter project restrictions and report conflicting subordinate instructions.

### 1. Creative application access

For Maya, Blender, 3ds Max, and other creative/DCC applications:

- Use the application's authorized DCC/MCP integration exclusively.
- Perform supported scene inspection, editing, scripting, and validation through DCC/MCP.
- Never automatically substitute Windows computer-use, mouse/keyboard automation, UI scripting, or screen-based navigation.
- Never open another copy of a scene from disk merely because the live DCC connection failed.
- Preserve the user's active session, unsaved work, and original assets.

If DCC/MCP is unavailable:

1. Perform one bounded, read-only gateway health assessment using non-GUI diagnostics. Preserve any existing tighter investigation limit.
2. Identify the failed component and available logs; report uncertainty if the bounded evidence cannot identify the component.
3. Attempt only safe, previously validated, non-disruptive recovery steps.
4. Do not restart Maya, another creative application, Windows, or any service with potentially unsaved state without explicit authorization.
5. If access remains unavailable, report **BLOCKED** and stop. Wait for further instruction.

**DCC/MCP failure never authorizes computer-use fallback.**

### 2. Computer-use scheduling

Timezone: **America/New_York**, including daylight saving time. Convert the current time to this timezone before considering computer-use; do not use a fixed UTC offset.

Monday–Friday, **08:00 inclusive to 17:00 exclusive**:

- Computer-use is eligible for consideration for non-creative tasks.
- Explicit user approval is required for each specific task.
- Prefer APIs, MCP connectors, PowerShell, and other direct integrations first.

Monday–Friday, outside 08:00–17:00:

- Computer-use is disabled by default. An explicit user policy exception is required before proceeding.

Saturday and Sunday:

- Computer-use is prohibited by default.
- Do not initialize or fall back to a computer-use tool, including an inventory, app selection, browser selection, or screenshot operation.
- Request an explicit policy exception rather than proceeding.

Creative applications remain DCC/MCP-only even during permitted weekday hours. A scheduling exception does not revise the creative-application restriction.

### 3. Tool-routing enforcement

Before selecting or initializing any GUI/computer-use tool:

1. Determine whether the target is a creative application. If yes, prohibit computer-use.
2. Check the current local day/time against the permitted weekday window.
3. Verify explicit user approval for the specific non-creative action, and an explicit policy exception when outside that window.
4. Prefer available non-GUI methods.

If any requirement is not satisfied, do not invoke computer-use. Do not interpret general task authorization, saved blanket app approvals, an automatic approval reviewer, or a tool's availability as specific user approval for computer-use.

Where supported, enforce these restrictions at the tool-permission or routing layer in addition to AGENTS.md. Keep GUI automation providers disabled by default; do not enable them merely because a weekday window opens. Any task-scoped enablement requires the specific user approval and scheduling checks above, must remain limited to the approved non-creative action, and must not create persistent blanket approvals. Return temporary enablement to the disabled default when the approved task ends.

### 4. Credit conservation

- Preserve existing bounded investigation limits.
- Do not repeatedly troubleshoot an unavailable DCC gateway.
- Do not launch unrelated diagnostics or build replacement automation systems.
- Report the blocker and wait for further instruction.

### 5. Implementation and validation boundaries

- Add or maintain these rules in the appropriate existing AGENTS.md configuration without overwriting or removing unrelated instructions.
- Check for conflicting subordinate instructions and report them.
- Use filesystem editing only to implement this policy; do not invoke computer-use.
- Validate the policy and stop. Do not resume character testing automatically.
- Do not initialize creative applications, probe live scenes, open scene files, restart applications or services, or run character tests to validate this policy installation.

## RestoVisuals engineering boundaries

- First supported game: Assetto Corsa. This repository is the only development
  output location. The reference game and graphics stack are read-only in Phase 0.
- Locked: CSP 0.3.0-preview361 (owner-supplied build 3898) and Content Manager
  0.8.2913.40776. Never install, upgrade, downgrade, replace, reinstall, switch,
  or indirectly change these components or their automatic-update policies.
- Support exactly CSP 0.2.11 baseline and optional 0.3.0-preview361 development
  capabilities in one codebase with capability adapters. CSP 0.3.1 and newer are
  outside scope. Test other installations only in authorized isolation.
- Preserve Pure configuration, PP filters, shaders, drivers, and known-good game
  settings. Do not deploy prototypes into the working installation.
- Both Pure LCS and Gamma need separate calibration and validation. Do not rank
  them by hardware tier. Native resolution is always an option. Gate upscalers
  and frame generation independently on verified runtime capabilities.
- Prefer documented CSP/Pure interfaces. No custom injector, replay MCP, neural
  renderer, anti-cheat bypass, or GUI automation is authorized by Phase 0.
- Follow the access policy above. Do not start creative applications, open
  scenes, run character tests, or probe DCC gateways for this project foundation.
- Evidence labels: documented; observed locally; tested and validated; proposed;
  unknown. Offline tests do not validate visuals, gameplay FPS, or GPU support.
- Use original source and synthetic fixtures. Never publish proprietary assets,
  third-party source without permission, credentials, or private machine paths.
  Keep raw local observations under ignored .local/. Leave optional author,
  company, creator, AI model, and tooling metadata blank in project artifacts.
- Preserve existing Git history and unrelated work. Never force-push, reset or
  discard user changes, overwrite an existing checkout, change global Git
  configuration, or invent an author identity. Existing Git identity is allowed.
- Commits and pushes of authorized RestoVisuals work are explicitly permitted.
  Verify Metalroachtwo/RestoVisuals as destination, review staged content, run
  relevant checks, push at meaningful milestones, and verify remote SHA.
- Read actual weekly usage when available. Begin closeout at 6-7% remaining;
  stop new R&D at 5%; protect the final 3-5 percentage points for synchronization.
  If unavailable, use bounded work units and frequent verified checkpoints.
  Do not encode a session's starting reading as a permanent budget.
- Keep docs/PHASE0_HANDOFF.md current with actual results, pending gates,
  prerequisites, next milestone, rollback, branch, and checkpoint evidence.

## Permanent freeware policy

- RestoVisuals must remain 100% free for end users. Every RestoVisuals-developed
  graphics enhancement, shader, preset and optimization profile in an official
  release must be freely available.
- No purchase price, required subscription, paid graphics preset, premium shader
  package, paid GPU profile, paid feature tier, trial limitation or advertisement
  unlock. Never reduce free functionality to create a commercial upgrade.
- No account requirement for local rendering features. Do not add licensing,
  subscription, authentication or advertising infrastructure to enforce paid
  access or commercial feature restrictions.
- Optional donations/community sponsorship may be considered in the future;
  they must never be required for access to features.
- Use original implementations or appropriately licensed third-party components.
  Prefer freely redistributable dependencies and document separate external
  costs/distribution restrictions. Technical study of Dream Realism does not
  authorize copying or publishing its proprietary implementation or assets.
- Freeware is a pricing/distribution design requirement, distinct from open-source
  licensing. A public GitHub repository does not automatically grant broad rights
  to modify or redistribute. Do not select a repository license without the
  project owner's approval. Keep the licensing decision explicitly unresolved.

## Phase 0D scoped experiment authorization (2026-11-04)

- The owner's Phase 0D brief and follow-up GUI authorization conditionally revise
  the earlier Phase 0 blanket deployment/GUI prohibition for this task only.
  Assess isolation first. A live experiment may add uniquely owned RestoVisuals
  files only after exact paths/ownership, collision checks, verified backups,
  supported lifecycle and a tested rollback are established. Do not interpret
  this as permission to replace Pure's bridge or an existing mod/filter/script.
- Backed-up routine test configuration through supported CM/CSP/Pure/game
  interfaces is authorized. Preserve locked versions and update policies;
  stop and restore the last verified state after a failed experiment.
- GUI testing is authorized only Monday-Friday 08:00-17:00 America/New_York.
  Check the current Eastern time before use and stop at 17:00. Launch Assetto
  Corsa through Content Manager exclusively. Preserve unrelated active work.
  No creative/DCC access or persistent blanket GUI enablement is granted.
- Unknown registration/removal, format/encoding or cleanup blocks dependent
  rendering. A staged package, source declaration or synthetic rehearsal is not
  native load/unload, callback, neutral-image or game-performance validation.
- The permanent freeware policy, license-owner gate, protected installation
  versions, existing history and 5% weekly cutoff remain mandatory.

## Phase 0M original-fixture authoring exception

- The owner explicitly authorizes the Phase 0L original test-pad export task.
  Prefer the existing Blender DCC/MCP interface; computer-use for this specific
  authoring task and interactive Kunos ksEditor operation are allowed if needed.
  This revises the DCC-only and foundation no-launch/probe restrictions only
  within this task. It grants no access to unrelated projects or applications.
- The weekday 08:00-17:00 America/New_York computer-use window still applies.
  The authoring exception does not itself waive the separate scheduling gate.
  Check actual Eastern time before GUI operations; outside that window, require
  the owner's explicit scheduling exception before initializing GUI access.
- The owner subsequently answered "Authorize this export tonight" for the
  2026-11-04 evening Phase 0M run. After-hours GUI control is authorized for this
  original fixture export and its cleanup only. This exception ends with this
  run and grants no persistent scheduling or unrelated computer-use permission.
- Preserve original sources, existing sessions and unsaved work. Use separate
  owned outputs, verify relevant backups, and record real exporter results,
  scale, UVs, basis, materials and hashes. Do not substitute undocumented KN5
  writing or bypass a failed exporter. No Assetto Corsa launch/native material
  test, third-party asset change, or CSP/Pure/Dream/CM version/config change is
  authorized. Phase 0E HDR NO-GO and Phase 0J cold-recovery gates remain binding.
- Verify live allowances. Reserve approximately 15 five-hour percentage points
  for recovery, validation, documentation and synchronization; maintain the 5%
  weekly hard cutoff. Prefer one verified KN5 to additional infrastructure.
- Commit/push reviewed task results only to phase0/foundation, verify remote
  HEAD, and leave main unchanged. No permanent GUI enablement is authorized.

## Phase 0N temporary authoring access (2026-11-05 only)

- The owner authorizes RestoVisuals development computer-use from the start of
  Phase 0N until 17:00 America/New_York on 2026-11-05, including before 08:00.
  Prefer existing Blender DCC/MCP; GUI authoring fallback, ksEditor and relevant
  supported tools are explicitly allowed for this task. This temporary exception
  supersedes the earlier DCC/GUI start restrictions only within this scope/date.
- Verify actual Eastern time before operations. Begin final GUI cleanup no later
  than 16:30; finish owned-session closure, restoration and GUI evidence before
  17:00. Stop sooner if safe recovery time is insufficient. No persistent blanket
  access or authorization after the deadline is created.
- Preserve existing sessions/unsaved work, all original sources and the locked
  game/CSP/Pure/Dream/CM installation/configuration. Work only in uniquely owned
  workspace paths with fresh verified backups. No game launch, material deployment,
  arbitrary format matrix or undocumented KN5 modification is authorized.
- Compare exactly one payload-equivalent uncompressed traditional-header DDS
  against the original DX10 control. Establish decoding evidence separately from
  filenames/reload messages/metadata. KN5 export requires explicit documented
  safety-review GO and all required compatibility gates. Native testing remains
  separately gated; Phase 0E HDR NO-GO and Phase 0J recovery restrictions persist.
- Read both live allowances, review progress near 15 points consumed and preserve
  closeout/synchronization allowance plus the 5% weekly hard cutoff. Commit/push
  reviewed changes to phase0/foundation, verify remote HEAD and leave main intact.

## Phase 0O preview and sampling scope (2026-11-05)

- Today's temporary RestoVisuals GUI/DCC exception also covers Phase 0O through
  17:00 America/New_York, with final cleanup starting by 16:30. Check actual time;
  preserve existing sessions, locked software/configurations and all original
  assets. No game launch or installation/deployment is authorized.
- Reuse the validated original FBX and existing legacy DDS representation. In an
  isolated owned editor, test clear weather first, then default PP, one change at
  a time with backed-up preview preferences. Record effective illumination and
  distinguish saved defaults from actively applied settings. Stop if the preview
  stays uninformative after the bounded supported-control investigation.
- Only after an informative repeatable preview may the existing original +X/-X
  diagnostics be represented in the already validated legacy DDS container and
  compared under fixed geometry, UVs, shader, coefficients and lighting. A second
  controlled illumination direction is allowed if needed; arbitrary format or
  graphics-setting experimentation is not. Metadata/reload messages are not
  sampling proof. KN5 requires a fresh explicit safety-review GO and new owned
  output; preserve Phase 0E HDR NO-GO and Phase 0J cold-reload requirements.
- Restore original editor preferences and verify the 29 protected files, 49
  selected settings and 839 reviewed SDK files. Close owned sessions normally.
  Retain sufficient credit for verification/documentation/Git and the weekly 5%
  cutoff; use a progress review near 15 points consumed, not a rigid small cap.

## Phase 0P camera-validation scope (2026-11-05)

- Today's owner-authorized GUI/DCC exception covers the original fixture camera
  recovery through 17:00 America/New_York; start cleanup by 16:30. Recheck time,
  preserve other sessions and reuse the verified FBX and existing owned SDK mirror.
- Validate the supplied viewport controls with short recorded movements, FOV 60
  initially, and no initial scene-tree double-click. Establish the unchanged pad's
  visible face and reproduce the view in a fresh owned session. If visibility
  still fails, allow one bounded read-only flags/orientation/bounds inspection;
  stop speculation without editing geometry, winding, shader or coefficients.
- Directional normal comparisons remain conditional on the visible-pad gate.
  Reuse the established legacy representation with all texels/mips unchanged.
  KN5 requires a fresh export-safety GO; no game launch or deployment is allowed.
- Restore verified session changes, close owned applications normally and verify
  protected/source/settings/SDK hashes. Reserve approximately 15 five-hour points
  for closeout and the independent 5% weekly cutoff. Preserve existing tests,
  freeware policy, Phase 0E HDR NO-GO and Phase 0J cold-load requirements.

## Phase 0Q KN5 inspection and planning scope (2026-11-05)

- Verify the immutable Phase 0P KN5 and inspect only a byte-identical owned copy.
  Bound the inventory to existing SDK/Content Manager interfaces and documented
  public loader APIs. Do not assume a car showroom supports a standalone track.
- No custom KN5 reader/writer/patcher, tool installation, developer-option change,
  application reconfiguration or game launch is authorized. Preserve existing
  sessions, especially the owner's installed editor. Keep structural loading,
  texture decoding and rendered-resource validation distinct.
- If a suitable non-game loader is unavailable, prepare an exact original-track
  installation diff, collision checks, recovery rehearsal and cold-load/failure
  criteria in the workspace only. Explicit owner approval is required before
  staging to the game or launching any experiment.
- Today's GUI exception still ends at 17:00 Eastern, cleanup by 16:30; check time
  before GUI operations. Preserve locked versions, all prior evidence/tests,
  freeware, unresolved licensing, Phase 0E HDR NO-GO and Phase 0J recovery gates.

## Phase 0R selected real-mod testing scope (2026-11-05)

- The owner authorizes reversible experiments on the selected MM Lexus Rocket
  Bunny RC-A / JD Drift Mansion Open environment, with Burnt Orange Metallic skin.
  Identify actual IDs through CM before use; no complete original-track prerequisite
  applies to this scoped test. Preserve original KN5 files and third-party assets.
- Today's computer-use exception ends at 17:00 Eastern; begin cleanup by 16:30.
  Preserve pre-existing CM, editor and unrelated sessions. Launch the game through
  Content Manager exclusively after run-specific backups, ownership and recovery GO.
- Baseline capture is authorized. A material experiment additionally requires exact
  supported shader/normal-slot/basis and match count, config/include precedence,
  complete file manifest, verified backup and workspace transaction rehearsal.
  Reject unknown isolation or restoration. No paint/damage/glass/tyre/functional
  first target, broad replacement, physics change or arbitrary custom-HLSL injection.
- Cold-load original/enhanced/restored states when needed; static replacement
  removal alone is not recovery proof. Remove only verified manifest-owned changes,
  preserve conflicts, restore only verified owned preferences and record limitations.
- Keep private mod assets/captures under ignored .local/, locked software, 29 protected
  and 49 settings checks plus scoped target hashes, prior tests/reference, freeware,
  unresolved licensing and Phase 0E HDR NO-GO. Review near 15 allowance points used;
  preserve final cleanup/Git reserve and the independent 5% weekly hard cutoff.
- The owner subsequently answered "Allow CM cleanup restart if needed" for exact
  Phase 0R recovery. Normal CM close/reopen with verified backups is authorized;
  preserve its unsaved selection and leave the existing ksEditor untouched.
  This does not authorize Steam repair, a failed-baseline retry or any material
  activation before the Phase 0R gates pass.
- Verification errors must terminate a recovery before writing. PowerShell file
  sharing/hash errors can be non-terminating: use strict error handling and check
  native exit codes. Do not continue from an unavailable hash or reuse a past
  run's private recovery as an installer. Preserve both versions on uncertainty.

## Phase 0S Steam readiness investigation (2026-11-05)

- Read-only investigation of the Phase 0R Steam API initialization failure.
  Reuse its receipts and inventories. Keep CM closed and the owner editor untouched;
  no shaders, material textures, physics or graphics-setting investigation.
- Inspect only non-secret process/context, library and relevant log evidence.
  Compare Windows-user equality without retaining names/identifiers. Do not read
  Steam credentials, account IDs, login stores, cookies or licensing records.
  A running client does not prove signed-in/online or current entitlement.
- No Steam restart/termination, reboot, elevation change, verify/repair, software
  update/reinstall, launch retry, AppID-file workaround, DLL/config/manifest change
  or Steam licensing-data modification. Record inaccessible evidence as unknown;
  do not enable auditing or weaken access controls to obtain it.
- Today's GUI deadline and cleanup window still apply. Prefer non-activating
  APIs; do not expose account UI. Preserve allowances for documentation/Git and
  the 5% weekly cutoff. Existing freeware, license and HDR NO-GO gates persist.
