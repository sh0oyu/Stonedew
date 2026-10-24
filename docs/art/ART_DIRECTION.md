# Art direction and review — 0.2.9

The warm Stonedew banner and CODEX_REFERENCE_NEW guide shape, color and material treatment. The owner's latest correction takes priority: five recognizable fingers, fuller and larger natural branches, smaller flowers, clear spacing, cartoon surfaces, consistent UI/equipment and improved FPS.

## Current construction

Four saved asymmetric branch gestures carry staggered fans with varied pitch and roll. The mature plant uses twenty complete five-finger fans. Each fan has four gently folded patches and its own underside; distant fans use one patch and the same painting. Broad upper and lower leaf normals keep painted greens readable in vanilla lighting. Short sugar leaves remain separate solid silhouettes.

Mature flower loads remain 5/9/13. Smaller egg-shaped flowers retain the stepped bract contour. Coplanar exposed voxel faces merge into rectangles, and hidden surfaces disappear. Four short curved pistils, three sugar leaves and restrained resin accents provide fine detail without the former hundreds of detail faces per flower. Geometry peaks at **2,294 near / 106 distant faces**, versus **13,090 / 98** in the rejected 0.2.8 build. Distant detail begins at ten blocks. Saved genes, appearance identities and eventual harvest yield remain separate.

New shared paintings cover equipment, tools, pots, tents, lamps, botanical surfaces and Dewstone. Bold material planes and restrained marks replace the previous mixed surfaces. Tents use charcoal violet canvas, soft violet silver lining, steel frames and copper fittings. Existing equipment keeps its authored shape and receives the shared material revision.

Four tents, three pots and three lamps now have normal registered items and placeable blocks. Tent shells reserve a 3×3×3 footprint with clear interiors and an upper center lamp socket. Breaking a shell removes its structure and preserves contents. New pots are manually tended; new lamps use the existing Glow Cell fuel loop. Future automation remains gated by P3.

## UI and source handling

The Ledger uses a new original field-journal painting with walnut, copper fittings, violet navigation and quiet parchment. It shows the keeper's name, actual introductory progress, a care page and a workshop page. Tabs support mouse and keyboard navigation. The plant HUD uses matching colors, readable text and compact care bars.

Five original imagegen paintings live in `sources/`, recorded in `painted-sources.json`. Copies in runtime resources retain their original bytes. Minecraft's native atlas loader selects sixteen material windows, one full five-finger fan window, four botanical surfaces and one Dewstone window. Global mip level 4 remains. Alpha is read only to bound leaf geometry; Python does not edit paintings. The field-journal painting is drawn directly in the UI.

## Shading and measurement

Blender BVH bakes vertex occlusion and bounded authored key shadows. Foliage and flower ranges preserve the painted palette, with geometric shading on solid forms and upward-weighted artist normals on leaf fronts/backs. Runtime world light and actual fueled grow-light bounce remain conditional. Plant lighting samples are cached twice per second, outside the face loop. The HUD limits targeting queries to ten per second.

Soil contact/canopy silhouettes, additive fixture halos, bounded shafts and local floor spill remain. These are local techniques; full-scene shader shadows and HDR bloom require a compatible renderer/pack. Compatibility and broad hardware testing remain unverified. See [measured performance](../performance/0.2.9.md).

## Reproduction

```sh
python3 -m pip install -r tools/requirements-art.txt
python3 tools/generate_game_assets.py
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew runData build
```

Blender 4.x must be on PATH for art authoring. Normal builds use checked-in resources. The generator stages all work and installs after baking succeeds. Actual unedited current captures use `docs/screenshots/p1-unified-*`; older prefixes document rejected historical versions. Automated checks validate resource correctness and budgets; visual acceptance remains with the owner.
