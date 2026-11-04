# Phase 0E: HDR rendering contract and neutral-pass decision

Prepared 2026-11-04 from `phase0/foundation` checkpoint
`3c0e40aefd958c3de923534871ce20461e050be5`.

**Decision: NO-GO for native neutral rendering.** The bounded review did not
establish the dynamic source's format, encoding, exposure convention or the
downstream lifetime of a returned canvas. This is an evidence-backed limit of
the reviewed interfaces, not a claim that no CSP interface could ever supply
the missing contract. No shader, installer or native experiment was created.

## Scope and version provenance

The review starts with the exact gaps in [Phase 0D](PHASE0D_RUNTIME.md#neutral-rendering-remains-blocked).
It checks the corresponding installed declarations and reuses the existing
official stable SDK reference. It does not repeat SDK inventories, the native
observer, Dream analysis, D3D11 identity tests or hardware experiments.

| Source ID | Version and evidence | Boundaries |
|---|---|---|
| S1 | Installed preview361/build3898 WeatherFX SDK, `ac_wfx_impl/lib.lua`, SHA-256 `cdb084a21e9ae675fa1dc895b553d51dbadb7822a9e81c3b10af8c7a3ecea6fe` | Version-matched local public-interface annotations; reviewed read-only. Native build identity is retained Phase 0D evidence. |
| S2 | Same installation's PP SDK, `ac_pp_filters/lib.lua`, SHA-256 `c7cf5150dc41d05514628b3ce9614d87e7b222e0a54e4c4d41c0b16d7e3ed513` | Confirms the relevant PP-context declarations; no second PP-filter slot is established. |
| S3 | Existing [official CSP 0.2.11 archive](https://acstuff.club/patch/?get=0.2.11), SHA-256 `0729ccaebb403a7a6d1c40516990da8116cb5f56eea4c1fe0bdd29863a5a6ffb`; WeatherFX SDK SHA-256 `2e6f35c0050fdb9eb2d0016b0401a327e4df9fad0cb4e7b65e18621969dda999` | Extracted reference only; not installed or executed. Documentation agreement does not validate stable runtime behavior. |
| S4 | Public SDK snapshot `3aea8ce72caf0498f90e7977a488c403620a484f`: [post-processing callback](https://github.com/ac-custom-shaders-patch/acc-lua-sdk/blob/3aea8ce72caf0498f90e7977a488c403620a484f/wfx_impl/ac_postprocessing.lua), [canvas API](https://github.com/ac-custom-shaders-patch/acc-lua-sdk/blob/3aea8ce72caf0498f90e7977a488c403620a484f/common/ac_ui.lua), [PP host](https://github.com/ac-custom-shaders-patch/acc-lua-sdk/blob/3aea8ce72caf0498f90e7977a488c403620a484f/ac_pp_filters.lua) | Corroborating primary source. No verified mapping of this Git commit to either CSP release is claimed; S1-S3 supply release context. |

Private source receipts, exact local paths and bounded excerpts remain under
ignored `.local/phase0e-20261104/`. No third-party implementation is copied into
the repository. Generated installed SDK documentation itself warns that it can
omit information; silence is recorded as unknown, never an invented guarantee.

## Contract matrix

Here **documented** means a reviewed public declaration, **unknown** means a
required fact was not established, and **tested and validated** is explicitly
limited to the earlier observer where stated.

| Requirement | Confirmed behavior and source | Unresolved requirement / gate |
|---|---|---|
| Processing stage | **Documented:** `ac.onPostProcessing` runs when YEBIS is about to process; HDR/depth inputs are named, and the LDR target is already bound. A returned canvas substitutes YEBIS's HDR input (S1:17553-17559; S2:15821-15827; S3:17116-17122; S4 callback). | This is before YEBIS. The bound LDR destination does not make it a final-image callback. |
| Actual source format and precision | **Documented:** an HDR-format replacement of matching resolution is required by the callback annotation. | **Unknown:** actual resource/view format, channel precision, permitted replacement formats and conversion rules for `dynamic::pp::hdr`. |
| Transfer / linearity | The name identifies the source's role only. | **Unknown:** sampler-visible linear/encoded values and any automatic texture-view decoding. HDR, Gamma shader space and the display HDR flag establish none of these. |
| Primaries / working space | No applicable source-space declaration was identified in S1-S4. | **Unknown:** primaries, white point and any working-space transform. Do not assume Rec. 2020, ACEScg or another space. |
| Scene reference / pre-exposure | The callback receives a numeric `exposure` parameter (S1:17557; S3:17120). | **Unknown:** physical meaning, units, relationship to stored pixels, pre-exposure and any required scaling. Preserve Pure/CSP ownership; do not apply or invert the number by guesswork. |
| Exposure updates / auxiliary calls | **Documented:** distinguish `mainPass`; do not update autoexposure when `updateExposure` is false, including the described second-eye case (S1:17557; S4 callback). | No complete exposure transfer equation or auxiliary/VR rendering contract is established. Earlier zero auxiliary callbacks are not auxiliary support validation. |
| Alpha and sample conversion | No required alpha convention was found in the reviewed contract. | **Unknown:** alpha meaning, filtering/conversion requirements and whether a round trip through a chosen format is neutral. |
| Input access period | **Documented:** the named inputs are accessible at this callback stage (S1:17553-17557; S4 callback). | **Unknown:** validity outside the callback, retention across frames, aliasing/rebinding and access from another callback or asynchronous readback. No such retention was attempted. |
| Owned destination | **Documented:** `ui.ExtraCanvas` accepts explicit format/resolution; its default format is `R8G8B8A8.UNorm` (S1:16450-16458; S2:15124-15132; S3:15878-15886; S4 canvas). | Selecting a destination does not identify the source. Do not choose an HDR format until compatibility and conversion are established. |
| Returned surface lifetime | **Documented:** CSP can use the returned canvas as YEBIS input; `dispose()` releases canvas resources (S1:17557,16472-16473; S3:17120,15900-15901). | **Unknown:** when downstream consumption ends, whether CSP retains a resource reference, and the documented point at which replacement/disposal is safe. A Lua reference alone does not establish GPU completion. |
| Detach before disposal | **Documented:** the returned `ac.Disposable` is callable cancellation (S1:5379-5381,17558; S3:4638-4640,17121). **Tested and validated in Phase 0D:** observer unsubscribe followed by zero witnessed callbacks. | Cancellation stops the subscription; neither that declaration nor the observer proves that previously returned canvases are no longer consumed. Unsubscribe-before-dispose is necessary ordering in a proposed design, but its sufficiency remains unverified. |
| Resize / replacement | **Documented:** replacement resolution must match. `ac.onResolutionChange` reports window/screenshot size changes and disables automatic reload for relevant script hosts that register it (S1:3830-3835; S3:3206-3211). | **Unknown:** coverage of internal dynamic-resolution changes, safe retirement of the old surface and in-flight references. Do not add this handler assuming it is passive. |
| Shutdown / interruption | **Documented:** `ac.onRelease` is best effort; rapid closure/crash may omit it. Its optional item is weakly held (S1:5440-5447; S3:4698-4705). | A release callback cannot be the sole recovery guarantee. No returned-canvas failure/interruption behavior was validated. |

## Metadata and lifecycle findings

The targeted review of the existing image/texture declarations identified no
supported general source-format/encoding query. `ui.imageSize` reports dimensions;
`ui.imageState` reports readiness with a special-texture caveat (S1:13573,15133).
Neither discovers the HDR contract.

`ExtraCanvas:accessData` downloads an **owned** canvas asynchronously. Its typed
CPU accessors document R32FLOAT scalar data and RGBA8888 color data
(S1:16594,16630,16637; S3:16022,16058,16065). This is not a query of the dynamic
source. Copying or drawing into a chosen destination first would already impose
that destination's representation; reading it back cannot establish the original
resource's precision or transfer function. The documented copy/clone operations
and shared handle do not provide a source metadata contract either.

`ExtraCanvas:setExposure` is an override for the described YEBIS antialiasing
canvas use (S1:16537), not source pre-exposure metadata. Render-target
backup/restore declarations (S1:13335,13338) do not promise a downstream completion
fence. No private FFI call, native pointer or external graphics hook is used to
fill these gaps.

The public callback wrapper delegates to a helper. One exact public helper-path
lookup returned 404; that establishes no implementation or lifetime behavior.
No alternate-path search or private implementation investigation was pursued.
The research stops here rather than treating missing documentation as permission
to infer resource ownership.

## One supported alternative assessed

The public PP host documents a per-frame `script.update` redraw using
`dynamic::screen` and marks its script single-instance (S4 PP host). S2's
`ac.setFilterActive` (line 12120) switches that PP filter on/off; it is not a
handle for detaching a separately owned appended effect.

The [existing ownership assessment](DREAM_WEATHER_ARCHITECTURE.md#supported-interfaces-and-lifecycle-decision)
establishes that Pure occupies the active scriptable-filter slot for its LDR
bridge. Using a replacement PP script would violate that ownership boundary.
No documented independent secondary slot or reversible final-image registration
was established by this alternative. Its input encoding and downstream ordering
must not be inferred from the name `dynamic::screen` either. **Rejected for this
installation; no replacement or chaining experiment was performed.**

Pure SPICE's known addition/removal gap is retained from Phase 0D without another
search: additions alone do not establish supported removal. No private list,
replacement of another effect, or UI-only deletion is an acceptable teardown.

## Critical safety decision and conditional next plan

The current agent evaluated the source contract, resource lifecycle and rollback
requirements sequentially. **NO-GO:** independent critical prerequisites remain
unknown. This is not a new independent review or a deployment approval. No Astra
invocation was needed to identify the documented gaps. GUI authorization does not
resolve them.

The highest-value next milestone is a **version-specific maintainer/SDK contract**
answering the missing source representation and retirement guarantees. No message
was sent to maintainers. A useful authoritative answer must identify:

1. Source resource/view format, sampled representation, primaries/white point,
   alpha and exposure/pre-exposure relationship for each supported mode/version.
2. Permitted replacement formats, size rules, source-access period, downstream
   consumption boundary and safe disposal/replacement after cancellation.
3. Internal-resolution notification/reload behavior and supported error/unload
   handling, or one independently removable stage that supplies these guarantees.

Only then can an original implementation plan select an explicit destination
format, preserve Pure's scaling, define owned references through consumption and
retire surfaces at a documented safe boundary. An unbounded retained-surface list
or arbitrary frame delay is not an ownership contract.

Before deployment, obtain a fresh critical GO review, exact owned file paths and
collision checks, fresh backup hashes, registration/teardown rules and a reviewed
run-bound transaction. Rehearse its failure recovery in the workspace, then test
the proposed identity operation in the existing D3D11 harness. Preserve all 124
baseline tests. No old deployment package automatically authorizes a new run.

A future native test must use Content Manager, leave Pure's bridge/filter/weather
and exposure ownership intact, fit the weekday Eastern testing window, compare
controlled matched captures with declared exact/tolerance criteria, measure only
trustworthy timings, and prove removal/restoration. Gamma/LCS, stable/preview,
auxiliary/VR, dynamic resize and physical GPU coverage remain separate validations.

## Phase 0E validation and known-good state

This checkpoint changes documentation only. The 124-test Phase 0D baseline is
retained; its unchanged tests and runtime/shader code are verified against the
starting commit rather than unnecessarily rerunning successful tests. Phase 0E
checks document links, source-reference locations, provenance, preserved tracked
bytes and staged-content boundaries. All six validation groups passed, including
22 local links/anchors, three SDK files and 27 declaration locations. All 29
protected files and 49 selected settings files match preflight hashes; the old
probe directory is absent and the reference PNG is unchanged/untracked. These
checks do not validate native pixels.

No GUI, game session, rendering callback, shader draw, asynchronous readback or
performance capture was performed in Phase 0E. There is no native installation
diff, transaction, registration or teardown to test. No setting was intentionally
changed. Final targeted preservation results and usage are recorded in the
[handoff](PHASE0_HANDOFF.md) and ignored private receipts.

The project remains freeware; license selection remains an owner decision.
No dependency, model metadata, proprietary implementation or paid asset is added.
