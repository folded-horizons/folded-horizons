# Folded Horizons — docs index

| Doc | What it is | Read it when |
| --- | --- | --- |
| [`design/`](design/) | Gameplay design — the source of truth | You want to know *what the pack is* |
| [`companion-mod/`](companion-mod/) | Technical spec for the companion mod | You want to know *how it's built* |
| [`multiplayer.md`](multiplayer.md) | Co-op plan (FTB suite) | You're touching claims/teams/quests |
| [`decisions.md`](decisions.md) | Settled decisions with rationale | You're about to question something already decided |

Reading order for newcomers: README → `design/` → `companion-mod/`.

**Conventions:**

- All logic lives in the companion mod; **KubeJS is for recipes only**.
- Technical namespace is `foldedhorizons` (mod ids, packages,
  dimension ids) — the pack is named *Folded Horizons*.
- Docs describe intent, not implementation status — the build order
  lives in [`companion-mod/build-order.md`](companion-mod/build-order.md),
  and work tracking happens in the git issue tracker, never in docs.
