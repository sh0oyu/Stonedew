# P1 Plant Core playtest

Use Minecraft Java 1.21.1 / NeoForge 21.1.264 with **only the P1 Stonedew JAR**. Back up worlds. Start in a disposable world with commands enabled; obtain items from the creative tab or `/stonedew debug givekit 0`.

1. **Plant:** place a pot and bed. Plant one seed in the pot and four in the bed's separate soil positions. Check that packets decrease in Survival and every slot has a seedling.
2. **Water:** use the full can on foliage and soil. Check that the selected plant gains water and one pour is consumed in Survival. Full plants should refuse wasted water. Refill at source water and a water cauldron; the latter uses one cauldron level in Survival.
3. **Light:** fuel a nearby Bulb Lamp with a Glow Cell in Survival. Verify consumption, visible light, and changed plant Lume within ten seconds. `timewarp 10` should exhaust it; another cell should relight it.
4. **Grow:** inspect the foliage HUD. Try `/stonedew debug grow 240000`, or tend plants normally. Compare four stages. Poor care slows growth without death; ripe plants persist.
5. **Identity:** compare four seed colors. Try `genome show` and `genome set habit tall tall` on a targeted plant. Observe color/silhouette changes. This is persistent identity, not the later breeding system.
6. **Save:** save/quit and reopen. Confirm stages, water, genomes, lamp fuel and directive. Break a planted tray in Survival: seed identity drops, while growth progress resets.
7. **Ledger:** in a fresh world, plant, water and fuel a lamp. Follow the top-left directive and open the Ledger. It should progress to tending, then ripe inspection. Esc closes it.
8. **Art/feel:** run `/stonedew debug demo` in clear loaded space. Inspect models from several angles and beyond 14 blocks. Compare directly with CODEX_REFERENCE_NEW. Plant several seeds from one stack; compare branch layouts, proportions and bud loads, then save/reload. Use `/stonedew debug appearance 42` to repeat an identity. Check individually tilted seven-finger fans on uneven branches, small sugar leaves/curved pistils/resin and solid flower bracts, rebuilt tapered pots/bolted beds/UV fixtures and shared pixel materials, parchment HUD/Ledger, sway, pouring motion, clipping and your shader setup. Report screenshots and what feels wrong.

## Still provisional / unimplemented

- Current hybrid art/shading pass still requires owner visual review; richer animation, custom sound design and broader play-feel/accessibility review remain. Vanilla sounds supply feedback. Dewstone is decorative.
- Baseline humidity, temperature, airflow, nutrients and schedule; simple nearby-lamp/sun light. Enclosed rooms, schedules, environmental equipment, problems and historical environment sampling arrive in **P2**. Catch-up caps at two Minecraft days per visit.
- Genome alleles persist and drive pigment/habit. Inheritance, named strains and stat expression arrive in **P5**. Seed crafting is a temporary acquisition path ahead of worldgen/progression.
- Harvest/trim/dry/cure, quality, Orders and first Cycle arrive in **P3**. Consumption, Herbal Mode presentation switching, later story, machines and automation are not implemented. Future-system settings remain foundations.
- Multiplayer, shader compatibility, audible mix and the 500-plant target require dedicated validation. Mesh budgets and software-rendered checks do not establish these results.

## Next phase

**P2 — Rooms and environment:** bounded detection/cache invalidation, measured environment, stage comfort feedback, schedules/equipment, persistence, multiplayer checks and measured simulation cost. P3 then completes the manual processing loop. Stop after P3 for the owner's Fun Gate before automation.

## 0.2.3 reference revision validation

57 Java tests and eight asset checks pass. All 64 plant meshes and ten equipment states package correctly; no obsolete habit meshes remain in the JAR. Regeneration is byte-identical across 179 files. Real client review covered legacy plants, fresh sowing from one packet stack, the three mature visual flower loads, fuller canopy targeting, new equipment, F3+T reload with mip level 4, and save/quit/reopen with identity/genome/stage/care unchanged. Survival watering used one pour (8→7), water about 37→67. Screenshots p1-reference-*.png are actual Minecraft captures; equipment tool displays are enlarged 1.6× for review. Prior validation below documents earlier passes.

## 0.2.4 shading revision validation

60 Java tests and nine asset checks pass. Added directional-normal/rotation/occlusion tests and checks for shaded undersides and exposed pistil caps. Asset regeneration is byte-identical across 187 files. The client loads existing P1 plants and new artwork; F3+T retains mip level 4. Same-camera fueled lamp on/off captures demonstrate local UV spill and daylight attenuation. Corrected a ray origin that otherwise hits the fixture's own collision hull. Survival watering of the new canopy used one pour (8→7), water 34.6→64.3, without changing its saved seed/genome/stage/care. Current p1-shaded-*.png are actual Minecraft captures; studio views use an elevated camera and 45° FOV. Earlier screenshots document rejected/intermediate art. These checks do not establish aesthetic acceptance or the full hardware/shader/multiplayer performance target.


## 0.2.5 reference rebuild checks

- Compare actual `p1-rebuilt-*.png` captures with unchanged CODEX_REFERENCE_NEW. Inspect near leaf serrations/midribs/undersides, puffy flower seams/pistils, the taller bolted wood bed and blue-gray can from front/side/back.
- Use `/stonedew debug art` in clear loaded space in a disposable world. Inspect all four pot, UV and tent tiers; all future-tier models must be clearly labeled art previews. Check reflective panels, fabric straps, hardware, ducts and controls without neighboring atlas textures appearing.
- Verify the exhibit refuses an occupied volume and does not replace it. Preview entities carry `stonedew_art_preview`; the floor/backdrop are ordinary blocks.
- Compare the same plant camera with the actual lamp fueled/empty. Tube cores, halo/shaft and colored plant/floor effects follow `lit`; atmosphere off hides decorative effects. Check the shaft stops at receiving geometry.
- Water plants in both pot and raised bed, preserve the appearance identity through save/reopen, and inspect the fourteen-block detail transition. Higher geometry detail has not been benchmarked at 500 plants.
- Aesthetic acceptance and full-scene shader effects remain separate from automated asset integrity/gameplay validation.

0.2.5 verification: clean build/datagen, 60 JUnit tests and 11 asset checks pass. All 236 resource/report files reproduce byte-identically; the JAR's 231 asset files match current sources. Real-client captures cover both flower palettes, all stages, 5/9/13 saved loads, working props, the complete catalog and lit/empty UV. The gallery refuses its occupied volume; new labels/poses load without display decode errors. Raised-bed Survival watering consumes one pour and changes only the selected plant while preserving all appearance seeds. Resource reload retains the block atlas at mip level four. Cloud offline-auth/audio warnings remain unrelated to asset loading.


## 0.2.6 art revision checks

The owner rejected 0.2.5. Compare current `p1-revision-*.png` actual game captures against CODEX_REFERENCE_NEW; the new art is not automatically approved. Check broad stepped fan silhouettes, filled upper canopy, three leafy stages followed by irregular voxel flowers, darker leaf intersections, soil silhouettes, painted ceramic/wood/metal, visible can spout/rose and gathered tent cloth. Keep future catalog models labeled art previews.

The clean build and datagen pass, with 57 JUnit tests and 11 asset checks. Removed tests exercised only the deleted duplicate CPU lighting helper. Current resources reproduce byte-identically across 271 files and all 267 packaged asset files match source. The native painting swatches retain mip level 4 without overriding vanilla sprites. Real Survival watering changes the tested plant from 0→30 water and the can from 8→7, preserving appearance seed, genome and stage. Actual fueling consumes one cell (8→7) and supplies 24,000 ticks. Same-camera on/off captures show the conditional local effects. Save/reopen preserved appearance seed 3, stage 3, the green genome and the can’s seven-pour component; remaining water followed normal simulation. Studio captures use a 30° FOV, and equipment tool displays use 1.6× inspection scale. The reference gallery contains art previews, not new machine gameplay.

## 0.2.7 natural-branch checks

The owner rejected 0.2.6's leaf shapes and Christmas-tree silhouette. Compare current `p1-botanical-*` captures with the unchanged banner. Look for recognizable seven-finger cannabis fans, visible petioles and branch gaps, uneven branch tips, varied leaf pitch/roll, and no radial shelves. Bud close-ups should retain their established volume while adding small sugar leaves, paired curved pistils and sparse resin points. Low/medium/high loads remain 5/9/13; extra flowers are smaller and sit at branch joints. Check all four saved layouts, all stages and beyond fourteen blocks.

This revision passes the build, datagen, 57 JUnit tests and 11 asset checks. The 272 resource/report files reproduce byte-identically, and all 268 packaged assets match source. Actual client review covers both palettes, front/back/detail, stages/load variations, mip-level-four reload and fueled lamp on/off. Survival watering uses one pour (8→7) and changes water about 7.48→37.28, preserving appearance seed 3, genome and stage. Save/reopen also retained the green genome, stage 3, appearance seed 3 and seven-pour can component; water followed normal simulation. These checks verify implementation, not owner visual approval. Equipment remains unchanged and P1 remains the gameplay scope.

## 0.2.8 canopy comparison

The owner rejected the sparse 0.2.7 branching diagram. Compare `p1-canopy-*` with the warm banner: foliage overlaps through the center and around the main flower, branches are shorter, each compound leaf has separately curved/folded fingers, and paint is quieter green. Inspect raised bract crowns, shared painted sugar leaves, curved pistils and resin detail. Check all stages, saved layouts/loads and the distant transition. The cave scene is a local art comparison; its tent remains a display preview, not automation gameplay.

The build, datagen, 58 JUnit tests and 11 asset checks pass. All 272 resource/report files reproduce byte-identically. Native leaf/material windows retain mip level 4. All 268 packaged assets match source. Actual Survival watering changes water about 7.80→37.70 and uses one pour (8→7), preserving seed 3, genome and stage. A renderer regression exercises real shipped pistil/resin faces. No gameplay/save schema changes were made; visual acceptance and broader performance/shader checks remain separate.
