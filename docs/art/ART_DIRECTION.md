# Stonedew art direction — current owner references

## Authority

`CODEX_REFERENCE_NEW/kush.png`, `violet.png`, `pots and tents.png`, and `uvs.png` are the owner's current exact visual references. They supersede the earlier generic Hytale / World of Warcraft interpretation and the soft painted 0.2.2 pass. Preserve the uploaded originals. Actual game captures document implementation; reference renders are not evidence of the game running or owner approval.

## Rules for every mod asset

- Plants combine crisp serrated flat leaf fans with solid stepped clusters of flower bracts. Build a broad lower canopy and taper it toward the dominant top cola. Overlap skirts, inner fans and the crown; avoid a visible ladder of bare stem.
- Leaf colors are fresh grassy green, forest shadow and lime tips. Buds carry the cultivar color. Use broad discrete pixel patches, readable facets and controlled highlights; avoid soft airbrushed foliage or noisy realistic surfaces.
- Terracotta vessels taper toward a narrower foot, with a thick lip and recessed soil. Timber beds use separate warm planks, seams, dark reinforced corners, feet and pale bolts.
- UV fixtures use cool charcoal/purple steel, reinforced end housings, inset violet tubes, driver housings, finned ballast and actual open chain links. Pewter fittings replace the previous decorative copper-heavy kit.
- Tools, packets, cells, Ledger, Dewstone and interface materials inherit the same pixel scale, material palette and restrained glow. Keep text readable and plant information away from chat.
- Reference tiers for fabric/automated pots and grow tents guide future equipment. Those systems are not introduced by this art revision. Do not make decorative fake upgrades imply working room simulation or automation.

## Plant variety

Every planting receives a server-generated saved `appearanceSeed`, separate from its genome. Four branch layouts alter node phase, lean, tier spacing and branch/leaf lengths. Three bud loads produce **5 / 9 / 13 solid mature flower clusters**. Each identity also fixes height/spread (90–110%) and rotation; genetic tall habit still affects proportions. Flowers swell between flowering and ripe stages. Planting from a single seed stack produces varied plants without rewriting genes.

Identity persists through watering, growth, debug time changes, genome edits, chunk load and save/reload. Old P1 plant saves acquire a deterministic identity from lineage, block position and slot. Client snapshots contain bounded appearance parameters rather than the full genome or server appearance seed. Bud load is visual in P1; harvest quantity/quality is not implemented until P3.

## Asset pipeline and rendering

Original reference-guided imagegen sprites replace the previous paintings: a transparent serrated seven-finger leaf fan and a 4×4 pixel material atlas. Source files are copied unchanged from tool output; source hashes/dimensions and briefs are recorded alongside this guide. No reference-image crops or third-party game assets are used as game textures.

`tools/plant_art.py` authors 64 shared OBJ models across four stages, four shapes, three flowering bud loads and near/distant detail. `tools/equipment_art.py` authors all ten current equipment model states, including non-cuboid tapered ceramics and closed rectangular/angled components. `tools/generate_game_assets.py` generates bindings, fallback sprites and budget reports. Baked geometry is shared; no per-frame mesh generation or per-plant baked model copy.

NeoForge 21.1.264's built-in OBJ loader supports separate material tints and emissive ambient light; the equipment MTL uses emission only for actual light sources. A SpriteSource imports the untouched source sheet to 256px materials and foliage to a 512px sprite, retaining Minecraft mip level 4. The foliage layer uses Minecraft's entity cutout shader with mip filtering and fixed world-space cards with explicit back faces. Simplified meshes beyond 24 blocks preserve bud-load differences. Resource reload releases old quad groups.

Exact version-matched NeoForge OBJ/material and Minecraft NativeImage/SpriteSource/RenderType sources were inspected for these APIs. Source artifact: https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.264/neoforge-21.1.264-sources.jar . No custom GLSL shader or new rendering dependency is needed.

Budgets: **1800 faces near / 100 distant**, measured **1454 / 82**; equipment max **534 faces**. These are geometry counts, not a 500-plant performance certification. Shader packs and broad hardware/multiplayer performance remain untested.

## Review and reproduce

Run asset generation, Python asset validation, datagen, then the Gradle build in separate invocations. Inspect `docs/screenshots/p1-reference-*.png` against the owner references: silhouette, visible flower clusters, canopy underside, plant-to-plant differences, tapered ceramics, bolts/chains, tool framing and UI contrast. Earlier screenshots document earlier passes and are not current style benchmarks. Automated tests cannot certify aesthetic acceptance.
