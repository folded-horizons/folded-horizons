# Folded Horizons Core

Companion mod for the **Folded Horizons** GregTech modpack
(NeoForge, Minecraft **1.21.1**, NeoForge **21.1.65**).

Will live as its own repo at
[`folded-horizons/folded-horizons-core`](https://github.com/orgs/folded-horizons/repositories)
(for now it is a directory inside the pack repo).

This mod implements the systems described in the pack docs:

- `docs/companion-mod/` — the companion mod specification
- `docs/design/` — root spaces, exploit dimensions, grid architecture

## What this is

A **skeleton**: NeoForge MDK layout, registration plumbing, and
package stubs with design-javadoc TODOs. No gameplay logic is
implemented yet. The stubs exist to lock down package/class structure
and naming before implementation passes.

- `dev.foldedhorizons.core.FoldedHorizons` — `@Mod` entry point; registers the DeferredRegisters
- `dimension/` — `PocketType` (ROOT, REPEATABLE, UNSTABLE, SPECIAL),
  `PocketInstance` record, `PocketRegistry` (SavedData), `PocketGrid` (2048-block-pitch spiral allocator)
- `machine/` — `BreacherBlock`, `RootBinderBlock`, `TradePostBlock`, `DimensionGenMultiblock` placeholders with designed-behavior TODOs
- `item/` — `TempKeyItem` (tiered)
- `ae2/` — `AE2Bridge` stub (cross-dimensional ME grid bridging via Applied Energistics 2 19.2.x)
- `setup/` — `ModBlocks`, `ModItems`, `ModBlockEntities` DeferredRegisters
- `config/` — `ModConfig` (pocket base size, breach energy cost, grace window, expansion thresholds)

## Building

```sh
gradle build
```

Requires a standard Gradle 8.8 install (wrapper properties are provided;
the wrapper jar is not committed). Toolchain: Java 21.

## Integration status

**Not yet hooked into the pakku manifest.** Once the mod builds, the
produced jar (`build/libs/foldedhorizons-<version>.jar`) will be
added to the pack as a local jar via `pakku.json`.
