# Art direction and review — 0.2.8

The unchanged CODEX_REFERENCE_NEW sheets and the warm Stonedew grow-room banner remain authoritative. The owner rejected 0.2.7: its long bare branches and rigid full-fan paintings did not match the reference's dense, overlapping foliage. This revision changes those proportions and the construction of individual leaves. Actual game captures are the review evidence; resource tests do not establish aesthetic acceptance.

## Plant forms

Four short, uneven side branches support overlapping leaf clusters. Twelve branch fans and ten staggered stem/apical fans fill the mature plant's center. Sizes taper gradually and attachments stay staggered, avoiding symmetric rings or an exposed branching diagram. Each fan has seven separate fingers, each with its own pitch, twist, arch, droop and real midrib fold. Branch gestures and saved size/rotation identities remain distinct across four layouts.

The fixed original `sources/cannabis-leaflet-v8.png` supplies a single serrated finger with quiet green facets. Imagegen created and simplified the painting; Python never edits, resizes or rewrites it. Read-only alpha measurements determine six compact longitudinal mesh bands and one native 512×1024 atlas window. Front and underside faces have opposite normals and retain the original painting's colors. The rejected full-fan v7 painting remains unchanged in documentation, outside runtime resources.

Seedlings retain cotyledons; young plants have three staggered compound leaves. The leafy stage develops the same branch structure before flowers. Mature flowers keep the established egg-shaped bract volume but sit smaller within the foliage. Selected exposed bracts gain shallow raised crowns with sloping shoulders. Sugar leaves use the new painting too; paired curved pistils and sparse non-emissive resin points remain. Medium/high loads add small axillary flowers, retaining the 5/9/13 mature-load contract. The green flower palette is brighter. No planting, growth, harvesting or save-schema mechanics change.

## Materials and equipment

`docs/art/sources/materials-v6.png` is a **new original reference-guided painting**, created with imagegen. It is distinct from the rejected 0.2.3 artwork. Its original bytes are packaged unchanged at `textures/art/materials_v6.png`; the original output also remains in the execution workspace. Python does not resample, edit or regenerate that painting.

`tools/material_atlas.py` defines sixteen inset 256px UV swatches using Minecraft's built-in `minecraft:unstitch` source. All have separate `stonedew:block/painted/*` IDs. The non-power-of-two source stays outside `textures/block`, so global block mip levels remain **4**. Native UV windows avoid adjacent materials. This uses the engine's atlas loader, without a custom Java importer or overriding vanilla sprites. Terracotta, timber, dark metal, fittings, lining, soil, blue-gray enamel and parchment supply the equipment and UI surfaces. The seed-envelope print, small sugar-leaf/cotyledon materials, distant leaf cards and effects remain original authored pixel assets. The near fan uses the separate original painting described above.

Working pots/beds retain tapered ceramic lips, recessed soil, broad wood planks, heavy posts/feet and slotted hardware. The watering can now has a longer visible neck and tilted nine-hole rose, open riveted handle, rolled seams and cast body. The cell, bound Ledger, seed packaging and open twin UV fixture use the revised materials too.

All four pot, UV and tent tiers are available through `/stonedew debug art`. Tent art has broad gathered cloth flaps, straps, reflective floors/lining, poles, couplers, bolts, grilles, ribbed ducts, cables and cyan controls. The fan/control side follows the reference's front view. Advanced pots, lamps and tents remain **labeled art previews**, without automation functionality. The checked gallery refuses occupied or unloaded space; its display entities carry `stonedew_art_preview`. The floor/backdrop are ordinary blocks. P2/P3 and the P3 Fun Gate remain ahead of automation.

## Shading and light

Blender's BVH bakes sixteen-ray ambient occlusion into native OBJ `vc` colors. Plant meshes additionally receive a bounded three-ray authored key shadow. Foliage uses gentler ambient/key shadow ranges than solid props, preserving green interiors when many leaves overlap. This is baked stylized lighting. The entity shader applies diffuse surface lighting **once**; the removed CPU pass previously compounded it and dulled the colors. Cultivar colors, height-based world light and obstruction-aware fueled UV bounce remain runtime inputs.

Original geometry rasterization produces soft foliage-shaped soil shadows. The renderer maps them through the plant's saved rotation/spread and clips them to the actual pot/bed soil. They augment the small base contact shadow; they are not reference-image crops or global dynamic shadows.

Lit catalog previews bake violet reflections from the actual emitting geometry onto their frame/lining. Native composite item models separate diffuse bodies from unlit additive emission. Small local glow meshes use RGB radiance falloff with black borders: Minecraft's ONE/ONE additive blending ignores alpha. Glow planes are excluded from occlusion rays and working lamp chunk geometry. Actual lamps use a fuel/atmosphere-gated additive halo, local spill and depth-bounded shaft; intensity controls the halo/shaft. No shader pack is required.

These techniques do **not** implement a world shadow-map renderer, screen-space AO or full-scene HDR bloom. Shader-pack compatibility, broader hardware checks, the 500-plant performance target and aesthetic acceptance remain unverified. Model shape/material fidelity still matters independently of those scene effects.

## Reproduction and review

Normal builds use checked-in resources. Art regeneration requires Python 3, Pillow, NumPy and Blender 4.x:

```sh
python3 -m pip install -r tools/requirements-art.txt
python3 tools/generate_game_assets.py
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew runData
./gradlew build
```

The generator stages resources, requires a successful bake and installs results afterward. Whole-prop AO caches include source/baker hashes; body-pass colors derive from the complete prop. The fixed material painting is copied unchanged. Reports record budgets and provenance. Measured plant maxima are **13,090 near / 98 distant faces**, within **14,000 / 100** limits; the detailed mesh changes after fourteen blocks. Equipment maximum: **1,337**; catalog maximum: **2,775**. These budgets are not a performance benchmark.

Current `p1-canopy-*.png` images are unedited Minecraft captures. Inspect both flower palettes, front/back, close details, growth stages and saved loads against the reference. Studio views use 30° FOV with a lower viewing angle to compare the banner silhouette; the gameplay view uses 70°. The cave comparison scene uses ordinary Minecraft blocks, working P1 equipment and an existing tent display preview; it is a local art test, not new worldgen or functional automation. Earlier `p1-botanical-*` and other plant captures document rejected historical revisions. Equipment/catalog geometry is unchanged this revision.

The tray renderer now rejects only degenerate surfaces: its old area threshold discarded most thin pistil faces and every resin facet in the inspected small bud. The lower threshold retains those valid surfaces and small leaf bands.
