# Phase 0T: original in-game baseline captured

2026-11-05. Starting verified checkpoint on `phase0/foundation`:
`4f7ba0530c8ab4724fa0d9af0fc624978343c716`.

**The separately authorized second attempt loaded the original Lexus/Drift Mansion
scene and produced private 1920×1080 baseline captures.** It exited through native
Exit/Leave controls with **code 0** at 17:18:22 Eastern. No RestoVisuals material,
shader, filter, bridge or physics change was installed. The owner's CM/editor
sessions remain open. Recovery has the explicit live-CM exception and runtime-state
coverage limits below; this is not a claim of complete user-data rollback.

Read [observations](../examples/phase0t-baseline/observations.json). Raw game images,
logs, generated configuration, replay and receipts remain ignored under
`.local/phase0t-20261105/`. No third-party media or private configuration is published.

## Authorization and actual attempts

The first preflight clock read 16:29:53. The retained 16:30 cleanup checkpoint
blocked a new launch. Current-state backups covered 29 protected files, 49 selected
settings and three runtime files. When the explicit 16:45 checkpoint approval was
processed at 16:52, its guard also refused GUI initialization/input. No GO was sent
under either expired checkpoint.

The owner subsequently extended access; the final, unambiguous instruction permits
computer-use through **18:15**, cleanup by **18:00**, for this task/date only.

| Attempt | Evidence/result |
|---|---|
| First T attempt, 16:54:26 | Existing CM Go control started the reviewed executable. Steam API initialization failed before scene loading. Error image/logs saved. |
| Intervening owner action | The game was already gone before the agent's close guard; no close/restart input was sent. Exit code/cause unknown. Owner confirmed: **Steam restarted only; settings unchanged**. |
| Explicit retry approval | Owner answered **Authorize one new baseline attempt** after fresh separate backups and recovery of first-attempt game files. No automatic retry occurred. |
| Second T attempt, 17:11:43 | Existing CM Go loaded the original scene. Private baseline captured; normal native shutdown code 0 at 17:18:22. |

The same Windows user/session and Medium integrity were observed for Steam, CM,
the game and diagnostic process while each attempt was alive. No primary-process
context mismatch was observed. The first capture used the old Steam client; the
successful retry used the owner-restarted client. Success followed that restart,
but this does not uniquely prove the underlying Phase 0R/T initialization cause.
No Steam restart, account query, repair, elevation change, software update or reset
was performed by the agent.

## Original baseline and reproducible camera procedure

Targets remain `mm_lexus_rca`, skin `Burnt_Orange Metallic`, track
`jd_drift_mansion`, layout `open`, existing VDC 2024 track skin. CM retained Practice
from Pits, Pure, 13:06, 13.5°C, Optimum and 8.1 km/h SSW. No settings were tuned.

**The loaded game's information panel instead reported** approximately 13:07,
clear/no-cloud weather, air **19°C**, road **30°C**, wind **0 km/h**, track grip
100%. These are observed panel values, not reconciled weather-controller semantics.
Simulation time was advancing; the later exterior frame's exact simulation time
and exposure were not frozen or measured. Do not label the native baseline as
the requested CM weather values without this qualification.

The existing PP configuration is Dream Realism 7.3 Gamma, with Pure Gamma 3.50
configured. Native logs explicitly report loading that PP set and a ready PP Lua
script. The configured 1920×1080 output and existing FSR/quality settings were
preserved. Captured PNG dimensions are 1920×1080; internal render resolution,
source texture precision, transfer function and HDR contract were not measured.

Camera procedure from this cold-loaded session:

1. Capture the initial in-game information panel/cockpit view.
2. Click the native **Drive** control while spawned in Pits.
3. Press **F1 once** from the loaded cockpit camera, yielding the captured rear
   exterior view with the orange car, pit grass and track asphalt visible.
4. Capture a second witness in the same view. No agent throttle, steering, brake
   or gear input was sent; the car appeared parked.
5. Press Escape, select native **Exit**, then **Leave**. The confirmation's
   “Don't ask me next time” checkbox was left unchanged.

This records repeatable operations, not a certified camera/world pose or fixed
replay frame. Two exterior captures and menu/cockpit context images are hashed
privately. A matching newly generated replay candidate was copied and hash-checked
privately; replay load, frame selection and weather reproducibility were not tested.
No exact pixel equality, tolerance-based visual equivalence or photorealism gain
is claimed. There is no trustworthy frame-time/GPU draw measurement in this run.

The known missing/empty `dm_layout_pits.kn5` warning remains, plus existing app-icon
warnings. The scene loaded despite them. No warning was concealed or repaired;
this is an as-installed baseline, not a clean-resource certification.

## Recovery and explicit limits

All pre/post data was preserved before restoring fresh-backed game files. First
attempt recovery restored five formatting-only INI files whose parsed values
matched exactly, plus four race/log/output files, after workspace rehearsals and
hash guards. Second-attempt recovery restored five fresh-backed camera/race/log/
output files after a separate workspace rehearsal. The successful game closed
normally, and its final logs witness AC/CSP/Steam API shutdown. No force termination.

The owner explicitly chose **Keep CM open; preserve working session**. Therefore
the live preference store `Values.data` was not overwritten or the app closed.
Both versions are preserved. **48 of 49 selected settings files match the original
T backup exactly; CM's live store is the declared exception.** Visible original
CM selections were rechecked. This is not 49/49 byte restoration.

Two additional files differ from an older Phase 0R receipt:
`extension/state/lua/app/WebBrowser.ini` and `extension/state/odometers.ini`.
There is no fresh T2 pretest hash for those files. Their current data was archived
and retained to avoid overwriting uncertain pre-existing state. Their complete
pretest contents/change attribution and a full user-state rollback are unverified.
No unsupported repair or old-backup overwrite was attempted.

Post-run SHA checks confirm **29 protected files, 1,265 car files, 386 track files,
13 shared configs, both 839-file SDK baseline sets and 25 original sources** match
their recorded baselines. The original untracked visual target remains unchanged.
The protected installation and material payloads were not modified. No installer,
old run-bound deployment transaction or proprietary implementation was reused.

## Closeout and next milestone

All 201 existing test definitions, including the historical 124 baseline, remain
unchanged. Project shader/code/asset bytes did not change; the unit suite was not
rerun. Nine closeout validation groups passed, covering evidence hashes,
fresh-backed recovery receipts, preservation, privacy, documentation links and
Git history. Workspace checks do
not establish native material selection, normal orientation or teardown.

Meter history: **20% five-hour / 34% weekly** at first preflight, **17%/33%** while
the timing gate was pending, then **99%/33%** when a replenished five-hour window
was observed. No reset action was invoked; **two reset credits remained available**
at closeout. The successful baseline ended optional native work; closeout read
**78%/30%**. Final live meters/SHA are in the private synchronization receipt.

The next engineering milestone is a controlled replay/camera baseline and
read-only native inventory of one opaque normal-mapped material, with exact mesh/
material/slot counts, UV/basis, original resources and config precedence. No material
enhancement is authorized by this result. Phase 0E HDR NO-GO, freeware, locked
software, owner-undecided licensing and unchanged main remain binding.
