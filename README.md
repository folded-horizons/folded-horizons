# Folded Horizons

A **GregTech modpack about space scarcity** — you start sealed in a
box, and every horizon you ever see afterwards is one you built or
breached your way into.

Built and packaged with [Pakku](https://github.com/juraj-hrivnak/Pakku).

## Platform

- **Minecraft 1.21.1** · **NeoForge 21.1.65**
- Export target: **CurseForge** (FTB suite is CF-only)
- 26 pinned projects — see `pakku-lock.json`

## The idea

- **You wake up inside a sealed cell.** No ores, no sky, no crafting
  table. The walls are unbreakable — but mining them *yields* starter
  resources. The space you are given is the resource you exploit.
- **Root space**: your persistent cell in a void dimension. Expand it,
  fill it, then **compact** the fill — LV+ compact spaces fold a
  production line into a 3×3 block, higher GT tiers fold multiblock
  chains into single machines. Expand → fill → compact → repeat.
- **Exploit dimensions (EV+)**: temporary, energy-expensive pockets —
  enter, strip, and they collapse the moment the last player leaves.
- **Late game**: break through the sky, or claim permanent pockets of
  impossible places (Moon, Mars, ... a glass wall looking into a black
  hole).

Full gameplay design: [`docs/design/`](docs/design/)

## Mod list

| Mod | Version | Role |
|-----|---------|------|
| **GregTech CEu Modern** | 1.21.1-7.0.2 | Tech progression backbone |
| **Applied Energistics 2** | 19.2.18 | Storage & digital logistics; trading-hall network layer |
| Applied Flux | 1.21-2.1.6 | FE⇄ME energy integration |
| GT Modern Ore Generation Standalone | 1.21.1-1.0.6 | GT ore veins in pockets |
| GregTech Placeable Emitters | 1.21-1.0.9 | Portable GT emitters |
| **Bonsai Trees 4** | 4.0.9 | Renewable wood, zero footprint |
| **Farmer's Delight** | 1.21.1-1.3.4 | Food loop |
| Expanded Delight | 0.1.4 | Extra FD content |
| Sophisticated Storage / Backpacks | — | Upgraded storage |
| Functional Storage | — | Drawer banks |
| **FTB Chunks / Teams / Quests / Essentials** | 2101.1.x | Claims, parties, quests, /back /tpa /warp |
| EMI | 1.1.24+1.21.1 | Recipe viewer |
| Sodium | 0.8.13+mc1.21.1 | Client rendering |
| AppleSkin | 3.0.9 | Hunger HUD |

Pulled in as dependencies: Configuration, LDLib, GuideME, Architectury
API, FTB Library, Glodium, Titanium, Sophisticated Core.
Client/server optimization: FerriteCore, ModernFix.

## Repository layout

```
.devcontainer/           Java 21 + Pakku baked into the image
pakku.json / pakku-lock.json   Pakku manifest & resolved lockfile
overrides/               pack content: configs, FTB Quests chapters
folded-horizons-core      companion mod source — separate repo (github.com/folded-horizons/folded-horizons-core)
docs/                    design & development docs — start at docs/INDEX.md
```

## Working on the pack

Pakku is installed in the dev container image — just run `pakku`.
A **CurseForge API key** is required for CF operations (read from the
environment).

```sh
pakku ls                 # list pinned projects
pakku status             # verify lockfile freshness
pakku add prj --cf <slug>   # add a mod (resolves deps)
pakku fetch              # download locked files
pakku export --cf        # export CurseForge pack
```

Key conventions (see `docs/`):

- **All logic lives in the companion mod; KubeJS is for recipes only.**
- The companion mod is **modular** (core + optional `-ae2` / `-gt` /
  `-ftb` modules) and usable standalone by other pack authors.

## Docs

- [`docs/INDEX.md`](docs/INDEX.md) — doc map & reading order
- [`docs/design/`](docs/design/) — gameplay design (source of truth)
- [`docs/companion-mod/`](docs/companion-mod/) — technical spec for the companion mod
- [`docs/multiplayer.md`](docs/multiplayer.md) — co-op plan (FTB suite)

## Roadmap

Work tracking lives in the git issue tracker; the technical build
order is in [`docs/companion-mod/build-order.md`](docs/companion-mod/build-order.md).

Milestones:

1. Companion mod implementation (12-step build order)
2. Pack-side content: KubeJS recipes, pack-specific datapack overrides
3. Classic infinite-resource methods (lava/cobble gens, GT drilling)
4. First exportable alpha (CurseForge format)

## Dev container

- Java 21 (SDKMAN) + Pakku 1.5.0 baked into the image
- Port 25565 forwarded for local server testing
