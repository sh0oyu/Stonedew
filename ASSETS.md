# Asset manifest — 0.2.6 art revision

The unchanged CODEX_REFERENCE_NEW sheets and supplied grow-room image remain authoritative. The owner rejected 0.2.5. Current work remains subject to visual review; tests do not imply a 1:1 match. See [art direction](docs/art/ART_DIRECTION.md).

| Asset | Source | Runtime use |
| --- | --- | --- |
| 64 plant meshes | `tools/plant_art.py` | Broad stepped flat fans, irregular voxel bracts, all stages/layouts/loads and distant meshes |
| Working equipment | `tools/equipment_art.py` | Pot/bed/lamp states, longer-spout can, cell, packet and Ledger |
| Complete pot/UV/tent catalog | `tools/reference_catalog.py` | Labeled previews via `/stonedew debug art`; gathered cloth, hardware and local fixture glow |
| New material painting | `docs/art/sources/materials-v6.png` | Original imagegen source, packaged unchanged; equipment and UI |
| Native material bindings | `tools/material_atlas.py` | Sixteen distinct inset 256px swatches through Minecraft's built-in atlas loader |
| Foliage, packet and effects | `tools/stylized_textures.py` | Original pixel textures and RGB radiance maps |
| Baked spatial shading | `tools/bake_occlusion.py` | Vertex AO, authored canopy shadows and violet preview reflections |
| Soil silhouettes | `tools/plant_art.py`, `TrayRenderer` | Geometry-derived soft shadows clipped to soil |
| Fueled UV effects | `GrowLightCache`, `LampSpill`, `LampBeam`, `LampRenderer` | Conditional plant bounce, floor spill, additive halo and shaft |

Resources live under `src/main/resources/assets/stonedew`, plus a native atlas definition under `assets/minecraft/atlases/blocks.json`. Its distinct Stonedew sprite IDs do not replace vanilla sprites. The non-power-of-two source image is outside the block sprite directory; selected swatches retain mip level 4. No custom Java atlas importer is used.

Budgets/provenance are under `docs/art`. The generator stages resources and requires successful Blender baking before installation. Python 3 and Blender 4.x are authoring dependencies; normal builds use checked-in assets. The fixed material painting is copied unchanged, not regenerated procedurally.

Original uploads and rejected historical imagegen sources remain intact. No reference crops or third-party game art are bundled. Advanced gallery tiers do not implement automation; bud loads do not invent harvest yield. Full-scene shadow maps/HDR bloom, shader compatibility, broad hardware/performance checks and owner aesthetic approval remain outstanding.
