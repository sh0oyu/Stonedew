# Asset manifest — P1

The owner's original reference PNGs remain unchanged at the repository root. Target: dimensional, animated, stylized voxel forms, layered leaves/buds, dark wood, copper and violet/cyan cave lighting. **P1 is the first gameplay art pass**, not a declaration of final art approval. No third-party art/model pack is bundled.

## Original asset sources

`tools/generate_game_assets.py` deterministically authors textures and geometry. `tools/generate_placeholder_assets.py` remains a compatibility entrypoint. Change source recipes and regenerate; do not hand-edit output JSON. All paths below are relative to `src/main/resources/assets/stonedew` unless stated.

| IDs / paths | Kind and status | Revision / replacement source |
| --- | --- | --- |
| Root `Pixel cannabis farm automation sprite sheet.png`, `StoneDew Underground Voxel Garden.png` | Owner references only | Preserve originals; guide palette, silhouette, equipment and atmosphere |
| `textures/block/{ceramic,wood,wood_edge,copper,iron,soil,soil_wet,leaf,bud,hair,stem,glow,glass,paper,teal,dewstone}.png` | 16 original 16×16 material textures; P1 first pass | Generator material palettes/grain recipes |
| `textures/effect/lamp_halo.png` | Original radial alpha emissive halo; P1 first pass | Generator halo function; LampRenderer controls quad |
| `textures/item/glow_cell.png` | Legacy P0 icon retained, no longer item model source | Generator compatibility texture |
| `models/block/clay_pot{,_wet}.json` | Hollow stepped ceramic pot, inset soil/copper plate | Generator equipment recipe; first gameplay pass |
| `models/block/planter_bed{,_wet}.json` | Dimensional wood rails/posts/copper bands and soil | Same; first gameplay pass |
| `models/block/bulb_lamp{,_lit}.json` | Hanging iron/copper frame, modeled chain, emissive core | Same; LampRenderer adds shader-free halo |
| `models/block/ledger.json` | Wood/brass paper terminal with violet fitting | Same; LedgerScreen supplies functional UI |
| `models/item/{glow_cell,watering_can,wild_seed}.json` | Volumetric fuel cell, open-handled can/spout, paper packet | Same; seed tint follows genome; can has first-person pour transform |
| `models/block/plants/{bushy,hybrid,tall}_{0,1,2,3}{,_lod}.json` | 24 stepped volumetric plant meshes | Generator plant/mesh recipes; independent leaf/bud/hair tint channels; sway in TrayRenderer |
| Generated Dewstone cube / block item | Decorative foundation; revised restrained stone texture | StonedewData; still not a gameplay machine |
| Generated blockstates / block-item parents | Pot/bed wet variants, lamp lit variants, Ledger | `StonedewData`, under `src/generated/resources` |
| Generated loot/mining tags/recipes/advancements | Registered blocks and P1 craftable supplies | Same; seed acquisition and balance remain provisional |
| Generated `lang/en_us.json` | UI/item/command/config labels + merged directive prose | StonedewData labels; prose in `src/main/narrative/en_us.json` |
| Vanilla amethyst, water, particle and block sound references | Temporary sound/feedback palette | Java feedback hooks; no custom sound recordings yet |
| Vanilla deepslate/dark oak/glass/chains/lanterns in debug exhibit | Registry references, not redistributed artwork | DebugShowcase; optional checked developer scene, not worldgen |
| `docs/screenshots/p1-*.png` | Actual P1 development-client captures | Capture game window; never substitute concept art |
| `docs/screenshots/p0-creative-tab.png` | Historical P0 evidence | Preserved; not current art benchmark |

Genome schema, cultivar/Wing bindings, growth profile and introductory directive have P1 runtime consumers. Process/effect definitions and generic future content categories remain foundations, as documented in docs/DATAPACKS.md. Original authoring provenance, version-matched API research and mesh budgets are in [art notes](docs/art/ART_DIRECTION.md). Mesh report: `docs/art/mesh-budget.json`.

## Review and remaining work

Near plant meshes max 925 quads; distant variants at most 40. Four Python tests validate geometry/material references/pixel density/original source credits. The in-game review covers stage silhouettes, tints, soil contact, hand framing, lamp light/halo and Ledger readability. These checks do not establish final quality, shader compatibility or the 500-plant performance target.

Still pending: final art iteration against owner feedback, richer stage/interaction animation, custom audio, jars and processing gear (P3), later machines/NPCs/structures and accessibility/theme presentation variants. No reference artwork has been cropped into shipped textures.

## Dead-End Audit

| Item | Current use | Later use / story hook | Status |
| --- | --- | --- | --- |
| Dewstone | Decorative material | Terroir/generation; Dew/Heart thread | Later systems pending |
| Glow Cell | Bulb Lamp fuel | Machine component; inherited Keeper equipment | P1 fuel active; second use later |
| Seed / pot / bed / can / lamp | Planting and tending | Breeding, infrastructure/upgrades, Keeper progression | P1 loop active; later hooks pending |
| Ledger | Introductory directive screen | Journals, clues, contracts and Cycles | Intro active; full narrative later |

The full two-uses/story-hook audit is not claimed complete for phase-limited items.
