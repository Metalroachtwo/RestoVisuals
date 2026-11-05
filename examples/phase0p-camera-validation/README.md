# Phase 0P camera and native sampling receipts

Read [the camera report](../../docs/PHASE0P_CAMERA_VALIDATION.md).
[resumed-observations.json](resumed-observations.json) records the successful
fresh-session camera repeat, signed-X texture sampling and private KN5 export.
[native-sampling.json](native-sampling.json) contains capture hashes, exact display
comparisons, metrics and limitations. The KN5 is exported, not load-validated;
in-game integration and Phase 0E HDR rendering remain NO-GO.

[directional-dds.json](directional-dds.json) verifies the two original +X/-X legacy
DDS files against unchanged Phase 0K sources, including every mip pixel. These
reuse the Phase 0N adapter without compression, channel or color conversion.
[observations.json](observations.json) preserves the earlier blocked attempt as
history. This package is not an installer. Raw screenshots, the KN5 and private
SDK output remain ignored under `.local/phase0p-20261105/`.
