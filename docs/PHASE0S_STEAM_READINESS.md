# Phase 0S: Steam launch-readiness evidence

2026-11-05. Verified starting local/remote `phase0/foundation`:
`a98d1cb0fcc722e44719882a07d70e9c1d8a9523`.

**The failure is narrowed, but its root cause is not established.** Steam was
already running, and its own log tracked the Phase 0R game process under the
correct App ID **244210**. The reviewed game installation is present in the
configured Steam library. Current inspected Windows-user/session and integrity
levels match. These facts do not prove the failed process acquired usable Steam
interfaces, historical context equality, sign-in/online state or entitlement.
**NO-GO for a new launch or repair under this read-only investigation.**

Read the [sanitized findings](../examples/phase0s-steam-readiness/findings.json).
Phase 0R's [failure/recovery report](PHASE0R_REAL_MOD_VALIDATION.md) and
[evidence](../examples/phase0r-real-mod-validation/failure-evidence.json) remain
the authoritative record of the one failed native attempt. No new attempt occurred.

## Findings against the requested checks

| Check | Confirmed evidence | Limit |
|---|---|---|
| Steam process running | Same live client process was created before the Phase 0R failure; its creation time is on November 4. Client/UI processes are still running. | Existence is not usable API, authentication or connection proof. |
| Signed in and online | No affirmative privacy-safe visible indicator obtained. | Exact allowlisted UI labels returned no matches. No account labels, screenshot, menu activation, login store or account IDs were retrieved. Do not classify this as signed out/offline. |
| Installed library | Five configured library roots; one Assetto Corsa manifest for App ID 244210 resolves to the reviewed game root and present `acs.exe`. Manifest reports build 14923034 and StateFlags 4. | Installation metadata is not a license/active-account entitlement check. No ownership/license data was queried. |
| Windows user/session | Current Steam client, Steam UI and diagnostic process compare equal for Windows user and session. Only booleans were retained. | Previous CM and game are exited; no historical token witness was captured in Phase 0R. |
| Elevation/integrity | All three currently inspected processes are Medium integrity, not elevated. Neither checked compatibility hive has RUNASADMIN entries for CM, game or Steam. | Static flags/current tokens cannot establish the old CM/game tokens or rule out a historical mismatch. No elevation was changed. |
| Prior executable | Phase 0R receipt selected the expected `acs.exe`; CM's existing log names it at 14:33:50 and 14:35:36. | No additional executable was started here. |
| Prior Steam App ID | Steam `gameprocess_log.txt` pairs the reviewed game process with App ID 244210 at 14:33:50; console log removes that tracked process at 14:35:38. Content log marks that app running at 14:33:50. | Client process tracking does not prove `SteamAPI_Init` returned true. |
| Working directory | No explicit working-directory record found in the bounded existing launch logs. | It was not captured before the old process exited. The expected install path is not proof of its actual working directory. |
| Existing App ID file | An already-present `steam_appid.txt` contains numeric 244210. It was only read. | Presence/correct value at the game root does not prove the failed process searched that directory or used the intended environment. No file was added, moved or modified. |
| Relevant errors | Retained Phase 0R game/CSP evidence states Steam API initialization failed. Existing client logs corroborate the process/App ID timeline. | No unique client-side root-cause result was obtained. Connection-log extraction yielded no recognized affirmative status marker; that is not proof of disconnection. |

## Historical Windows evidence and privacy

Supported Windows token queries used query-only handles; Windows-user equality
was compared without serializing names or identifiers. No privilege adjustment,
application elevation, memory/environment dump or credential access was used.
Microsoft documents the query access required by
[GetTokenInformation](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-gettokeninformation).

A narrowly filtered historical Security process-creation query was denied by
Windows (`UnauthorizedAccessException`). Sysmon process-creation evidence was
not obtained. The bounded Application-error query yielded no supporting record
through the available interface. These are evidence gaps, not proof of absent
events or a clean historical context. Logging/auditing was not enabled, and no
administrative rerun was used to bypass access restrictions.

Only selected non-account library fields and safe event markers were retained.
No raw Steam/CM log copy, login/account store, passwords, tokens, cookies, Steam
account identifier or licensing record was collected. Private receipts contain
machine paths/process metadata under ignored `.local/phase0s-20261105/`;
public findings omit them. Steam UI inspection was a non-activating exact-label
query: no screenshots, clicks, menu opening, window restoration or selection change.

## Interpretation and rejected conclusions

Valve lists client availability, App ID discovery, OS-user/elevation context,
account entitlement and application setup among initialization failure conditions.
Its documentation also explains that a direct launch's App ID file is searched
in the current working directory. This is a diagnostic framework, not permission
to add/move that file or change launch settings. [SteamAPI_Init reference](https://partner.steamgames.com/doc/api/steam_api#SteamAPI_Init)

The evidence supports these narrower conclusions:

- Steam had not simply remained unstarted until after the failure: the same
  client process predates it and its logs tracked the failed game.
- The selected installation and the App ID Steam tracked agree with the intended
  Assetto Corsa target. A missing App ID file is not observed.
- A present library manifest does not establish entitlement. Current matching
  process context is not a retrospective proof for the old CM/game pair.
- No evidence supports blaming CSP, Pure, the selected car/track, shaders,
  account ownership or a specific DLL. Those were not repaired or investigated.

The remaining questions are the failed pair's actual user/integrity, working
directory and App ID environment; a privacy-safe confirmation of Steam's visible
signed-in/online state; and whether its active session can supply the game's
interfaces. Existing evidence cannot distinguish these uniquely. No cause is
invented from the generic failure message.

## Preservation and next prerequisite

Fresh checks compare the **29 protected files and 49 selected settings** against
the restored Phase 0R baselines. Existing manifests/receipts for **1,265 car
files, 386 track files, 13 shared configs and both 839-file SDK inventories** are
reused; those completed inventories are not repeated. All project code/shaders,
201 existing test definitions and the approved untracked reference are preserved.
No new functional implementation requires a unit-suite rerun; receipt/privacy,
history and preservation consistency are validated separately.

CM and the game remain closed. The owner editor is untouched, and Steam remains
running without restart or termination. No restoration transaction is required
for this read-only work. No game/Steam/CM/CSP settings, manifests, launch options,
DLLs, licensing data, update policies or access controls were written.

**Next:** owner verification of Steam's visible readiness and game availability,
without sharing account identifiers, followed only by a separately reviewed
baseline authorization with live CM/game context evidence. This report does not
authorize that launch, restart, repair, auditing change or elevated workaround.
Phase 0R material and Phase 0E HDR NO-GO remain binding. RestoVisuals remains
freeware; repository licensing is owner-undecided.

Live allowance began **31% five-hour / 36% weekly**. Bounded investigation ended
and closeout began at **25%/35%**. Final meters and verified Git SHA are retained
in the private synchronization receipt. No model escalation or delegation occurred.
