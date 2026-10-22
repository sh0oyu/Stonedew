# Changelog

## 0.2.0-p1 — 2026-10-22

Playable Plant Core: seed → watering/fueled light → four visible stages → ripe plants. Harvest and processing remain P3.

### Added

- Shared one-/four-slot tray block entity for Clay Pot and Planter Bed, bounded lazy timestamp growth, stage comfort/Vigor, no-death slowdown, capped catch-up, sleep-aware monotonic growth clock and versioned persistent plant/care/owner data.
- Immutable genome Codec/StreamCodec seed components with eight stub genes; pigment/habit presentation. Full inheritance/stat expression remains P5.
- Survival planting and watering, eight-pour can, source-water/cauldron refills, server permission checks, obstruction/reach-aware per-slot foliage targeting and no cauldron consumption when already full.
- Glow Cells fuel Bulb Lamps with real light and fuel exhaustion/relighting. Basic nearby lamp/sun Lume contributes to growth; full rooms/environment remain P2.
- Compact changed-slot presentation sync separate from disk state, accumulated same-tick deltas, initial chunk snapshots, plant HUD and real server-opened Ledger menu. Persisted per-player introductory flags and compact directive payload; localized prose authored outside Java.
- Original dimensional voxel equipment, 24 stage/habit/LOD plant meshes, tint channels, gentle sway, first-person can pouring, 16 material textures and shader-free emissive halo. Corrected tiny-face UV density and sampled foliage light after actual close-up review. No third-party art bundled.
- Survival recipes/loot/tags and operator kit/growth/stage/genome/timewarp tools. Optional clear-space-checked grow-room exhibit. Deferred-system debug entries report their phase instead of faking success.
- P1 playtest, asset manifest, research/production notes, mesh budget and actual in-game screenshots. P0 download retained as history; install only one Stonedew JAR.

### Validation

- Java 21 / NeoForge 21.1.264 build passes: **53 JUnit tests, zero failures/errors/skips**. Four Python asset checks pass.
- Asset/datagen repeat is byte-identical across 94 resource/report files. Near plant meshes max 925 quads; LOD max 40. These geometry budgets do not prove the future performance target.
- Development client launched and loaded an existing P0 singleplayer world with seven P1 definitions. Real item interactions planted a seed, watered in Survival (water increase, can 8→7), refilled from a cauldron (7→8, level 3→2), exhausted/refueled a lamp and opened the Ledger directive screen.
- Accelerated a real planted tray to ripe, saved/quit and reopened: genome, stage and care history persisted. Watering upper foliage changed the selected bed slot while other slots retained their water.
- Solid block obstruction prevented a foliage pour (can remained at 8); a full can left the water cauldron at level 3.
- Actual game captures record the models/HUD/Ledger. Art remains a first gameplay pass for owner review.

### Limits / next phase

Baseline humidity/temperature/air/nutrients/schedule and simple light sampling are P1 foundations. Next is **P2 Rooms and environment**; P3 then completes manual harvesting/processing before the explicit Fun Gate. No scope removed. Multiplayer, shader packs, audible mix and 500-plant performance remain untested. Cloud audio was disabled; offline authentication warnings are not gameplay failures.

## Download follow-up — 2026-10-22

- Added the verified P0 JAR and SHA-256 to `downloads/`, with a direct GitHub download link. Mod code and gameplay are unchanged.

## Documentation follow-up — 2026-10-22

- Added client installation and development-launch steps, and recorded the owner's stylized, animated 3D voxel art direction in the living design and asset guidance. Gameplay and the P0 JAR are unchanged.

## 0.1.0-p0 — 2026-10-22

First implementation phase: a loadable NeoForge foundation. This is not the playable cultivation loop.

### Added

- Minecraft 1.21.1 / NeoForge 21.1.264 / Java 21 project, Gradle 9.2.1 wrapper with distribution checksum, ModDevGradle 2.0.148, official Mojang mappings, and GitHub Actions build/datagen/test workflow.
- Stonedew creative tab, decorative glowing Dewstone and Glow Cell item, with provisional recipe and advancement.
- Deterministic 16x16 texture generator and NeoForge datagen for models, blockstate, loot, recipe, advancements, language and mining tag.
- Server and client config scaffolding: Grower / Uneasy defaults, cannabis theme with optional Herbal Mode, and future-feature accessibility controls.
- Organism-neutral Cultivar interface and immutable profile; Wing manifests; six base JSON definitions; validated, transactional datapack reloads. Generic later-phase payloads remain explicit foundations.
- Authoritative gameplay-event bridge, immutable versioned world story state, prototype-to-current migration, and guards against corrupt/future saves being replaced by empty data.
- Operator commands `/stonedew debug status`, `story`, and `probe`.
- Living design, decisions, asset manifest, architecture/datapack/cloud docs, screenshot and eight-item P0 playtest checklist. Original uploaded brief/images preserved.

### Validation

- `./gradlew --no-daemon --console=plain runData build`: passed. **24 unit tests; 0 failures, 0 errors, 0 skipped.**
- Datagen repeat: all ten generated files unchanged (zero written). Texture regeneration byte-identical.
- Cached `./gradlew --offline --no-daemon --console=plain build`: passed.
- Packaged JAR checked for mod metadata, entrypoint, generated resources and textures; datagen cache excluded.
- `runClient` launched under Xvfb/Mesa software rendering. Created and reopened a Creative singleplayer world with the mod loaded. Stonedew creative tab and both textured objects visible (docs/screenshots/p0-creative-tab.png).
- `/stonedew debug status`: six definitions, Grower/Uneasy. `/give` resolved both registered items. Generated advancement awarded.
- Real event probe saved to `stonedew_story.dat` with dataVersion 1 and count 1; that count remained after reopening the world.
- `/reload` succeeded. A disposable test datapack loaded a seventh definition; malformed JSON then correctly rejected reload and retained the previous seven-definition index. Removing the test pack restored six definitions. Test pack removed from the ignored development world.
- Cloud installation script rerun successfully with the project build; authenticated Debian package indexes used for local Xvfb. Updated installation/startup instructions saved to the environment configuration draft.

### Limitations and next phase

- Runtime dependency networking is working. The offline development client's online profile/public-key requests log warnings; online multiplayer authentication is not validated. Audio was disabled for cloud smoke validation.
- No plant gameplay, genome components, Ledger UI, processing, worldgen, automation or final visual/audio assets yet. Future-feature controls are declarations until their gameplay systems arrive.
- Human playtest, sound, two-client synchronization, shader compatibility and the 500-plant performance target remain unrun. They are not claimed to pass.
- Next: **P1 Plant Core**, including unified trays, stages, watering, Bulb Lamp, seed genome, tooltips and the Ledger/Directive stub. See docs/P0_PLAYTEST.md. Full scope remains planned; no cuts.
