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