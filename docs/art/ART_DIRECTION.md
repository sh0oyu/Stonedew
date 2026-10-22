# Stonedew art direction — painted 2D and 3D

## Owner direction

The target is an illustrated fantasy style, with **Hytale / World of Warcraft** as visual shorthand. This applies across the entire mod. The owner rejected both the literal all-voxel plants and the sparse, fully modeled leaf pass. The current plant benchmark is a **puffy Christmas-tree-shaped bush**: broad at the base, progressively narrower toward the tip, dense painted 2D leaves, and smaller solid 3D flowers nested among the foliage. Hide most of the trunk.

The unchanged owner reference PNGs at the repository root remain the brief. Use their canopy density, warm wood/copper, colorful flower clusters and cozy cave atmosphere. Do not copy other games' artwork. A screenshot from an earlier rejected pass is historical evidence, not an approved target.

## Visual rules for current and future assets

- **Silhouette first:** broad readable masses, a tapered plant canopy, irregular flower clusters, characterful prop proportions. Avoid long exposed sticks with isolated balls on the ends.
- **2D leaves, 3D flowers:** painted serrated leaf fans on overlapping alpha cards, arranged around the plant in fixed world space. A slight bend in a card gives depth without modeling every leaflet. Flowers keep solid rounded geometry, bracts and smaller tufts. Cards do not swivel toward the camera.
- **Painted surfaces:** broad brush marks, warm highlights, cool shadows and restrained surface detail. Geometry supplies useful depth; painting supplies veins, grain, material variation and softness. Avoid flat plastic color, excessive pixel noise and a compulsory voxel treatment on every object.
- **Shared palette:** green foliage with lime/olive highlights, cool forest shadows, violet/teal/amber flower accents; walnut wood, warm copper, terracotta, teal enamel and cream parchment. Reserve strong glow for actual light/fuel objects.
- **Props and tools:** use the same painted material family as the plants. Beds, pots, lamps, seed packets, cells and the watering can must look like a coherent kit. Minecraft's placement grid can remain visible without forcing every detail to be a cube.
- **UI and icons:** a fantasy field journal: painted wood/copper framing, parchment, dark readable type and the shared leaf emblem. Plant information should leave the bush visible and avoid the chat area. Future jars, processing equipment, machines, NPCs and story screens inherit this direction.
- **Animation:** gentle readable motion and tactile interactions. Current plant sway/can pouring remain; richer leaf, flower and processing animation belongs to later work. Do not claim unimplemented animation as shipped.

## Actual source assets and provenance

`textures/art/leaf_fan.png` is an original imagegen texture: one transparent seven-leaf fan with painted veins, teeth and color masses. `textures/art/painted_materials.png` is an original imagegen 4×4 material source sheet. They are used in the game, rather than presented as concept renders. The source PNGs are preserved unchanged; hashes, dimensions and provenance are in `painted-sources.json`. Prompt briefs are in `PAINTED_TEXTURE_SOURCES.md`.

Geometry and bindings are authored in `tools/plant_art.py` and `tools/generate_game_assets.py`. Regenerating those is deterministic; it does not rerun or reproduce the stochastic image generation process. The versioned PNGs are the painting sources. Earlier 16px procedural textures remain fallbacks and supply datagen resource identities.

No third-party game texture/model pack or cropped reference artwork is bundled. The visual influence is not a claim that these are Hytale/WoW assets or that the owner has approved the finished style.

## Rendering and technical research

Inspected exact NeoForge **21.1.264** OBJ loader/material and SpriteSource registration sources, plus Minecraft 1.21.1 / NeoForm `20240808.144430` SpriteSource, LazyLoadedImage, NativeImage, RenderType, TextureAtlasSprite and GuiGraphics sources. NeoForge source artifact: https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.264/neoforge-21.1.264-sources.jar . Public documentation hosts previously returned HTTP 403; installed version-matched sources supplied the API evidence.

- 24 OBJ models cover four stages, three habits and near/distant detail. Mature plants use eight staggered foliage skirts and inner cards. The immutable genome continues to drive habit and flower tint; leaf tint is subtle so it preserves the painted palette.
- A client SpriteSource imports the unchanged source sheet as 256px material sprites and the foliage as a 512px sprite. This keeps sprite dimensions suitable for Minecraft mipmaps and avoids lowering the whole world's mip level. The same material identities update every existing Stonedew prop.
- The foliage layer uses a vanilla entity cutout shader with mip filtering; no new GLSL shader or rendering dependency. An initial direct high-resolution preview shimmered at game distance; the atlas/mip path replaces it.
- Plant meshes are shared; cached quad groups are released with old models after resource reload. Distant detail switches beyond 24 blocks. Upward foliage normals keep the painted leaf cards readable from both sides.
- The Ledger/HUD sample the same material source and use the same painted leaf emblem. Vanilla world blocks remain vanilla.

The geometry ceiling remains **3000 faces near / 100 distant**, measured **2260 / 86**. This is a geometry bound, not the future 500-plant performance result. Shader packs, multiplayer and broad hardware testing still need dedicated validation.

## Review and reproduce

Judge actual game captures: `docs/screenshots/p1-painted-*.png`. Check the bush from several angles and distances, the underside of leaves, source alpha edges, flower visibility, all stages/habits, tool framing and UI contrast. Earlier `p1-grow-room.png` and `p1-organic-*.png` show rejected/intermediate passes. Automated checks cannot certify aesthetics.

```sh
python3 tools/generate_game_assets.py
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew runData
./gradlew build
```

Edit geometry recipes or intentionally replace the versioned painting sources, then regenerate and review in-game. Preserve original reference images. Full manual-loop gameplay still proceeds through P2/P3, with the explicit Fun Gate before automation.
