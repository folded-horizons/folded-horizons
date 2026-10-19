# Decisions — Folded Horizons

Settled design decisions and their rationale. When a debate keeps
resurfacing, record the outcome here instead of re-litigating it.

| # | Decision | Rationale |
| --- | --- | --- |
| 1 | **No magic mods** — reality-breaking stays tech-flavored | GT multiblocks + AE2 + quest text deliver the "breaking reality" feel within one aesthetic |
| 3 | **Pre-HV storage = drive + discs, not ME interface** | Disc crafting is a mini production chain teaching the pack grammar; interface-first is passive. Interface arrives at HV as the upgrade |
| 4 | **LV meteorite dimension via Dimension-Gen multiblock; multiblock consumed in the jump** | One machine per pocket = real economy decision; previews the exploit cycle |
| 5 | **Unstable pockets collapse when the last player leaves; no re-entry** | The exit IS the collapse — teams plan extraction around one visit; no stability-counter bookkeeping |
| 6 | **Repeatable space is empty, like root; buildable recursively** | Unbounded space, but each pocket costs energy + multiblocks — the limit is the compaction economy, not a hardcoded cap |
| 7 | **Special dimensions: address, not door** (one pocket per owner per body) | Second multiblock links into the same pocket — prevents duplicate-farming of celestial bodies |
| 8 | **Companion mod split into core + `-ae2` / `-gt` / `-ftb` modules** | Self-contained by construction; other pack authors install only what they want; core runs standalone |
| 9 | **All logic in the mod; KubeJS for recipes only** | Mod owns state machines, tuning, datapack content → standalone-capable; KubeJS glue scripts would break that |
| 10 | **Machines use the GTCEu framework** | Breacher/Binder/TradePost/Dim-Gen are real GT multiblocks/singleblocks — free formation preview, casing UI, tier/energy plumbing for GT players |
| 11 | **Static void dimension with grid cells; no runtime dimension creation** | "Temporary" is a gameplay state (exhaustion + collapse), never a technical one — crash-safe, snapshot-friendly |
| 12 | **Claiming inside pockets is disabled; permanent pockets auto-claimed, no limit, permanently chunk-loaded** | Your space is fully owned by construction — manual claim bookkeeping contradicts the pack premise; automation must run while players are away |
