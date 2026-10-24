# Asset manifest — 0.2.9

The warm Stonedew banner and unchanged CODEX_REFERENCE_NEW sheets remain authoritative. The latest correction calls for five clear fingers, larger natural plants, smaller flowers, readable spacing, cartoon materials, a cohesive UI and affordable rendering. Actual game captures provide the visual review evidence.

| Asset | Authoring source | Runtime use |
| --- | --- | --- |
| 64 plant models | `tools/plant_art.py` | Four stages, four saved gestures, three mature flower loads, near/distant meshes |
| Five-finger fans | `docs/art/sources/cannabis-fan-v9.png` | Original transparent painting, four folded patches near / one patch far, explicit front/back faces |
| Bracts / stems / sugar leaves | `docs/art/sources/botanical-materials-v9.png` | Neutral tintable painted facets; merged exposed flower geometry with small hairs/resin |
| Equipment material sheet | `docs/art/sources/materials-v9.png` | Shared terracotta, walnut, violet steel/canvas, silver lining, enamel, copper, soil and glass |
| Working equipment / catalog | `tools/equipment_art.py`, `tools/reference_catalog.py` | All existing equipment plus normal item/block bindings for three pots, three lamps and four tents |
| Dewstone | `docs/art/sources/dewstone-v9.png` | Painted plum rock with amethyst/cyan crystal seams |
| Field journal | `docs/art/sources/journal-v9.png`, `LedgerScreen` | Personalized progress page and keyboard-accessible care/workshop tabs |
| Plant HUD | `PaintedUi`, `PlantHud` | Quiet violet panels, green/copper identity, stage and care bars |
| Spatial shading | `tools/bake_occlusion.py` | Vertex occlusion with separate foliage/flower ranges, authored key shading |
| Local effects | `LampRenderer`, `GrowLightCache`, `LampSpill`, `LampBeam` | Fuel-dependent plant bounce, halo, floor spill and bounded shaft |

All five new imagegen paintings are preserved and packaged byte-for-byte. Native atlas windows expose 22 material sprites, with mip level 4. Pillow/NumPy only read the leaf alpha for geometry. Original uploads and rejected historical paintings remain intact in documentation.

The staged generator installs resources after successful Blender baking. Ordinary builds use checked-in resources; Python authoring requirements and Blender are needed only for regeneration. Budget/provenance files live under `docs/art`.

Tent shells are static chunk geometry with collision cells and open interiors; pots and lamps are working P1 blocks. The legacy `/stonedew debug art` gallery also retains explicitly labeled future-tier display previews. Climate/automation behavior is not supplied by those previews. Full-scene shader effects, broader hardware checks and owner aesthetic acceptance remain open.
