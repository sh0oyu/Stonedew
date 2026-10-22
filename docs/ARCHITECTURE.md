# Architecture

Target: Minecraft 1.21.1, NeoForge 21.1.264, ModDevGradle 2.0.148, Java 21, Gradle 9.2.1, official Mojang mappings. Parchment is not enabled: the design explicitly selects Mojang mappings.

| Package | Responsibility / implementation milestone |
| --- | --- |
| `core` | Registries, server/client config, status contract; payload networking begins with P1 state sync |
| `plant` | Organism-neutral Cultivar and immutable profile now; slot-based trays and PlantState in P1 |
| `env` | Room caches, Lume and environment in P2 |
| `genetics` | Immutable genome and seed components in P1, full breeding in P5 |
| `process` | Harvest, trim, dry, cure and quality in P3 |
| `consume` | Products, effects and tolerance in P4 |
| `automation` | Capabilities, machines, networks and routines after the Fun Gate |
| `world.story` | World persistence, versioning, events now; Ledger/Directives P1, Hatch/Cycles P3 |
| `client` | Config screen now, later renderers, HUD, screens and effects; never imported by common entrypoint |
| `data` | Transactional JSON reloads, Wing/cultivar bindings and generated resources |
| `compat` | Optional integrations in later phases; none required to load the base mod |
| `debug` | Operator-only status, persistent event probe and story inspection; gameplay tools in P1+ |

## Day-one contracts

1. Trays share one block entity and an N-slot plant representation (P1).
2. Simulation is lazy and timestamp-based, with bounded offline catch-up (P1).
3. Environment belongs to bounded, cached, invalidated rooms (P2).
4. Genomes are immutable Codec/StreamCodec values stored on item components; no mutable NBT genetics (P1/P5).
5. All gameplay is server-authoritative. No client-only classes in the common entrypoint. State sync begins when mutable gameplay exists.
6. Applicable machines expose NeoForge item/fluid/energy capabilities when implemented.
7. StatusSource returns a language key. Future plants and machines implement it.
8. Persisted classes carry explicit versions and migrations. Story saves are the first implementation.
9. Cultivar bindings refer to schemas/profiles/chains/effect maps by namespaced ID, including future FUNGUS support.
10. Base content is the first Wing; additional Wings are manifest definitions.
11. GameplayEvent uses NeoForge's event bus and requires the server thread. No always-ticking narrative poller.
12. StorySavedData lives in Overworld data storage per world. StorySnapshot is immutable. Player journals/know-how/tolerance and future Controller ownership/trust are separate scopes. Story-level Standing/Attention are the initial world narrator state; per-facility aggregation is defined when Controllers arrive.
13. Narrative definitions are JSON, prose is localized. P0 contains no new lore prose. Gameplay/story handlers for generic content categories arrive in their documented phases.

## Story saves

`<world>/data/stonedew_story.dat` contains an explicit NBT `dataVersion` and a versioned JSON `story` payload. Version 1 stores flags, clues, thread progress, verified rules, Attention, Standing, Keeper count, and event counters. JSON is an intentional P0 persistence boundary: it keeps migration logic independent of Minecraft and directly unit-testable; this small per-world snapshot is written only on dirty saves.

Schema 0 is the pre-release migration fixture: `knownClues` becomes `discoveredClues`, and newly introduced fields receive initial values. Schema 1 requires its fields and validates meters/collections. Unknown future schemas and corrupt progress fail; the SavedData factory blocks vanilla's empty-save fallback on a decoding failure. No progress should be silently replaced.

P0's only event producer is the debug probe. It verifies the bus → authoritative handler → dirty save pipeline without pretending later gameplay exists. All future producers publish semantic events, not per-frame notifications.
