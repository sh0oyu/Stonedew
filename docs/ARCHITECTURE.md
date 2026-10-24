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

Hybrid plant OBJ meshes combine broad stepped flat fans and solid irregular voxel bracts; distant meshes retain alpha fans. The first three stages are leafy; flowers appear at maturity. Blender BVH bakes ambient occlusion and a three-ray authored canopy key into native OBJ vertex colors. Minecraft's entity shader applies diffuse light once; the removed CPU diffuse pass previously compounded it. Original geometry rasterization authors soft foliage-shaped soil shadows, clipped by the renderer to soil boundaries. Cultivar colors, height-based world light and obstruction-aware fueled UV bounce remain runtime inputs.

A new unchanged original material painting is packaged outside the block sprite directory. A native `minecraft:unstitch` atlas source exposes sixteen distinct, inset 256px swatches under `stonedew:block/painted/`; it neither overrides vanilla sprites nor lowers global mip levels. Large equipment panels are still clipped into atlas-safe UV tiles. The staged generator requires successful Blender baking before installing assets. Normal builds use checked-in resources. Native composite item models separate diffuse bodies and unlit additive emission. Glow meshes store radiance falloff in RGB, because additive ONE/ONE blending ignores alpha; they are excluded from occlusion geometry. Lit previews bake violet reflections from their fixtures. The actual lamp's additive halo, spill and depth-bounded shaft remain fuel/atmosphere gated. These are local effects, without a global shadow-map/HDR postprocessing renderer.

Every planted seed gets a server-random appearance identity without changing its immutable genome. PlantView synchronizes shape/load/height/spread/rotation; disk stores the full identity. Legacy version-1 JSON acquires a deterministic identity from lineage, tray position and slot. The four branch layouts and three mature flower loads use 64 shared near/distant models; existing genetic habits still affect scale. See PlantAppearanceTest for persistence/migration/diversity coverage.

The optional checked `ArtGallery` uses tagged vanilla item/text display entities to inspect every pot/tent/UV reference tier. Future-tier models are custom-model previews on existing items, with no added machine gameplay. Existing P1 registries and saved plant state remain authoritative.

## 0.2.7 plant authoring

Plant fans use a fixed original RGBA painting exposed through 25 native 256px atlas windows. `botanical_leaf.py` reads alpha with Pillow/NumPy to author conservative double-sided mesh coverage, without rewriting images. `plant_art.py` poses the leaves on four asymmetric connected branch layouts; the distant mesh preserves that architecture. Painted leaf tint is white at runtime. Small sugar leaves, crossed curved-pistil ribbons and non-emissive resin geometry supplement the retained bract volume. Save/network schemas and simulation are unchanged.

## 0.2.8 leaf construction

The rejected full-fan runtime painting is retired. A new fixed individual-leaflet painting binds through one native power-of-two atlas window. Read-only alpha measurements bound six longitudinal bands; each of seven fingers receives independent pose/curvature. Compact branches carry overlapping fans. Foliage has gentler baked occlusion than solid materials. Raised bract crowns supplement existing flower volume. These are art changes; save/network/simulation schemas remain unchanged.

The tray renderer now rejects only degenerate surfaces: its old area threshold discarded most thin pistil faces and every resin facet in the inspected small bud. The lower threshold retains those valid surfaces and small leaf bands.


## Current rendering and workshop integration — 0.2.9

The current complete five-finger source supersedes the dated 0.2.7/0.2.8 construction notes above. A near fan has four folded double-sided patches; its distant counterpart has one. Artist normals preserve green undersides. Flower surfaces merge coplanar exposed bracts, retaining the stepped outline and attached hairs/resin. The maximum is 2,294 / 106 faces. A per-level/per-tray light sample cache refreshes every ten ticks and caps its map; vertices use its small height table. The HUD queries targeting at most ten times per second. Opt-in client timings are documented under `docs/performance`.

`ModContent.CATALOG` registers ten normal block items and their recipes/Creative access. Pots reuse `GrowTrayBlockEntity`, with soil heights matching geometry; the crate has one slot and the bed has four. All lamp variants join the existing block-entity type, scheduled fuel loop, client effects and server growth-light query.

`GrowTentBlock` places a facing-aware static model and reserved `GrowTentPartBlock` shell cells in a 3×3×3 footprint. The center and front doorway remain available, including the upper center socket for a real fueled lamp. Placement checks loaded space/world bounds before writing. Parts reference the anchor by rotated index; breaking a part removes the anchor/shell and drops one item, while Creative removal suppresses the drop. Contents remain ordinary independent blocks. Collision shapes are cached. This adds no per-frame tent block-entity renderer or automatic irrigation/climate simulation.

`LedgerScreen` presents three local mouse/keyboard tabs over the original journal painting, showing player name and synced progress. P1 save/network schemas and the P3 Fun Gate are preserved.
