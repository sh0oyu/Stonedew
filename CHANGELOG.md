# Changelog

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
