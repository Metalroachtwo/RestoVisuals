# Phase 0D native observer experiment

Date: 2026-11-04. Branch `phase0/foundation`, resumed from
`5fa7c42491ecb0cd049232fc70ae35d08ca21dbb` with no tracked changes. The approved
owner-supplied reference PNG remains untracked and unchanged; its relative
location/hash and visual purpose are in [the architecture findings](DREAM_WEATHER_ARCHITECTURE.md).

## Preflight and scope

The first actual weekly reading was 100% remaining; prior readings are historical.
The 5% cutoff still prohibits all new development/research/testing. Installed
version metadata agrees with CSP preview361/build3898, CM 0.8.2913.40776 and Pure
Gamma/LCS 3.50. Saved settings select Gamma, the static Pure controller and Dream
Realism 7.3 Gamma. They are not runtime receipts.

Twenty-nine targeted protected-file hashes were captured, including the seven
prior core hashes, which still match. Forty-nine relevant settings backups are
byte/hash verified: root user configuration INIs, five rendering/weather
overrides and CM state. Two unrelated unreadable LUT/instrument entries were
excluded and not modified. This is not a whole-installation or all-user-data backup.

The owner explicitly conditionally authorized uniquely owned live files and
weekday 08:00-17:00 Eastern GUI testing. No CSP/CM version or update policy,
Pure bridge/filter slot, shared test-ground script or existing mod may be
replaced. Content Manager is the exclusive game launcher. A genuinely isolated
host remains preferred but none has been supplied/provisioned.

## Original implementation and validation

`prepare-observer-probe` stages three original Lua files with a per-run hash
manifest under a new ignored workspace directory. It does not install or launch.
The entry is inert until prepared, uses a uniquely owned lifetime guard, and
reuses the original observer unchanged. It requests no draw/texture/effect or
setting write. A ten-second host timer invokes owned stop; a subsequent
one-second timer checks for later native callbacks. These are script-timer
intervals, not guaranteed wall-clock deadlines while the host is paused/stopped.

All **118 tests pass with optional LuaJIT**, preserving the original 104 tests
unchanged. New coverage includes lifecycle/sink failures, no-callback receipts,
late callback detection, workspace-only package safety and a prior mode fault
surviving normal shutdown. A retained pre-stop snapshot prevents successful
cleanup from concealing that fault. These are synthetic contracts, not native proof.

The first deployment review returned NO-GO: file writes preceded their journal,
rollback could not resume, damaged output blocked executable removal, original
root aliases were obscured, and stop could hide an observer fault. Those paths
were revised before any game-installation write.

The revised exact-file transaction persists intent first, builds a non-loadable
uniquely named staging sibling, publishes the complete new directory by rename,
and supports resumed recovery. It disables a verified loader first, preserves
modified/unknown files and malformed output, and reports incomplete directory
rollback accurately. No recursive deletion or foreign-file writer is used.

The package-bound workspace rehearsal recovered **26 installation and 25 removal
failure points**, including partial source writes, publication, journal updates
and deletions. Repeated recovery, collision refusal, preservation of a foreign
fixture/edited source, damaged-output handling and original ancestry guards pass.
Original game-path ancestry was checked read only. These are filesystem results,
not native unload certification.

A second critical review issued **conditional GO for one observer-only run**,
bound to run `517dbe86abfa432e8f99d6b64ad860fd` and package-manifest SHA256
`c0b6ccddd587b16681c772a385df0045900e6910ecdcca6a0ff33f6b4f12227b`.
Rendering remains NO-GO pending its separate prerequisites. The reviewed package,
journal, source review and fault receipts remain ignored locally for recovery.

## Native acceptance gate and pending execution

Content Manager was opened at 11:59 Eastern for authorized read-only inspection;
no active game was present. Its own state file changed during startup, while the
selected game settings and all 29 protected files stayed unchanged. Original CM
state backup and a fresh before-game settings baseline are retained separately.

One experiment may proceed only after fresh time/usage, process, collision,
ancestry and backup checks. It must produce a terminal receipt matching the run
ID, actual preview361/build3898 and Gamma context, with a valid main callback,
clean pre-stop state, successful owned lifecycle calls and zero callbacks after
stop while rendering continues. Missing/intermediate output or zero callbacks
fails the runtime gate. Normal session exit, no remaining game process, owned
file recovery and protected/settings comparisons are required afterward.

At this documentation checkpoint, no RestoVisuals file has been installed in
the game and no game or neutral pass has run. Actual native results will be
recorded after the bounded attempt. Format/encoding, exposure stage, supported
named-effect removal, LCS execution and game frame/image comparisons remain unknown.
