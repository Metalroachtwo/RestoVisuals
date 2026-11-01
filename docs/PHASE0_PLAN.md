# Phase 0 execution plan

RestoVisuals: Modern visuals. Legacy hardware.

## Scope and delivery gates

1. Preserve existing remote history; establish a verified early GitHub checkpoint.
2. Read the reference installation selectively. Never write to the game, Pure,
   CSP, Content Manager, drivers, or automatic-update policies.
3. Record evidence separately as documented, observed locally, tested and
   validated, proposed, or unknown. Local installation evidence is not proof of
   in-game compatibility or image quality.
4. Research supported CSP/Pure interfaces and FSR integration before choosing
   any new rendering hook. Target CSP 0.2.11 and 0.3.0-preview361 only.
5. Deliver a small offline engineering foundation with meaningful tests, a
   capability model, configuration validation, and conservative recommendations
   if supported by findings. No active installation or rendering deployment.
6. Publish architecture, compatibility, research, roadmap, and continuation
   documents with unresolved visual and hardware validation gates.
7. Commit, push, and independently verify the remote SHA after each work unit.

## Protected environment

- CSP development version: 0.3.0-preview361, owner-supplied build ID 3898.
- Content Manager: 0.8.2913.40776.
- Minimum compatibility target: CSP 0.2.11, requiring isolated validation.
- CSP 0.3.1 and newer: outside the authorized development scope.
- Both Pure LCS and Gamma are independent calibration targets.
- Native resolution remains supported; frame generation is never mandatory.

## Credit handling

Use actual account readings when available. Begin closeout at 6-7% weekly
remaining; start no new research or development at 5%. Preserve the final 3-5
percentage points for synchronization. These are percentage points of the
weekly allowance. If readings become unavailable, use bounded work units and
frequent verified pushes. Never infer exact usage from tokens or elapsed time.

## Evidence and publication

The repository is public. Keep private paths, raw machine reports, third-party
source, game assets, and configuration dumps under ignored `.local/`. Publish
only original source, synthetic fixtures, redacted findings, primary-source
links, and validation results. A project license has not been selected.

## Starting state, 2026-11-01

The local workspace was empty and had no Git metadata. The authorized remote
has two existing commits and a README; these were fetched and preserved.
Development proceeds on `phase0/foundation` from remote `main`.
The first actual weekly meter reading was 26% remaining, compared with the
owner's approximate 27% at authorization. No gameplay measurements exist yet.
