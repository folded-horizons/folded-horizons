# Pocket System

## Topology

One custom void dimension (`foldedhorizons:void_space`) hosts all
**root** and **repeatable** pockets as cells on a static grid. Exploit
tiers are **data-defined, not hardcoded**: the mod reads a config list
`pocket.exploitDimensions` (default
`["foldedhorizons:exploit_t1", "exploit_t2", "exploit_t3"]`); a pack
may ship any number of tier dimensions (or none — breaching and Temp
Keys simply have no targets). Special pockets live in one shared
dimension per body (`foldedhorizons:special`), keyed by body id. **No
dimension is created or deleted at runtime** — "temporary" is a
gameplay state, never a technical one.

- Grid pitch: **2048 blocks** between cell centers
  (`PocketGrid.PITCH = 2048`, `PocketGrid.cellCenter(cellX, cellZ)`).
- Cell (0,0) is the **Lobby**, reserved forever.
- A cell is materialized by placing a **structure template**
  (per-cell-type) centered at the cell position on first allocation.
  Before materialization the cell region is untouched void.
- `PocketType { ROOT, REPEATABLE, UNSTABLE, SPECIAL }`.

## Registry — `PocketRegistry extends SavedData`

`dimension/PocketRegistry.java` — one instance on the **overworld's**
`DimensionDataStorage`. Every pocket in every dimension lives here;
there is no per-dimension storage to lose.

```snbt
{
  next_free: 42,                          // spiral allocation cursor
  cells: {
    "12,-3": {                            // cellKey "x,z" per dimension
      dim: "foldedhorizons:void_space",
      type: "ROOT" | "REPEATABLE" | "UNSTABLE" | "SPECIAL",
      owner: <most-significant-bits, least-significant-bits>,
      owner_kind: "PLAYER" | "TEAM",
      materialized: true,
      body: "moon",                       // SPECIAL only; "" otherwise
      exhaust_index: -1,                  // UNSTABLE only
      return_dim: "minecraft:overworld",
      return_x: 128L, return_y: 64L, return_z: -300L,
      created: 1730000000000L
    }
  },
  by_owner: { "<uuid>": [ "12,-3" ] },
  cursor_by_dim: { "foldedhorizons:exploit_t1": 7 },
  team_tier_cursor: { "<teamUuid>|exploit_t1": <cellKey> },
  pending_conversions: {                  // grace-window queue
    "<cellKey>": { at_expiry: <tick>, action: "MERGE"|"PURGE"|"SPLIT",
                   actor: <uuid>, target: <uuid> }
  }
}
```

- `by_owner` maps to a **list** (an owner holds one ROOT + many
  REPEATABLE + one SPECIAL per body; exploit cells are never owned —
  transient addresses).
- `PocketInstance` is the immutable record
  `(type, dimension, cellKey, owner, ownerKind, materialized, returnPoint, createdAt)`;
  mutations go through registry methods that replace-and-save.

## Allocation — `PocketGrid`

- **Root/repeatable/special**: spiral allocation outward from (0,0).
  `next_free` indexes a precomputed spiral path; occupied cells and
  the lobby are skipped. Amortized O(1).
- **Unstable**: per-team offset. A team's first breach in a tier opens
  the tier dimension's shared cursor, then the team cursor advances by
  `teams_per_ring` (config, default 8) — different teams strip
  different pockets without colliding.
- Materialization: structure template placed at
  `cellCenter`, `materialized=true`, claim registered for the owner,
  registry saved.

## Pocket behaviors

| Type | Persistence | Uniqueness | Collapse | Expansion |
| --- | --- | --- | --- | --- |
| ROOT | permanent | 1 per owner | never | yes |
| REPEATABLE | permanent | unlimited, recursive | never | yes |
| UNSTABLE | dies on leave | spent on use | **last-player-leaves** | no |
| SPECIAL | permanent | 1 per owner per body | never | yes |

**Unstable collapse** — `UnstablePocketWatcher` (server tick, every
20 t):

1. For each materialized UNSTABLE cell with occupants > 0, count
   players inside the cell's region.
2. Count → 0: sweep the interior bounds (config `pocket.interiorSize`,
   default 33³) to air, leaving the sky-block shell, then delete the
   registry entry.
3. The spent cell is **never re-entered**; the team's per-tier cursor
   already points to the next pocket. Optional FTB auto-unclaim.
4. Crash-safe: mark the cell "dying" before the sweep, delete after;
   on restart, dying cells are re-swept.

**Special "address not door" rule** — a second copy of e.g. the Moon
multiblock does not allocate: its controller calls
`PocketRegistry.findOrAllocate(owner, SPECIAL, body)` and binds as a
second link into the same pocket.

## Dimension JSONs (mod-shipped, datapack-overridable)

`data/foldedhorizons/dimension/void_space.json` ships in the mod jar:
overworld-style dimension with a flat-void chunk generator (single
biome, no features, no mob spawning, fixed day, no weather). The mod
reads these by `ResourceKey` only — packs can re-tune them.
