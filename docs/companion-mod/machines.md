# Machines

Class stubs live under
`companion/src/main/java/dev/foldedhorizons/core/machine/`.

## Dimensional Breacher — GT multiblock (GTCEu framework)

`machine/BreacherBlock` + `machine/BreacherBlockEntity`. Built on the
GTCEu machine framework — a real GT multiblock with a GT controller
(see [integration.md](integration.md#gtceu-modern-7x-what-goes-where)).

- Formation: 3×3×3 hollow casing shell, controller center; a "breach
  frame" interior block (the return pad) sits in the middle layer.
- Energy: GT EU (tiered intake); config `pocket.breachEnergyCost`
  (default 10,000,000 EU) for UNSTABLE entry; flat 100,000 EU per
  root/lobby breach; free return trip.
- `use()` opens `BreacherMenu` — a pure destination list:
  - **Personal** → the player's ROOT; allocate+materialize if absent.
  - **Team** → the FTB team's ROOT; if the team has none, allocate
    fresh (the team space is born here).
  - **Lobby** → teleport to lobby spawn, cell (0,0).
  - **Temp Key slot**: consumes the key, opens the team's next
    UNSTABLE pocket of the key's tier, burns breach energy, teleports
    the inserting player.
- **Refusal rules** (checked before teleport): pending conversion
  touching the destination cell ("Space is re-addressing (Ns
  remaining)"), unformed multiblock, insufficient energy.
- **Return:** the destination's breach frame reads the player's
  recorded return point from the registry (`last_return` overlay map,
  keyed by player UUID — multiple players can return through one
  frame).

## Root Binder — GT singleblock

`machine/RootBinderBlock` + `RootBinderBlockEntity`. Lives inside the
team space. GUI: three buttons operating on the inserting player —
**Merge / Purge / Split** (behavior in
[`../design/machines.md`](../design/machines.md#root-binder-gt-singleblock)).

- **30-second grace window** (config `pocket.graceWindowSeconds`,
  default 30): a confirmed action writes a `pending_conversions` entry
  with `at_expiry = serverTick + 600`. The breacher refuses the
  affected space during the window; the binder GUI shows a countdown;
  the same actor can cancel before expiry — no one else may.
- At expiry (`ConversionTicker`): the registry switch applies
  atomically (cells, by_owner, FTB claims, queue entry deleted). For
  MERGE the personal cell's entry is re-keyed to the team UUID —
  interior preserved block-for-block; the team space *becomes* the old
  personal cell.

## LV Dimension-Generation Multiblock — consumed-in-jump

`machine/DimensionGenMultiblock` + `DimensionGenMultiblockEntity`.
GT casing pattern, LV-locked. One dedicated target: the meteorite
pocket template (skystone crust, buried meteorite with the four
Inscriber Presses, budding certus patch).

- On fire: materialize the next unexhausted meteorite pocket
  (per-**server** cursor — a preview of scarcity), teleport players
  standing on the frame, then **consume itself**: every multiblock
  block is replaced with air and the controller drops a "collapsed
  frame" junk item.
- No stability counter; finite by loot. This pocket does **not**
  collapse on leave — it stays until mined out.

## Trade Post — cross-dimensional trading

`machine/TradePostBlock` + `TradePostBlockEntity`. GT singleblock,
needs EU power (config `tradePost.powerPerTrade`).

- **Owner link:** one-time bind to the owner's network anchor; the BE
  stores `linked_net: {dim, x, y, z}`, resolved lazily by the storage
  backend (see [integration.md](integration.md#ae2-192x)).
- **Trades:** up to 9 standing trades, each
  `{ offer: item+count, want: item+count }`, configured in owner mode.
- **Visitor flow:** the visitor confirms a trade while standing in
  their own network's coverage; items move **storage-to-storage**
  (AE2-to-AE2 via the `-ae2` module, chest-to-chest via core's plain
  provider). Both legs staged, committed atomically — either both
  move or neither. Energy drawn from the visitor's side.
- Trades visible to everyone while powered; owner can disable
  individual trades or the whole post.
