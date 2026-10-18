# Walls & Expansion

## Wall-start mechanic

The starter cell's walls are four mod blocks (`ModBlocks`):
`wall_stone`, `wall_wood`, `wall_metal`, `wall_shell` (unbreakable
exterior).

- **Behavior (`StarterWallBlock`):** mining does NOT break the block —
  on a successful break event, roll the block's loot table, leave the
  block in place, apply a small tool durability cost, play a chip
  sound. Infinite yield, per-block material table.
- Loot tables (mod-shipped under
  `data/foldedhorizons/loot_tables/...`, datapack-overridable):
  - `wall_stone` → cobblestone + occasional raw stone
  - `wall_wood` → wood scraps (4 planks' worth per ~8 chips) +
    occasional **bonsai sapling**
  - `wall_metal` → filler scrap; **with a pickaxe** (tool check in
    harvest logic) → **iron chunks + copper chunks** (mod-registered
    items, enough to bootstrap a steam-age GT chain)
- **No crafting table in the cell:** the interior template contains
  none; 2×2 crafting only until the player crafts one from 4 planks.
  The mod enforces nothing — this falls out of template + loot design.
- `wall_shell`: unbreakable (`destroyTime -1`), forms the sky-cube
  shell. Lategame tier gate allows a special tool to break shell
  blocks into corrupted space — reserved event `shell_broken`.

## Root space expansion

- Fresh root interior: `pocket.baseSize` (default 33³). Expansion is
  **not automatic**: the registry holds `expansion_stage` per cell.
- `EXPANSION_THRESHOLDS` config (list of
  `"<tier_token>:interiorSize"`, e.g. `["EV:33","IV:49","LuV:65"]`):
  tier tokens are **arbitrary strings matched against events the mod
  fires** — a non-GT pack redefines them (`["steel:25","endgame:65"]`).
  v1 hook: an explicit **Expansion Lever** block inside the root that
  reads the owner's best machine tier (via the
  [TierProvider SPI](architecture.md#the-seams-core-owned-spis)) and
  grows the interior when thresholds are met.
- Expansion is a **shell-growing operation**, not a teleport:
  `expandRoot(cell, newSize)` sweeps the difference region, fills the
  outer face with `wall_shell`, leaves interior air. Repeatable and
  SPECIAL pockets use the identical code path
  (`PocketGrid.expandInterior`).
