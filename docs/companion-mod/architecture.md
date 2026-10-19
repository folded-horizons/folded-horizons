# Architecture — Module Split

The mod is **split into independent jars**, each usable on its own —
not soft-dependencies inside one blob, but a hard module boundary. A
pack author installs exactly the modules they want; core runs with
none of the others.

## Module layout

| Module (mod id) | Depends on | Ships |
| --- | --- | --- |
| `foldedhorizons` (core) | nothing | Pocket grid/registry/allocation, Breacher, Root Binder, Dimension-Gen, Temp Keys, wall blocks + chip mechanic, expansion, grace window, collapse watcher, game-event emission, built-in fallback owner list ("parties") for team identity, **StorageNetwork SPI (no default provider — Trade Post is AE2-only)** |
| `foldedhorizons-ae2` | AE2 19.2.x, core | `AE2Bridge`, Trade Post ME backend (cross-dim remote grid access), ME-flavored Trade Post tooltips |
| `foldedhorizons-gt` | GTCEu Modern 8.x, core | GT voltage-tier detection feeding expansion tokens, GT machine-framework registration helpers (controller/singleblock boilerplate), GT recipe hooks |
| `foldedhorizons-ftb` | FTB Chunks + Teams, core | `FtbClaimAdapter` (auto-claim at materialization — manual claiming disabled inside pockets, no claim limit — auto-unclaim on collapse, re-register on conversion), team identity provider (FTB team UUIDs as registry keys), permanent chunk-loading via FTB |

Each module is a separate NeoForge jar with its own
`neoforge.mods.toml` (deps on core marked required-if-present; AE2/GT/
FTB optional). One gradle repo, subprojects, shared versioning. Core
declares **no integration code paths at all** — the adapters above ARE
the modules.

## The seams (core-owned SPIs)

Core defines small interfaces so modules plug in without core knowing
them:

- **`StorageNetwork` SPI** — `resolve(owner)` → extract/insert
  primitives + energy accounting. **Trade Post's networked mode is
  AE2-only (user decision): core registers no ME/remote provider;
  the AE2 module registers the ME provider.** The crate-based lobby
  handoff (physical input/output crates at the post) is core-owned
  and needs no storage module — it is the early-game trading path
  (pre-network players). The SPI stays core-owned so a future
  storage module could plug in without core changes.
- **`TierProvider` SPI** — "what tier token has this player reached?"
  Core default: advancement/expansion-lever events. GT module
  overrides with GT voltage tiers.
- **`TeamIdentityProvider` SPI** — maps a player to a stable group id
  + name. Core default: the built-in party list. FTB module overrides
  with FTB teams (and enables real claims).

## What a pack must supply vs. what modules guarantee

- **Mods supply** (datapack, shipped in the jar): recipes for every
  item and machine they register, plus loot tables, templates and
  dimension JSONs. A mod must be reachable in survival on its own —
  that is what makes it testable and standalone-installable
  (decision #14).
- **Pack supplies** (datapack/config): recipe **overrides** via KubeJS
  (the only KubeJS use) — replace or rebalance what the mod ships,
  rewire it into pack-specific materials, gate it behind GT tiers.
  Also: optional datapack overrides of the mod's other content,
  `pocket.exploitDimensions` list, quest content on the mod's events.
- **Core guarantees**: grid + registry + allocation, all machine
  behaviors, grace window, collapse-on-leave, address-not-door
  specials, shell-growing expansion, event emission (`cell_allocated`,
  `conversion_merged`, `unstable_pocket_collapsed`, `trade_executed`,
  `shell_broken`).

## Rules that keep the boundary honest

1. Modules may import core's API; core imports no module. Feature code
   must never check `ModList.isLoaded` — if it needs to, it belongs in
   a module.
2. No cross-mod item ids anywhere except inside the owning module.
3. All templates/loot/dimension JSONs live on overridable datapack
   paths; the mod ships only minimal defaults (empty starter cell +
   lobby + one demo meteorite pocket).
4. Core's branding, creative tab, and toasts are neutral (no
   GregTech/AE2 references).

**Consequence:** our pack installs `core + ae2 + gt + ftb`; a
tech-lite pack installs `core + ae2`; a vanilla+ pack installs core
alone and still gets pockets, walls, breacher, binder, expansion, and
**crate-based trading** (networked AE2 trading requires `core + ae2`).

## Residual risks

- AE2 19.2.x exact interface names may shift — contained to
  `AE2Bridge`.
- FTB Chunks claim API is internal/unstable — contained to
  `FtbClaimAdapter`.
- GT tier detection for expansion (v1 lever heuristic) may need a
  GTCEu API call later — isolated in one helper.
