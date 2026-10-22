# Asset manifest — shaded hybrid revision 0.2.4

The authoritative target remains the unchanged images in CODEX_REFERENCE_NEW. The owner rejected 0.2.3's foliage, textures and flat rendering. See [current art and rendering notes](docs/art/ART_DIRECTION.md) and actual `p1-shaded-*.png` game captures; aesthetic acceptance is not implied by tests.

| Active asset | Purpose | Authoring source |
| --- | --- | --- |
| `textures/block/leaf_fan.png` | Broad serrated 64px alpha fan; neutral crease tones receive foliage tint and shading | tools/stylized_textures.py |
| `textures/block/leaf_emblem.png` | Green UI emblem, same authored silhouette | Same |
| `textures/block/*.png` | Original 32px ceramic, timber, steel, soil, parchment, enamel, stone and plant materials | Same |
| `textures/gui/materials.png` | 128px UI sheet composed from the same authored material tiles | Same |
| `textures/effect/{contact_shadow,lamp_halo}.png` | Soil contact shadow and soft UV halo/spill | Same |
| `models/block/plants/plant_{stage}_{shape}_{load}{,_lod}.{obj,json}` | 64 meshes: broad fans, upright fill, connected stepped bracts and exposed pistils | tools/plant_art.py |
| `models/block/equipment/*.obj`, `equipment.mtl` | All current prop states; dimension-based UVs and darker pot undercut | tools/equipment_art.py |
| Equipment block/item JSON | Existing IDs and wet/lit states, poses and tint bindings | Same |
| Plant shading | Geometric normals, directional light, canopy occlusion, cultivar highlights, world light by height | ModelLighting, TrayRenderer |
| UV lighting | Cached loaded-chunk fixture queries, obstruction-aware colored plant bounce, floor projection | GrowLightCache, LampSpill, LampRenderer |
| HUD / Ledger | Shared original materials and emblem | PaintedUi, PlantHud, LedgerScreen |
| Datagen / narrative | Existing P1 recipes, tags, loot, model parents, language and authored prose | StonedewData and narrative source |

Paths are relative to `src/main/resources/assets/stonedew` except named tools/docs/classes. The legacy 16px item particle identity is retained. All geometry and active pixel art are original deterministic authoring; no other game's assets or reference-image crops are bundled. `docs/art/authored-sources.json` records the generated artwork and integrity hashes. The main generator writes geometry budgets and manifests.

The rejected imagegen sources are archived unchanged under `docs/art/archive/0.2.3`, with their provenance hashes preserved; they are no longer shipped. Earlier screenshots/JARs remain historical artifacts. The former painted atlas importer and dedicated foliage layer have been removed. Minecraft's standard sprite/lighting pipeline retains world mip level 4.

Plant shape/load/height/spread/rotation remain persistent, with 5/9/13 visible mature flower sites. Harvest/quality yield is not invented ahead of P3. Future pots, tents, processing equipment and machines inherit the reference language when their gameplay phases arrive. Audio and richer animation remain future work; the full performance target and shader packs remain unvalidated.
