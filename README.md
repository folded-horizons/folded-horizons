# Folded Horizons

A **GregTech modpack about space scarcity** — you start sealed in a
box, and every horizon you ever see afterwards is one you built or
breached your way into.

Built and packaged with [Pakku](https://github.com/juraj-hrivnak/Pakku).

## Platform

- **Minecraft 1.21.1** · **NeoForge 21.1.264**
- Export target: **CurseForge** (FTB suite is CF-only)
- Pinned projects: see `pakku-lock.json` (authoritative)
- **GTCEu comes from GitHub**, not CurseForge: `1.21.1-7.0.2` is the
  latest CF build and it cannot start a dedicated server (upstream
  [GTCEu#4155](https://github.com/GregTechCEu/GregTech-Modern/issues/4155)
  — it loads a client class during common init). The pack tracks the
  `latest-1.21` GitHub release (`8.0.0-SNAPSHOT`), which drops LDLib and
  boots cleanly. This is the one non-CurseForge project; a CF release
  will replace it when upstream publishes a fixed 1.21.1 build.

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

## Mods

The authoritative mod list is `pakku-lock.json` — kept out of this
README on purpose so it never drifts. In short: GregTech CEu Modern
backbone, Applied Energistics 2, FTB suite, Bonsai Trees, Farmer's
Delight, storage mods, EMI, plus the companion mod (built from
`folded-horizons-core`).

Sodium is a **client-only** project (`side = CLIENT` in the lockfile):
it crashes dedicated servers on startup, so it is skipped by
`scripts/test-server.sh` and never exported server-side.

## Repository layout

```
.devcontainer/           Java 21 + Pakku baked into the image
pakku.json / pakku-lock.json   Pakku manifest & resolved lockfile
overrides/               pack content: configs, FTB Quests chapters
scripts/                 repo tooling (quest validator, test server)
docs/                    design & development docs — start at docs/INDEX.md
```

Companion mods live in their own repositories under the
[folded-horizons](https://github.com/orgs/folded-horizons/repositories)
org:

```
folded-horizons-core     pocket system, machines, walls, registry
folded-horizons-ae2      AE2 integration   (optional module)
folded-horizons-gt       GTCEu integration (optional module)
folded-horizons-ftb      FTB integration   (optional module)
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

**Work tracking lives in the git issue tracker** — these docs describe
design intent, not status.

Implemented so far: the companion mod core covers the whole technical
build order (see [`docs/companion-mod/build-order.md`](docs/companion-mod/build-order.md)),
with the FTB Quests book and quest validator in this repo.

## Testing

```sh
cd companion && gradle :core:build && cd ..   # build the companion jar
scripts/test-server.sh                        # stand up a test server
```

The script downloads NeoForge into `.test-server/`, copies the locked pack
mods plus the built companion jar, skips client-only projects, accepts the
EULA, and waits until the server reports `Done (…)`. It prints the connect
address and a log path, and refuses to claim success if the server crashes.

```sh
scripts/test-server.sh --fresh   # wipe the world first
scripts/test-server.sh --stop    # stop it
```

Server console: `.test-server/console.log`. Inside the game, `/give` and
`/setblock` work on the mod's content — e.g. `foldedhorizons:breacher`,
`foldedhorizons:wall_metal`, `foldedhorizons:iron_chunk`.

Note that **Sodium and GTCEu's LDLib dependency are excluded from servers**:
Sodium's client bootstrap and GTCEu 7 both crash dedicated servers. The pack
therefore tracks GTCEu 8 from GitHub (see Platform above), and Sodium is
marked client-only.

## Dev container

- Java 21 (SDKMAN) + Pakku 1.5.0 baked into the image
- Port 25565 forwarded for local server testing
- `python3 scripts/validate_quests.py` checks the FTB Quests files
  (parses SNBT, verifies quest ids, dependencies, and item namespaces)
