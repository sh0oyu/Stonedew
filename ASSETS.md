# Asset manifest — painted 2D/3D revision 0.2.2

The owner wants an illustrated fantasy style, using Hytale / World of Warcraft as visual shorthand: a dense puffy Christmas-tree bush, painted 2D leaves and solid 3D flowers. Apply the same color/shading/material language across the entire mod. The supplied reference PNGs remain unchanged; the earlier all-voxel and sparse organic passes are historical/intermediate work.

## Current sources and bindings

Paths below are relative to `src/main/resources/assets/stonedew` unless stated.

| Source / IDs | Purpose and status | How to revise |
| --- | --- | --- |
| Root owner reference PNGs | Visual brief, unchanged | Preserve; use for canopy, palette and atmosphere |
| `textures/art/leaf_fan.png` | Original imagegen painted seven-leaf fan, true RGBA transparency; actual foliage/UI texture | Intentionally replace the source painting and review cards in-game; provenance/hash in docs/art/painted-sources.json |
| `textures/art/painted_materials.png` | Original imagegen 4×4 painted material source sheet | Keep layout contract; prompts/layout in docs/art/PAINTED_TEXTURE_SOURCES.md |
| `models/block/plants/{bushy,hybrid,tall}_{0,1,2,3}{,_lod}.{json,obj}`, `plants.mtl` | 24 meshes: 2D alpha cards + solid flower/branch geometry | `tools/plant_art.py`; staggered canopy skirts and nested flowers, shared baked stage/habit meshes |
| `stonedew:block/painted_leaf` | Runtime 512px foliage sprite, separate tint channel | PaintedMaterialSource imports unchanged leaf source; PaintedFoliageLayer uses vanilla cutout shader with mip filtering |
| `stonedew:block/{wood,wood_edge,ceramic,teal,copper,iron,soil,soil_wet,paper,glow,glass,dewstone,plant_bud,plant_leaf,plant_stem,plant_pistil}` | Runtime 256px material sprites from painted sheet | PaintedMaterialSource tile contract; native texture import preserves world mip level |
| `stonedew:block/{leaf,bud,hair,stem}` | Legacy material aliases, now painted too | Same importer; ordinary texture identities retained |
| `textures/block/*.png`, `textures/item/glow_cell.png` | Earlier small procedural textures, retained as resource/datagen fallback | Main asset generator; current appearance uses imported paintings |
| `models/block/clay_pot{,_wet}.json` | Hollow ceramic pot, inset soil, copper plaque; painted surfaces | Equipment geometry in tools/generate_game_assets.py; material source sheet |
| `models/block/planter_bed{,_wet}.json` | Wood rails/posts/copper bands with four plant slots; painted surfaces | Same |
| `models/block/bulb_lamp{,_lit}.json` | Hanging iron/copper lamp, emissive core and fuel state; painted surfaces | Same; LampRenderer halo remains |
| `models/block/ledger.json` | Wood/copper paper terminal; painted surfaces | Same; functional LedgerScreen now uses matching parchment UI |
| `models/item/{glow_cell,watering_can,wild_seed}.json` | 3D cell/can/packet with painted materials | Same; seed tint and can pour pose retained |
| Generated Dewstone block/item | Decorative material, now painted stone | StonedewData geometry + painted sprite import |
| `textures/effect/lamp_halo.png` | Shader-free alpha halo | Main generator + LampRenderer |
| `assets/minecraft/atlases/blocks.json` | Adds Stonedew's client SpriteSource to the shared atlas | Preserves vanilla sources; imports only Stonedew material IDs |
| HUD / Ledger screen | Shared painted wood/copper/parchment and leaf emblem | PaintedUi, PlantHud, LedgerScreen; standard Minecraft font, no external UI library |
| Generated blockstates, block-item parents, loot/tags/recipes/advancements | P1 functional resources | StonedewData; runData before build |
| Generated language | Labels + separate authored directive prose | StonedewData labels; src/main/narrative/en_us.json prose |
| Vanilla sounds/particles | Temporary sound/interaction palette | No custom audio recordings yet |
| Vanilla debug-room blocks | Registry references, not copied textures | DebugShowcase; optional checked exhibit, not worldgen |
| `docs/screenshots/p1-painted-*.png` | Current actual game captures | Capture the game; never substitute generated texture/concept art |
| Earlier P0/P1 screenshot files | Historical and intermediate evidence | Preserved for comparison, not current approved art |

## Provenance and regeneration

Painted sources were created with imagegen specifically for this project, guided by the owner's art direction. No third-party game assets or reference-image crops are bundled. The two source PNGs are immutable versioned inputs with hashes/dimensions/creation method in `docs/art/painted-sources.json`. Geometry/bindings regenerate deterministically; procedural generation does not recreate the stochastic imagegen process. Original tool outputs remain intact.

`tools/generate_game_assets.py` delegates plant meshes to `tools/plant_art.py`; the legacy placeholder entrypoint still works. Runtime texture import converts paintings to mip-compatible sprites without rewriting source artwork. Near mesh ceiling 3000 faces, distant 100; measured 2260 / 86. These are asset bounds, not a 500-plant performance result. See docs/art/ART_DIRECTION.md for rendering research and the mod-wide style rules.

## Remaining art work

Owner feedback still guides final visual acceptance. Richer animations/custom audio, jars and processing gear, machines/NPCs/structures and accessibility/theme variants remain with their gameplay phases. Every future asset inherits this painted 2D/3D direction. Vanilla world blocks remain vanilla. Shader packs, broader hardware/multiplayer and the full performance target remain unvalidated.

## Dead-End Audit

| Item | Active use | Later second use / story hook |
| --- | --- | --- |
| Dewstone | Decorative material | Terroir/generation; Dew/Heart thread |
| Glow Cell | Bulb Lamp fuel | Machine component; inherited Keeper equipment |
| Seed / trays / can / lamp | Planting and tending | Breeding, upgrades and Keeper progression |
| Ledger | Introductory directive screen | Journals, clues, contracts and Cycles |

The complete two-uses/story-hook audit remains phase-dependent and is not claimed finished.
