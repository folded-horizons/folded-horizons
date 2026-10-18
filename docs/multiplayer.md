# Multiplayer — Folded Horizons

The pack is designed for small co-op groups (2–8 players) sharing one
root space, then diverging as they open their own exploit dimensions.

## Layers

| Concern | Mod | Where configured |
| --- | --- | --- |
| Claims & chunk protection | FTB Chunks | `overrides/config/ftbchunks/` |
| Parties / teams | FTB Teams | `overrides/config/ftbteams/` |
| Shared progression | FTB Quests | `overrides/ftbquests/quests/` |

Dependencies (Architectury API, FTB Library, FTB Teams) are pulled in
automatically by `pakku add`.

## Defaults shipped in overrides

- **Claims**: classic protection — only team members may interact
  inside claimed chunks; GUIs stay inspectable (read-only) for
  strangers. Generous claim limits (512) so late-game strip-mining of
  temporary dimensions works.
- **Teams**: opt-in parties, allies allowed, no friendly fire.
- **Quests**: per-team progress — the group advances one quest book
  together. Five chapters in the standard FTBQ 2101.1.x loadable
  layout (`data.snbt`, `chapter_groups.snbt`, `chapters/`).
- **In-game identity**: player UUID / FTB team UUID are the registry
  keys for pocket ownership; the Root Binder handles
  personal⇄team conversions (see
  [`design/machines.md`](design/machines.md)).
