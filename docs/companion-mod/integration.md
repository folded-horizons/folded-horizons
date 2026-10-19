# Integration

## AE2 19.2.x

All AE2 contact lives in the **`foldedhorizons-ae2` module**; core
never imports `appeng.*`. Core defines a storage SPI so the Trade Post
works with any backend; the AE2 module supplies the ME backend.

- **Grid node host:** `TradePostBlockEntity implements IGridHost`;
  node created via `GridHelper.createGridNode`. REQUIRE_CHANNEL off
  (controller-less friendly), `setIdlePowerUsage(tradePost.idlePower)`.
- **Cross-dimensional bridging:** AE2 19.2 grids are per-dimension by
  construction, so the Trade Post does **not** join the owner's grid
  physically. `AE2Bridge.resolveNetwork(anchorPos)` looks up the grid
  node at the stored anchor (any dimension), caches the resolved
  `IGrid`, and performs storage operations **remotely through that
  grid** (`getStorageService().getInventory()` for extract/insert,
  `getEnergyService()` for power draw). Logical remote access — no
  grid topology hacks. If AE2 ships native cross-dim bridging, only
  `AE2Bridge` changes.
- **Primitives (AE2Bridge static methods):** `extract(grid, key,
  count, mode)`, `insert(grid, key, count, mode)`. Trade commit:
  SIMULATE both legs → if both succeed, MODULATE both. Single-tick,
  atomic by construction.
- Build note: AE2 is a compile-time-only dependency;
  `AE2Bridge` is the only class importing `appeng.*`.

## GTCEu Modern 8.x — what goes where

**The machines ARE GTCEu machines.** Breacher, Root Binder, Dim-Gen
and Trade Post use the GTCEu Modern machine framework — GT multiblock
controllers / singleblocks with real formation logic, EU energy, tier
gating and GT textures. GTCEu contact lives entirely in the
**`foldedhorizons-gt` module**; core has zero GT imports.

Why the framework:

1. **They are GT machines to the player.** Tiered energy intake (LV
   breacher, LV Dim-Gen, HV upgrades later), GT casings, formation
   preview and tooltips come for free — consistent with every other
   machine in the pack.
2. **Energy speaks EU.** Breach costs (`pocket.breachEnergyCost`,
   default 10,000,000 EU unstable / 100,000 EU root-lobby) are paid
   from the multiblock's GT energy buffer, charged by GT cables — no
   FE/EU conversion layer.
3. **Recipe hooks** (crafting the machines, Temp Keys) go through
   KubeJS recipes (the only KubeJS use).
4. **What stays mod-side (core, no GT imports):** the pocket registry,
   allocation, grace window, collapse watcher, trade logic — the
   framework runs the machines, the mod runs the dimension logic
   behind them.

Porting note: the older "custom vanilla-style blocks" plan is
superseded — `machine/` stubs will be reworked onto the GTCEu
framework in build-order step 5+.

## Mod vs. data

**Decision: ALL logic lives in the mod. KubeJS is used for RECIPES
ONLY.** No gameplay behavior is implemented in KubeJS scripts.

**In the mod (code):** everything with behavior — registry,
allocation, collapse, expansion, machines, grace window, wall blocks +
loot logic, AE2/FTB adapters, event emission, config (`ModConfig`).

Concretely:

- Wall loot tables, dimension JSONs, structure templates, and custom
  items (iron/copper chunks, Temp Keys) ship in the mod jar as
  standard datapack content (`data/foldedhorizons/...`). Packs can
  still datapack-override them — a vanilla mechanism, not a KubeJS
  dependency.
- Quest integration uses the mod's emitted game events directly
  (FTB Quests task types / event triggers); no KubeJS glue scripts.
- Default data (starter cell, lobby, demo meteorite pocket) lives in
  the mod jar so the mod works standalone.

**In KubeJS (recipes only):** GT-tiered recipes for Temp Keys,
machines, expansion lever, starter-cell crafting table (4 planks), and
pack recipe rebalancing. Nothing else.

**Rule of thumb:** behavior/state/tuning/content → the mod
(datapack-overridable). Crafting recipe → KubeJS. A future need that
seems to require KubeJS logic → extend the mod's config instead.

## Tick logic

- `UnstablePocketWatcher` (server tick, every 20 t): occupancy scan →
  collapse when zero occupants.
- `ConversionTicker` (every 10 t): drain expired pending conversions.
- `TradePostBlockEntity.serverTick` (every 20 t per BE): keep the grid
  node alive; trades execute synchronously on confirmation.
- No per-tick registry scanning; no per-tick AE2 queries. Heavy work
  is event-driven.

## Save format

Single `SavedData` blob (`foldedhorizons_pockets`) on the overworld's
`DimensionDataStorage`; SNBT shape in
[pocket-system.md](pocket-system.md#registry--pocketregistry-extends-saveddata).
Version field `v:1` for migrations. Pocket *content* is ordinary world
data in the void dimensions — nothing extra to save. Trade configs
live in the Trade Post BE's own NBT.
