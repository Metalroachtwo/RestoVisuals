# Original DDS header comparison

`flat-legacy-rgba8.dds` is the one original traditional-header candidate derived
from the unchanged Phase 0K flat DDS. All nine mip payloads, RGBA pixels and opaque
alpha are identical. Only the container representation differs; no compression,
gamma conversion or channel swapping was applied.

`comparison.json` records independent offline decoding. `editor-observations.json`
records the controlled ksEditor result and export-safety review. Legacy metadata
recognition passes; actual shader sampling and native compatibility remain unknown.
KN5 export is NO-GO. This folder provides no installer or enabled configuration.

See [Phase 0N](../../docs/PHASE0N_DDS_COMPATIBILITY.md) for exact masks, evidence,
limitations, recovery and reproduction. Raw editor screenshots and source exports
remain ignored. Original assets remain freeware; repository licensing is unresolved.
