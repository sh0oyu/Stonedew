# Art direction and review — 0.2.6

The unchanged `CODEX_REFERENCE_NEW/kush.png`, `violet.png`, `pots and tents.png`, `uvs.png` and the supplied grow-room illustration remain authoritative. The owner rejected **0.2.5**. This revision is a new review candidate, **not an approved or certified 1:1 recreation**. Automated checks establish resource integrity and gameplay behavior, not aesthetic quality.

## Plant forms

`tools/plant_art.py` authors broad, flat seven-finger fans. Their square stepped outlines are actual geometry, with shallow midrib folds and explicit undersides. Wider upper whorls, differently inclined secondary branch fans and a substantial green stem form the canopy. Seedlings use two stepped cotyledons; young and leafy stages precede mature flowers, following the reference sheet.

Flowers are irregular solid clusters of small voxel bracts, with only exposed faces emitted, pale shoulders, varied purple/green facets and five short pistil clusters on exposed top faces. They replace the rejected large chamfered cylinders/box tiers. Side flowers lean along their branches. Four saved branch layouts, 5/9/13 mature sites, size and rotation variation remain independent of genetics and persist through care, genome edits and reload. Bud load is visual until P3 harvesting.

## Materials and equipment

`docs/art/sources/materials-v6.png` is a **new original reference-guided painting**, created with imagegen. It is distinct from the rejected 0.2.3 artwork. Its original bytes are packaged unchanged at `textures/art/materials_v6.png`; the original output also remains in the execution workspace. Python does not resample, edit or regenerate that painting.

`tools/material_atlas.py` defines sixteen inset 256px UV swatches using Minecraft's built-in `minecraft:unstitch` source. All have separate `stonedew:block/painted/*` IDs. The non-power-of-two source stays outside `textures/block`, so global block mip levels remain **4**. Native UV windows avoid adjacent materials. This uses the engine's atlas loader, without a custom Java importer or overriding vanilla sprites. Terracotta, timber, dark metal, fittings, lining, soil, blue-gray enamel and parchment supply the equipment and UI surfaces. The seed-envelope print, foliage materials and effects remain original authored pixel assets.

Working pots/beds retain tapered ceramic lips, recessed soil, broad wood planks, heavy posts/feet and slotted hardware. The watering can now has a longer visible neck and tilted nine-hole rose, open riveted handle, rolled seams and cast body. The cell, bound Ledger, seed packaging and open twin UV fixture use the revised materials too.

All four pot, UV and tent tiers are available through `/stonedew debug art`. Tent art has broad gathered cloth flaps, straps, reflective floors/lining, poles, couplers, bolts, grilles, ribbed ducts, cables and cyan controls. The fan/control side follows the reference's front view. Advanced pots, lamps and tents remain **labeled art previews**, without automation functionality. The checked gallery refuses occupied or unloaded space; its display entities carry `stonedew_art_preview`. The floor/backdrop are ordinary blocks. P2/P3 and the P3 Fun Gate remain ahead of automation.

## Shading and light

Blender's BVH bakes sixteen-ray ambient occlusion into native OBJ `vc` colors. Plant meshes additionally receive a bounded three-ray authored key shadow, giving overlapping fans and flower bracts distinct interior shading. This is baked stylized lighting. The entity shader applies diffuse surface lighting **once**; the removed CPU pass previously compounded it and dulled the colors. Cultivar colors, height-based world light and obstruction-aware fueled UV bounce remain runtime inputs.

Original geometry rasterization produces soft foliage-shaped soil shadows. The renderer maps them through the plant's saved rotation/spread and clips them to the actual pot/bed soil. They augment the small base contact shadow; they are not reference-image crops or global dynamic shadows.

Lit catalog previews bake violet reflections from the actual emitting geometry onto their frame/lining. Native composite item models separate diffuse bodies from unlit additive emission. Small local glow meshes use RGB radiance falloff with black borders: Minecraft's ONE/ONE additive blending ignores alpha. Glow planes are excluded from occlusion rays and working lamp chunk geometry. Actual lamps use a fuel/atmosphere-gated additive halo, local spill and depth-bounded shaft; intensity controls the halo/shaft. No shader pack is required.

These techniques do **not** implement a world shadow-map renderer, screen-space AO or full-scene HDR bloom. Shader-pack compatibility, broader hardware checks, the 500-plant performance target and aesthetic acceptance remain unverified. Model shape/material fidelity still matters independently of those scene effects.

## Reproduction and review

Normal builds use checked-in resources. Art regeneration requires Python 3 and Blender 4.x:

```sh
python3 tools/generate_game_assets.py
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew runData
./gradlew build
```

The generator stages resources, requires a successful bake and installs results afterward. Whole-prop AO caches include source/baker hashes; body-pass colors derive from the complete prop. The fixed material painting is copied unchanged. Reports record budgets and provenance. Measured plant maxima are **12,250 near / 64 distant faces**, within **14,000 / 100** limits; the detailed mesh changes after fourteen blocks. Equipment maximum: **1,337**; catalog maximum: **2,775**. These budgets are not a performance benchmark.

Current `p1-revision-*.png` files are unedited actual Minecraft captures. Compare stages, flower loads, front/side/back geometry, tools and all catalog tiers against the originals. Studio views use a 30° FOV; equipment tool displays are enlarged 1.6×. Older `p1-rebuilt-*`, `p1-shaded-*` and `p1-reference-*` captures document rejected historical revisions.
