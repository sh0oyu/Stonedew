# Reference-guided pixel texture sources — 0.2.3

The historical filenames are retained to avoid broken resource-pack bindings. These are now crisp pixel textures matching CODEX_REFERENCE_NEW rather than the soft painted 0.2.2 sources. Tool output PNGs are copied unchanged; hashes and exact dimensions are in painted-sources.json. The leaf source may be rectangular; native runtime import normalizes it to a square sprite. Materials use a square 4×4 layout.

## Leaf brief

One isolated seven-finger cannabis fan, top-down flat orthographic game texture. Stem root at bottom center, longest finger up. Narrow serrated fingers with transparent gaps, fresh grassy greens, lime tips and forest-green creases. Crisp stepped 64px-style pixel edges; no realistic veins, airbrush, background, soil, buds or text. Guided by kush.png and violet.png.

## Material brief / layout contract

A flat, even 4×4 atlas of pixel surfaces, edge to edge, no borders/gaps/labels/objects. Discrete broad square patches with reference-matched ceramic, wood and purple-charcoal machinery. Guided by pots and tents.png, uvs.png and kush.png.

| Row | Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- | --- |
| 1 | Warm horizontal timber planks | Amber end grain | Orange terracotta | Teal enamel |
| 2 | Pale pewter | Purple-charcoal steel | Brown soil | Wet soil |
| 3 | Cream parchment | Violet UV emission | Frosted lavender glass | Dark violet-flecked stone |
| 4 | Neutral white/gray flower bracts for tinting | Green leaf surface | Dark green stem | Ivory pistil |

Runtime SpriteSource uses a small tile inset to avoid boundary bleed. Equipment materials use per-face normals and bounded material multipliers; flower colors use existing genome tint channels. Only the emission material receives full ambient light. Alpha leaf cards remain fixed world geometry with mip filtering. Source images are original project artwork, not crops of the user's renders or another game's assets.
