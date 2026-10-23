# Reference art rebuild — 0.2.5

## Target and current status

The unchanged uploads in `CODEX_REFERENCE_NEW` and the owner's supplied grow-room image are the targets. They show substantial seven-finger leaf fans, a puffy tapered canopy, individual solid flower bracts, reinforced timber, heavy dark steel and luminous violet fixtures. The owner rejected 0.2.4's thin foliage, tower-like flowers, shallow equipment and flat presentation. Earlier screenshots are historical work, not approved art. Automated tests establish asset integrity, not an aesthetic match.

This revision rebuilds every working P1 prop and authors all four pot, all four UV-fixture and all four tent designs for inspection. `p1-rebuilt-*.png` are unedited Minecraft captures. Studio captures use a 45° field of view; equipment tool display entities are enlarged 1.6× for inspection; the normal client default remains the player's choice. Display previews are explicitly labeled and do not implement future-tier gameplay.

## Geometry

Close foliage uses individually outlined, serrated **2D leaflets**, folded at their midribs, with explicit shaded undersides. Their visible edges are geometry, so distant alpha mipmaps cannot destroy the near silhouette. Seven leaflets meet at a petiole. Five staggered whorls, a crown and limited interior/branch collars form the cone. Leaf material has painted midribs and side veins. Distant models retain inexpensive alpha fans.

Flowers have a fat central heart and three offset rings of individually chamfered bracts, with recessed seams, brighter shoulders and exposed raised pistils. Bracts have separate rotations; side flowers lean with their branches. This replaces the aligned voxel grids. Four saved branch layouts, three flower loads (5/9/13 mature sites) and persistent height/spread/rotation variation remain independent of genetics. Bud load remains visual until harvesting exists.

The wood bed now has a nearly full-block body, three substantial boards per side, an upper lip, chamfered corner posts, feet, plates and slotted bolts. Its collision shape, soil height and foliage targeting move together. The clay pot retains a tapered vessel and recessed soil, with a beveled lip. The can has a blue-gray chamfered reservoir, rolled seams, an open riveted handle, a segmented neck and a nine-hole rose. The twin UV fixture has an open chassis, inset lenses, pale cores, corner windows, a driver, fins, cable and open chains. Seed packaging has an original printed envelope face, folded seam and genome-colored seal. The Ledger gains beveled binding, page edges and hardware; the cell and Dewstone share the updated material treatment.

## Complete reference catalog

`tools/reference_catalog.py` authors fabric and automated-pot previews, a pendant, four/six-bar panels, a twin-bar preview and four tent shells. Tent details include reflective lining, panel seams, gathered flaps and straps, rolled corners, metal poles/couplers, valances, matching suspended fixtures, fan grilles, ribbed ducting, service cables and the final controller. These share materials with working equipment.

In a disposable Creative world with commands, `/stonedew debug art` checks an empty, already-loaded **18 × 7 × 14** volume four blocks east/south and two blocks above the player, then builds a labeled gallery. It refuses occupied or unloaded space. The previews use tagged vanilla display entities and custom models, not new functional machines. Remove preview entities with `/kill @e[tag=stonedew_art_preview]`; the optional exhibit floor/backdrop remain ordinary blocks. Existing P1 pots, lamps and tools remain in the Creative tab. P2/P3 scope and the P3 Fun Gate still precede automation.

## Materials, shading and light

`tools/stylized_textures.py` authors original pixel materials from explicit ramps and material-specific marks: flowing timber grain, kiln mottling, cool metal facets/scuffs, soil clods, fabric/lining, parchment and the seed-envelope illustration. Material tiles are 32px, the envelope/emblem/far fan/light effects 64px, and the UI material sheet 128px. No reference-image crops or other game's textures are used. The rejected imagegen sources remain unchanged in the historical archive, outside runtime assets.

**Ray-baked vertex ambient occlusion** supplies spatial shading at leaf intersections, flower seams, handles, frames, fabric folds and hardware. Blender's BVH casts sixteen cosine-weighted hemisphere rays per unique position/normal, with bounded distance and a contact offset. Results are stored using NeoForge OBJ's native fourth vertex-color index (`vc`); no runtime Blender dependency or custom atlas importer is required. Emissive surfaces stay unoccluded. Lit catalog previews additionally bake ray-tested violet reflections from their actual lens geometry onto the surrounding frame/lining. Native composite models render luminous surfaces in a separate unlit additive item pass (Minecraft's built-in eyes shader), so ordinary item diffuse lighting cannot turn the tube undersides gray. Working P1 fixture effects still follow real fuel state. Indexed vertices and quantized color indices limit file size. Shared meshes are reused across plants.

The plant renderer additionally supplies geometric directional diffuse light, inner-canopy shading, cultivar highlights, world light sampled by height and a soft soil contact shadow. Actual fueled UV fixtures contribute obstruction-aware colored plant light, floor spill, pale emissive tube cores, a soft halo and a subtle light shaft that stops at receiving collision geometry. Effects follow the lamp's lit state and atmosphere setting; shaft intensity follows the visual-intensity setting. Queries inspect only loaded chunks and cache results. Floor projections continue past partial trays to their actual receiving floor; depth testing hides covered pixels instead of leaving an unlit square cell around the pot.

These are baked/local lighting techniques. They do **not** add world-wide shadow maps, screen-space ambient occlusion, HDR bloom or the promotional image's full scene lighting to vanilla Minecraft. Matching those scene effects requires a compatible shader renderer/pack; none is bundled or claimed tested. The actual game captures show the dependency-free result. Authoring a faithful silhouette and materials remains necessary regardless of renderer.

## Budgets and reproducibility

Near plants are bounded to **14,000 faces** (measured maximum 13,300); distant plants remain **100** (measured 64). Detailed geometry switches to the distant mesh after fourteen blocks. Working equipment is bounded to 1,400 faces; catalog models have separate reported counts. This increased geometry is a deliberate quality cost, not a claim that the 500-plant performance target has passed. Cross-hardware and shader-pack validation remain outstanding.

Normal Java builds use checked-in baked resources. Regenerating art requires **Python 3 and Blender 4.x**:

```sh
python3 tools/generate_game_assets.py
python3 -m unittest discover -s tools -p 'test_*.py'
./gradlew runData
./gradlew build
```

Run generation, validation, datagen and build in that order, with no overlapping asset mutations. Generation stages all outputs in a temporary directory, requires the Blender bake to succeed, then installs them. The baker caches whole-prop results by source geometry and baker-code hash, then derives body-pass colors from that complete bake; cold and cached results must agree. Source hashes, dimensions and mesh budgets are recorded beside this document. Inspect real game captures, multiple angles, all stages/load variants, fueled/empty UV and gameplay interactions before publishing a build. Aesthetic acceptance remains with the owner.
