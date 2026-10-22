# Asset manifest — reference revision 0.2.3

The authoritative visual brief is the four unchanged images in **CODEX_REFERENCE_NEW**. Current art follows their crisp flat serrated foliage, chunky solid buds, orange tapered ceramics, reinforced timber and cool steel/violet fixtures. See [style guide](docs/art/ART_DIRECTION.md).

| Source / binding | Current use | Authoring source |
| --- | --- | --- |
| `textures/art/leaf_fan.png` | Transparent pixel leaf fans, HUD/Ledger leaf emblem | Original imagegen PNG, reference-guided, copied unchanged |
| `textures/art/painted_materials.png` | Shared 4×4 pixel materials for all current equipment, flowers, Dewstone and UI | Original imagegen PNG, layout in docs/art/PAINTED_TEXTURE_SOURCES.md |
| `models/block/plants/plant_{stage}_{shape}_{load}{,_lod}.{obj,json}` | 64 plant meshes: four stages, four branch layouts, three flowering bud loads | tools/plant_art.py |
| `models/block/equipment/*.obj`, `equipment.mtl` | Tapered pot, plank bed, UV fixture, can, cell, packet and field Ledger; 10 model states | tools/equipment_art.py |
| `models/block/{clay_pot,planter_bed,bulb_lamp,ledger}*.json` | Equipment OBJ bindings, wet/lit variants | Same |
| `models/item/{watering_can,glow_cell,wild_seed}.json` | Rebuilt 3D tool/fuel/packet bindings, item pose/tint retained | Same |
| Runtime material sprites | 256px tiles, 512px leaf sprite, world mip level retained | PaintedMaterialSource, vanilla shader foliage layer |
| `textures/block/*.png`, item particle fallback | Small generated fallback resource identities | tools/generate_game_assets.py |
| HUD / Ledger | Shared pewter/wood/parchment materials, crisp leaf emblem | PaintedUi, PlantHud, LedgerScreen |
| Language, blockstates, recipes, loot, advancements | Existing P1 gameplay resources | StonedewData, narrative source |
| Lamp halo / vanilla sound and particle references | Existing interaction and lighting feedback | Generator, LampRenderer; custom audio remains future work |
| `docs/screenshots/p1-reference-*.png` | Actual current Minecraft captures | In-game review; never generated concept renders |

Paths above are relative to `src/main/resources/assets/stonedew` except named tools/docs. The material ID `copper` remains a compatibility alias but now imports pale pewter. No new registrations are needed for existing worlds to display rebuilt props.

All geometry is original deterministic authoring. Imagegen source PNGs remain unchanged and versioned with SHA-256, dimensions and creation method in docs/art/painted-sources.json; regeneration does not reproduce imagegen's stochastic source creation. Original tool output is retained outside the repository. No third-party texture/model packs or image crops from the references are shipped as game assets.

Plant identity is saved separately from genes; 5/9/13 visible flower sites do not claim working harvest yield in P1. Future pots, tents, jars, processing gear and machines inherit the same reference language when their gameplay phases arrive. Broader animation/audio and final aesthetic acceptance remain open. P3 Fun Gate still precedes automation.

Dead-end audit: Dewstone remains decoration with future terroir/story use; Glow Cells fuel lamps and later equipment; seeds/trays/cans/lamps serve tending and later breeding/upgrades; Ledger serves introductory directives and later journals/contracts. Complete phase-wide audit remains future work.
