# Stonedew visual direction and rendering — 0.2.4

## Target and acceptance

The four unchanged uploads in **CODEX_REFERENCE_NEW** are the exact target: broad legible serrated leaf fans, a full tapered canopy, bulging clustered flower bracts, warm pixel-textured ceramics/timber and cool steel fixtures with violet light. The owner rejected 0.2.3's noisy needle-like foliage, texture treatment and flat lighting. Its screenshots and sources are historical evidence, not an approved benchmark. Automated checks do not establish aesthetic acceptance.

Current actual game captures are `docs/screenshots/p1-shaded-*.png`. Compare these directly with kush.png, violet.png, pots and tents.png and uvs.png. Studio plant captures use a 45-degree field of view and an elevated camera to examine the same surfaces visible in the references. They are unedited Minecraft captures, not generated renders. Room captures document the ordinary world lighting path. Same-camera daylight lamp [on](../screenshots/p1-shaded-uv-day-on.png) / [off](../screenshots/p1-shaded-uv-day-off.png) views show the fueled effect separately from the material palette.

## Shape and color rules

- The canopy has five staggered whorls of broad seven-finger 2D fans, a crown collar, upright inner fill and small leaves at flowering branch tips. Keep individual silhouettes readable; adding many narrow overlapping fans creates a noisy cone. Leaf halves have a restrained crease and contrasting tones; real geometric normals distinguish their tops and undersides.
- Flowers have a bulging six-layer arrangement of connected bracts. Emit only exposed faces. Side colas lean outward; the central leader is larger. Bract tops receive a lighter version of the cultivar color, and visible pistils sit on exposed faces. Violet and olive/orange plants share geometry and material logic.
- Keep four saved branch layouts, three flower loads (5/9/13 mature sites), height/spread/rotation variation and genetic habit proportions. Identity is independent of genetics and persists across care, growth and reload. Visible bud load is not implemented harvest yield; that arrives in P3.
- Material marks use a controlled palette, a deliberate pixel scale and actual shape depth. Orange ceramics have a recessed soil opening, highlighted lip and dark undercut. Timber boards have grain/seams, steel has subdued patches/reflected strips and fittings have pale highlights. Avoid noisy full-sheet textures squeezed onto tiny bolts or thin rails.
- Future fabric pots, tents, processing gear and UI inherit these rules when their gameplay phases arrive. Current uploaded reference tiers do not imply those gameplay systems already exist. P3 Fun Gate still precedes automation.

## Texture authoring

`tools/stylized_textures.py` is the source for the active original artwork: explicit silhouettes, serrations, crease tones, material palettes and marks. Materials are 32px tiles; the leaf fan, emblem and halo are 64px; UI materials form a 128px sheet. The grayscale alpha foliage is tinted in the renderer; the green UI emblem is a separate authored output. All sources regenerate deterministically. Hashes/dimensions are in `authored-sources.json`.

The rejected imagegen fan and material sheet are preserved **unchanged** in `docs/art/archive/0.2.3`, with their original provenance in `painted-sources.json`. They are not used at runtime or packaged in the mod. No reference crops or third-party game assets are used as textures. The old custom SpriteSource/atlas importer and foliage shader wrapper were removed; ordinary Minecraft material sprites retain mip level 4.

Equipment UVs use model-space dimensions so narrow rails/handles/fittings share an intentional texel scale. Do not map an entire material sheet onto each tiny part. Geometry comes from `tools/equipment_art.py`; foliage and flowers from `tools/plant_art.py`; the main generator writes bindings, budgets and source manifests.

## Shading and light

The rejected BER supplied uniform brightness for all flower faces and forced leaf normals upward. The replacement caches geometric surface normals, rotates them with the plant and applies directional diffuse shading per face. Vertex canopy occlusion darkens the interior and preserves brighter exposed tips. World light is sampled by height; plants remain dependent on their real environment. Bract highlights use a separate cultivar-derived tint. Proper reverse normals retain shaded leaf undersides.

A soft alpha contact shadow anchors each plant to its actual soil height. Fueled UV lamps contribute a bounded colored bounce to plant surfaces and a soft violet projection on actual full receiving floors below them. Light queries inspect only already-loaded nearby chunks, cache results and reject blocked rays. Rays begin below the fixture collision hull so the emitter does not block itself; ambient daylight attenuates the colored bounce. Floor receivers are cached and stop at obstructions; these effects turn off with the lamp. The lamp still supplies real Minecraft block light.

These are local directional/ambient/contact and UV effects, not a world-wide shadow-map or ray-tracing implementation. No shader pack, custom GLSL shader or new mod dependency is required. Equipment continues to use Minecraft block/item lighting with its authored surface normals, material shading and emission. Broader shader-pack/hardware/multiplayer validation remains outstanding.

Budgets: **2400 faces near / 100 distant**. Current measured maximum **2376 / 64**; equipment maximum **534**. Extra faces support connected bracts and visible pistils; internal flower faces are discarded. Shared baked meshes and cached surfaces avoid rebuilding geometry per frame. These are geometry bounds, not a 500-plant benchmark.

## Reproduction

Run asset generation and Python checks, then datagen and the Gradle build in separate invocations. Check all stages, both reference colors, side/back foliage, fixture fuel states, shaded lower/upper surfaces, contact shadows, resource reload, planting/watering and saved plant identity. Inspect both a close studio view and a normal gameplay view before publishing screenshots or a JAR.
