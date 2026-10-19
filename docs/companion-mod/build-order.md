# Build Order

Implementation checklist. Each step is independently testable on a
running server; nothing before step 9 requires AE2 code paths to be
load-bearing.

Tracking happens in the **git issue tracker**, not here — each step
becomes an issue when work starts.

1. `PocketType`, `PocketInstance`, `PocketGrid` (spiral + cellCenter) —
   pure logic, unit-testable.
2. `PocketRegistry` SavedData: save/load round-trip, `by_owner`
   authority, allocation cursor persistence.
3. Void dimension data files + starter-cell/lobby templates (shipped
   in the mod jar as `data/`, overridable by datapack); manual
   teleport test.
4. Materialization path (template placement + FTB claim adapter with
   graceful no-FTB fallback).
5. `BreacherBlock`/BE + menu: Personal/Team/Lobby,
   allocation-on-demand, return frames, `last_return` overlay.
6. `RootBinderBlock`/BE: merge/purge/split + grace window +
   `ConversionTicker` + claim re-registration.
7. Wall blocks + chip behavior + mod-shipped loot tables;
   iron/copper chunk items; verify 2×2-only opening.
8. `DimensionGenMultiblock` (GT multiblock, GT module): consumed-on-
   fire, meteorite template, server cursor. Core ships a vanilla
   stand-in block + BE so the jump works without GT.
9. `TempKeyItem` tiers + breacher key slot + per-team unstable cursors
   + `UnstablePocketWatcher` collapse.
10. `AE2Bridge`: node hosting, remote grid resolve, extract/insert
    primitives; `TradePostBlock`/BE + trades + visitor flow.
11. Expansion: `expandInterior`, `EXPANSION_THRESHOLDS`, Expansion
    Lever.
12. Game events for quests (FTB event triggers); polish: toasts,
    tooltips, creative tab, sounds.
