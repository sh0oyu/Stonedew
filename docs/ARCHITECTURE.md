# Architecture

Target: Minecraft 1.21.1, NeoForge 21.1.264, ModDevGradle 2.0.148, Java 21, Gradle 9.2.1, official Mojang mappings. Parchment is not enabled: the design explicitly selects Mojang mappings.

| Package | Responsibility / implementation milestone |
| --- | --- |
| `core` | Registries, server/client config, status contract; growth clock, player progress and compact progress payloads |
| `plant` | Cultivar, slot-based trays, immutable PlantState, bounded simulation and tools |
| `env` | Room caches, Lume and environment in P2 |
| `genetics` | Immutable Codec/StreamCodec genome and seed components; full breeding in P5 |
| `process` | Harvest, trim, dry, cure and quality in P3 |
| `consume` | Products, effects and tolerance in P4 |
| `automation` | Capabilities, machines, networks and routines after the Fun Gate |
| `world.story` | World persistence, versioning, events; Ledger/Directives in world.ledger; Hatch/Cycles P3 |
| `client` | Config, tray/lamp renderers, HUD, Ledger screen and tool transforms; isolated from common entrypoint |
| `data` | Transactional JSON reloads, Wing/cultivar bindings and generated resources |
| `compat` | Optional integrations in later phases; none required to load the base mod |
| `debug` | Operator-only inspection, kit, growth/stage/genome/timewarp tools and checked showcase |

## Day-one contracts

1. Trays share one block entity and an N-slot plant representation (P1).
2. Simulation is lazy and timestamp-based, with bounded offline catch-up (P1).
3. Environment belongs to bounded, cached, invalidated rooms (P2).
4. Genomes are immutable Codec/StreamCodec values stored on item components; no mutable NBT genetics (P1/P5).
5. All gameplay is server-authoritative. No client-only classes in the common entrypoint. State sync begins when mutable gameplay exists.
6. Applicable machines expose NeoForge item/fluid/energy capabilities when implemented.
7. StatusSource returns a language key; trays and lamps implement it.
8. Persisted classes carry explicit versions and migrations. Story saves are the first implementation.
9. Cultivar bindings refer to schemas/profiles/chains/effect maps by namespaced ID, including future FUNGUS support.
10. Base content is the first Wing; additional Wings are manifest definitions.
11. GameplayEvent uses NeoForge's event bus and requires the server thread. No always-ticking narrative poller.
12. StorySavedData lives in Overworld data storage per world. StorySnapshot is immutable. Player journals/know-how/tolerance and future Controller ownership/trust are separate scopes. Story-level Standing/Attention are the initial world narrator state; per-facility aggregation is defined when Controllers arrive.
13. Narrative definitions are JSON, prose is localized. P0 contains no new lore prose. Gameplay/story handlers for generic content categories arrive in their documented phases.

## Story saves

`<world>/data/stonedew_story.dat` contains an explicit NBT `dataVersion` and a versioned JSON `story` payload. Version 1 stores flags, clues, thread progress, verified rules, Attention, Standing, Keeper count, and event counters. JSON is an intentional P0 persistence boundary: it keeps migration logic independent of Minecraft and directly unit-testable; this small per-world snapshot is written only on dirty saves.

Schema 0 is the pre-release migration fixture: `knownClues` becomes `discoveredClues`, and newly introduced fields receive initial values. Schema 1 requires its fields and validates meters/collections. Unknown future schemas and corrupt progress fail; the SavedData factory blocks vanilla's empty-save fallback on a decoding failure. No progress should be silently replaced.

P1 publishes semantic planting/watering/lighting/growth events as well as the debug probe. Events are server-side actions, not per-frame notifications.

## P1 simulation and synchronization

A pot/bed uses one `GrowTrayBlockEntity` with N slots (1/4 now). `PlantState` holds stage/progress/water, immutable Genome, timestamp, aggregate care, owner and a persistent independent appearance seed. Disk JSON is explicitly versioned and validated; client `PlantView` is a separate compact representation without hidden genes/history/ownership. Initial chunk snapshots include every occupied slot; later pending per-slot changes accumulate until dispatched. Packet decode does not invoke the full disk loader.

Plants advance at scheduled visits, interactions and chunk load through bounded integration. No plant BE ticker is registered. Catch-up stamps current time even when capped. `GrowthClock` uses monotonic world game time plus a persisted offset for sleep/debug skips. Basic P1 lamp/sun sampling does not force unloaded chunks; full historical environment and room caching remain P2.

Seeds store immutable Genome values through Codec/StreamCodec data components. Water/capacity components provide the can's state. Server checks govern mutations, survival consumption and refill. Foliage targeting is a bounded ray query clipped by block obstruction and interaction reach, with per-slot bounds.

Player introductory flags use versioned per-player persisted data, clone hooks and a compact progress payload. A typed directive definition selects the localized primary instruction. Ledger uses vanilla server-opened menu validation.

Hybrid plant OBJ meshes combine individually serrated flat leaflets and offset chamfered bracts, shared by stage/shape/load. Distant meshes retain alpha fans. Blender BVH bakes bounded hemisphere ambient occlusion into native OBJ vertex colors; indexed positions/UVs/normals and quantized color indices reduce resource size. The authoring generator stages outputs before installing them; ordinary builds require no Blender runtime. Large equipment panels are clipped into atlas-safe material tiles. Standard power-of-two material sprites replace the rejected custom atlas importer. The tray renderer caches geometric normals/positions and supplies directional shading, vertex canopy occlusion, cultivar highlights and height-based world light. A translucent contact shadow anchors foliage to soil. Cached loaded-chunk fixture queries add obstruction-aware UV bounce; the lamp renderer projects a soft local spill onto actual receiving floors and a subtle depth-bounded light shaft. No runtime shader or dependency is added; these are local effects rather than global shadow mapping. See the art notes for budgets, source provenance and review captures.

Every planted seed gets a server-random appearance identity without changing its immutable genome. PlantView synchronizes shape/load/height/spread/rotation; disk stores the full identity. Legacy version-1 JSON acquires a deterministic identity from lineage, tray position and slot. The four branch layouts and three mature flower loads use 64 shared near/distant models; existing genetic habits still affect scale. See PlantAppearanceTest for persistence/migration/diversity coverage.

The optional checked `ArtGallery` uses tagged vanilla item/text display entities to inspect every pot/tent/UV reference tier. Future-tier models are custom-model previews on existing items, with no added machine gameplay. Existing P1 registries and saved plant state remain authoritative.
