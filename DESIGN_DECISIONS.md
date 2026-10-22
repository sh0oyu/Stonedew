# Design decisions

## 2026-10-22 — approved scope

The owner approved Minecraft Java 1.21.1 / NeoForge, Uneasy default dread, the full story (all three endings plus Remember), Hollow Runs, Stonedew as the name, and the cannabis theme with optional Herbal Mode. All later content remains planned; no features have been cut. Automation waits for explicit approval after P3's Fun Gate.

## P0 implementation choices

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
