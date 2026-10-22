# Painted texture source briefs

Both source PNGs were created with the imagegen tool for Stonedew on 2026-10-22. The original imagegen outputs remain intact in `textures/art/`. Hashes and dimensions: `painted-sources.json`. These are actual production texture inputs; in-game screenshots are captured separately.

## Leaf fan

Creation used the owner's two reference images for visual direction. Brief: a single flat, broad seven-leaf cannabis fan on true transparency, petiole at bottom center, central leaflet toward top center. Painted fantasy RPG treatment: confident broad brush strokes, lime/olive highlights, forest/teal shadows, readable serrated edges and veins. No pot, flowers, scene, labels, external cast shadow or voxel geometry. The whole leaf fan maps onto alpha cards, so the cutout supplies the leaf shapes rather than hundreds of leaflet polygons.

## Material sheet

Creation brief: a square exact 4×4 grid of flat painted material swatches, no labels/borders/gutters/objects, all tiles edge to edge. Broad low-frequency brush texture and warm highlights/cool shadows.

| Row | Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- | --- |
| 1 | Dark walnut planks | Lighter wood/end grain | Terracotta ceramic | Teal enamel |
| 2 | Burnished copper | Charcoal-purple iron | Rich soil | Moist soil |
| 3 | Cream parchment | Violet crystal/glow | Pale cyan glass | Muted violet stone |
| 4 | Pale neutral bud/bracts for tinting | Painted leaf surface | Plant stem | Cream-gold pistils |

The runtime importer samples each tile with a small inset and normalizes it to a 256px sprite; the foliage source becomes a 512px sprite. This is the game's texture import path, preserving the source files and ordinary Minecraft mip filtering. UI panels sample the original sheet by normalized tile coordinates.

Future generated or authored assets must follow `ART_DIRECTION.md`. Do not present generated source textures or concept art as screenshots of implemented gameplay.
