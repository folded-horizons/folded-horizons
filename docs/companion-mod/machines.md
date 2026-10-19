# Machines

Class stubs live under
`companion/src/main/java/dev/foldedhorizons/core/machine/`.

**Blanket rule (decision #13): every multiblock and machine in this
pack is a GT machine — GTCEu Modern framework, GT controller, casings,
EU energy, tier gating. The only exception is AE2 machinery, which
stays AE2-native.** The core mod currently ships vanilla-style stand-ins
so the pocket system works standalone; the `foldedhorizons-gt` module
re-homes every machine listed below onto the GTCEu framework (see
[integration.md](integration.md#gtceu-modern-7x-what-goes-where)).

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

`machine/TradePostBlock` + `TradePostBlockEntity`. GT singleblock, needs EU power (config `tradePost.powerPerTrade`).

**Progression intent (user decision): the crate-based lobby handoff is how EARLY-GAME players trade.** A brand-new player in a starter cell has no AE2 network yet — but they can still visit the lobby, drop their offer into the post's crate, and take a standing deal. Storage-to-storage AE2-to-AE2 trading is the LATER upgrade that automates the same trades once both sides have networks. The Trade Post therefore works from day one of the lobby (crate-based), and gains network automation only when AE2 exists.

**Cross-network storage-to-storage (AE2-only, `-ae2` module):** the direct AE2-to-AE2 handoff exists only when AE2 is installed; there is no remote chest/barrel fallback backend. Without AE2 the post is crate-based only (still fully usable).

- **Owner link:** one-time bind to the owner's network anchor; the BE
  stores `linked_net: {dim, x, y, z}`, resolved lazily by the storage
  backend (see [integration.md](integration.md#ae2-192x)).
- **Trades:** up to 9 standing trades, each
  `{ offer: item+count, want: item+count }`, configured in owner mode.
- **Visitor flow — crate-based (default, early-game):** the lobby's
  input/output happens through physical crates/barrel blocks at the
  Trade Post — the post has an input crate (visitor offers go in)
  and an output crate (owner's goods come out), so trading works
  from day one, no network required on either side. Both legs
  staged, committed atomically — either both move or neither.
- **Visitor flow — networked (upgrade, AE2-only):** once the visitor
  has their own ME network, confirming a trade while standing in
  its coverage moves items **storage-to-storage** (AE2-to-AE2 via
  the `-ae2` module); the owner can restock output crates from their
  network automatically. Energy drawn from the visitor's side.
- Trades visible to everyone while powered; owner can disable
  individual trades or the whole post.
