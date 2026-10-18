# Concept & Pillars

## The idea

The overworld is never the real base. Players work inside a **root
space** — a cell in a custom void dimension — and keep expanding it.
Space is the scarce resource: mid-game unlocks **compact spaces** that
fold a production line into a 3×3 block; GT tiers unlock larger
compaction up to multiblock scale. Late game adds **exploit
dimensions** — resource-rich pockets you enter, strip, and abandon.

The spiral: **expand the root → fill it → compact the fill → repeat.**

## Pillars

1. **Root space** — one persistent cell per owner (player or team),
   expandable. Spawn point, safety net, identity anchor.
2. **Compaction** — tiered compact spaces from 3×3 up to multiblock
   scale; how you "win space".
3. **Exploit dimensions** — tiered pockets with finite resources,
   entered via the Dimensional Breacher.
4. **Lobby** — neutral ground at grid origin; the routing point that
   divides players into their own spaces.

## Identity — the player is the key

**No key item.** Player UUID and FTB Team UUID are the registry keys;
the Dimensional Breacher reads the inserting player directly — nothing
to carry, bind, or lose.

- Solo: FTB gives every player a single-member team, so "personal" and
  "team" are effectively the same until a team forms.
- Co-op: a team owns exactly one shared root; inviting a friend shares
  it instantly.

## Grid architecture

One custom void dimension hosts root and repeatable pockets as cells
on a giant grid — no runtime dimension generation. **Grid pitch:
2048 blocks** between cell centers; lobby at cell (0,0); a cell is
materialized by placing a structure template on first allocation.
Exploit tiers are additional static dimension files. "Temporary" is a
gameplay state (exhaustion + collapse), never a technical one.
