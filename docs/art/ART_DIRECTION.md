# P1 voxel art direction and production notes

## Target and references

The owner requested dimensional, animated, stylized voxel art. The two owner-supplied reference PNGs remain the visual brief: stepped plant silhouettes, layered leaves and dense colored buds, dark wooden raised beds, copper fittings, hanging violet lighting, glass and warm cave contrast. P0's cubes/icons were tooling checks and are not the art benchmark.

P1 assets are original shape/material recipes authored in `tools/generate_game_assets.py`. No downloaded third-party artwork, model pack, texture pack or AI concept image is represented as a shipped game model. The source recipes are editable and regenerate every texture/model deterministically. The room exhibit uses ordinary Minecraft blocks through registry references; no vanilla texture copies are redistributed.

## Technical research

- Inspected the version-matched **NeoForge 21.1.264 sources** distributed at https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.264/neoforge-21.1.264-sources.jar and the Minecraft 1.21.1 sources prepared by NeoForm `20240808.144430`.
- Confirmed additional-model registration through `ModelResourceLocation.standalone`, block-entity renderer registration/culling bounds, client item transforms, per-item tint handlers and the block texture atlas rendering path.
- Confirmed the difference between initial chunk update tags and later block-entity data packets; presentation snapshots have separate decode paths from full persisted plant state.
- Consulted the official NeoForge BER/model documentation URLs; their host returned HTTP 403 in this environment. Implementation therefore uses the exact installed sources, rather than guessing from another Minecraft version's API.
- Looked to the owner references and the game's existing art language for pixel density, material hierarchy, silhouettes and in-hand readability. All custom shapes and material textures are authored for Stonedew.

## Asset language

- **Plants:** stepped volumetric stems, branching palmate leaves and separate modeled bud/pistil clusters. Four visibly different stages and three habits. Leaf, bud and hair colors are separate channels driven by the seed genome. Gentle whole-plant sway is rendered without altering simulation state.
- **Clay pot:** inset soil, an open modeled rim, stepped ceramic walls and a small copper maker plate. Wet soil gets a separate darker material.
- **Planter:** open soil bed, dark wood rails, structural posts and copper corner bands; four independently rendered plant slots.
- **Bulb Lamp:** suspended iron frame, chain geometry, copper end fittings and an emissive violet bulb. Burning fuel changes the actual block's light and appearance. The larger UV Tube tier remains a later gameplay tier.
- **Watering can:** modeled body, handle opening, lid, stepped spout and copper rose. Its custom first-person transform tilts during pouring; water particles/sounds accompany a successful pour.
- **Seed packet / Glow Cell:** volumetric paper packet and copper-framed violet energy cell. Seed packet accents reflect the genome pigment.
- **Ledger:** wooden/brass terminal with paper and violet side light; a usable framed Directive screen.

## Rendering and budgets

Materials are 16×16 RGBA, using restrained three-tone ramps and low-frequency grain. Plants use opaque voxel surfaces, with interior faces removed and coplanar material faces greedily merged. Tiny voxel faces use proportional UV coverage to maintain readable pixel density, and plants sample light at foliage height. Stage/habit meshes are baked and shared; per-tray presentation changes tint and transforms only. Near meshes are capped at 1000 quads and LOD meshes at 40 by `tools/test_assets.py`; the current mesh report is `mesh-budget.json`. LOD switches beyond 24 blocks. No custom shader or external animation library is required.

These budgets are asset checks, not a claim that the future 500-plant performance target has been measured. Test the complete scene in-game, including silhouette, soil contact, hand framing, light-on/off readability, distant plants, and view-frustum edges. Screen captures must be real game captures, not concept renders.

## Reproduce and revise

```sh
python3 tools/generate_game_assets.py
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew runData
```

Change the source recipes and regenerate. Do not edit output JSON by hand. Record each revision and its in-game review in ASSETS.md. This is the first gameplay art pass; later art/animation/audio work stays in the roadmap and must be judged against the owner references.
