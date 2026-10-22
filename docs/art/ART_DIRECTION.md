# Plant art correction — 0.2.1

## Owner direction and references

The owner rejected the first P1 plant pass: rigid column buds, sparse stems and literal voxel geometry did not resemble the supplied references. The correction is **puffy organic weed plants with fuller leaves**, not an all-voxel requirement. Equipment and the Minecraft room may remain blockier.

The unchanged root references are `Pixel cannabis farm automation sprite sheet.png` and `StoneDew Underground Voxel Garden.png`. Their useful plant cues are a tapered bush silhouette, broad palmate serrated leaves, dense layered foliage, rounded irregular flower clusters among green bracts, and distinct seedling/vegetative/flowering forms. Purple/teal/amber accents should not erase the foliage structure.

## Authored assets

- `tools/plant_art.py` authors OBJ surface meshes: folded/arched leaflets with serrated edges and explicit back faces; branching stems; lobed ellipsoid flower bodies with overlapping rounded tufts, green bracts, small sugar leaves and pistils. Four stages × three habits × near/distant detail = 24 models.
- `tools/generate_game_assets.py` authors blockier equipment and original material textures. Four new organic materials provide leaf veins, grouped bud detail/resin glints, stems and pistils. These remain 16×16; geometry provides the silhouette.
- Matching JSON definitions use NeoForge's built-in `neoforge:obj` loader and a shared `plants.mtl`. Tint channels remain driven by persistent genome data. No external rendering library or custom shader is required.
- TrayRenderer preserves baked material color and per-vertex normals. It shares baked meshes, samples foliage light and adds gentle sway. Equipment, pouring animation and gameplay remain P1.

No third-party artwork/model pack, reference-image crop or generated concept image is bundled as a game asset. Every custom mesh/material is reproducible from the authored source. Vanilla room blocks are registry references, not copied textures.

## Technical research

Inspected the exact **NeoForge 21.1.264** `ObjLoader`, `ObjModel` and `ObjMaterialLibrary` sources from https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.264/neoforge-21.1.264-sources.jar. Confirmed loader JSON fields, relative MTL resolution, namespaced material textures, `neoforge_TintIndex`, triangle/quad baking and explicit normals. Inspected Minecraft 1.21.1/NeoForm `20240808.144430` VertexConsumer and Sheets sources to retain baked colors/normals and correct foliage back faces. Earlier additional-model, BER, component and update-packet research remains applicable. Official web docs returned HTTP 403; version-matched installed sources supplied the API evidence.

## Budgets and review

The organic revision changes the geometry budget explicitly: at most **3000 baked faces near / 100 distant**, measured **2970 / 98**. Distant models switch beyond 24 blocks. `mesh-budget.json` records each mesh. This is a geometry bound, not proof of the future 500-plant performance target.

Five Python tests validate model coverage/bounds/budgets, OBJ indices/unit normals/materials, texture references, pixel density and source credits. Review actual in-game close-ups, bed density, multiple angles, all stages/pigments/habits, underside foliage and distant silhouettes. Compare with `docs/screenshots/p1-grow-room.png`, the rejected previous pass. Current captures use `p1-organic-*.png`.

```sh
python3 tools/generate_game_assets.py
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew runData
./gradlew build
```

Edit source recipes and regenerate. Do not hand-edit OBJ/JSON output. Further visual iteration remains subject to the owner's feedback; tests cannot certify aesthetics.
