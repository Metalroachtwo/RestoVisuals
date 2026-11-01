# Phase 0 validation record

## Current Phase 0B checkpoint

Code: `9290fde1fc9793916f0382690562979cab50af4f`, pushed and verified.
All **93 tests pass with no skips** when the optional project-local LuaJIT test
dependency is provided. A fresh 52-file tracked-source export passes the same
93 tests using that declared toolchain, without reading the private CSP/Pure
reference files. Without LuaJIT, 25 contract tests explicitly skip; 68 execute
on the Windows development host. All original 56 tests remain covered.

Actual GPU execution also passed independently from the source export: four
exact identity cases and six CPU-reference color cases on RX 5700 XT using a
separate D3D11 feature-level-11_0 context. Own COM references were released.
GPU math and compilation are now validated within that narrow scope; the
original NOT ASSESSED items below remain historical Phase 0 status, not a denial
of this new hardware evidence. No CSP game renderer was executed or certified.

The original shader failed strict identity; its corrected neutral path now has
zero channel differences in RGBA32F and RGBA16F. Color cases use documented
precision tolerances and preserve alpha exactly. See [Phase 0B](PHASE0B_RUNTIME.md)
for errors, source hashes, timing scope and the original failure evidence.

Seven targeted reference files (locked binaries, CSP manifest, Pure weather
sources, Pure LDR bridge and PP SDK) retained their hashes throughout Phase 0B.
Dream Realism's INI and checked dependency/missing-file states also remained
unchanged. A full installation audit was not repeated. The official 0.2.11
archive/reference binary was inspected privately without installation/execution.
No third-party assets/source or optional dependency binaries were tracked.

The callback observer ran only under LuaJIT synthetic hosts; actual CSP/Pure
invocation, stage/format/encoding, visual comparisons, low-memory board support
and game frame times remain pending. See [stable SDK provenance](CSP0211_REFERENCE.md)
and [Dream reference limits](DREAM_REALISM_REFERENCE.md).

## Original Phase 0 record

Date: 2026-11-01, America/New_York. Code checkpoint:
`0e5628e5e594061ee69313419ed37c6349012caa`, pushed and independently verified on
`phase0/foundation`. Later closeout documentation does not change that source.

## Reproducible results

| Check | Result | Scope |
|---|---|---|
| Python unit/integration/CLI suite | PASS, 56 tests, no skips on the Windows development host | INI parsing, no-write audit, strict schemas, vendor-neutral capability gates, memory arithmetic, benchmark definitions, context drift rejection, CLI handling, color reference and native compilation |
| Independent tracked-source export | PASS, same 56 tests; demo usable; both shaders compile | `git archive` of the code checkpoint extracted under ignored `.local/`, independent of original private observations |
| Export content comparison | PASS, 39 tracked files equal after line-ending normalization | Source-export integrity; not a release package or installer |
| Native shader compilation | PASS, both entry points ps_5_0, S_OK, warnings-as-errors | 1568/2020 bytecode bytes; no GPU dispatch or visual/performance result |
| Native GPU diagnostic | PASS, RX 5700 XT FL 12_1; software adapter excluded | Windowless D3D11 device capability; game adapter and GPU workload unmeasured |
| PowerShell 5.1 JSON pipeline | PASS, 5.1.26100.9711 inline commands | Native CLI stdout -> UTF-8 file -> Python/PowerShell reads; no execution-policy change |
| PowerShell 7 JSON pipeline | PASS, 7.6.5 | Same data flow with native CLI examples |
| Reference preservation | PASS, 112 audited entries unchanged | Before/after SHA256 comparison, including missing-file state and all 101 top-level PP INIs |
| Policy preservation | PASS | Project AGENTS starts with the existing global policy verbatim; only root project AGENTS found; no conflicting subordinate instructions |
| Sensitive content review | PASS for committed source/docs/examples | No credentials, raw machine paths/reports, proprietary game/Pure assets or third-party source staged |

Python tested: 3.14.6. The source uses Python 3.11+ syntax/APIs; other Python
versions have not been executed in this session. PowerShell checks are wrapper
compatibility checks, not a separate application implementation.

The sandbox initially denied the default test temporary directory. Tests now
create temporary fixtures under repository-local ignored `.local/test-tmp`.
The host rejected a PowerShell 5.1 script-file invocation; supported inline
commands passed without changing execution policy. A temporary shell-check
variable collision was corrected in the ignored validation helper. These
development checks did not alter the reference graphics configuration.

## Commands

```powershell
python -m unittest discover -s tests -v
python -m restovisuals compile-shader shaders/RV_ColorPrototype.hlsl
python -m restovisuals plan --config profiles/gamma.json --gpu examples/gpu-synthetic-2gb.json --adapter-index 0 --capabilities examples/capabilities-unknown.json
python -m restovisuals benchmark examples/frame-times-synthetic.csv
python -m restovisuals compare examples/frame-times-synthetic.csv examples/capture-synthetic-baseline.json examples/frame-times-synthetic.csv examples/capture-synthetic-candidate.json
```

See [CLI](CLI.md) for private audit and preservation commands. Local reports,
source ZIP/export, shell-check receipts and runtime candidate plans remain
ignored. Published evidence contains summaries and original source only.

## NOT ASSESSED

- Runtime CSP 0.2.11 support, runtime preview shader binding or loaded upscaler
  payloads, and physical legacy-board compatibility.
- GPU execution/readback of the color shader, actual pass cost/VRAM allocation,
  game frame times, FPS/1% lows, image quality or exposure behavior.
- Exact Pure hotfix package, ReShade current activation, HDR/VR output and
  rain/night/reflection compatibility.
- In-process GPU memory/workload, safe live adaptation, installer ownership,
  apply/rollback, release packaging or replay MCP operation.

No offline test or synthetic figure above is an in-game benchmark or evidence
of improved visual quality. See [compatibility gates](COMPATIBILITY.md).
