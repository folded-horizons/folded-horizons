# Companion Mod — Folded Horizons Core

**Mod ID family:** `foldedhorizons` (core), `foldedhorizons-ae2`,
`foldedhorizons-gt`, `foldedhorizons-ftb` (integration modules) ·
**Target:** NeoForge 1.21.1 · **Companions (all optional at runtime):
AE2 19.2.x, GTCEu Modern 8.x, KubeJS, FTB Chunks/Teams**

This directory is the **technical contract**: class names, data
shapes, save format, tick logic, and build order. The gameplay
source of truth lives in [`../design/`](../design/). Scaffolded stubs
exist under `companion/src/main/java/dev/foldedhorizons/core/` and the
names below match those stubs.

| File | Contents |
| --- | --- |
| [`architecture.md`](architecture.md) | Module split, SPIs, packaging rules |
| [`pocket-system.md`](pocket-system.md) | Topology, registry, allocation, collapse |
| [`machines.md`](machines.md) | Breacher, Root Binder, Dim-Gen, Trade Post |
| [`walls-expansion.md`](walls-expansion.md) | Wall-start blocks, root expansion |
| [`integration.md`](integration.md) | AE2, GTCEu, mod-vs-data boundary, tick logic, save format |
| [`build-order.md`](build-order.md) | Implementation checklist (tracked as issues) |

**Design principle:** all logic lives in the mod, and each mod **ships
its own default recipes** so it is reachable in survival on its own;
**KubeJS is for recipe overrides only**
([§ Mod vs. data](integration.md#mod-vs-data)). The mod owns state
machines, tuning defaults, recipes, and its own datapack content so it
works standalone.

**Self-containedness goal:** the mod builds and runs with NONE of
AE2 / GTCEu / FTB present — features degrade gracefully, any modpack
author can ship the modules they want ([architecture.md](architecture.md)).
