# Asset manifest — 0.2.5 reference rebuild

The unchanged `CODEX_REFERENCE_NEW` sheets and supplied grow-room image remain the target. Earlier art was rejected; tests do not imply approval. See [art direction, lighting limits and gallery](docs/art/ART_DIRECTION.md).

| Asset | Authoring source | Runtime use |
| --- | --- | --- |
| 64 plant meshes | `tools/plant_art.py` | Individually serrated flat leaflets, chamfered flower bracts; cheap distant fans |
| Working equipment | `tools/equipment_art.py` | Rebuilt pot/bed/lamp states, can, cell, packet and Ledger |
| Complete pot/UV/tent catalog | `tools/reference_catalog.py` | Labeled display previews via `/stonedew debug art`; future gameplay remains deferred |
| Pixel materials / effects / seed illustration | `tools/stylized_textures.py` | Original 32/64px material maps and 128px shared UI sheet |
| Ray-baked vertex AO | `tools/bake_occlusion.py` | Native OBJ vertex AO and lit-preview reflections, baked with Blender; no runtime dependency |
| Directional/canopy shading | `ModelLighting`, `TrayRenderer` | Cached geometric normals, cultivar colors, world light, soil contact |
| Fueled UV effects | `GrowLightCache`, `LampSpill`, `LampBeam`, `LampRenderer` | Local colored plant light, floor spill, halo/shaft and separate emissive surface passes |
| HUD / Ledger UI | `PaintedUi`, `PlantHud`, `LedgerScreen` | Shared materials and leaf emblem |

Resources live under `src/main/resources/assets/stonedew`. Geometry/material budgets and texture integrity hashes are in `docs/art`. The generator stages results before installation and fails if baking fails. Python 3 and Blender 4.x are required only when regenerating artwork; Gradle builds use checked-in assets.

No reference crops or third-party game art are bundled. The old rejected imagegen sources remain unchanged in `docs/art/archive/0.2.3`, outside mod resources. Original reference uploads are preserved. Vanilla world blocks remain vanilla. Full scene shadows/bloom, shader compatibility, broad hardware/performance and owner aesthetic approval remain outstanding. Bud loads do not invent harvest yield; future-tier display models do not implement automation.
