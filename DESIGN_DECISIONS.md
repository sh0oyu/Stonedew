# Design decisions

## 2026-10-22 — approved scope

The owner approved Minecraft Java 1.21.1 / NeoForge, Uneasy default dread, the full story (all three endings plus Remember), Hollow Runs, Stonedew as the name, and the cannabis theme with optional Herbal Mode. All later content remains planned; no features have been cut. Automation waits for explicit approval after P3's Fun Gate.

## P0 implementation choices

- Owner clarified the intended art style after P0: chunky, dimensional 3D voxel forms with stylized animation. Gameplay models must establish that direction; use modeled depth and stepped silhouettes, supported by pixel textures and the supplied reference palette. Keep P0 placeholders explicitly provisional. This clarifies presentation without changing gameplay scope.

- Pin Java 21, Gradle 9.2.1, NeoForge 21.1.264 and ModDevGradle 2.0.148, following the inspected official 1.21.1 MDK. Use Mojang mappings without Parchment, matching the brief. The wrapper verifies the distribution SHA-256.
- Preserve the original brief and images. DESIGN.md is the living copy with an implementation-status preface. Assets are generated as small placeholders, rather than cropping the reference sheets into final textures.
- Start with two registered developer objects: decorative Dewstone and Glow Cell. The cell's amethyst/copper recipe exercises the datagen pipeline and is explicitly provisional. Neither object implies that power, plant simulation or worldgen exists yet.
- Use NeoForge's existing event bus for server-only gameplay events; avoid a second bus and a perpetual story tick loop. A persisted debug probe exercises the event bridge now.
- Use an immutable pure-Java story snapshot and an explicit JSON payload inside versioned SavedData. This keeps migrations testable without launching Minecraft. Guard against vanilla's empty-save fallback when a future/corrupt story save fails to decode.
- Validate and atomically publish Wing/cultivar bindings on reload. Generic content categories retain versioned JSON now; their semantic codecs and gameplay handlers arrive with the relevant phases. This is a foundation boundary, not a cut from the design.
- Use separate SERVER and CLIENT configuration. Uneasy/Grower/cannabis defaults are saved; later effect/minigame toggles are declared now and gain behavior when those features exist.
- No custom sound or renderer is necessary for P0. Dewstone uses vanilla amethyst sounds. Shader-free atmospheric effects, plants, machines and mature-theme asset swapping remain scheduled features.
- Keep the full thirteen day-one contracts documented in docs/ARCHITECTURE.md. Trays, genome components, simulation, capabilities and networking are introduced alongside their first real consumers, avoiding fake/inert gameplay implementations.

## Known implementation risks

- P3 first-hour pacing conflicts with the three-day baseline grow plus drying/curing. Resolve through explicit data-driven introductory pacing and dried-only first Orders, then test the complete Cycle. No timing change is hidden in P0.
- Room/environment caching and story-state scopes need multiplayer checks when the corresponding systems exist. The 500-plant performance target is untested until plants/rooms exist.
- A cloud virtual display can verify client boot and UI behavior, but cannot judge tactile feel, audible mix, accessibility comfort or the Fun Gate. Those require the owner's playtest.

## P1 implementation choices

- Implement the approved P1 boundary before processing/automation: real seed → water/light → ripe growth, one shared slot-based tray BE for pot/bed, immutable seed components and compact presentation deltas. Full server plant/genome/care/owner state is never used as the client update payload.
- Use bounded timestamp integration, scheduled visits and a monotonic SavedData growth clock that accounts for sleeping. Catch-up is capped at two Minecraft days and stamps the current visit time, preventing repeated free catch-up. No per-tick loop over all plants.
- P1 samples basic nearby lamps/sun and baseline environment. Full rooms, schedules, problems and historical environment sampling belong to P2. Genome identity drives colors/habits now; inheritance/stat expression remain P5. No claim that these future systems are complete.
- Author original dimensional voxel meshes/materials in a deterministic editable source generator. Inspect exact version-matched NeoForge/Minecraft sources for model, rendering, component and packet APIs. No third-party artwork bundled. See docs/art/ART_DIRECTION.md for sources and budgets.
- First art pass uses shared baked stage/habit meshes, tint channels, subtle sway and a pouring transform; shader-free emissive lamp halos. Near meshes are capped at 1000 quads and distant meshes at 40; these are geometry checks, not the 500-plant performance result.
- Use a separate narrative language input plus typed JSON introductory directive. Player progress survives cloning/relogin and is sent through a compact payload. The Ledger is an actual server-opened menu, not a decorative prop.
- Provide craftable P1 items. Seed crafting is a provisional acquisition route before progression/worldgen. Optional operator demo checks loaded empty space before building, and does not overwrite occupied blocks.
- Debug commands for future rooms/events/contracts/progression explicitly fail with a deferred-phase explanation. Keep implemented commands useful rather than simulate unbuilt systems.
- Keep P0 download archived and publish a new versioned P1 JAR/checksum. Users must remove the old JAR to avoid duplicate mod IDs. P1 worlds are not downgrade-compatible with P0.
