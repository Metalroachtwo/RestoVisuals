# Bounded Dream Realism reference analysis

Date: 2026-11-01. Explicitly authorized technical investigation. Third-party
files were read only; no source, shader, LUT or parameter preset is redistributed.
No decryption, obfuscation removal, binary decompilation or access-control bypass
was attempted. Private file hashes and structural notes remain ignored locally.

## What is actually installed

Saved video configuration still names **Dream Realism 7.3 Gamma**. Its matching
INI reports version 7.3 and contains standard AC/YEBIS and CSP extension sections.
The matching plaintext Lua script, conventional nested script folder, and
encrypted-script companion were not found in the bounded PP script locations.
The loader-specific Pure weather `ppf_scripts` candidate is also absent.

The INI enables external color grading and names `dream_blue_cine.png` under its
filter-specific LUT folder. That referenced file is absent at the PP-filter
relative location. No matching filter folder was found at the checked roots.
This is a missing local dependency observation, not proof of a visible failure:
alternate runtime resource resolution, cached content and actual rendering were
not observed. Do not install, repair or replace the filter without a separate
authorized change procedure. No assets were searched for across unrelated drives.

Pure's installed Gamma loader checks its weather-specific PP script path, then
the common `pure_scripts` path, then `default_script.lua`, including encrypted
companion presence checks. The common Pure default script exists. Given these
files, source inspection predicts a fallback to Pure's default PP script; an
actual loaded-script/runtime receipt is still required to confirm it. The
encrypted candidate names were checked for existence only.

## Findings by research objective

| Objective | Evidence and conclusion | Limit |
|---|---|---|
| Gamma/LCS integration | Selected Gamma INI participates in the normal PP-filter path; installed Pure loader supplies script behavior/fallback | No Dream-specific Lua or matching LCS implementation found in bounded roots; LCS support unknown |
| Exposure | INI enables standard auto-exposure and CSP adaptation controls; Pure's default script exposes CBE/exposure handling | Static configuration and expected fallback, not measured adaptation or verified Dream custom controller |
| Tonemapping/color | INI uses standard tonemapping function ID 2, mapped by installed CSP enum to Sensitometric; color grading references the missing LUT | No proprietary custom tone shader available to analyze; no color-space correctness or appearance claim |
| Glare/bloom/godrays | Existing YEBIS/PP sections enable/configure those optical effects, with custom glare-shape controls | Configuration of engine effects is not a newly implemented Dream rendering algorithm |
| Lighting/reflections | No dedicated reflection engine or new lighting shader established from the available INI; those depend on CSP/Pure/car/track configuration | Do not attribute the whole scene's lighting/reflections to the filter or infer no other code exists elsewhere |
| APIs/callbacks/shaders | Standard INI parameters and Pure's expected default-script integration are observable; Dream-specific callable/shader source not located | No Dream callback or shader technique can be certified from absent source |
| Encoding/order | Pure parses PP settings, resolves its script and participates in PP processing; YEBIS and Pure replacement paths may differ | The INI's HDR-related settings do not establish texture encoding, full operation order, SDR/HDR conversion or a gamma/linear sampler contract |
| Low-overhead lessons | Separate calibration from engine effects; let Pure own exposure; use one verified stage, avoid duplicate bloom/sharpening/tonemapping | RestoVisuals source remains independently authored; no LUT, curve, parameter table or code copied |

The INI marks DXGI HDR output support disabled and YEBIS enabled. These are
declared filter settings, not proof of which renderer or output transfer ran.
No performance measurements or visual comparisons of Dream Realism were made.

## Safer integration avenue from the related Pure SDK inspection

The installed Pure SDK exposes `pure.pp.isEnabled()` and
`pure.pp.YEBISisBypassed()` as read-only queries. It also maps named
`pure.pp.spice.addLDRFilter` and `addHDRFilter` registration functions and separate
global HDR/LDR effect directories. This is a candidate extension path that can
preserve the existing Pure LDR bridge, unlike replacing its scriptable-filter
slot. These functions belong to Pure; they are not a Dream Realism invention.

The registration implementations replace same-name effect entries, so a future
RestoVisuals module must use its own unique name and verify ownership. A public
remove/unregister lifecycle and exact shader/table contract have not been
established. Do not call internal list-mutating helpers, claim rollback safety,
or register an effect in the reference game. The current observer records API
presence and PP/bypass state only and never calls registration or forcing APIs.

Proposed next isolated experiment: keep Pure's bridge, collect its actual
callback/PP/bypass/stage receipt, verify a supported named effect's lifecycle
and neutral rendering with engine-owned surfaces, then compare GPU output and
images before enabling color changes. Reject stage ambiguity and duplicate
exposure/tone processing. No additional LUT or full-resolution history target
is justified by these findings.

## Preservation and remaining prerequisites

The original Dream INI hash and expected missing dependencies are recorded in
the private research receipt. No Lua/shader contents, original LUT, author
metadata, raw configuration or third-party implementation was added to Git.
The GPU validation code and Lua observer were written independently.

An authorized complete package or supplied source may resolve missing companion
files; that is not permission to redistribute them. An isolated running game
host is required to identify the actual loaded script, PP order and output.
The targeted process assessment observed no running `acs`/`acs_x86` process;
none was launched. Existing in-game integration blockers remain in force.
