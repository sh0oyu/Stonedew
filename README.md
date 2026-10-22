# Stonedew

A Minecraft Java **1.21.1 / NeoForge** mod: a cozy underground cultivation cave with colorful strains, tactile processing, automation, and an unsettling mystery.

**Current milestone: P0 — foundations.** This build adds a Stonedew creative tab, decorative Dewstone, a Glow Cell item and developer recipe, configuration, reloadable datapack definitions, persistent story state, and operator debug commands. Growing, watering, processing, the Ledger and all later gameplay are not implemented yet. The reference images describe the intended appearance, not the current build.

## Develop

Install a **Java 21 JDK**, then use the checked-in Gradle wrapper. Python 3 is needed only to regenerate placeholder textures.

```sh
./gradlew build       # compile, run unit tests, package build/libs/stonedew-0.1.0-p0.jar
./gradlew runClient   # launch the NeoForge development client
./gradlew runData     # regenerate models, loot, language, tags, recipe and advancement
python3 tools/generate_placeholder_assets.py
```

In this cloud environment, first run `source /workspace/.stonedew-env/activate.sh` in each shell. It selects the installed JDK/Gradle, the retained dependency cache and current-instance proxy routing. A graphical client needs a display; see [cloud startup](docs/CLOUD_DEVELOPMENT.md). Each cloud task is already isolated: use this checkout, without creating a worktree unless explicitly requested.

To play the packaged mod, install NeoForge **21.1.264** for Minecraft 1.21.1 and copy the built JAR into that instance's `mods` directory. No other mods are required. The development client does not require copying a JAR.

## P0 playtest

See the [eight-step checklist](docs/P0_PLAYTEST.md) and [actual P0 screenshot](docs/screenshots/p0-creative-tab.png).

Create a disposable Creative world with commands enabled. The Stonedew tab contains Dewstone and Glow Cell. Dewstone is placeable, emits a little light, and drops itself. The placeholder Glow Cell recipe combines an amethyst shard and copper ingot.

Operator commands (permission level 2):

- `/stonedew debug status` — loaded definitions and selected defaults.
- `/stonedew debug story` — Keeper number, story meters and persisted probe count.
- `/stonedew debug probe` — publish a real server-side event and increment its saved counter.

`/reload` reloads the six base definitions. Invalid schemas or broken Wing/cultivar references reject the replacement rather than publishing a partial registry. Save/quit and reopen the world to check the probe counter. Game-facing narrative and plants arrive in later phases; debug output is developer-facing.

With the pinned NeoForge version, server settings are in `run/config/stonedew-server.toml` and client accessibility settings are in `run/config/stonedew-client.toml` for development (`config/` in a regular instance). The config screen is available under Mods → Stonedew → Config. Settings for later gameplay are foundations, with consumers added in their corresponding phases.

## Design and status

- [Living design bible](DESIGN.md), [decisions](DESIGN_DECISIONS.md), [changelog](CHANGELOG.md), [assets](ASSETS.md).
- [Architecture](docs/ARCHITECTURE.md) and [datapack format](docs/DATAPACKS.md).
- The original uploaded brief and both reference images remain at the repository root.

The build uses official Mojang mappings. See [Mojang's mapping license](https://github.com/NeoForged/NeoForm/blob/main/Mojang.md). Project code/assets are All Rights Reserved pending the owner's license choice. Build tooling follows the official NeoForge MDK (LGPL-2.1 template notice in `TEMPLATE_LICENSE.txt`).
