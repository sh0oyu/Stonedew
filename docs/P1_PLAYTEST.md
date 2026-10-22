# P1 Plant Core playtest

Use Minecraft Java 1.21.1 / NeoForge 21.1.264 with **only the P1 Stonedew JAR**. Back up worlds. Start in a disposable world with commands enabled; obtain items from the creative tab or `/stonedew debug givekit 0`.

1. **Plant:** place a pot and bed. Plant one seed in the pot and four in the bed's separate soil positions. Check that packets decrease in Survival and every slot has a seedling.
2. **Water:** use the full can on foliage and soil. Check that the selected plant gains water and one pour is consumed in Survival. Full plants should refuse wasted water. Refill at source water and a water cauldron; the latter uses one cauldron level in Survival.
3. **Light:** fuel a nearby Bulb Lamp with a Glow Cell in Survival. Verify consumption, visible light, and changed plant Lume within ten seconds. `timewarp 10` should exhaust it; another cell should relight it.
4. **Grow:** inspect the foliage HUD. Try `/stonedew debug grow 240000`, or tend plants normally. Compare four stages. Poor care slows growth without death; ripe plants persist.
5. **Identity:** compare four seed colors. Try `genome show` and `genome set habit tall tall` on a targeted plant. Observe color/silhouette changes. This is persistent identity, not the later breeding system.
6. **Save:** save/quit and reopen. Confirm stages, water, genomes, lamp fuel and directive. Break a planted tray in Survival: seed identity drops, while growth progress resets.
7. **Ledger:** in a fresh world, plant, water and fuel a lamp. Follow the top-left directive and open the Ledger. It should progress to tending, then ripe inspection. Esc closes it.
8. **Art/feel:** run `/stonedew debug demo` in clear loaded space. Inspect models from several angles and beyond 24 blocks. Check sway, pouring motion, clipping, HUD readability and your shader setup. Report screenshots and what feels wrong.

## Still provisional / unimplemented

- First original gameplay voxel-art pass; final detailing, richer animation, custom sound design and broader play-feel/accessibility review remain. Vanilla sounds supply feedback. Dewstone is decorative.
- Baseline humidity, temperature, airflow, nutrients and schedule; simple nearby-lamp/sun light. Enclosed rooms, schedules, environmental equipment, problems and historical environment sampling arrive in **P2**. Catch-up caps at two Minecraft days per visit.
- Genome alleles persist and drive pigment/habit. Inheritance, named strains and stat expression arrive in **P5**. Seed crafting is a temporary acquisition path ahead of worldgen/progression.
- Harvest/trim/dry/cure, quality, Orders and first Cycle arrive in **P3**. Consumption, Herbal Mode presentation switching, later story, machines and automation are not implemented. Future-system settings remain foundations.
- Multiplayer, shader compatibility, audible mix and the 500-plant target require dedicated validation. Mesh budgets and software-rendered checks do not establish these results.

## Next phase

**P2 — Rooms and environment:** bounded detection/cache invalidation, measured environment, stage comfort feedback, schedules/equipment, persistence, multiplayer checks and measured simulation cost. P3 then completes the manual processing loop. Stop after P3 for the owner's Fun Gate before automation.
