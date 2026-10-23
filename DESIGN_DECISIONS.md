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

## 0.2.1 — owner art correction

- Owner rejected the literal all-voxel plant interpretation. Replace the rigid column buds/sparse foliage with organic puffy flower clusters, green bracts and a dense tapered canopy of arched serrated leaf fans. This overrides the earlier P1 art interpretation; it is not a gameplay scope change.
- Use NeoForge's built-in OBJ loader (inspected exact 21.1.264 ObjLoader/ObjModel/ObjMaterialLibrary sources), with baked smooth normals, material tints and original authored meshes. Do not attempt rounded flowers using only vanilla cuboid elements. No added rendering dependency or custom shader.
- Separate plant authoring into tools/plant_art.py; retain cuboid equipment where appropriate. The renderer preserves baked material color and vertex normals. Organic plants have a revised explicit ceiling of 3000 faces near / 100 distant; the measured maxima are 2970 / 98. Full 500-plant performance remains unproven.
- Preserve P1 save identities and mechanics; adjust foliage selection bounds to fit the fuller canopy. Publish a versioned art correction JAR rather than overwrite the prior artifact. Judge the result using real before/after game captures, not a concept render.

## 0.2.2 — painted 2D/3D style across the mod

- Owner clarified the target as Hytale / World of Warcraft-like illustrated fantasy: painted 2D leaves with solid 3D flowers, forming a dense puffy Christmas-tree bush. This supersedes the earlier all-modeled leaf interpretation and applies to all current/future mod art.
- Create original painted source artwork with imagegen: one transparent seven-leaf fan and a shared 4×4 material sheet. These are actual texture assets. Keep their original files intact, record provenance, and do not claim procedural regeneration reproduces the image generation process. Geometry and bindings remain deterministic.
- Build the canopy with staggered layers of fixed, hinged alpha leaf cards, progressively narrower toward the tip, plus inner cards to hide the trunk. Preserve solid clustered flower geometry. Cards stay in world space; they do not swivel toward the camera.
- Import the source artwork through a client SpriteSource: 256px material tiles and a 512px foliage sprite, with ordinary Minecraft mipmaps. A vanilla entity shader render layer enables mip filtering for leaf cards. This resolves the noisy first direct-texture preview without new GLSL shaders or third-party rendering dependencies. The original imagegen PNGs remain unchanged.
- Bind the shared materials to all existing Stonedew props, tools, seed packets, lamps/cells and Dewstone. Give the Ledger/HUD matching wood/copper/parchment and the same leaf emblem. Vanilla world blocks are not reskinned.
- Keep existing saves and gameplay; widen foliage selection to match the new canopy. Publish a new versioned JAR and actual game screenshots. Art acceptance still requires the owner's visual judgment; unit tests cannot certify style.

## Reference overhaul and plant individuality — 0.2.3

CODEX_REFERENCE_NEW supersedes the earlier painted interpretation. Rebuild the geometry of every existing prop, not only its surfaces. Keep original reference PNGs intact; author new geometry and pixel materials guided by them. Future equipment/tents inherit this direction alongside their gameplay phases.

Appearance is independent of genetics: server-random identity per planting; saved once; four shared branching meshes, three visible flower loads and small continuous proportion/rotation variation. Preserve identity through simulation/care/genome edits and use deterministic position/slot migration for old saves. Sync bounded visual parameters, not the hidden seed or genetics. Flower load describes visual sites; harvest yield is not invented ahead of P3.

## Visual rendering correction — 0.2.4

Owner rejected 0.2.3 as unlike the references, with ugly textures and insufficient shading/lighting. Remove the active imagegen atlas path and archive its originals unchanged; author controlled silhouettes/material ramps directly. Give leaf tops and undersides actual geometric normals. The BER must apply directional and canopy shading rather than supplying equal brightness to every flower face. Use cultivar-derived bract highlights and exposed pistils. UV bounce must depend on actual fueled fixtures, loaded chunks and obstruction checks; contact shadows must sit on actual soil. These local effects do not claim a full world shadow-map pipeline. Review real close-up and gameplay captures against CODEX_REFERENCE_NEW; tests do not establish art approval.


## Reference geometry, baked shading and complete art catalog — 0.2.5

The owner rejected 0.2.4 and asked for substantially closer reference fidelity across all models. Replace close alpha fans with individually outlined flat serrated leaflets, and aligned flower grids with offset chamfered bracts. Keep cheap alpha geometry at distance and preserve saved identities. Rebuild every current prop; the taller wood bed requires matching soil height, collision and targeting changes.

Bake actual spatial ambient occlusion through Blender BVH rays into NeoForge OBJ vertex colors, preserving emission. Blender is an authoring dependency only. Keep indexed geometry and bounded near/distant budgets; the increased detail has an explicit performance cost and is not a completed 500-plant benchmark. Atlas UVs must stay inside each sprite; clip large panels into material tiles to prevent neighboring-texture sampling. Stage generated resources and fail on any bake error before installing results.

Author all referenced pot, lamp and tent tiers now as inspectable art. `/stonedew debug art` creates labeled vanilla display previews in a checked empty loaded volume. It does not register fake functional automation, consume the P3 Fun Gate or change the gameplay phase. Clearly label those limits in the gallery and docs. Do not claim vanilla local effects reproduce a promotional render's full scene shadows/HDR bloom; publish actual in-game evidence.


## Reference art revision — 0.2.6

The owner rejected 0.2.5. Use broader stepped flat fans and a fuller upper canopy, an irregular exposed-voxel bract cluster rather than large cylinder/box tiers, and the reference's leafy-to-flowering stage progression. Preserve saved identities and mature 5/9/13 bud loads.

Create a new original reference-guided material painting with imagegen; preserve and package it unchanged. Bind distinct inset 256px swatches through Minecraft's native unstitch source, without a custom importer, reference-image extraction, vanilla sprite overrides or reduced global mip levels. Equipment and UI share the painting. Keep procedural foliage/effect art separate.

Remove duplicate CPU diffuse shading: the vanilla entity shader already lights normals. Bake spatial AO plus authored leaf-to-leaf shadows, and rasterize original mesh silhouettes for clipped soil shadows. Catalog fixture glow stores radiance in RGB with black borders for additive blending; exclude those planes from occlusion and working chunk models. Actual lamp effects remain fuel-gated. Publish actual game captures, with no claim that tests establish reference identity or a full scene-render match. Automation remains behind the P3 Fun Gate.

## 0.2.7 — natural branch and cannabis leaf correction

- The owner rejected the stacked 0.2.6 canopy and non-cannabis leaflet shapes. The latest banner-led instruction overrides earlier Christmas-tree/cone guidance. Replace radial whorls and crown filler with four uneven connected branches, a slender bent leader, visible gaps and independently pitched/rolled leaf fans. Keep saved identities and four distinct layouts.
- Use a new original seven-finger cannabis leaf painting, preserved and packaged unchanged. Read alpha only for mesh coverage; bind all of it through 25 native 256px atlas windows. Pillow/NumPy are authoring dependencies, with no runtime dependency or image editing. Existing sixteen material swatches remain intact and global mip level 4 remains.
- Keep the bud's established bract volume, as requested; add small sugar leaves, paired curved pistils and non-emissive resin points. Preserve 5/9/13 mature flower counts, placing extra smaller flowers at branch joints. No gameplay or persistence schema changes. Fourteen-block LOD uses the same branch gesture.
- Judge the result in actual Minecraft, from several angles and stages. Equipment is unchanged this revision; tests/resource budgets do not constitute owner visual approval. P1 remains the active gameplay milestone; P2/P3 and the P3 Fun Gate still precede automation.

## 0.2.8 — banner proportions and individual leaf fingers

- The owner rejected 0.2.7 and supplied the warm banner again. Correct the sparse exposed-branch proportions: shorten branch reaches, add overlapping foliage through the center, reduce flower scale and avoid rigid full-fan emblems. Keep four asymmetric layouts, staggered attachments and saved 5/9/13 flower loads.
- Build fans from seven independently posed/folded fingers using a new original quiet green leaflet painting. Imagegen simplified an initial draft after actual client review. Original output bytes remain unchanged in source/runtime; Python only reads alpha. A native 512×1024 window replaces twenty-five v7 fan windows. The rejected v7 original remains in documentation.
- Preserve the established flower volume; add selected raised bract crowns/shoulders. Sugar leaves share the new painting. Existing pistils/resin remain. Use gentler occlusion for overlapping foliage and a brighter green bud color without changing genotype/save data.
- Compare in Minecraft before publication, both neutrally and in a local cave scene. The tent in that scene remains a display preview. No new gameplay, worldgen or automation is implied; P1 and the P3 Fun Gate remain in effect.
