# Changelog


## 0.2.7-p1 — cannabis fans and natural branches — 2026-10-23

Replaces the rejected 0.2.6 plant architecture following the owner's latest banner-led correction.

- Four uneven connected side branches, a slender bent stem and eleven individually pitched/rolled mature leaf fans replace radial tiers and the crown rosette. Larger fans have recognizable narrow serrated fingers, veins and visible petioles; gaps and different facing directions preserve the branch silhouette. Young plants use three staggered fans before the leafy branch stage.
- New original seven-finger cannabis painting, preserved and packaged unchanged. Read-only alpha analysis authors conservative double-sided geometry; 25 native 256px atlas windows cover the entire original without image editing. Existing material swatches and mip level 4 remain. White runtime leaf tint preserves the painted greens.
- Retained the established flower bract volume; added small serrated sugar leaves, eight pairs of curved pistils and sparse non-emissive resin points per detailed flower. Saved 5/9/13 mature loads now add smaller axillary flowers rather than equal-sized flower tiers. Persistence and gameplay remain P1.
- All 64 near/distant plant meshes regenerated; maximum **11,762 / 98 faces**, within existing 14,000/100 limits. Distant flowers also use tapered eight-face silhouettes instead of rectangular blocks. Equipment/catalog art is unchanged.

Validation: Java 21 / NeoForge build and datagen pass (zero changed data outputs); **57 JUnit tests** and **11 asset checks** pass. All **272 resource/report files** regenerate byte-identically; all **268 packaged asset files** match source. Actual Minecraft checks cover both flower palettes, front/back and bud close-up, four growth stages, saved 5/9/13 loads, native atlas reload at mip level 4 and fueled lamp on/off. Survival watering changes water about **7.48→37.28**, using one pour (8→7) while preserving appearance seed 3, genome and stage. Save/reopen also retained the green genome, stage 3, appearance seed 3 and seven-pour can component; water followed normal simulation. Unedited captures use the `p1-botanical-*` prefix. Reference images and the original master brief remain unchanged. Owner aesthetic acceptance, shader compatibility and the full hardware/performance target remain open.


## 0.2.6-p1 — leaf forms, painted materials and local radiance — 2026-10-23

Revises the owner-rejected 0.2.5 art. This is an art review candidate, without a claimed 1:1 recreation or aesthetic approval.

- Broad square-stepped flat leaflets, fuller upper whorls, differently inclined branch/interior fans and a thicker stem replace the drooping narrow canopy. Stepped seedling leaves and leafy young/middle stages follow the reference progression; irregular exposed-voxel bract clusters replace tall cylinder/box tiers at maturity. Saved layouts, proportions, rotation and 5/9/13 mature flower loads remain intact.
- A new original reference-guided material painting supplies equipment/UI surfaces. The original is preserved and packaged unchanged. Minecraft's native atlas loader exposes sixteen distinct inset 256px swatches; no vanilla sprite overrides, custom Java importer or global mip reduction. Large-panel UV clipping remains.
- Longer watering-can neck, tilted nine-hole rose, broad gathered tent flaps, reflective floors, corrected fan/control side and automated-pot fasteners. Every current equipment/catalog model uses revised material bindings. Advanced tiers remain labeled art previews.
- Removed duplicate CPU diffuse shading that dulled the entity shader's lighting. Baked canopy self-shadows supplement spatial AO; original mesh rasterization supplies foliage-shaped soil shadows. Bract facets have stronger painted value variation and a more saturated violet pigment.
- Lit catalog frames/lining receive stronger ray-tested violet reflections. Separate additive emission passes preserve pale cores and local glow. RGB falloff maps prevent rectangular halos with ONE/ONE blending, and glow planes do not occlude baking. Actual lamps retain fuel/atmosphere-gated halo, spill and shaft. UI parchment is subdued behind small text.
- Plant detail measures **12,250 / 64 faces** near/distant, within the existing 14,000/100 ceiling. Equipment maximum remains 1,337; catalog maximum is 2,775. This is not a 500-plant performance result.

Validation: clean Java 21 / NeoForge build, datagen with zero changed data outputs, **57 JUnit tests** and **11 asset checks** pass. Removed three tests for the deleted duplicate-lighting helper; gameplay coverage remains. All **267 packaged asset files** match source; **271 resource/report files** regenerate byte-identically. Actual client checks cover loading/reload at mip level 4, stages/load variants, equipment/catalog, Survival watering (0→30 water; 8→7 pours), fuel consumption (8→7 cells; 24,000 ticks of fuel), local lamp on/off and save/reopen with appearance seed 3, genome, stage and can water component intact. Captures are unedited Minecraft output; no shader pack, multiplayer, audio mix or broad hardware benchmark is claimed. Full scene-render identity remains outstanding.


## 0.2.5-p1 — reference geometry, baked shading and complete art catalog — 2026-10-23

Rebuilds the rejected 0.2.4 presentation against CODEX_REFERENCE_NEW and the supplied grow-room reference. Art acceptance remains with the owner; automated checks do not certify a 1:1 match.

- Individually serrated, folded 2D leaflets replace near alpha fans. Rounded seedling cotyledons, a more open young plant, five mature whorls, a crown and restrained inner/branch collars distinguish the stages. Offset chamfered flower bracts replace aligned voxel towers. Saved four-layout / 5,9,13-flower identities and proportional variation remain.
- Rebuilt working equipment: full-height reinforced wood bed, broad boards, posts/feet, slotted bolts; beveled pot lip; open-chassis twin UV fixture with lens cores, windows, driver/fins/cable/chains; blue-gray can with rolled seams, open handle and nine-hole rose; printed/folded seed envelope, bound Ledger and caged cell. The bed's soil, collision and foliage-target bounds move together.
- Material-specific painted pixel ramps/marks, original seed-envelope illustration and shared UI materials. Atlas-safe polygon tiling prevents large panels sampling neighboring sprites. Thin chamfers clamp to their actual thickness instead of generating degenerate surfaces.
- Blender ray-bakes spatial ambient occlusion into native OBJ vertex colors. Lit reference previews bake ray-tested violet reflections. Native composite item passes keep tubes/indicators emissive instead of dimming them with ordinary item lighting. Working lamps retain fuel-dependent block light, local colored plant light, floor spill/halo and a depth-bounded shaft controlled by atmosphere/intensity settings. Floor projection continues past partial trays, preventing a hard square gap around pots.
- All four pot, all four UV and all four tent designs are inspectable via `/stonedew debug art`. The checked gallery uses labeled display entities; advanced tiers are art previews, without future automation gameplay. Tent art includes reflective lining, seams, flaps/straps, frame fittings, fan grilles, ribbed ducts, service cables and the final controller.
- Indexed resources, bounded detail (13,300/64 measured plant faces, 14,000/100 limits; working equipment maximum 1,337), fourteen-block distant transition, staged asset generation and source-hash bake caching. Normal builds use checked-in assets; art authoring requires Python 3 and Blender 4.x.

Validation: clean Java 21/NeoForge build and datagen pass; **60 JUnit tests** and **11 asset checks** pass. **236 resource/report files regenerate byte-identically**. Raised-bed Survival watering consumes one pour (8→7), changes only the selected plant (water 0→~29.97) and preserves all appearance identities. Final client captures and fuel/reload checks are recorded in the art/playtest notes. Full scene shadow maps/HDR bloom, shader-pack compatibility, the 500-plant target and broad hardware/multiplayer validation remain outstanding. Gameplay remains P1; automation still waits for the P3 Fun Gate.

## 0.2.4-p1 — broader foliage, authored materials and shaded lighting — 2026-10-22

The owner rejected 0.2.3 as unlike the reference shapes/textures and missing convincing shading. This revision replaces that presentation and fixes the renderer's equal-brightness flower faces and forced-up leaf normals. CODEX_REFERENCE_NEW remains the target; aesthetic approval is not implied by validation.

- Broad seven-finger serrated fans, five canopy whorls, crown collar, upright fill and branch-tip leaves. Connected, outward-leaning flower clusters emit only exposed bract faces, with cultivar-derived top highlights and five visible pistil caps. Four saved layouts, 5/9/13 mature flower sites and persistent proportion/rotation variation remain.
- Original authored 32px material tiles, 64px foliage/emblem/halo, shared UI sheet, dimension-based equipment UVs and a shaded pot-lip undercut. Rejected imagegen PNGs are archived unchanged outside the mod resources; the old atlas importer and foliage shader wrapper were removed. No reference crops or third-party game assets are used.
- Geometric directional shading, vertex canopy occlusion, real leaf underside normals, height-based world light and soil contact shadows. Fueled lamps add cached, obstruction-aware colored plant bounce and a soft local floor projection. Ambient daylight limits the tint so it preserves the leaf palette. Ray checks start below the fixture's collision hull to avoid blocking their own emitter. These are local effects, not global shadow maps.
- 64 shared plant meshes; maximum 2376 near / 64 distant faces within 2400/100 limits. Equipment maximum 534. Source/budget/integrity manifests regenerate deterministically. Updated guide and actual close-up, equipment, night and daylight on/off captures. No additional mod or shader pack is required.

Validation: Java 21 / NeoForge build passes; **60 JUnit tests**, no failures/errors/skips; **nine asset checks** pass, including exposed-pistil and underside-normal regressions. Regeneration leaves **187 files byte-identical**; datagen succeeds with zero changed outputs. Client loads existing P1 plants and all rebuilt assets, and resource reload retains mip level 4 (1024×512 block atlas). Same-camera fueled on/off captures verify UV effects and daylight attenuation. Survival watering consumes one pour (8→7), water ~34.6→64.3, preserving appearance seed 3, genome, stage and care. The JAR excludes rejected texture PNGs and deleted renderer/importer classes. Studio captures use an elevated camera and 45° FOV; equipment tools use enlarged display entities. Shader packs, broad hardware/multiplayer, the 500-plant target and owner art acceptance remain outstanding. Gameplay remains P1; P3 Fun Gate still precedes automation.

## 0.2.3-p1 — exact-reference rebuild and plant individuality — 2026-10-22

The four owner uploads in CODEX_REFERENCE_NEW replace the generic painted interpretation as the mod-wide visual brief. Preserve those images unchanged and apply their crisp leaf silhouettes, stepped flowers, terracotta, timber and cool steel/violet material language to current and future mod art.

- Rebuilt every current equipment model: sloped hollow terracotta pot with thick lip and recessed soil, separate timber bed rails with reinforced feet/corners and bolts, inset twin UV tubes with open chain links/driver/finned ballast, shaped can with open handle and rising spout, caged cell, seed packet emblem and bound field Ledger on a stand. Wet/lit states, item poses and gameplay IDs remain compatible.
- New original reference-guided pixel leaf fan and shared material atlas, copied unchanged from imagegen output with provenance/hashes. Dewstone and HUD/Ledger inherit the new materials. No reference-image crops or third-party game assets are bundled.
- Fuller tapered canopy with staggered skirts, upright fill and crown; solid stepped flower clusters replace the previous rounded puffs. Four branch layouts and three flower loads yield 5/9/13 mature sites, plus independently saved height/spread/rotation. Seedlings and flowering stages share that identity; distant models preserve load differences.
- Server-random appearance per planting from the same stack, independent of genetics. Saves/care/growth/genome edits preserve identity. Legacy version-1 plants migrate deterministically by lineage/position/slot. Compact client snapshots send bounded appearance parameters. Visible flower load does not invent harvest yield before P3.
- 64 shared near/distant plant meshes, maximum 1454/82 faces under tighter 1800/100 budgets. Equipment maximum 534 faces. Existing baked model/material/rendering APIs retained; no new mod dependency or custom shader.
- `/stonedew debug appearance <seed>` reproduces an identity and reports its mature flower count. Updated targeting accounts for varied proportions.

Validation: Java 21 / NeoForge build passes; **57 JUnit tests**, no failures/errors/skips; **eight asset checks** pass. Deterministic regeneration leaves **179 resource/art files byte-identical**; datagen succeeds with zero changed outputs. The real client loads existing P1 plants and rebuilt props without model/texture errors; F3+T retains world mip level 4. Fresh planting from one seed stack works; 5/9/13 load examples render. Survival foliage watering consumes one charge (8→7), water ~37→67. Save/quit/reopen preserves the exact appearance seed, stage, genome and care history. Actual game captures show plants, load/layout variation and equipment (tool display entities enlarged 1.6× for review). Offline auth/audio warnings in the cloud are unrelated to asset loading. Shader packs, broad hardware/multiplayer performance and owner aesthetic acceptance remain unvalidated. P3 Fun Gate remains before automation.

## 0.2.2-p1 — painted 2D/3D art direction — 2026-10-22

Owner clarified the whole mod's target: a painted fantasy style, using Hytale / World of Warcraft as shorthand. The weed bush should have a dense tapered Christmas-tree silhouette, painted 2D leaves and solid 3D flowers. This replaces the earlier all-modeled leaf treatment.

- Original imagegen foliage fan and shared 4×4 material painting, preserved unchanged with source hashes/provenance and prompt briefs. These are shipped texture inputs, not concept images used as screenshots.
- Fixed, slightly hinged alpha foliage cards in eight staggered canopy skirts, inner fill, smaller nested 3D flower clusters, all growth stages/habits and distant detail. Most of the trunk is hidden. Geometry max 2260 faces near / 86 distant, under the existing 3000 / 100 limits.
- Native SpriteSource import creates 256px material sprites and 512px foliage, preserving ordinary world mip levels. Vanilla entity shader layer enables foliage mip filtering; it fixes the noisy direct-texture prototype without a custom GLSL shader or dependency.
- Painted material bindings cover every existing Stonedew prop, tool, packet, lamp/cell and Dewstone. Ledger and HUD share painted wood/copper/parchment and the leaf emblem. Plant HUD moved to the upper right to leave chat and the bush visible. Vanilla world blocks remain vanilla.
- Existing plant saves, genome identity and P1 gameplay retained; foliage targeting widened for the new canopy. New mod-wide guide applies to future art as well.

Validation: Java 21 / NeoForge build passes; 53 JUnit tests, no failures/errors/skips; six asset checks pass. Regeneration is byte-identical across 126 resource/report files; datagen writes zero changes. Client loads existing P1 world and imported paintings with the block atlas retaining mip level 4. Real Survival watering of the new canopy consumes one pour (8→7); painted Ledger opens. Resource reload retains the paintings and mip level 4; side/back views retain alpha foliage. Actual game captures document plants, props, HUD and Ledger. Performance target, shader packs, broader hardware/multiplayer and final visual acceptance remain unvalidated.

## 0.2.1-p1 — organic plant art correction — 2026-10-22

The owner rejected the rigid, sparse all-voxel plants. This revision replaces their geometry rather than recoloring the old columns.

- Original curved serrated leaf fans, fuller tapered foliage, green bracts and irregular rounded bud clusters with smaller overlapping tufts, sugar leaves and short pistils. Equipment retains its Minecraft cuboid construction.
- 24 OBJ plant meshes across stages/habits/detail levels, shared MTL, four original organic material textures, built-in NeoForge OBJ loader. Renderer preserves baked colors and vertex normals. No extra mod dependency/custom shader.
- Foliage selection bounds expanded to fit the new canopy. Existing genome identities, plant saves and growth mechanics retained.
- Revised geometry ceiling 3000 faces near / 100 distant; measured maxima 2970 / 98. These replace the previous cuboid limits, not a performance certification.
- Updated owner art direction, source/asset notes, current screenshot and versioned downloadable JAR. Rejected 0.2.0 capture/artifact retained for comparison/history.

Validation: Java 21/NeoForge build passes; 53 JUnit tests with no failures/errors/skips; five asset checks pass. Regeneration is byte-identical across 123 resource/report files; datagen writes zero changed outputs. Development client loads existing P1 plants with new models, resource reload succeeds, and upper-canopy Survival watering consumes one pour (8→7). Pigment/habit changes render correctly. Real screenshots document the visual review. Broader performance/shader/multiplayer testing and final owner art approval remain outstanding.

## 0.2.0-p1 — 2026-10-22

Playable Plant Core: seed → watering/fueled light → four visible stages → ripe plants. Harvest and processing remain P3.

### Added

- Shared one-/four-slot tray block entity for Clay Pot and Planter Bed, bounded lazy timestamp growth, stage comfort/Vigor, no-death slowdown, capped catch-up, sleep-aware monotonic growth clock and versioned persistent plant/care/owner data.
- Immutable genome Codec/StreamCodec seed components with eight stub genes; pigment/habit presentation. Full inheritance/stat expression remains P5.
- Survival planting and watering, eight-pour can, source-water/cauldron refills, server permission checks, obstruction/reach-aware per-slot foliage targeting and no cauldron consumption when already full.
- Glow Cells fuel Bulb Lamps with real light and fuel exhaustion/relighting. Basic nearby lamp/sun Lume contributes to growth; full rooms/environment remain P2.
- Compact changed-slot presentation sync separate from disk state, accumulated same-tick deltas, initial chunk snapshots, plant HUD and real server-opened Ledger menu. Persisted per-player introductory flags and compact directive payload; localized prose authored outside Java.
- Original dimensional voxel equipment, 24 stage/habit/LOD plant meshes, tint channels, gentle sway, first-person can pouring, 16 material textures and shader-free emissive halo. Corrected tiny-face UV density and sampled foliage light after actual close-up review. No third-party art bundled.
- Survival recipes/loot/tags and operator kit/growth/stage/genome/timewarp tools. Optional clear-space-checked grow-room exhibit. Deferred-system debug entries report their phase instead of faking success.
- P1 playtest, asset manifest, research/production notes, mesh budget and actual in-game screenshots. P0 download retained as history; install only one Stonedew JAR.

### Validation

- Java 21 / NeoForge 21.1.264 build passes: **53 JUnit tests, zero failures/errors/skips**. Four Python asset checks pass.
- Asset/datagen repeat is byte-identical across 94 resource/report files. Near plant meshes max 925 quads; LOD max 40. These geometry budgets do not prove the future performance target.
- Development client launched and loaded an existing P0 singleplayer world with seven P1 definitions. Real item interactions planted a seed, watered in Survival (water increase, can 8→7), refilled from a cauldron (7→8, level 3→2), exhausted/refueled a lamp and opened the Ledger directive screen.
- Accelerated a real planted tray to ripe, saved/quit and reopened: genome, stage and care history persisted. Watering upper foliage changed the selected bed slot while other slots retained their water.
- Solid block obstruction prevented a foliage pour (can remained at 8); a full can left the water cauldron at level 3.
- Actual game captures record the models/HUD/Ledger. Art remains a first gameplay pass for owner review.

### Limits / next phase

Baseline humidity/temperature/air/nutrients/schedule and simple light sampling are P1 foundations. Next is **P2 Rooms and environment**; P3 then completes manual harvesting/processing before the explicit Fun Gate. No scope removed. Multiplayer, shader packs, audible mix and 500-plant performance remain untested. Cloud audio was disabled; offline authentication warnings are not gameplay failures.

## Download follow-up — 2026-10-22

- Added the verified P0 JAR and SHA-256 to `downloads/`, with a direct GitHub download link. Mod code and gameplay are unchanged.

## Documentation follow-up — 2026-10-22

- Added client installation and development-launch steps, and recorded the owner's stylized, animated 3D voxel art direction in the living design and asset guidance. Gameplay and the P0 JAR are unchanged.

## 0.1.0-p0 — 2026-10-22

First implementation phase: a loadable NeoForge foundation. This is not the playable cultivation loop.

### Added

- Minecraft 1.21.1 / NeoForge 21.1.264 / Java 21 project, Gradle 9.2.1 wrapper with distribution checksum, ModDevGradle 2.0.148, official Mojang mappings, and GitHub Actions build/datagen/test workflow.
- Stonedew creative tab, decorative glowing Dewstone and Glow Cell item, with provisional recipe and advancement.
- Deterministic 16x16 texture generator and NeoForge datagen for models, blockstate, loot, recipe, advancements, language and mining tag.
- Server and client config scaffolding: Grower / Uneasy defaults, cannabis theme with optional Herbal Mode, and future-feature accessibility controls.
- Organism-neutral Cultivar interface and immutable profile; Wing manifests; six base JSON definitions; validated, transactional datapack reloads. Generic later-phase payloads remain explicit foundations.
- Authoritative gameplay-event bridge, immutable versioned world story state, prototype-to-current migration, and guards against corrupt/future saves being replaced by empty data.
- Operator commands `/stonedew debug status`, `story`, and `probe`.
- Living design, decisions, asset manifest, architecture/datapack/cloud docs, screenshot and eight-item P0 playtest checklist. Original uploaded brief/images preserved.

### Validation

- `./gradlew --no-daemon --console=plain runData build`: passed. **24 unit tests; 0 failures, 0 errors, 0 skipped.**
- Datagen repeat: all ten generated files unchanged (zero written). Texture regeneration byte-identical.
- Cached `./gradlew --offline --no-daemon --console=plain build`: passed.
- Packaged JAR checked for mod metadata, entrypoint, generated resources and textures; datagen cache excluded.
- `runClient` launched under Xvfb/Mesa software rendering. Created and reopened a Creative singleplayer world with the mod loaded. Stonedew creative tab and both textured objects visible (docs/screenshots/p0-creative-tab.png).
- `/stonedew debug status`: six definitions, Grower/Uneasy. `/give` resolved both registered items. Generated advancement awarded.
- Real event probe saved to `stonedew_story.dat` with dataVersion 1 and count 1; that count remained after reopening the world.
- `/reload` succeeded. A disposable test datapack loaded a seventh definition; malformed JSON then correctly rejected reload and retained the previous seven-definition index. Removing the test pack restored six definitions. Test pack removed from the ignored development world.
- Cloud installation script rerun successfully with the project build; authenticated Debian package indexes used for local Xvfb. Updated installation/startup instructions saved to the environment configuration draft.

### Limitations and next phase

- Runtime dependency networking is working. The offline development client's online profile/public-key requests log warnings; online multiplayer authentication is not validated. Audio was disabled for cloud smoke validation.
- No plant gameplay, genome components, Ledger UI, processing, worldgen, automation or final visual/audio assets yet. Future-feature controls are declarations until their gameplay systems arrive.
- Human playtest, sound, two-client synchronization, shader compatibility and the 500-plant performance target remain unrun. They are not claimed to pass.
- Next: **P1 Plant Core**, including unified trays, stages, watering, Bulb Lamp, seed genome, tooltips and the Ledger/Directive stub. See docs/P0_PLAYTEST.md. Full scope remains planned; no cuts.
