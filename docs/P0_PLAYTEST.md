# P0 playtest checklist

Use Minecraft Java 1.21.1 and NeoForge 21.1.264, or `./gradlew runClient`. This is a foundation build; growing is not implemented yet.

1. Start the client. Check Mods → Stonedew shows `0.1.0-p0` and opens the config screen.
2. Create a disposable Creative world with commands enabled. Find the **Stonedew** creative tab (page 2 if needed): Dewstone and Glow Cell should have textures and readable names.
3. Place and break Dewstone. Check its subdued glow, amethyst feedback and self-drop.
4. Combine one amethyst shard and one copper ingot to craft a Glow Cell. This developer recipe is provisional.
5. Run `/stonedew debug status`. Expect six base definitions, `GROWER` and `UNEASY` defaults.
6. Run `/stonedew debug probe`, then `/stonedew debug story`. The probe count should increase once. Save/quit and reopen the world: the count must remain.
7. Run `/reload`, then `/stonedew debug status`. The six definitions should reload without losing progress.
8. Inspect the config screen: Herbal Mode defaults off, sudden sounds default off, and difficulty, dread and presentation controls are present. Presentation controls for later features do not change anything yet.

## Still placeholder

Dewstone/Glow Cell textures and models; the developer recipe and advancement; Wing profile payloads; settings for later gameplay. No final audio, growing, genome item components, lamps, trays, HUD, Ledger, Hatch, processing or automation exists in P0. Full scope is retained in DESIGN.md.

## Proposed next phase: P1

Implement the shared GrowTray block entity (pot and planter), four visual growth stages, lazy PlantState simulation, seed genome components, watering can, Bulb Lamp/Glow Cell fuel, plant status tooltip, and the Ledger stub with the first Directive. Introduce the required P1 debug commands with real effects only where their corresponding systems exist; clearly identify deferred operations. Preserve the architecture and P3 Fun Gate.

Playtest report: **What felt great; what felt tedious; what confused me; what broke; one thing I wanted that wasn't there.**
