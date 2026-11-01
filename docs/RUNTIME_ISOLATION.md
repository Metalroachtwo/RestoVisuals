# Runtime host isolation readiness

Phase 0C, 2026-11-01. **BLOCKED for game launch/deployment**: no validated isolated
Assetto Corsa host or native loading path is available in this workspace. The
assessment below specifies how that gate can be satisfied without changing the
owner's working stack. No game copy, VM, Sandbox, account, feature, registry
override, launcher or installer was created or started.

## Confirmed reason a same-user copy is insufficient

Content Manager's public [AcPaths source](https://github.com/gro-ove/actools/blob/master/AcTools/Utils/AcPaths.cs)
derives game user data from the Windows Documents location, including configuration,
race settings, output, logs, replays and screenshots. Its
[game preparation code](https://github.com/gro-ove/actools/blob/master/AcTools/Processes/Game.cs)
uses that race configuration path. This establishes a shared-user-state hazard;
it does not prove every native game/CSP path or identify a supported redirect.
No complete per-process user-data override was established in the bounded review.

Inference: a copied executable/content directory, a different working directory,
environment-variable changes alone, hard links or junctions do not demonstrate
isolation of Documents/AppData/Steam/mod state. Do not test that assumption by
launching the reference game. Writes through linked configuration/cache locations
would still be writes to the owner's state.

## Options and readiness

| Option | Required evidence | Current verdict |
|---|---|---|
| Independently provisioned machine or VM | Separate Windows/user data, separately licensed installation, owned snapshots, GPU/API capability and supported loading path | Preferred candidate; no ready instance supplied/verified |
| Dedicated Windows user on the same machine | Approved account/credentials, separate Documents/AppData/CM/Steam state, independent writable game/mod/cache roots | Conditional candidate; account creation/logon and complete isolation are not authorized or established here |
| Windows Sandbox | Feature/virtualization availability, licensed guest installation, GPU capability, controlled mappings and a supported loading/capture path | Documented OS candidate only; feature/runtime state and game compatibility unverified |
| Copy under the current user | Proven redirect for every writable location plus isolation of Steam/mod state | Not established; do not launch |
| Existing working installation | Experimental deployment would affect the protected stack | Outside this session's authorization |

The host registry reports Professional edition/build 26300 and the existing AMD
driver metadata remains 32.0.21043.12001. These observations do not establish a
ready VM, enabled Sandbox feature, guest licensing or GPU passthrough.

Microsoft documents [Sandbox vGPU, networking and mapped-folder controls](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file).
Writable mappings can persist guest changes to host files; input mappings would
need explicit read-only treatment and outputs a separate owned directory.
Guest rendering through a virtual GPU would not certify legacy physical boards
or comparable game performance. No feature enablement, reboot or Sandbox launch
is attempted to establish availability.

## Exact host acceptance gate

1. Identify the authorized host, owner and licensed game/Pure/CSP packages. Select
   only CSP 0.2.11/build3465 or preview361/build3898; preserve the reference install.
2. Before launch, identify resolved guest paths for executable/content, Documents,
   AppData, Steam user data, CM state, Pure/CSP configuration, shader caches,
   logs and output. None may resolve to a writable reference-host location.
3. Snapshot the isolated host and hash its owned inputs. Transfer private licensed
   content by an authorized method; do not publish it or use a shared writable
   Steam library/configuration. Do not invent command-line redirection flags.
4. Establish a supported native script host exposing the real CSP and Pure SDK
   namespaces. Load the existing read-only observer explicitly in isolation,
   preserve Pure's LDR bridge, and record the exact version/build/package.
5. Collect bounded callback receipts and verify teardown. Check PP/bypass state,
   main/auxiliary/eye flags, format/encoding, timing units and resource lifetime.
   Only then evaluate a uniquely owned named effect with documented removal.
6. Prove a neutral game-frame comparison and unchanged protected input hashes
   before color adjustments. Current standalone GPU evidence is not this gate.

Expected failure symptoms include a guest path resolving to owner Documents,
writes visible in reference hashes, unknown native APIs or texture encoding,
callback registration without a usable cleanup handle, and a callback never
invoked under Pure's active PP path. Each blocks dependent rendering work.

Rollback: stop only the owned observer when cleanup is known, preserve receipts,
then restore the isolated host's approved snapshot/owned files. Failed cleanup
stays inert and blocked; do not retry, remove another mod's registration, or
restart an application/service with unsaved work. No reference-game rollback
is needed now because no deployment or host creation occurred.
