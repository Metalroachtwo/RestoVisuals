# Permanent freeware and external dependency boundaries

RestoVisuals official functionality remains 100% free under the permanent policy
in README and AGENTS, first pushed in `92088687608b34ea8e43b9d96ddc1a022ebb37cc`.
That checkpoint preserved existing restrictions and corrected the premature
open-source description. **Repository license selection remains pending owner
approval**; freeware does not itself grant modification/redistribution rights.

| Component | Project use | Cost/distribution boundary |
|---|---|---|
| Original RestoVisuals code, shaders and profiles | Official enhancements | No purchase/subscription/premium/trial/ad/account gate; repository license undecided |
| Python standard library and Windows system graphics APIs | Core diagnostic/validation tools | No RestoVisuals-paid access component; host OS/runtime terms remain external |
| Optional Lupa/LuaJIT test wheel | Private hash-pinned contract tests only | No end-user rendering dependency; not bundled in this repository; review upstream licenses before redistribution |
| Assetto Corsa | First target game | Separately acquired commercial game and EULA; never bundled as free project content |
| Pure | Gamma/LCS integration target | Publisher-controlled development access and distribution terms; supplied separately, no source/assets bundled |
| CSP stable/preview and Content Manager | External game stack/tools | Publisher-controlled distribution/access terms, locked versions; no binaries redistributed or updater policies altered |
| Dream Realism | Authorized technical reference | No proprietary implementation, preset/LUT package or source redistribution |

The official [Steam product page](https://store.steampowered.com/app/244210/Assetto_Corsa/)
lists the game as a purchase with a third-party EULA. Pure's
[publisher membership information](https://www.patreon.com/cw/peterboese/membership?display_app_qr=1)
describes access to development through membership. Exact fees, regional prices,
ongoing eligibility and rights for an isolated host are not specified here and
must not be inferred from RestoVisuals being free.

Prefer appropriately licensed, freely redistributable components. Do not add
commercial licensing infrastructure, accounts for local features, subscriptions,
advertisement unlocks or paid functionality. Optional donations/sponsorship may
be considered later and must not control access to enhancements.
