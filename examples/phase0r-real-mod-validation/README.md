# Phase 0R real-mod baseline attempt and recovery

Read [the report](../../docs/PHASE0R_REAL_MOD_VALIDATION.md).
[observations.json](observations.json) records verified identities, scoped file
baselines, configured settings and unresolved runtime gates.
[ownership-manifest.json](ownership-manifest.json) declares an empty installation
diff and immutable original identities; it is not an installer.
[failure-evidence.json](failure-evidence.json) records the single Steam-init failure,
no-retry decision and hashes of the private evidence.

The single CM baseline launch failed at Steam API initialization before scene
loading. No live material compatibility is claimed. Exact scoped restoration is
verified; CM is left closed after its restored selection was verified. Raw screenshots, mod metadata and complete
private hash/backup receipts remain ignored under `.local/phase0r-20261105/`.
No third-party asset, proprietary shader or private machine path is included.
