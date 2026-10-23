<!-- Living design: implementation status below; original uploaded brief is preserved separately. -->

## Approved scope and current implementation status — 2026-10-23

- User approved the kickoff plan: NeoForge / Minecraft Java 1.21.1; Uneasy default; full story and endings, Remember overlay and Hollow Runs included; Stonedew name; cannabis theme with optional Herbal Mode.
- Current art direction: **CODEX_REFERENCE_NEW** and the Stonedew banner remain authoritative. The owner rejected 0.2.6’s unrecognizable leaf shapes and stacked tree structure. The 0.2.7 revision uses an unchanged original seven-finger cannabis painting on independently posed leaves, four uneven connected branches and a slender bent stem. Existing bud volumes gain sugar leaves, curved pistils and resin points. The latest natural-branch direction overrides earlier cone guidance. Saved identities, shading and local UV effects remain. Future-tier gallery models remain art previews.
- Work proceeds phase by phase. Automation remains gated on the user's explicit P3 Fun Gate approval. Full scope is retained, including the M3 Annex and later Wings; nothing has been cut.
- Current implementation: **P1 Plant Core** — planting, watering, fueled lamps, four-stage growth, persistent genome identity, HUD and Ledger. Harvest/processing and full room simulation remain future phases. See CHANGELOG.md and ASSETS.md for exact implementation and validation status.
- Part II overrides conflicting Part I systems; section 50 reconciles the three parts. The original Part I/II/III text follows unchanged.

---

# STONEDEW: Master Design Bible and Build Brief

*A cozy underground grow-cave mod for Minecraft Java. “Stonedew” is a working title. This is the single source of truth, written to be handed to an AI developer (Claude Code). Every number is a starting value to be tuned. Everything is fictional, gamified and simplified: it is a game, not a cultivation guide.*

**Contents:** 0 Working Agreement · 1 Technical Foundation · 2 Vision and Pillars · 3 Aesthetic Bible · 4 Gameplay Loops · 5 Plant Simulation · 6 Harvest, Trim, Dry, Cure · 7 Genetics and Strains · 8 Consumables and Tolerance · 9 Progression and Economy · 10 Automation Ladder · 11 Machine Catalog · 12 World, Lore, NPCs · 13 UI/UX · 14 Camera, Animation, Audio · 15 Replayability · 16 Asset Manifest · 17 Balance Sheet · 18 Testing · 19 Roadmap · 20 Risks and Cut-Lines · 21 Kickoff

---

## 0. Working agreement (read first)

You are my lead developer and game designer. This document is the design bible.

1. **Plan before code.** Your first reply contains only: (a) a technical plan, (b) a phased roadmap (confirm or adjust section 19), (c) risks and open questions (max 3), (d) a confirmation of every “day-one architecture decision” in section 1.4. Then wait for my go-ahead.
2. **Build in phases.** At the end of each phase: it compiles cleanly, `runClient` launches, automated tests pass, and you give me (i) a Playtest Checklist of 5-10 concrete things to try, (ii) a list of what is still placeholder, (iii) your proposal for the next phase.
3. **Fun Gate.** After phase P3, stop. I will play the fully manual loop. Do not start automation until I say it is fun. If it is not, fixing the manual loop is the next phase.
4. **Never silently cut.** If a feature is infeasible, too expensive, or conflicts with another, say so, propose the closest alternative, and log it in `DESIGN_DECISIONS.md`.
5. **Living docs.** Maintain `DESIGN.md` (this document, kept current), `CHANGELOG.md`, `DESIGN_DECISIONS.md`, and `ASSETS.md` (every asset: id, placeholder or final, how to replace it).
6. **No magic numbers.** Anything marked `[TUNE]` lives in config or datapack JSON, never hardcoded.
7. **Testing.** Unit tests for genetics, quality formulas, room detection and save migration, plus the debug commands in section 1.9.
8. **Ask sparingly.** Max 3 questions at once. Otherwise pick a sensible default and state the assumption.

---

## 1. Technical foundation

**1.1 Stack.** Minecraft Java `[MC_VERSION, default 1.21.1]`, `[LOADER, default NeoForge]`, Java 21, Gradle, Mojang mappings. Mod id `stonedew`. Datagen for models, blockstates, loot tables, recipes, lang, tags and advancements. Soft integrations: Jade/WTHIT (tooltips), JEI/REI/EMI (recipes). Must coexist with Iris/Oculus shader packs; no custom shaders required.

**1.2 Package layout.** `core` (registries, config, networking) · `plant` (tray block entity, plant state, stages) · `env` (rooms, sensors, light model) · `genetics` (genome, breeding, strains, names) · `process` (harvest, trim, dry, cure, quality) · `consume` (items, effects, tolerance) · `automation` (power, fluid, pipes, rails, routines) · `world` (structures, worldgen, NPCs, contracts, lore) · `client` (renderers, GUIs, camera, particles, sounds) · `data` (datagen, JSON schemas) · `compat` · `debug`.

**1.3 Data-driven content.** Datapack-loaded JSON for: terpenes, pigments, nutrients, effect maps, random events, contract templates, grow-recipe presets, heirloom strains, lore pages, and routine triggers and actions. Modpack makers can add content without code.

**1.4 Day-one architecture decisions (confirm each in your first reply; retrofitting later is painful).**

1. **Trays everywhere.** Every planter is a `GrowTrayBlockEntity` holding N plant slots (1 = pot, 4 = planter bed, 9 = large tray). A single pot is just a 1-slot tray, so the rail logistics in tier T4 never needs a rewrite.
2. **Lazy simulation.** Plants store `lastSimTime` and a compact `PlantState`. They advance via scheduled or random ticks and via catch-up math when a chunk loads or a player interacts. Never loop over all plants every tick.
3. **Room-level logic.** Environment is computed per Grow Room, not per plant. Room volumes are flood-filled once, cached, and invalidated by throttled block-change events.
4. **Genome as a value object.** An immutable record with Codec/StreamCodec, stored as a data component on seeds, pollen, plants, buds and jars.
5. **Server authority.** The server owns growth, genetics, quality and effects. The client only renders and plays feedback. Sync compact deltas only on change.
6. **Capabilities.** Machines expose standard item, fluid and energy capabilities so hoppers and other mods' pipes work.
7. **Explainability.** Every machine and plant implements `getStatusReason()` returning a lang key (“Idle: no power”, “Waiting for Growth Mix”). Tooltips surface it everywhere.
8. **Save versioning.** Every block entity and saved-data class stores `dataVersion` with migrations, because the plant model will evolve.

**1.5 Performance budget.** Target: 500 plants across 20 rooms under 1 ms average server cost per tick on mid-range hardware. Pipes and rails are graph networks rebuilt only on neighbor change. Client: plant models baked once per (stage, habit, tint set), instanced per tray, simplified beyond 24 blocks; particles are distance-culled and capped by a config budget.

**1.6 Multiplayer.** Journal, tolerance, know-how and rank are per player. Facilities have an owner and a trusted list stored on the Controller. Player-to-player Trade Depot listings are a stretch goal.

**1.7 Config and difficulty presets.** Every visual effect, camera moment, minigame, event category and screen tint has a toggle. Presets:

| Setting | Chill | Grower (default) | Connoisseur |
| --- | --- | --- | --- |
| Growth time multiplier | 0.7x | 1.0x | 1.3x |
| Problem frequency | 0.4x | 1.0x | 1.6x |
| Plant death | Impossible | Impossible | After 3 in-game days at critical |
| Automation quality cap (before Apprenticeship) | Prime | Fine | Common |
| Tolerance build-up | 0.5x | 1.0x | 1.5x |
| Contract deadline slack | +50% | normal | -20% |
| Offline catch-up cap | 3 days | 2 days | 1 day |

**1.8 Placeholder-first assets.** Generate 16x16 textures and JSON models by script with palette-aware helpers. Map every custom sound to a vanilla SoundEvent until final audio exists, so nothing is ever silent. Structure `assets/` so art can be swapped without touching code, and track every asset in `ASSETS.md`. An optional **Herbal Mode** config (section 8) swaps names and textures to a general herb and apothecary theme.

**1.9 Debug commands** (`/stonedew debug ...`, op only, required from P1): `grow <ticks>`, `setstage`, `genome show|set|random`, `room info`, `env set`, `event trigger`, `givekit <tier>`, `knowhow set`, `rank set`, `timewarp <days>`, `contract spawn`, `unlockall`.

---

## 2. Vision and design pillars

**Tagline.** Stardew Valley's coziness, Factorio's bottleneck-chasing, and an apothecary's moody violet glow, all inside a hidden underground cave.

**Player fantasy.** You inherit a forgotten valley and a lost craft. You start with a windowsill pot and a watering can, and end with a glowing automated facility that you designed, filled with strains you bred, restoring something that matters.

**Pillars.**

1. **Tactile joy.** Every verb (pour, snip, burp, pluck, place) has sound, particles and animation. Nothing is a silent state change.
2. **Always a next thing.** At any moment the player can see at least three achievable goals, one of them under five minutes away.
3. **Gentle failure.** Problems warn, give a grace period, and are recoverable. A crop is never wiped while the player is away.
4. **Decisions over chores.** Automation removes repetition, never choices. Machines turn the player from operator into designer.
5. **Hand-made is premium.** Machines give volume; only hands reach Legendary quality.
6. **Beauty by default.** A sloppy build still looks atmospheric thanks to glow, mist and soundscape.

**Anti-goals.** No real-world cultivation instructions. No crude or edgy humor. No punitive real-time timers. No mandatory minigames (every one is skippable with a trade-off). No busywork without a payoff.

**The Dopamine Ladder** (design every feature against this):

| Timescale | Feeling | Delivered by |
| --- | --- | --- |
| Seconds | Crunchy satisfaction | Particles, sound and animation on every verb, floating “+” numbers |
| Minutes | Visible growth | Stage-change sparkle, filling tooltip bars, a new strain color appearing, jar glow |
| One batch (30-60 min) | Payoff | Harvest reveal, trim score, jar reveal, contract fanfare |
| One session | Progress | Rank bar tick, Know-how milestone, new recipe, new strain logged in the Journal |
| Weeks | Mastery | New tier, new room, Legendary strain, Heirloom found, Legacy |

**Always-on motivation systems.**

- **Next Goal widget:** shows up to three goals generated from player state (one under 5 min, one under 20 min, one long-term).
- **Reveal moments:** information is hidden until a payoff (seed genes unknown until grown or sequenced, jar quality revealed on opening, mutation sparkle).
- **Near-miss feedback:** if quality lands just under a tier, the result screen names the exact factor that cost the points (“Humidity ran 8% high during flowering”). The player always knows what to improve.
- **Bottleneck Spotlight:** once automation exists, the dashboard highlights the current weakest link in the facility.

---

## 3. Aesthetic bible

**3.1 Reference image breakdown (replicate these).** Hanging violet tube lamps on iron chains with a bloom halo; a glass-pane greenhouse wall with glowing vines and a cyan mushroom terrarium; dark wooden raised planter beds with rich soil; a wooden pole with hanging dried bundles; shelves of colored glass jars holding visibly colored buds; potion flasks with glowing liquid; a bee drifting near flowering plants; low purple mist and sparkle particles; a black watering can in first person with droplet particles; an in-world tooltip at the top center (strain name in rarity color, grow stage, humidity).

**3.2 Palette.**

| Role | Hex values |
| --- | --- |
| Cave stone | `#1B1226`, `#2C2038`, `#3E3050` |
| Wood and copper | `#4A2E24`, `#6B4332`, copper trim `#B8693A` |
| UV violet | core `#B04CFF`, glow `#D78BFF`, shade `#7A2BD6` |
| Bloom pink | `#FF6FD8`, `#FF9BE8` |
| Leaf greens | `#2F7D3B`, `#4FBF5A`, highlight `#A6F27A` |
| Mushroom cyan | `#4FE8E0` |
| Honey amber | `#FFC247` |
| UI | panel `#1E1528`, border `#5A3A7A`, accent `#B04CFF`, text `#F2E8FF`, ok `#6BE585`, warn `#FFB347`, danger `#FF5A6E` |

**3.3 Texture rules.** 16x16, vanilla-compatible, three-tone ramps, light dithering, outlines in a darker hue (never pure black), saturated accents against dark stone. Emissive layers on lamps, flowers, mushrooms, status lights and fluorescent strains.

**3.4 Atmosphere without shaders.** Lamp halo (additive billboard particle), optional faint light-cone beam model under lamps, low-lying purple mist particles that hug the floor near lamps and plants, drifting dust motes and sparkle, a very soft violet screen vignette inside grow rooms (toggle). All of it must look good with no shader pack and better with one.

**3.5 Plant visuals.** Models for 4 stages across 3 habits (tall and narrow, bushy, hybrid). Three tint channels from genes: leaf tint, bud tint, pistil-hair tint, plus a “frost” sparkle overlay and an emissive layer for fluorescent strains. State visuals are readable at a glance: droop (tilted leaves), curl (heat), pale (deficiency), yellow tips (burn), bleached tops (light burn), grey fuzz plus spore particles (mold), red specks (mites).

**3.6 Block language.** Dark spruce wood with copper fittings, iron chains, glass panes, reed-and-copper pipes, apothecary-brass machines with violet gem accents. Every machine has a status light that is color and shape coded (green circle = running, amber triangle = waiting, red square = fault) for color-blind players.

**3.7 Animation language.** Ease-out-back “pops” on growth, light squash and stretch on pours and snips, slow idle sway on leaves, lamps that flicker on with a three-beat stutter. Nothing snaps; everything eases.

**3.8 UI style.** Dark wood panels with violet accent borders, pixel font, icon-first layouts, consistent 2px bevels. Details in section 13.

---

## 4. Gameplay loops

**Micro loop (every \~2 minutes).** Look at a plant, read the tooltip, adjust (water, lamp height, fan), enjoy feedback.

**Macro loop (one batch, 30-60 minutes).** Seed → plant → manage environment → 4 stages → harvest → trim → dry → cure → use, craft or sell → breed → bigger setup.

**Meta loop (days to weeks).** Facility Rank → new tiers and recipes → automation → breeding lab → Heirlooms and lore → restore the Valley Greenhouse → Legacy.

**Example 45-minute session at Rank 5 (use as the pacing target).**

- 00:00 Step into the cave: lamp hum, mist, sparkle. Grow Monitor shows two flowering trays with humidity 8% high.
- 02:00 Switch on a fan; the hygrometer needle eases down. Tiny relief sound.
- 03:00 A tray is ripe: harvest snip cinematic, six Wet Clusters.
- 05:00 Trim minigame: Fine quality, one near-miss message tells you which sugar leaves were missed.
- 10:00 Hang bundles on the rack, load a jar onto the shelf.
- 12:00 Burp yesterday's jars (quick timing mini-moment), see color glow in glass.
- 14:00 Contract board: new request wants violet buds with Calm. You own a candidate seed line.
- 15:00 Sequence new seeds; one has an unknown gene. Plant it.
- 20:00 Spend Dew Coins on a better lamp; hang it with chains.
- 25:00 Explore a nearby cave; find a Journal Page and a Wild Sprout.
- 35:00 Back home: seedlings pop into vegetative stage with a sparkle.
- 40:00 The Green Hermit wanders in with a story contract.
- 45:00 Rank-up fanfare, new recipe unlocked, next goal appears.

---

## 5. Plant simulation

No real-world accuracy is intended. Everything is a readable game system.

**5.1 Units.** In-game day = 24000 ticks = 24 in-game hours. Temperature 0-40 “degrees”. Humidity 0-100%. Light in **Lume** 0-100 (separate from vanilla block light). Airflow 0-100. Water and each nutrient 0-100 per plant. Soil Quality 0-100.

**5.2 Lifecycle.**

| Stage | Base duration `[TUNE]` | Visual | Notes |
| --- | --- | --- | --- |
| 1 Seedling | 0.5 day | Tiny two-leaf sprout | Loves humidity, gentle light |
| 2 Vegetative | 1.0 day | Bushy leafy growth | Habit (tall/bushy) becomes visible |
| 3 Flowering | 1.25 days | Buds form, pistil hairs, tint shows | Needs a long dark period; mold-prone |
| 4 Ripe | peak window 0.4 day | Glistening, full bloom | Harvest now; slowly overripens, never destroyed |

Baseline seed-to-ripe is about 3 in-game days (about 60 minutes real time). Sleeping advances time as normal. Genes and care shift this by roughly 0.7x to 1.4x.

**5.3 Sweet spots per stage `[TUNE]`.**

| Stage | Light (Lume) | Lit hours/day | Humidity | Temp | Water | Nutrient |
| --- | --- | --- | --- | --- | --- | --- |
| Seedling | 35-60 | 14-20 | 65-85 | 20-26 | 55-85 | Sprout 20-50 |
| Vegetative | 55-90 | 14-20 | 50-70 | 22-28 | 45-75 | Growth 30-70 |
| Flowering | 70-100 | 9-13 | 35-55 | 20-26 | 40-65 | Bloom 30-70 |
| Ripe (flush) | 60-100 | 9-13 | 30-45 | 18-24 | 30-50 | none (Flush) |

**5.4 Comfort, Vigor, growth.** For each variable, `comfort = 1` inside the sweet spot and falls linearly to 0 at `tolerance` units outside it (default 20, widened by up to +10 by the Resilience gene). Then:

`Vigor = 0.6 * weightedMean(comforts) + 0.4 * min(comforts)`

Weights: water 0.25, light 0.25, humidity 0.15, temperature 0.15, nutrients 0.10, schedule 0.10. The `min` term makes one disaster hurt, so players fix the worst problem first.

`growthRate = 1/baseStageSeconds * speedGene * lerp(0.35, 1.15, Vigor)`

A struggling plant slows to 35% but never fully stalls, which is gentle failure by design. A perfect plant grows 15% faster than baseline.

**5.5 Quality accumulation.** `CareScore` is the time-weighted mean Vigor over Vegetative (weight 0.35) and Flowering (weight 0.65), plus bonuses: correct tonic per stage (+3 each, max +9), perfect light-schedule streak (+0.5 per day, max +5), completed Flush (+4); minus penalties from problems left untreated.

`FieldQuality = 0.55 * CareScore + 0.30 * GeneQuality + 0.15 * Terroir`

Terroir comes from Soil Quality (Dirt 20, Compost mix 50, Dewloam 70, Enriched Dewloam 90) and nearby ambiance (glow mushrooms, Dewstone, a happy Bee Hutch). Yield: `clusters = round(2 + Yield gene * 0.7 + Vigor bonus)`, giving 2-9 Wet Clusters per plant.

**5.6 Light.**

- **Lamp tiers:** Bulb Lamp (weak, glowstone, cheap), UV Tube Lamp (the reference image bar light), Full-Spectrum Panel (wide coverage), Amethyst Array (huge output and heat, needs power), plus Dimmable and Timer upgrades.
- **Hang height:** lamps hang from chains. Crouch-scroll on a lamp to adjust chain length. Intensity at the canopy: `Lume = output / (1 + k * distance^2)`; too close (Lume above 110) causes light burn, too far wastes output. A satisfying real decision with a visible reward (the beam shrinks and brightens).
- **Overlap:** footprints add, capped at 120.
- **Schedule:** plants track lit hours over a rolling day. Flowering needs 9-13 lit hours and one continuous dark stretch of at least 8 hours. A Timer block sets a 24-slot dial. Light leaks during the dark period flash a moon icon and delay flowering a little, never ruin it.
- **Heat:** lamps add heat in their room; fans and vents remove it. Layout becomes a puzzle.

**5.7 Water and nutrients.** Water drains with growth and heat. Three nutrient bottles (**Sprout Tonic**, **Growth Mix**, **Bloom Booster**) each have a stage where they shine; wrong-stage dosing gives a small penalty, not a disaster. **Flush** (plain water for the last 20% of Ripe) gives a quality bonus. Tonics are brewed at the Mixing Station from foraged ingredients (glow mushroom, honey, compost tea, amethyst dust).

**5.8 Problems (never instant death; each has a telegraph, a grace period and a cure).**

| Problem | Trigger | Telegraph | Effect | Cure |
| --- | --- | --- | --- | --- |
| Thirst | water < 20 | leaves tilt, droplet icon pulses | 35% growth | water |
| Overwater | water > 90 for 1 day | glossy soil, yellow tips | -Vigor | let dry, Drainage Grit |
| Nutrient burn | any nutrient > 85 | tips yellow then brown | -quality | Flush |
| Deficiency | nutrient < 10 in veg/flower | pale leaves | slower | feed |
| Heat stress | temp > upper + 4 | leaves curl, heat shimmer | -Vigor | fan, vent, raise lamp |
| Cold | temp < lower - 6 | blue-purple tint | slower | warm up |
| Light burn | Lume > 110 | bleached tops | -quality | raise lamp |
| Light leak | light in dark period | flickering moon icon | delayed flowering | fix schedule |
| Mold | humidity > 60 in flower, airflow < 30 | grey fuzz, spore particles, musty sound | spreads to neighbors, -30% yield if ignored a day | Mold Spray, dehumidifier, prune the spot |
| Mites | airflow < 25, heat, or a visitor | red specks, speckled leaves | drains Vigor, spreads | Ladybug Hutch, Neem Soap, Sticky Traps |
| Dormant | water 0 for 1 day | grey-green droop | growth pauses | water plus Revival Tonic |

Only Connoisseur preset allows death, after 3 in-game days at critical.

**5.9 Bees and pollination.** Flowering plants attract vanilla bees (tag them as flowers for bee AI). A bee carrying nectar stores a **pollen memory** (the genome of the last plant visited). When it reaches another flowering plant it may cross-pollinate it: the plant becomes **Seeded** (quality -15, yields 3-6 seeds with mixed genes). Natural, emergent breeding. Players choose: install a **Bee Screen** (mesh block) to keep bees out, or invite them. Bees near plants also make **Terpene Honey** (honeycomb tagged with the nearest strain's terpene), used in edibles. Pollination is server-side, polled at low frequency.

**5.10 Tools and instruments.**

- **Watering Can:** Tin Can (8 pours), Copper Can (16, wider splash), Brass Rose Can (24, 3x3 splash). First-person pour animation, droplet particles, and an audible fill level.
- **Pocket Meter:** right-click air or plant for temperature, humidity, Lume, airflow. Upgrades with Know-how.
- **Grower's Loupe:** reveals genes (tier 1 shows 2 genes, tier 2 shows 5, Sequencer shows all).
- **Clip Hygrometer:** attaches to a tray or rack for live readings.
- **Mold Spray, Neem Soap, Sticky Traps, Revival Tonic, Drainage Grit:** problem cures.

**5.11 First 20 minutes (onboarding script).**

1. Break a **Wild Sprout** in a lush cave or buy a **Dusty Seed Packet** from the Herbalist.
2. Craft a Clay Pot and Tin Can; plant and water. First tooltip appears, with a hint about lamps.
3. Craft a Bulb Lamp; hang it. First chain, first glow, first particles.
4. At \~8 minutes the first stage-change sparkle teaches “growth is visible”.
5. At \~15 minutes the first harvest triggers the snip cinematic, a tiny hand trim, a drying string and a jar.
6. The Green Hermit shows up with a one-line first contract and a Journal. Rank 2 unlocks.

---

## 6. Harvest, trim, dry, cure

**6.1 Harvest.** Shears on a Ripe plant start a short cinematic snip: camera eases in 0.6 s, two snips, a satisfying crunch, a burst of leaf and sparkle particles. Skippable. Yields Wet Clusters (stack item with strain, quality and weight data), Stalks (compost or biogas) and Fan Leaves (compost).

**6.2 Trim minigame (hand trimming, close-up camera).**

- Place Wet Clusters on a **Trim Station** (bench with a lamp and a mat) with Shears in hand.
- The camera eases into a macro view of one cluster, rendered large from the strain's actual colors.
- Each cluster has 8-14 **sugar leaf nodes** highlighted by a soft shimmer. Click a node to snip it. Rotate the cluster with scroll or A/D.
- Hitting the bud core is a **nick** (small quality penalty, a soft “oops” cue). Perfect snips on beat of a gentle metronome build a **Flow** streak that raises a score multiplier and swells a lo-fi music layer.
- Result: **Bag Appeal** 0-100 with a 1-5 star readout and a near-miss breakdown.
- A cluster takes 10-15 seconds; a batch of six takes about a minute.
- **Relaxed mode** (config): larger hit zones, no rhythm, no nick penalty, but Bag Appeal capped at 80.
- **Quick Trim** (hold to auto-trim): Bag Appeal capped at 65, so hand-trimming stays the premium path.
- **Tool tiers:** Rusty Shears, Steel Snips (smaller nick penalty), Silver Micro-Snips (wider flow window), Amethyst-edged Snips (combo bonus and sparkle trail).
- **Resin Gloves:** collect Resin Specks while trimming; spend them at the Resin Press for Pressed Resin, a potent crafting ingredient.
- **By-products:** Sugar Leaf Trim (edibles, tinctures), Kief Sift (sifting screen), Resin Specks.

**6.3 Drying.** Hang bundles on **Drying Racks** (holds 8; hanging pole look from the reference image). Needs temperature 16-22, humidity 45-60, and darkness (Lume < 20). Takes 1.0 in-game day. Bundles visibly change from deep green to pale, curled bunches. Too hot or too dry gives “Crispy” (-quality); too humid risks mold. A Clip Hygrometer on the rack shows a three-color ring. Rack state is cached per room, not per bundle.

**6.4 Curing (jars).** Dried buds go into **Curing Jars** placed on a **Jar Shelf** (3 rows x 4 slots, as in the reference). Each in-game day the jar has a **Burp Window** (about 4000 ticks). Right-click and hold to open; a moisture gauge fills, release in the green zone for a satisfying fizz. Success adds quality. Missing a day slows the cure but never loses anything. Buds are visible through the glass in their strain colors, and a label shows the strain name. Three good burps = **Cured** (+10 quality, terpene expression boost). After 10 days the jar becomes **Aged** (a small bonus and a “Vintage Day N” label). Collectors can build a Reserve Shelf of vintage jars.

**6.5 Quality tiers.**

| Tier | Score | Color |
| --- | --- | --- |
| Dusty | under 30 | grey `#9A9A9A` |
| Common | 30-54 | green |
| Fine | 55-74 | teal |
| Prime | 75-91 | violet |
| Legendary | 92+ | animated gold shimmer |

`FinalQuality = FieldQuality * (0.7 + 0.3 * BagAppeal/100) + DryBonus + CureBonus + AgeBonus`

Legendary additionally requires a hand trim (Bag Appeal 90+) and a Cured jar. Automation can reach Fine at launch; the **Apprenticeship** rule (section 9) lets repeated hand-crafted Prime+ batches of a strain raise the machine quality cap for that strain.

**6.6 Products.** Stackable items carry strain, quality, terpene and vintage data as components, so any machine can read them: Wet Cluster, Dried Bud, Cured Bud, Trimmed Bud, Sugar Leaf Trim, Kief Sift, Pressed Resin.

---

## 7. Genetics and strains

**7.1 The genome.** Eight genes, each with two alleles (one per parent). Stored as an immutable value object (section 1.4).

| Gene | Type | What it does |
| --- | --- | --- |
| Potency (POT) | 1-10 | Effect strength and duration; feeds GeneQuality |
| Yield (YLD) | 1-10 | Number of Wet Clusters |
| Speed (GRO) | 1-10 | Growth rate, 0.7x to 1.4x |
| Resilience (RES) | 1-10 | Widens comfort tolerance by 0-10, resists mold and mites |
| Terpene (TRP) | one of 8, primary + secondary | Decides the consumable effect line and the aroma |
| Pigment (PIG) | one of 7 + Frost 0-3 | Leaf, bud and hair colors; sparkle intensity |
| Habit (HAB) | Tall / Hybrid / Bushy | Model, height, spacing; Tall grows faster and needs a higher lamp, Bushy gives more clusters but is mold-prone |
| Luminescence (LUM) | recessive, very rare | Plant glows under UV and for a while after; emits light level 4-7 |

`GeneQuality = 10 * (0.45*POT + 0.25*RES + 0.15*GRO + 0.15*YLD) + 5*Frost` (0-100).

**7.2 Phenotype rules.** Numeric genes: average of the two alleles, plus **hybrid vigor** (+0.5) when alleles differ by 2 or less. **Inbreeding depression:** two identical low alleles (3 or below) on RES or GRO cost 1 point, creating realistic dead-end lines. Categorical genes use dominance. Pigment dominance order: Green < Violet < Pink < Blue < Amber < Crimson < Black. The dominant allele sets the main hue and the other shows as a secondary gradient tint, so hybrids look two-toned.

**7.3 Inheritance.** For every gene the offspring takes one random allele from each parent. Each allele then rolls a **mutation** (base 4%, 12% with Mutagen Dew): numeric alleles shift by 1-2, categorical alleles move to an adjacent type with a small chance of a rare one, and Luminescence appears at roughly 0.4%. A mutation triggers a sparkle on the seed and a Journal toast.

**7.4 Stabilizing a line.** A strain is **Stable** when both alleles of every gene match; its seeds breed true apart from mutations. Players get there by back-crossing and inbreeding, with the Seed Sequencer showing progress per gene. A Stable strain can be **Registered** at the Journal desk: it gets a permanent name (rename allowed), a Strain Card item, and a Seed Packet that always breeds true. This is the late-game mastery loop for breeders.

**7.5 Discovering genes.** Genes are hidden as `?` until revealed: Pigment and Habit are visible from Vegetative, Terpene shows as an aroma-colored particle from Flowering, Potency and Yield reveal at harvest, and the Loupe (2 / 5 genes) or Sequencer (all) reveal them directly. This creates reveal moments and gives the Loupe real value.

**7.6 Breeding procedure.**

1. **Pollen Brush** on a Flowering plant collects a **Pollen Vial** (once per stage per plant). The vial carries the donor's genome.
2. Use the vial on another Flowering plant. That plant becomes **Seeded** (quality -15, 3-6 seeds with independently rolled offspring genomes; 5% of seeds are Duds).
3. Harvest yields the seeds. Bees do the same job naturally (section 5.9).

**7.7 Terpenes** (aroma particle color and effect line; numbers in section 8).

| Terpene | Aroma color | Effect line |
| --- | --- | --- |
| Myrcene | amber | Couchlock |
| Limonene | yellow-green | Uplift |
| Pinene | forest green | Clarity |
| Linalool | lavender | Calm |
| Caryophyllene | warm red | Ward |
| Humulene | tan | Hearty |
| Terpinolene | teal | Whimsy |
| Ocimene | pink | Muse |

**7.8 Strain names.** Procedural and deterministic from the genome hash (same genes, same name). Format: `[Prefix] [Place] [Noun]`; Common and Wild strains drop the prefix. Example: “Stonedew Valley Kush”, “Twilight Hollow Lullaby”.

- **Prefix from Pigment:** Green: Mossy, Verdant, Fernlit. Violet: Twilight, Amethyst, Plum. Pink: Rosy, Blush, Peony. Blue: Frostbitten, Glacier, Cobalt. Amber: Honeyed, Golden, Emberglow. Crimson: Scarlet, Garnet, Ruby. Black: Midnight, Obsidian, Eclipse.
- **Place from the lineage seed:** Stonedew Valley, Lantern Ridge, Mirewater, Copperfall, Hushwood, Glimmer Deep, Mothlight Hollow, Pebblebrook, Ashen Vale, and so on. A strain born from bee cross-pollination gets a place named after the nearest landmark or biome.
- **Noun from primary Terpene:** Myrcene: Kush, Slumber, Dream. Limonene: Zest, Sunrise, Spritz. Pinene: Pine, Frost, Haze. Linalool: Lullaby, Lavender, Mist. Caryophyllene: Ember, Spice, Hearth. Humulene: Hops, Biscuit, Feast. Terpinolene: Whimsy, Sparkle, Wisp. Ocimene: Basil, Bloom, Muse.

**7.9 Strain rarity** (name color): Wild (white), Cultivar (green), Select (blue), Rare (purple), Heirloom (gold), Mythic (animated shimmer). Based on GeneQuality plus rare traits (Luminescence, Black pigment, rare terpene combos, Heirloom origin).

**7.10 Strain Journal.** Auto-logs every strain grown. Undiscovered Heirlooms show as silhouettes. Features: lineage tree viewer (pixel-art family tree), personal best quality, favorite star, notes field, per-strain Apprenticeship points, completion percentage with rewards at 10/25/50/100 strains. **Strain Cards** are craftable collectibles that can be displayed in a Display Case.

**7.11 Heirloom strains.** 30 hand-authored fixed genomes defined in datapack JSON, each with lore, a unique visual flourish and a hiding place in the world (journals, structures, Hermit rewards). Five are the **Founders' Lines** needed for the endgame (section 12).

---

## 8. Consumables, effects and tolerance

**8.1 Consumable items.**

| Item | Made at | Use | Onset | Duration | Notes |
| --- | --- | --- | --- | --- | --- |
| Joint | Rolling Table (paper + bud) | 1.6 s | instant | 1.0x | Smoke puff particle, soft crackle |
| Pipe | crafted, reusable | 3 hits per packed bowl | instant | 0.8x per hit | Ember glow, bowl animation |
| Edibles (brownie, cookie, gummy, toffee) | Mixing Station, Oven | 1.2 s | 20 s | 2.5x | Also restores hunger |
| Tincture | Apothecary Still | 4 drops | 5 s | 3.0x, amplifier -1 | Dropper animation |
| Calm Tea | kettle | 1.5 s | instant | 1.5x | Gentle, always Calm line |

**8.2 Effect math.** Base duration `= 60 s + 20 s * POT`. Amplifier 0, or 1 when POT is 8 or higher. The secondary terpene runs at half duration and amplifier 0. Final magnitude is multiplied by the player's tolerance factor (8.4).

| Effect line | Mechanics |
| --- | --- |
| Couchlock (Myrcene) | Slowness I + Regeneration I; extra regen while seated on stairs |
| Uplift (Limonene) | Speed I + Haste I |
| Clarity (Pinene) | Night Vision; Trim Flow window +20% |
| Calm (Linalool) | Custom: hostile detection radius halved, hunger drains slower |
| Ward (Caryophyllene) | Resistance I + short Fire Resistance |
| Hearty (Humulene) | Saturation + Absorption (2 hearts) |
| Whimsy (Terpinolene) | Jump Boost I + Slow Falling, sparkle trail |
| Muse (Ocimene) | Luck I + 10% bonus Dew XP while active |

**8.3 Terpene combos** (primary + secondary), each adds a bonus line:

- Myrcene + Linalool = **Deep Dream:** sleeping while active records a Dream Journal collectible and grants Regeneration II on waking.
- Limonene + Pinene = **Bright Mind:** Haste II for 60 s.
- Caryophyllene + Humulene = **Hearth:** extra regeneration near a furnace or campfire.
- Terpinolene + Ocimene = **Dreamer's Luck:** Slow Falling + Luck II.
- Linalool + Limonene = **Sunset:** Calm and Speed together.
- Pinene + Caryophyllene = **Sentinel:** nearby hostile mobs within 16 blocks get a faint outline.

**8.4 Tolerance.** Per player, per terpene, 0-100%. Each use adds 12% (scaled by preset). It decays about 1% per in-game hour. Effect duration and strength are multiplied by `1 - 0.6 * tolerance`. The Journal shows a small bar per terpene. **Tolerance Break Tea** halves one terpene's tolerance. Result: variety is rewarded and breeding for different terpenes has purpose.

**8.5 Too Cozy.** Using 4 or more consumables within 2 minutes triggers **Too Cozy**: Slowness II, a soft vignette blur, and a hint to take a nap. It is never lethal and does no damage.

**8.6 Visual and audio feel.** Each effect line has a subtle color grade, soft chime and particle trail. All are config toggles with an intensity slider. No flashing effects.

**8.7 Herbal Mode (config).** Replaces consumable names and textures with an apothecary theme (Joint becomes Herbal Roll, Bud becomes Flower, Pipe becomes Herb Pipe), swaps smoke for incense-style particles, and uses alternate lore text. Gameplay is identical. This keeps the mod easy to share on platforms with content rules and friendly to younger players.

---

## 9. Progression and economy

**9.1 Currency.** **Dew Coins** from contracts and Trade Depot sales. The Herbalist exchanges them for emeralds (rate `[TUNE]`).

**9.2 Facility Rank (1-30).** **Dew XP** comes from nearly every action: first harvest of a strain, quality tiers achieved, trim scores, jar burps, contract completions, strain discoveries, lore pages. Key unlocks:

| Rank | Title | Unlocks |
| --- | --- | --- |
| 1 | Sprout | Clay Pot, Tin Can, Bulb Lamp, Journal |
| 2 | Seedkeeper | Planter Bed, Jars, string drying line, first Hermit contract |
| 3 | Gardener | UV Tube Lamp, hand Mixing Bench, Trim Station |
| 4 | Cultivator | Jar Shelf, Rolling Table, Pocket Meter |
| 5 | Tinkerer | Tier T1 machines, Contract Board |
| 8 | Plumber | Tier T2 (pipes, power, Mixing Station) |
| 10 | Climatist | Tier T3 (Grow Room Controller) |
| 13 | Logistician | Tier T4 (trays and rails) |
| 16 | Geneticist | Tier T5 (Breeding Lab) |
| 20 | Operator | Tier T6 (Control Room, routines) |
| 24 | Restorer | Access to Valley Greenhouse quests |
| 30 | Circle Master | Legacy (prestige) |

The **Cultivator's Almanac** (progress book) always shows upcoming unlocks as locked silhouettes with their exact requirements and your current progress. There is never a mystery about what to do next.

**9.3 Know-How meters.** Eleven per-player meters (0-100): Watering, Feeding, Lighting, Climate, Trimming, Drying, Curing, Breeding, Mixing, Plumbing, Logistics. They fill by doing the task by hand. Thresholds unlock the matching automation blueprint (together with the Rank requirement) and small passive perks.

| Meter | Threshold | Unlocks |
| --- | --- | --- |
| Watering | 30 | Drip Tray |
| Feeding | 40 | Mixing Station |
| Climate | 50 | Grow Room Controller |
| Trimming | 60 | Auto-Trimmer |
| Curing | 40 | Burp Valve |
| Logistics | 40 | Tray Rails |
| Breeding | 50 | Cross-Breeder |

Perks example: Watering 50 = Can refills 10% faster; Trimming 30 = wider Flow window; Curing 30 = jars show an exact burp timer.

**9.4 Apprenticeship.** Automation starts capped at Fine (Grower preset). For each strain, every Prime-or-better hand-trim or hand-cure batch adds 1 point. At 3 points the machine cap for that strain rises to Prime. Legendary always needs hands. Result: hand-crafting stays relevant forever.

**9.5 Sale value.** `value = baseByRarity * tierMult * freshness * demand`. tierMult: Dusty 0.4, Common 1, Fine 1.8, Prime 3.2, Legendary 6. freshness: Cured 1.0, Dried 0.8, Wet 0.3. **Market Demand** rotates daily (0.8 to 1.4 per terpene or color) on a Market Board, rewarding variety over mass-producing one strain.

**9.6 Sinks (so coins always matter).** Lamp and machine upgrades, Heritage Market cosmetics (lamp skins, jar labels, trolley paint), decor, Strain Show entry fees, blueprints, rare seed shop stock that rotates daily.

**9.7 Celebration beats.** Rank-up: fanfare, a brief violet burst, banner, and the next three unlocks revealed. Tier unlock: a mini cinematic of the new machine blueprint appearing on the Hermit's table. First Legendary: golden sparkle, a framed Strain Card, and a server-wide toast in multiplayer.

**9.8 Advancements.** About 60, grouped into Growing, Craft, Breeding, Automation, Lore and Collecting. Examples: “First Snip”, “Perfect Burp”, “Two-Tone Hybrid”, “The Glow Mutation”, “No Hands Needed” (first fully automated batch), “Vintage Reserve” (a 30-day aged jar).

**9.9 Pacing targets `[TUNE]`.** First harvest 15 min. Rank 5 / T1 about 2 h. T2 about 4 h. T3 about 7 h. T4 about 11 h. T5 about 15 h. T6 about 22 h. Valley Greenhouse about 30 h. Legacy about 40 h. At every point a new unlock or visible goal should be under 15 minutes away.

---

## 10. Automation ladder (tiers T1-T7)

Automation is the long-term addiction engine, built as a chain of **bottlenecks**, Factorio-style. It is never just “unlock auto-everything”.

**10.1 Design rules.**

1. **Earn it by doing it.** Each automation unlocks after the player has done the manual version enough times (Know-How, section 9.3) and has the Rank. You never automate a chore you haven't felt.
2. **Each machine fixes a pain the player already has and exposes the next bottleneck downstream.** There is always a visible “next thing to fix”.
3. **Every tier adds one new decision, not just a bigger number:** layout puzzle (T1-T2), power design (T2), recipe tuning (T3), logistics routing (T4), breeding goals (T5), routine design (T6), legacy choices (T7).
4. **Two economies.** Hand-crafted means low volume and top quality (Legendary). Automated means high volume capped by Apprenticeship (section 9.4).
5. **Failure is gentle and readable.** Machines fail safe with an amber light and a tooltip reason; a crop is never wiped while the player is away.
6. **Everything is alive.** Visible fluid in pipes, trolleys gliding, lamps cycling, status lights, and a sound on every handoff.

**10.2 Power model.** Unit: **Watts (W)**, mapped 1:1 to Forge Energy per tick `[TUNE]`, exposed via the standard energy capability. Redstone signals can switch any machine on or off. Early lamps (T0-T1) run on consumable **Glow Cells** (amethyst + glowstone + copper, lasting about 5 in-game days) swapped by right-click. T2 introduces wired power and removes that chore while creating the power puzzle.

| Source | Output | Notes |
| --- | --- | --- |
| Hand Dynamo | +10 W while cranked | Tactile starter power (hold right-click) |
| Water Wheel | 0-40 W | Scales with flowing water; placed in streams |
| Solar Panel | 30 W by day, 0 at night | Needs Battery Bank |
| Battery Bank | stores about 10 min of 120 W | Smooths day and night |
| Biogas Digester | +60 W for 8 min per compost bundle | Turns trim, stems and fan leaves into power |
| Dewstone Generator (T7) | 150 W passive | Endgame, needs Dewloam |

**10.3 Fluid model.** Two fluids: **Water** and **Nutrient Solution** (carries the three tonic levels). Pipes are graph networks rebuilt only on neighbor change, with simple capacity and demand rules, no per-tick scanning.

### T1. Tinkerer's Corner (Rank 5, Watering 30)

- **Lamp Timer** (24-slot dial; satisfying clunk per slot), **Drip Tray** (a reservoir beside pots that waters adjacent slots, 8-bucket capacity, visible droplets), **Hygrometer Alarm** (a chime when out of range), **Clip Hygrometer**, **Hand Dynamo**.
- **Wow moment:** the first dusk where the lamps switch on by themselves with the three-beat flicker.
- **Solves:** forgetting to water and switch lights. **New bottleneck:** refilling and dosing.

### T2. Plumbed Room (Rank 8, Feeding 40)

- **Reservoir Tank** (tall glass cylinder with a visible level), **Reed-and-Copper Pipes**, **Pump**, **Drip Emitters** on planters, **Mixing Station** (three Nutrient Tanks + a Recipe Card slot + water gives auto-dosed solution), **Copper Wire** power, **Water Wheel, Solar Panel, Battery Bank, Biogas Digester**.
- Nutrient Tanks are still refilled by hand from brewed tonics.
- **Wow moment:** colored fluid visibly flows through the pipes; the Mixing Station gauges bubble.
- **Solves:** manual watering and feeding. **New bottleneck:** power budget and lamp heat.

### T3. Climate Controller (Rank 10, Climate 50)

- A **Grow Room** is any sealed volume (flood-fill from the Controller, cap 2000 blocks, glass counts, closed doors seal, vents are controlled openings). Cached and invalidated with throttling.
- **Grow Room Controller:** auto-links every actuator and sensor inside the room with zero wiring; floating icons show what it found.
- **Actuators:** Humidifier, Dehumidifier, Intake and Exhaust Fans, Cooling Coil, Vent/Duct (moves heat between rooms), Sensor Probe.
- **Grow Recipe item:** per-stage target ranges, light schedule, nutrient ratios and flush timing. Presets: Gentle Start, Fast Flower, Terpene Max, Mold Guard. Editable with sliders and a live **predicted quality** preview. Copyable and shareable; rare recipes are found in structures.
- **Live graph:** 24-hour temperature, humidity and Lume lines, plus a Room Efficiency score.
- **Wow moment:** place the Controller and watch the floating icons connect as the graph starts drawing itself.
- **Solves:** micromanaging climate. **New bottleneck:** moving plants between rooms.

### T4. Tray Logistics (Rank 13, Logistics 40)

- **Large Grow Trays (3x3)** ride **Cultivator Rails** (attach under the ceiling, curves and junctions) via **Trolleys** (small brass carts with a hanging lantern).
- **Stations:** Load Dock, Room Gate (passes through doors and glass), Strain / Stage / Quality **Filters**, **Hand-Trim Dock** (the tray parks at a Trim Station for the minigame), **Auto-Trimmer** (quality capped by Apprenticeship), **Drying Gallery** (auto-rack), **Curing Cellar** with **Burp Valves**, **Packing Dock** (to the Trade Depot).
- A tray automatically advances Veg to Flower to Dry to Cure when each stage completes.
- Trolley motion is animated client-side along the rail; the server only computes arrival times.
- **Wow moment:** a tray of ripe plants glides through the doorway on its own, chain rattling, door opening.
- **Solves:** hauling and sorting. **New bottleneck:** room throughput and power.

### T5. Breeding Lab (Rank 16, Breeding 50)

- **Pollen Collector** (a hovering brush arm that collects automatically), **Seed Sequencer** (helix animation, reveals all genes and per-gene stability), **Cross-Breeder**, **Seed Vault** (54 slots with search by strain, terpene, color, stability, favorites), **Mutation Chamber** (Mutagen Dew + UV raises mutation chance for a batch, at the cost of more Dud seeds).
- **Breeding Goal Card:** sliders for POT/YLD/GRO/RES minimums, target terpene, target pigment, Luminescence yes/no, Stable required. The Cross-Breeder runs one generation per in-game day, picks the best seed by goal score each time, and delivers after N generations. RNG matters: mutation events, lucky “Eureka” sparkles, and dead-end lines from inbreeding.
- **Wow moment:** the generation counter ticks, the helix glows, and a new Strain Card reveals.
- **Solves:** manual cross-breeding. **New bottleneck:** chasing rare genes and stabilizing lines.

### T6. Facility Control Room (Rank 20)

- **Control Console + Display Panels** that tile into a wall. Widgets: output per minute, quality histogram, power balance, water, per-room health lights, **Bottleneck Spotlight**, contract tracker, Market Demand.
- **Routine Rack:** physical **Routine Cards** (IF / THEN, no coding). Triggers: room metric above or below, plant stage, tank level, power percent, inventory count, time of day, contract deadline, mold risk. Actions: start or stop a device, switch Grow Recipe, dispatch a tray, send a Pager alert, sound an alarm, open a vent, export to the Trade Depot. Up to 24 routines per console. Example: “IF Flower Room mold risk is above 60% THEN run dehumidifier and alert me.”
- **Pager:** handheld alert item (HUD ping, chat line, soft chime) with filters.
- **Dew Sprites:** little lantern fairies that live at a **Sprite Perch**. They handle edge-case chores (small pours, squashing mites, carrying trim, pollinating with a chosen vial). Limit 8, upgraded via Know-How. They never replace hand quality.
- **Trade Depot Export Port:** auto-fulfills contracts from sorted storage.
- **Wow moment:** the screen wall lights up with live data, and the first alert saves a batch.

### T7. Heritage and Legacy (Rank 24 / 30)

- Restore the **Valley Greenhouse** (section 12) to unlock **Legacy**, a prestige reset. You keep the Journal, Registered strains, 50% of Know-How, and all cosmetics. The facility resets.
- On each Legacy choose one permanent **Heirloom Bonus**: Green Thumb (+8% growth), Keen Eye (Loupe reveals +1 gene), Frugal Mixer (-15% tonic cost), Calm Hands (+10% trim Flow window), Bee Whisperer (pollen memory lasts 2x), Deep Pockets (+10% sale value), Quick Study (1.25x Know-How gain).
- Unlocks **Heritage Contracts**, a unique Legacy Seed lineage, new Valley Seasons modifiers, and cosmetics (lamp skins, jar labels, trolley paint). Legacy 1-10 with escalating prestige titles.

**10.4 Supporting systems.**

- **Compost loop:** trim, stems and fan leaves go into a Compost Bin for better soil, a Worm Bin for Rich Compost, or a Biogas Digester for power. Waste always has a use.
- **Heat and space puzzle:** lamps produce heat; ducts, vents and room layout matter.
- **Facility Score:** a visible number blending output, quality, efficiency and uptime. Optimizing it is its own game.
- **Blueprints (stretch, P9):** a Blueprint Table scans a room into an item; a Builder's Ghost overlay lets you place it, consuming materials as you build.
- **Offline catch-up:** when a chunk loads, simulate elapsed time up to the preset cap. Stepping away is never punished.
- **Safety net:** every machine has a “last known good” recipe fallback and fails safe.

---

## 11. Machine catalog

| Machine | Tier | Function | Power | Connects |
| --- | --- | --- | --- | --- |
| Clay Pot / Planter Bed / Large Grow Tray | T0 / T0 / T4 | 1 / 4 / 9 plant slots | none | items, drip |
| Bulb Lamp | T0 | Weak light, Glow Cell | Glow Cell | none |
| UV Tube Lamp | T1 | Lume 55-80, 3x1 footprint | 20 W / Glow Cell | wire |
| Full-Spectrum Panel | T2 | 3x3 footprint | 45 W | wire |
| Amethyst Array | T4 | 5x5 footprint, high heat | 90 W | wire |
| Lamp Timer | T1 | 24-slot light schedule | 0 | adjacent |
| Drip Tray | T1 | Auto-waters adjacent slots | 0 | bucket, pipe |
| Hygrometer Alarm | T1 | Chime out of range | 0 | none |
| Hand Dynamo | T1 | +10 W while cranked | source | wire |
| Reservoir Tank | T2 | 16-bucket fluid storage | 0 | pipe |
| Pump | T2 | Moves fluid | 8 W | pipe |
| Drip Emitter | T2 | Per-planter feed | 0 | pipe |
| Mixing Station | T2 | Auto-doses three nutrients | 12 W | pipe, items |
| Water Wheel / Solar Panel | T2 | 0-40 W / 30 W day | source | wire |
| Battery Bank / Biogas Digester | T2 | Storage / power from compost | source | wire |
| Grow Room Controller | T3 | Runs the room by recipe | 5 W | auto-link |
| Humidifier / Dehumidifier | T3 | +/- room humidity | 10 / 14 W | auto-link |
| Intake / Exhaust Fan | T3 | Airflow, heat removal | 6 W | auto-link |
| Cooling Coil | T3 | -4 temperature | 18 W | auto-link |
| Vent / Duct | T3 | Moves air and heat between rooms | 0 | duct |
| Sensor Probe | T3 | Extra sensing point | 1 W | auto-link |
| Cultivator Rail | T4 | Ceiling rail network | 0 | rail |
| Trolley | T4 | Carries a tray | 4 W moving | rail |
| Dock / Room Gate / Filter | T4 | Load, pass walls, sort | 3 W | rail |
| Auto-Trimmer | T4 | Machine trim (capped) | 25 W | rail, items |
| Burp Valve | T4 | Auto-burps cellar jars | 2 W | auto-link |
| Pollen Collector | T5 | Automates pollen | 6 W | trays |
| Seed Sequencer | T5 | Reveals genes | 18 W | items |
| Cross-Breeder | T5 | Runs breeding goals | 30 W | items |
| Seed Vault | T5 | Searchable seed storage | 0 | items |
| Mutation Chamber | T5 | Boosts mutation | 22 W | items |
| Control Console / Display Panel | T6 | Dashboard wall | 3 W each | auto-link |
| Routine Rack | T6 | IF / THEN cards | 2 W | auto-link |
| Sprite Perch | T6 | Home for Dew Sprites | 0 | none |
| Trade Depot Export Port | T6 | Auto-sell and fulfill | 6 W | items |
| Dewstone Generator | T7 | 150 W passive | source | wire |
| Legacy Pedestal | T7 | Prestige | 0 | none |

---

## 12. World, lore and NPCs

**12.1 Stonedew Hollow (the setting).** A rare underground cave biome (data-driven worldgen) found deep below lush and dripstone caves. Features: **Dewloam** (dark soil with glowing flecks, the best growing soil), **Dewstone** crystals (violet-cyan, light source and ingredient), glow mushrooms, hanging glow vines, amethyst clusters, harmless **Dew Moths** (ambient sparkle fliers), and **Wild Sprouts** (the first seeds). Hints to find it come from Journal Pages and the Hermit.

**12.2 Story in five acts (cozy mystery tone).**

| Act | Rank | Beat |
| --- | --- | --- |
| I. Seedkeeper | 1-4 | Find the Old Grower's Note; the Green Hermit appears; you learn a Circle once lived here |
| II. The Circle's Trail | 5-12 | Journal Pages 1-6 in abandoned grow caves reveal the five Founders |
| III. The Long Dry | 13-19 | Pages 7-12: the dew stopped. Recover the five Founders' Lines as Heirloom strains |
| IV. Restoring the Greenhouse | 20-27 | Five Wings of the Valley Greenhouse, each needs a Founder's Line plus a facility feat |
| V. The Mother | 28-30 | Cross the five lines into the Mother Strain; the Dewstone Heart wakes; Legacy opens |

**The Founders and their Lines (Heirloom strains, section 7.11).**

| Founder | Specialty | Heirloom Line | Wing |
| --- | --- | --- | --- |
| Maren Ashgrove | Soil and compost | Ashgrove Loam (Myrcene, Green/Amber) | Nursery |
| Tobias Quill | Tinctures and alchemy | Quill's Cordial (Linalool, Violet) | Apothecary |
| Ilsa Moorwick | Genetics | Moorwick Frost (Pinene, Blue, Frost 3) | Library and Lab |
| Pell Harrow | Machines and plumbing | Harrow Spark (Ocimene, Amber) | Workshop |
| Wren Duskmantle | Light and UV | Duskmantle Glow (Terpinolene, Black, Luminescent) | Observatory Dome |

**The twist.** The Circle did not vanish. They over-harvested the Dewstone Heart, the dew ran thin, and they sealed it to save the valley. The Green Hermit is **Fen**, their youngest apprentice, who has kept watch for decades. The ending is warm and bittersweet, not grim.

**12.3 The 15 Journal Pages** (one collectible each; found in structures, shops and Hermit rewards):

1. *Found a Hollow* (Maren): the first dew drip, the soil glows.
2. *Rules of the Circle*: never rush, never waste, always share a jar.
3. *Quill's Margin Notes*: the first tincture recipe.
4. *Moorwick's Wager*: a bet over stabilizing a line.
5. *Harrow's First Pump*: plumbing breakthrough.
6. *Dusk Lamps* (Wren): discovering UV glow.
7. *The Bee Accord*: what bees taught them about crossing.
8. *Bumper Year*: the Circle at its height.
9. *Dew Runs Thin*: first sign of decline.
10. *The Argument*: whether to keep drawing on the Heart.
11. *The Long Dry*: the dew stops.
12. *Sealing Notes*: the plan to seal the Heart.
13. *Fen's Vigil*: decades of waiting.
14. *A Recipe for the Mother*: a hint at the five lines.
15. *Letter to Whoever Comes Next*: the emotional final page.

**12.4 Structures** (all with loot tables, all in `stonedew:` structure sets):

- **Abandoned Grow Cave** (small, common): broken planters, cracked jars, seeds, old shears, 30% chance of a Journal Page. Variants: Closet, Greenhouse Ruin, Flooded Nursery.
- **Circle Outpost** (medium, rare): Recipe Cards, an Heirloom seed chest, a lamp-alignment puzzle that opens a vault.
- **Valley Greenhouse** (unique per world, in the Hollow): the restoration set piece with five Wings, each visibly transforming as restored.
- **Hermit's Lantern Camp** (small, wandering): a cozy rest stop with a bed, lantern and trade chest.

**12.5 NPCs.**

- **Herbalist villager** (job site: Herbalist's Bench). Trades by level: Novice (Dusty Seed Packets, Clay Pots, Tin Cans), Apprentice (jars, tonic bases, Loupe tier 1), Journeyman (Glow Cells, paper), Expert (Market intel, rotating rare seeds), Master (Wild Heirloom seed, Dew Coin exchange). Buys cured buds for emeralds.
- **The Green Hermit** (moss cloak, lantern, a tame Dew Moth companion). Appears near your facility after Rank 2. Gives story contracts, lore, Recipe Cards and Tolerance Break Tea. Dialogue uses a typewriter effect with soft blips; the Hermit is the emotional anchor.
- **Brisk Barrow** (rival grower, random visitor): swaps samples, challenges you to bets at Strain Shows. If you accept his sample, you may get a rare seed but also a mite outbreak.
- **Judge Thistlewick** (wandering judge for Strain Shows, section 15.4).

**12.6 Contracts.**

| Type | Example |
| --- | --- |
| Standard | “Violet, high-terpene, Fine or better, 6 buds, by day 5” |
| Chain (story) | Hermit asks for a specific aroma to test an old theory |
| Rush | Short deadline, big reward |
| Collector | A specific Strain Card from your Journal |
| Vintage | A jar cured at least N days |
| Heritage (T7) | Prestige-tier demands |

The generator checks your Journal and owned seeds so a contract is never impossible. Failing costs nothing; the contract just expires and the Hermit says something kind. Rewards: Dew Coins, Reputation, rare seeds, Recipe Cards, cosmetics. Two reputations: **Herbalist Guild** (1-5 stars; affects prices) and **Hermit's Trust** (1-5 stars; affects lore and rare recipes).

**12.7 Decor and display.** Glow Mushroom Terrarium (decor plus a Glowcap harvest used in tonics), Display Case (Strain Cards), Trophy Shelf (ribbons), Reserve Shelf (vintage jars), neon-style Dewstone signs, string lights, plant stands.

---

## 13. UI/UX

**13.1 In-world plant tooltip** (matches the reference image). Top-center panel appears when looking at a plant. Line 1: small strain icon and **Grow Stage x/4**. Line 2: **Humidity y%** with a red or green arrow when out of range. Line 3: strain name in rarity color. Hold sneak to expand: four icons (water, light, nutrients, health) with 5-pip fills, a status reason in amber (“Humidity too high for flowering (target 35-55)”), and an optional “ripe in about N minutes” line.

**13.2 Grow Monitor** (wall-mounted block). Four gauge rings (temperature, humidity, Lume, airflow), color-coded, with a status light. Replaced by the Controller at T3.

**13.3 Strain Journal** (book GUI). Tabs: Strains, Lore Pages, Contracts, Stats, Almanac (progress), Tolerance, Settings. The strain page shows a rotating 3D bud model, the genome as bars (`?` for unknown), a lineage tree, notes, and Apprenticeship points.

**13.4 Trim GUI.** Macro cluster view, a Flow meter, cluster counter, Bag Appeal ring, hint line. Details in section 6.2.

**13.5 Controller GUI.** Left: devices and status. Center: 24-hour graph. Right: **Grow Recipe editor** with stage tabs and sliders showing the sweet-spot band, plus a predicted quality bar.

**13.6 Routine UI.** Drag-and-drop **Routine Cards** into the Rack. Each card reads “IF \[icon + threshold\] THEN \[icon\]”, with a ghost preview of the result.

**13.7 Dashboard.** Tileable widget wall (output/min, power, water, per-room lights, Bottleneck Spotlight, contracts, Market Demand).

**13.8 HUD.** Collapsible **Next Goal** widget, Pager pings, small discovery toasts, optional tolerance mini-bars, and context hints near the crosshair (“Right-click: pour”).

**13.9 Accessibility.** Shape-coded icons for color-blind players, text scale, reduced motion, subtitles for all sounds, no flashing effects, high-contrast UI toggle, one-handed minigame assist, hold-to-confirm for destructive actions.

**13.10 Consistency rules.** One pixel font, 2px bevels, dark-wood panels with violet borders. Tooltip format: name in rarity color, category, stat lines, status reason in amber. Jade/WTHIT shows the same information on every block.

---

## 14. Camera, animation and audio

All camera moments have a config (Off / Minimal / Full), can be skipped with Space, and cancel immediately if the player takes damage.

**14.1 Camera moments.**

| Moment | Length | Notes |
| --- | --- | --- |
| Harvest snip | 1.2 s | Dolly in 0.6 s, two snips, FOV 70 to 58, optional depth blur |
| Trim macro | eases in 0.5 s | Free exit any time |
| Stage-change time-lapse | 1.5 s | Plant scale tween with sparkle; soft FOV nudge if you are looking at it |
| Lamp power-on | 0.8 s | Three-beat flicker and bloom |
| Tier unlock reveal | 3 s | Blueprint appears on the Hermit's table |
| Rank-up | 2 s | Banner and violet burst |
| Greenhouse finale | 20 s | Full cinematic, skippable |

**14.2 First-person animations.** Watering can (tilt and arc, stream particles), shears (open-close), jar burp (lid twist), Pager (flip), Loupe (raise to eye), Pipe (bowl glow), tincture dropper.

**14.3 Particles.** Purple ground mist, sparkle (stage-up, quality-up), water droplets, mold spores, mite specks, pollen motes, resin glints, terpene aroma wisps (color-coded), UV beam motes, dew drips from lamps, Dew Moth glow, rank burst, jar fizz, Legendary shimmer, incense-style smoke (Herbal Mode).

**14.4 Sound palette (about 45 sounds).** Water pour (pitch follows fill level), droplet on leaf, shear snip (two pitches for rhythm), resin tack, jar lid twist and fizz, glass clink, lamp hum loop (volume follows power), lamp stutter-on, chain rattle, trolley glide with chain ticks, pipe gurgle, Mixing Station bubbling, fan whir, humidifier hiss, dehumidifier drip, routine relay click, Pager chime, stage-up chime (pentatonic), rank-up fanfare, discovery stinger, mutation shimmer, Legendary shimmer, plant rustle, harvest crunch, paper rustle, joint crackle (soft), Dew Sprite chime, Hermit typewriter blips, cave ambience, moth flutter.

**The facility hums.** Ambient audio is layered by what you have built: lamps, pipes, fans and trolleys add their own quiet layer, so a bigger facility literally sounds richer. This is progress feedback you can hear.

**14.5 Music (6 tracks, soft lo-fi ambient with vibes and plucked strings).** *Dewdrop* (growing), *Hollow Hum* (caves), *Evening Harvest* (trim, with a rhythm layer that swells with Flow), *Tinker's Waltz* (automation), *Fen's Vigil* (lore), *The Mother* (finale). Per-category volume sliders.

---

## 15. Replayability and live systems

**15.1 Strain depth.** Procedural strains, 30 Heirlooms, and the stabilization chase give the breeding loop effectively unlimited depth.

**15.2 Dew Seasons** (each lasts 7 in-game days and rotates; announced by the Hermit with an event banner).

| Season | Effect |
| --- | --- |
| Mistfall | Ambient humidity up, mold risk up, more mushrooms |
| Glowbloom | Mutation chance up, extra sparkle |
| Dryspell | Humidity down, water drains faster, potency slightly up |
| Frostwake | Cold ambient, heating matters, Blue pigment more likely |

Adapting to a season earns a **Season Rosette** collectible.

**15.3 Random events** (max one negative per in-game day, always recoverable, each with a 10-20 s telegraph and a reward for handling it): Heatwave, Mite Outbreak, Lucky Mutation, Rival Visitor, Power Flicker (T2+), Pipe Leak, Moth Swarm, Market Boom, Hermit's Gift, Storm (solar dips). Categories are individually toggleable.

**15.4 Strain Show** (every 10 in-game days). Judge Thistlewick scores entries on Bag Appeal, Aroma (terpene richness), Color (pigment contrast) and Potency. Bronze, Silver, Gold and Best in Show ribbons; trophies for the Trophy Shelf; themed categories (“Best Violet”).

**15.5 Challenge modifiers** (chosen at Legacy or new game): Windowsill (nothing past T1), No-Hands (automation only), Drought Year, Heritage Hunter (found strains only), Wild Start (no purchased seeds), Speed Run (local timer records).

**15.6 Collection hooks.** Journal 100%, Strain Cards in Display Cases, Vintage Reserve Shelf, Dream Journal (30 entries), Journal Pages, Ribbons, Facility Score records, cosmetic sets, mastery titles.

**15.7 Extensibility.** Datapack terpenes, effects, events and contract templates, so modpack makers extend replay value.

**15.8 Anti-boredom guardrails.**

- After 20 manual repetitions of a chore, the game hints at the matching automation.
- Any loop longer than 90 seconds without a decision or feedback beat is a bug to be fixed.
- Nothing requires attention for long stretches without a payoff, and nothing punishes stepping away.
- Chill preset exists for players who want cozy only.

**15.9 Co-op (optional).** Shared facilities with owner and trusted roles; per-player Journal, Know-How and tolerance.

---

## 16. Asset manifest

Everything below is generated as a placeholder first and tracked in `ASSETS.md` with status (placeholder or final) and replacement instructions.

**Blocks.** Clay Pot, Planter Bed, Large Grow Tray, Dewloam, Enriched Dewloam, Compost Bin, Worm Bin, Trim Station, Drying Rack, Jar Shelf, Curing Jar, Rolling Table, Apothecary Still, Hand Mixing Bench, Herbalist's Bench, Contract Board, Market Board, Grow Monitor, Bee Screen, Bee Hutch, Ladybug Hutch, Glow Mushroom Terrarium, Display Case, Trophy Shelf, Reserve Shelf, framed Greenhouse Glass Panes, Bulb Lamp, UV Tube Lamp, Full-Spectrum Panel, Amethyst Array, Lamp Timer, Drip Tray, Hygrometer Alarm, Hand Dynamo, Reservoir Tank, Pump, Reed-and-Copper Pipe, Drip Emitter, Mixing Station, Nutrient Tanks (3 colors), Water Wheel, Solar Panel, Battery Bank, Biogas Digester, Copper Wire, Grow Room Controller, Humidifier, Dehumidifier, Fan, Cooling Coil, Vent/Duct, Sensor Probe, Cultivator Rail, Dock, Room Gate, Filter, Auto-Trimmer, Burp Valve, Pollen Collector, Seed Sequencer, Cross-Breeder, Seed Vault, Mutation Chamber, Control Console, Display Panel, Routine Rack, Sprite Perch, Export Port, Dewstone crystal and ore, Dewstone Generator, Legacy Pedestal, glow vines and mushrooms.

**Items.** Wild Seed, Dusty Seed Packet, Strain Seed Packet, Watering Cans (3 tiers), Pocket Meter, Loupes (3 tiers), Clip Hygrometer, Sprout Tonic, Growth Mix, Bloom Booster, Mold Spray, Neem Soap, Sticky Trap, Revival Tonic, Drainage Grit, Mutagen Dew, Shears (4 tiers), Resin Gloves, Pollen Brush, Pollen Vial, Wet Cluster, Dried Bud, Cured Bud, Trimmed Bud, Sugar Leaf Trim, Kief Sift, Pressed Resin, Rolling Paper, Joint, Pipe, Edibles (brownie, cookie, gummy, toffee), Tincture, Calm Tea, Tolerance Break Tea, Glow Cell, Strain Card, Strain Journal, Journal Pages (15), Grow Recipe Card, Routine Card, Pager, Blueprint, Dew Coin, Ladybug Jar, Terpene Honey, Season Rosettes, Ribbons.

**Entities and NPCs.** Trolley, Dew Sprite, Dew Moth, Green Hermit, Brisk Barrow, Judge Thistlewick, Herbalist villager profession.

**Models and animation.** Plants: 4 stages x 3 habits with tint channels (leaf, bud, hair), frost overlay, emissive layer, and state variants (droop, curl, pale, burn, mold, mites). Drying bundle states (3), jar fill states (5), tray models (pot, bed, large), lamp with chain and beam, first-person arms for can, shears, jar, loupe, pipe, dropper.

**UI textures.** Tooltip panel, Journal book, Trim GUI, Controller GUI, Routine Card art, dashboard widgets, toast frames, Next Goal widget, an icon set of about 60 icons (water, light, nutrients, health, terpene wisps, tier badges, status lights).

**Particles and sounds.** See sections 14.3 and 14.4. **Music.** See 14.5.

**Data and text.** Datapack JSON for terpenes, pigments, nutrients, effect maps, events, contracts, recipes, heirloom strains, lore pages; `en_us` and `en_us_herbal` language files.

---

## 17. Balance sheet (starting values)

| System | Starting value `[TUNE]` |
| --- | --- |
| Day length | 24000 ticks |
| Seed to ripe (baseline, Grower) | about 3 in-game days (60 min real) |
| Dry time | 1.0 in-game day |
| Cure | 3 good burps for Cured; 10 days for Aged |
| Cluster to bud ratio | 1 cluster = 2 buds |
| Clusters per plant | 2-9 (gene dependent) |
| Rank XP to next rank | `60 * rank^1.35` (about 75,000 XP total to Rank 30) |
| Dew XP examples | stage-up 3, burp 3, harvest 20, trim cluster 4 plus bonus, strain discovery 25, Journal Page 40, contract 50-300 |
| Dew Coin examples | Tin Can 8, standard contract 40-120, rush 150-300, rare seed 250 |
| Mutation chance per allele | 4% (12% with Mutagen Dew) |
| Tolerance gain per use | 12% (preset scaled), decay 1% per in-game hour |
| Effect duration | `60 s + 20 s * POT`, modified by item type and tolerance |
| Problem grace period | 1 in-game day before real penalties |
| Event cap | 1 negative event per in-game day |
| Room volume cap | 2000 blocks |
| Dew Sprite cap | 8 |

---

## 18. Testing and QA

**Unit tests.** Genetics (allele distribution over 10,000 crosses within tolerance, mutation rates, stabilization detection), quality formulas, Vigor curves, tolerance math, name generation determinism, save migrations.

**Game tests (headless).** Room sealing and invalidation, lazy simulation equivalence (one big catch-up vs many small ticks within 1%), pipe and rail graph rebuilds, power balance, contract generation never being impossible.

**Performance test.** A debug command spawns 500 plants in 20 rooms and reports average and worst-case tick cost; must meet the budget in section 1.5.

**Multiplayer test.** Two clients: independent Journals and tolerance, shared facility permissions, no desyncs on tooltips.

**Fun tests (human).**

- 15-minute blind playtest after P3 (the Fun Gate): can a new player grow and cure a batch without reading anything?
- Boredom log: a debug counter records repeated identical actions; any loop over 90 seconds with no decision or feedback is a bug.
- Near-miss check: every quality tier boundary result screen names the factor that cost the most points.
- Each phase ends with a Playtest Checklist of 5-10 items from the developer.

---

## 19. Roadmap

| Phase | Deliverable | Done when |
| --- | --- | --- |
| P0 Setup | Gradle project, registries, config framework, debug command skeleton, placeholder asset generator, datapack loaders, CI build | `runClient` boots with a creative tab |
| P1 Plant core | Tray block entity (pot, planter), PlantState, 4 stages with placeholder models, watering can, Bulb Lamp with Glow Cell, tooltip like the reference, lazy simulation, seed with stub genome | Seed to ripe with care; tooltip matches the reference |
| P2 Environment | Lume model, lamp hang height, Lamp Timer (basic), humidity and temperature sources, Pocket Meter, Grow Monitor, Vigor, problems with telegraphs and cures, basic bee pollination | Every problem is visible, explainable and curable |
| P3 Process loop | Harvest snip, Trim minigame, drying, curing jars, quality system with near-miss readout, basic Journal, Rank and Dew XP, Next Goal widget | **FUN GATE:** the full manual loop is playable and fun |
| A1 Power and plumbing | Glow Cell to wired power, Hand Dynamo, Water Wheel, Solar, Battery, Biogas, Drip Tray, Reservoir, Pump, Pipes, Mixing Station, Know-How system, Rank gating | A fully watered and fed room with no hands |
| P4 Consumables | Rolling Table, Joint, Pipe, edibles, tinctures, terpene effects and combos, tolerance, Too Cozy, Herbal Mode | Effects and tolerance work in multiplayer |
| P5 Genetics | Full genome, inheritance, mutation, Loupe, naming, Stable and Registered, Pollen Vials, lineage tree, Heirloom data | A controlled cross yields predictable stats |
| A2 Climate Controller | Room detection, actuators, Grow Recipes, live graph | One Controller runs a room from a recipe |
| A3 Trays and rails | Large trays, Cultivator Rails, Trolleys, Docks, Filters, Auto-Trimmer, Drying Gallery, Curing Cellar | A tray travels seed to jar unattended |
| A4 Breeding Lab | Sequencer, Cross-Breeder, Seed Vault, Mutation Chamber, Pollen Collector | A goal card delivers a target strain |
| A5 Control Room | Console, Panels, Routine Rack, Pager, Dew Sprites, Export Port | A routine saves a batch while you are away |
| P6 World and story | Hollow biome, structures, Journal Pages, NPCs, contracts, Market Board, Seasons, events, Strain Show | A new player can follow the story trail |
| P6b Heritage | Valley Greenhouse wings, Mother Strain, finale cinematic, Legacy with bonuses | Complete a Legacy loop |
| P7 Polish | Camera moments, animations, particles, sound layers, music, atmosphere, UI polish, accessibility | Everything feels juicy and passes the accessibility list |
| P8 Balance and release | Pacing pass against section 9.9, performance, compat (Jade, JEI), save migration, docs, bug pass | Targets met; no known crashers |
| P9 Stretch | Blueprints, Gene Capsules, co-op market, extra challenge modes | Optional |

---

## 20. Risks and cut-lines

**Risks and mitigations.**

- **Plant model explosion.** Use one base model per (stage, habit) tinted by vertex colors, not hundreds of models.
- **Trim minigame and camera jank.** Build the minigame as a GUI screen first (reliable), and add the world camera polish later. Fallback is a screen-only minigame.
- **Room detection edge cases.** Hard cap, throttled invalidation, and a manual “Define Room” corner wand as fallback.
- **Trolley sync cost.** Server sends start, end and timing only; the client interpolates along the rail.
- **Bee pollen memory.** Use data attachments if available; otherwise fall back to a proximity check.
- **Scope creep.** Phase gates and the Fun Gate exist to stop it.
- **Platform content rules.** Herbal Mode and toggles for smoke particles and effects.
- **Balance complexity.** Everything data-driven plus the `timewarp` and `knowhow` debug commands.

**Cut order if the project gets too big (first to go on the left):** co-op market, Blueprints, Dew Sprites, Mutation Chamber, Seasons, Strain Shows, extra camera cinematics (keep the trim and harvest moments), automatic Cross-Breeder runs (keep the Sequencer and manual breeding), Legacy extras (keep a basic Legacy).

**Never cut:** the grow, trim, dry and cure loop, basic genetics, Journal, automation T1-T3, the Hollow structures and the Next Goal widget.

---

## 21. Kickoff instructions

Your first reply must follow this template and nothing else:

1. **Understanding:** 5 bullets confirming what you will build and the tone.
2. **Technical plan:** loader, version, package layout, key classes.
3. **Day-one decisions:** confirm each of the eight items in section 1.4, noting any risk.
4. **Roadmap:** confirm or adjust section 19, with rough effort per phase.
5. **Risks and up to 3 questions** (Minecraft version and loader if not specified, otherwise defaults).

Then wait for my go-ahead.

**Definition of Done for every phase:** compiles cleanly; `runClient` launches; tests pass; `DESIGN_DECISIONS.md`, `CHANGELOG.md` and `ASSETS.md` updated; a Playtest Checklist of 5-10 items; a list of remaining placeholders; a proposal for the next phase.

**Playtest report format (for me to reply with):** What felt great, what felt tedious, what confused me, what broke, one thing I wanted that wasn't there.

---

# PART II: THE DIRECTIVE LAYER

*Added after the tone pivot. Part I stays the sim backbone (plants, genetics, processing, machines, tiers). Part II adds the mystery, the stakes and the structure that stops the loop from feeling empty or repetitive. **Where Part II conflicts with sections 2, 4, 9, 12 or 15, Part II wins.***

---

## 22. The pivot: an unsettling-cozy directive sim

**22.1 The feeling in one line.** *You always know what to do next, but you never fully know what is going on.* The formula: **Clear Task + Hidden Truth + Rising Stakes + Tactile Process + Variation.** The cozy surface from Part I stays (warm lamps, soft music, satisfying verbs). Underneath it, something is slightly wrong, and the player is slowly and voluntarily drawn toward finding out what.

**22.2 What we borrow (structure, never content; everything here is original).**

| Reference | Why it hooks | Stonedew version |
| --- | --- | --- |
| Lethal Company | A quota with a deadline, shifting conditions each run, a gear shop, risk versus greed, dread with dark humor | Quota Cycles, Hollow Weather, Dewline Catalog, Heart Attention meter |
| No, I'm Not a Human | Nightly visitors, hidden rules, deciding who to trust from their tells | Night Visitors, House Rules, tells and responses |
| Cash Cleaner Simulator | A tactile multi-step process chain, a faceless employer, escalating machinery, upgrades that change the workflow | The Ledger, the Collection Hatch, the grow-to-jar chain, automation tiers |
| Rule-mystery games like Don't Pick Up | An odd world with unexplained rules that you learn by observing and testing | House Rules, Mystery Board, verifying and busting myths |

**22.3 New pillars (appended to section 2).**

7. **Directive clarity.** The HUD always shows what to do now, in one concrete line.
8. **Curiosity debt.** At all times at least two open questions are pulling at the player.
9. **Escalation by transformation.** Each tier changes what the job is, not just how big it is.
10. **Nothing is a dead end.** Every item and machine has at least two uses and one story hook.
11. **Unease, never cruelty.** Dread is atmosphere. No jump scares by default, no permadeath, no lost progress.

**22.4 Anti-goals added.** No lore dumps. No clue that blocks progress. No question answered without raising a smaller one. No fake mystery without a payoff.

---

## 23. The Shift Cycle (the new macro structure)

Each in-game day is a **Shift**. A **Cycle** is 3 Shifts, which is about one batch of growing and about 60 minutes of real time on Grower preset `[TUNE]`. This replaces the loose macro loop in section 4.

| Phase | Time (hours after dawn) | What happens | Player focus |
| --- | --- | --- | --- |
| Dawn Briefing | 0-2 | The Ledger prints the Directive Sheet: today's orders, the Hollow Weather forecast, rule reminders | Plan |
| Day Shift | 2-14 | Grow, process, build, forage | Work and mastery |
| Dusk Delivery | 14-16 | The Collection Hatch opens for one in-game hour; deliver orders | Payoff |
| Night Watch | 16-24 | Anomalies, visitors, optional Hollow Runs, mystery time. Sleeping skips to dawn, but some events catch you sleeping | Curiosity and risk |

**23.1 The Cycle Quota.** Every Cycle the Ledger issues **3 Orders plus 1 Wildcard** (early Cycles have only 1-2 Orders). Orders are concrete: strain traits, quality tier, quantity. The **Wildcard** is a strange request (“A jar that smells like rain”) tied to an active Mystery Thread. Every order has three levels: **Bronze** (required to avoid a Shortfall), **Silver**, **Gold** (bonus rewards).

**23.2 Soft failure.** Missing Bronze creates a **Shortfall**: next Cycle's Orders are a little larger and the Heart becomes **Hungry** (slightly more anomalies, but better Wildcard rewards). Never a game over. Chill preset removes Shortfall penalties entirely.

**23.3 Cycle Report.** At the end of each Cycle the Ledger prints totals, your best quality, an odd observation about your habits (“The Ledger notes a preference for violet. Curious.”), a new piece of Mail, and the next unlock. Each Cycle ends with a small beat of reflection and a hook into the next.

---

## 24. The Ledger and the Employer

**24.1 The Ledger** is a brass-and-dewstone terminal block with a softly glowing screen of dew-stained paper. Pages: **Directives, Orders, Catalog, Mail, Rules, Annex Map, Standing.** It is the diegetic home of almost all UI that is not in the world.

**24.2 Voice.** The Ledger speaks in polite bureaucratic language that slowly cracks. Four voice stages driven by Standing and Heart Attention: **Formal, Familiar, Strained, Candid.** All lines are lang-file strings, never hardcoded.

**24.3 Standing (0-100).** The Collector's regard for you. Unlocks Catalog tiers, Mail chains and access to deeper Mystery Threads. Rises with Orders (Silver and Gold count more) and verified House Rules.

**24.4 Dewline Catalog (the shop).** Tools, seeds, machine blueprints and decor, paid in Dew Coins and gated by Standing. Items carry deadpan flavor text. **Surplus Crates** give variable rewards (transparent odds shown on the crate, never real-money) as a gentle gambling-style hook. A Daily Special rotates.

**24.5 The hidden truth** about who writes the Ledger is Thread 3 in section 26.

---

## 25. Directives: always know what to do

The **Directive Engine** keeps a stack on the HUD (the Next Goal widget from section 2 becomes this):

- **Primary:** the current Order or story Directive. Always exactly one line, verb first, measurable.
- **Facility:** the best improvement right now (the Bottleneck Spotlight pick).
- **Curiosity (`?`):** one open mystery question with a location hint.

**Phrasing rules.** Concrete, verb-first, one line, never “explore” without a place to go. Examples by Rank:

- Rank 1: “Plant the Wild Sprout. Water it. Await growth.”
- Rank 2: “Order 1: four Common buds. Deliver at dusk.”
- Rank 3 (`?`): “The Hatch is warm. Find out why.”
- Rank 5: “Humidity in the Nursery is 12% high. Run a fan.”
- Rank 8 (`?`): “The lamps hummed a pattern at midnight. Write it down.”

The stack never leaves the player without a next step, and the `?` line is how curiosity is steered without a quest log.

---

## 26. Mystery architecture (the Breadcrumb Engine)

**26.1 Principles.** Show before tell. Every answer raises a smaller question. At least two questions are always open. Clue density is roughly one per 10-15 minutes. Clues never gate the sim path. Every Thread completion pays out something tangible (a recipe, machine variant, cosmetic, or Wing access), not only text.

**26.2 Four clue types.**

| Type | Meaning | Examples |
| --- | --- | --- |
| Observe | Notice something odd in the world | Plants lean toward the Hatch; a lamp hums a pattern |
| Document | Find or read text or audio | Journal Pages, cassette logs, Ledger Mail, margin notes |
| Experiment | Test an idea | Break a House Rule; deliver a strange jar; use a Tuning Fork |
| Reveal | A moment that reframes things | The Hatch pipe leads somewhere; the Ledger addresses you by name |

**26.3 Mystery Board.** A Journal tab that works like a corkboard. Clues you find are pinned automatically. When three related clues exist, the Board offers a **Connect** action; clicking it starts a short **Revelation beat** (a line of text, a sound, a small world change). It is a light deduction moment, never a puzzle chore.

**26.4 The seven Threads (plus one hidden).**

| Thread | Question | Clue beats | Payoff |
| --- | --- | --- | --- |
| 1. The Hatch | Who collects the deliveries? | Hatch is warm; a pressed moth appears after payments; one unordered item in every payment; scratches inside from the far side; a pipe runs to the Heart Chamber | Hatch upgrades, **Return Slot** (send gifts back) |
| 2. The Hum | Why do lamps hum in patterns? | Hum pitch follows your Attention; a cassette with the same rhythm; a Circle cipher; Tuning Fork recipe; the hum answers back | Controllable Lamp Murmur, Resonant Lamp tier |
| 3. The Ledger | Who writes it? | Handwriting changes; entries dated before you arrived; margin notes signed K-6; the ink is dew; a last page addressed to you | Candid voice, Standing perks |
| 4. The Circle's Fate | What happened to the Circle? | Part I lore: Journal Pages 1-15 | Valley Greenhouse access |
| 5. The Dew | What is the Dew? | Dew pools show other rooms; moths follow it; samples move under the Loupe; it grows faster near sleepers; threads in Dewloam | **Spore Wing** unlock |
| 6. Fen | What does the Hermit want? | He never sleeps; his lantern burns without oil; a tally of Keepers; he apologizes at odd moments; he asks you to name a strain after someone | Hermit's Lantern (reveals visitor tells) |
| 7. The Mother | What does the Heart want? | Order terpene requests spell a pattern; Hungry reactions to certain strains; the Founders' lines carry its memories | The three endings (below) |
| 8. The Other Keepers (hidden) | Were you the first? | Initials K-1 to K-6 carved into beams; six hidden **Keeper's Caches**, each with a mini-story and a unique tool | Keeper's Coat, secret ending branch |

**26.5 Three endings** (chosen at the Mother, each becomes a Legacy path that changes the next run's House Rules and tone): **Feed** (Tithe path: huge output, the Heart consumes more), **Seal** (Fen's path: peace, the valley recovers slowly), **Free** (the Heart wakes; the expansion Wings open, section 35).

---

## 27. House Rules (the hidden-rule system)

Each facility gets a **Rule Card** pinned beside the Ledger with 8 rules drawn from a pool of 24. Some are true, some are false (default 5 true, 3 false, `[TUNE]`). The player learns which by observing and testing. The Journal tracks each as **Unverified, Verified, or Busted**. Verifying or busting a rule gives Dew XP and Standing. Consequences are mild and flavorful, never catastrophic.

| Rule text | Truth | If broken or tested | Tell |
| --- | --- | --- | --- |
| Water only before the second bell | True | Night watering sours the dew: Vigor penalty until dawn | Tooltip shows a violet “sour” tag |
| Never trim beneath a violet lamp | False | Nothing bad; secretly widens the Flow window 10% | Trim feels easier |
| If the Hatch is warm, do not open it | True | Delivery taken early, the Order slips one Shift | Warm glow on the hatch seams |
| Count the jars twice | True | Once per Cycle a jar goes missing (the Tithe); counting at the Ledger saves it | Jar count off by one |
| Do not answer the Pager after the third bell | True on visitor nights | The caller is a Mimic; you lose the night's events | Pager chimes the wrong note |
| Leave one lamp burning in the Nursery | True | A fully dark Nursery attracts mites at night | Faint skittering sound |
| Moths bring bad luck | False | Moths improve Hatch Returns | Moths gather near good drops |
| Names are heard | True | Naming a strain adds Attention | The Ledger remarks on the name |
| Fen sleeps at noon | False | He is simply never asleep | His lantern never dims |
| The jars hum when the Heart is hungry | True | Cure jars hum before a Shortfall | Low murmur from the shelf |
| Do not run in the Annex | True | Sprinting in Annex runs draws Wanderers | Dust falls from the ceiling |
| The Ledger is always right | False | It occasionally lies (Thread 3) | Forecast misses 20% of the time |

House Rules re-roll on Legacy so replay stays fresh. They are datapack JSON, so new rules are easy to add.

---

## 28. Hollow Weather and anomalies (the variation engine)

Each Shift can carry one **anomaly** (max 1 per day, max 2 per week in Chill). The Ledger forecasts it at Dawn but is right only about 80% of the time. Every anomaly has a 10-20 s telegraph, a counterplay option, and a reward or clue, so none are pure punishment.

| Anomaly | Telegraph | Effect | Counterplay | Reward or clue |
| --- | --- | --- | --- | --- |
| Still Air | Mist stops moving | No airflow; mold risk up | Fans, vents | Safety streak bonus |
| Lamp Murmur | Lamps hum a pattern | Cosmetic dread | Write it down or use a Tuning Fork | Hum thread clue |
| Dew Tide | Dew pools glow | Plants +20% growth, soil dries faster | Extra watering | Dew Samples |
| Sporefall | Drifting spores | Harmless | Collect with a jar | Spore Dust (Spore Wing seed) |
| Blackout | Lights sag | Power off 5 min | Hand Dynamo, batteries | First lantern achievement |
| Quiet Night | Everything softens | No events | Rest and tinker | Hermit visits |
| Mirror Dew | A pool shows another room | Cosmetic | Look closely | Reveals a hidden location |
| Long Shadows | Beams cast odd shadows | Cosmetic | Follow the shadows | Opens a hidden compartment |
| Warm Hatch | The Hatch glows | A special Order arrives | Deliver it | Rare reward |
| The Count | Jar count is off | One jar taken | Count twice | Moth Silk |

---

## 29. Night Visitors (Dusk Callers)

Some nights a visitor knocks. Each has **tells** (sound, lamp color, a detail). Players choose to open, ignore or respond. The Hermit's Lantern (Thread 6) reveals a visitor's true nature. Outcomes are mild and informative, never a wipe.

| Visitor | Tell | Wants | Right response | Reward | Wrong response |
| --- | --- | --- | --- | --- | --- |
| The Courier | Three polite knocks, brass bell | To collect an Order early | Hand over the Order | Standing and a rare seed | Order delayed one Shift |
| The Inspector | Clipboard scratch, cold draft | To grade the facility | Let in with all lamps on | Grade A-D; A gives a perk | Lamps off gives a Grade D hint |
| Brisk Barrow | Cheerful whistle, a ribboned lantern | A trade or bet | Accept one trade, decline the sample | Rare seed or winnings | Mites or a lost bet |
| The Hollow Stranger | Knock with no footsteps, a teal lamp | Warmth; mimics something you recently made | Do not open; leave a jar on the step | Dew Sample and a clue | A night of lamp flicker, one spoiled jar |
| The Quiet Tenant | A second set of footsteps, the Ledger types by itself | To be acknowledged | Say nothing, leave a lantern at the Hatch | A Keeper's Cache location | Confronting costs a lamp hour |
| The Moth Choir | Moths on the glass, a soft chime | Light | Switch off the nearest lamp for an hour | Moth Silk and a Hum clue | Keeping lamps on dips growth 5% that night |

---

## 30. Heart Attention (the greed versus risk meter)

Each facility has an **Attention** value (0-100): how closely the Heart is watching you. It is the Lethal-Company-style dial between playing safe and pushing for more.

| Level | Range | Effects |
| --- | --- | --- |
| Quiet | 0-25 | Fewer anomalies, mild Wildcards, Ledger Formal, baseline rewards |
| Noticed | 26-50 | Hatch Returns +10%, normal anomalies, Mail gets personal |
| Watched | 51-75 | Rewards +25%, anomalies x1.5, Orders +20%, trickier visitors, Ledger Strained |
| Called | 76-100 | A unique event chain (“The Calling”), rewards +40%, frequent Mimic nights, Ledger Candid |

**Gain per Cycle** `= 2 + 0.02 * buds delivered + 3 per Legendary + 5 per newly named strain + 4 per tier unlocked` `[TUNE]`. **Decay:** about -4 per Cycle. **Quiet Offerings** lower it: returning a jar through the Return Slot (-6), a lights-out night (-3), a Quiet Hour at the Hatch (-2).

The player chooses a style: **Quiet Keeper** (safe, steady) or **Greedy Keeper** (more reward and more strangeness). Nothing is ever destroyed or lost, only the dial of weirdness moves. UI is subtle: an eye icon in the Ledger, lamp hum pitch that rises with Attention, and a “Hum” reading on the Pocket Meter.

---

## 31. Machines remember (automation with mystery)

Automation must not delete the mystery; it multiplies **observation**.

- Every machine has a **Log tab** (diagnostics plus flavor, with rare anomalies). The Trolley logs a “Stop 13” that does not exist. The Auto-Trimmer counts more scrap than you fed it. The Sequencer shows one gene that maps to nothing. A pre-existing **Keeper Routine** sits in the Routine Rack: “IF Night THEN Open Hatch”.
- Each tier's blueprint is **inherited** from a previous Keeper. You restore, not invent, and each unlock comes with a short **Keeper's installation note** (one lore beat).
- Dashboards show **data anomalies** (a graph that dips at the same hour each night).
- Automation raises Attention (section 30), so scaling up has a built-in cost-benefit decision.

---

## 32. The Soul Checklist (anti-repetition and meaning toolkit)

These are binding design rules, each with a QA test.

| # | Rule | Implementation | Test |
| --- | --- | --- | --- |
| 1 | Every batch changes something visible | Facility Memory (section 33) | After 3 Cycles the room looks different |
| 2 | Every repetition has a variable | Strain, Order, anomaly, season, rule, visitor | Variation Budget below |
| 3 | Skill expression in the repeated action | Flow trims, burp timing, lamp height | A good player scores clearly higher |
| 4 | Chores become choices | Automation replaces repetition with new decisions | Each tier adds one decision |
| 5 | Orders are stories | Each Order has a client voice and a one-line reason | Orders read as people, not numbers |
| 6 | Curiosity pacing | At least 2 open questions at all times | Debug check on Mystery Board |
| 7 | Variable rewards | Hatch Returns, Surplus Crates, Wildcards, mutations | No two Cycles pay out the same |
| 8 | A sense of completeness | Completion Tracker and Annex Map silhouettes | Player can see what exists and how far they are |
| 9 | No dead-end items | Every item has 2+ uses and 1 story hook | Dead-End Audit list passes |
| 10 | Reactivity | Ledger, Hermit and visitors comment on your habits | Check 10 distinct reactive lines per Cycle |
| 11 | Rhythm of surprise | At least one non-routine moment every 3 Shifts | Event log shows no long flat stretches |
| 12 | Every Cycle ends with a hook | Cycle Report plus a pinned question | A new `?` is open at every Cycle end |

**Variation Budget.** No two consecutive Cycles may share more than 3 of: strain, Order type, anomaly, season, visitor, rule test. The Directive Engine biases the next Cycle's Wildcard and anomaly picks to respect this.

---

## 33. Facility Memory and completeness

The cave remembers what you do. These are persistent, visible changes (data-driven, each a small cosmetic block-state or decoration):

- Cycle 5: moths begin roosting under the lamps.
- First Legendary: one lamp turns gold and stays that way.
- First named strain: a nameplate appears on the jar shelf.
- Rank 5: you carve your initials into a beam as **K-7**, joining the other Keepers.
- Each cleared Thread adds a physical object to the Keeper's Desk (a moth in wax, a cassette, a lantern).
- Walls slowly grow glow moss near long-running rooms; machines gain patina and chain wear.

**Completion Tracker.** The Annex Map and Almanac show grayed silhouettes for undiscovered rooms, strains, rules, threads and Wings, with a percentage. The player can always see how much exists, which is the antidote to a game that feels unfinished.

**Dead-End Audit.** `ASSETS.md` gets a column listing each item's two uses and its story hook. Anything missing one is a bug.

---

## 34. Web of systems (everything touches something)

| System | Connects to |
| --- | --- |
| Trim and stems | Edibles, Resin Press, Biogas power, compost soil, “scrap count” clues |
| Dew | Growth bonus, power (Dewstone Generator), lore (Thread 5), Spore Wing |
| Moths | Light attraction, Hatch Returns, Moth Choir visitor, Hum clues |
| Pager | Alerts, Mimic nights, Routine actions |
| Bees | Pollination, honey, cross-breeding, Apiary Wing |
| Names | Strain Journal, Attention, Ledger reactions |
| Jars | Curing, vintage collection, the Tithe, Return Slot offerings |
| Lamps | Growth, heat, mood, the Hum cipher, visitor tells |

---

## 35. Expansion framework: Wings

**35.1 What a Wing is.** A self-contained expansion module that plugs into the same engine: a new organism class, a new process chain, a new mystery thread, new anomalies and rules, new machines, and new catalog items. Wings ship as in-mod modules with a config toggle, or as separate add-ons that use the same API.

**35.2 Wing manifest (`stonedew:wings/<id>.json`).** Fields: id; unlock conditions (thread, flag, rank); cultivar types; gene schema; environment profile; process chain steps; machines; order templates; anomaly set; House Rules; clues and threads; Ledger Catalog entries; lang files; assets; version compatibility.

**35.3 Planned Wings.**

| Wing | Organism or theme | Sim texture | Mystery tie |
| --- | --- | --- | --- |
| Spore Wing | Mushrooms | Dark, damp, slow colonization, repeating fruiting flushes, contamination risk | Thread 5: the Dew is one organism |
| Prism Wing | Prismatic Dew (psychedelic-style fictional compound) | Light-splitting machines, color-fraction crafting, a lucid sight layer | Threads 2 and 8: hidden echoes and the Hum |
| Apiary Wing | Bees and moths | Hive management, flavored honey, swarm logistics | Moth Choir |
| Alchemy Wing | Tinctures and elixirs | Minigame crafting, recipes that combine terpene lines | Quill's unfinished experiment |
| Deep Wing / Heart Chamber | The Heart itself | A multi-stage ritual puzzle, endings | Threads 1, 7 |
| Exotic Flora Wing (stretch) | Night-blooming and weather-driven plants | Weather and moon cycles | Dew Seasons |

**35.4 Spore Wing (flagship example).**

- **Verbs:** mix Substrate, inoculate Trays with Spore Prints, wait through **Colonization** (0-100%), then **Fruit** in repeating **flushes** (1-3 harvests per tray). Needs darkness, high humidity and stillness, the opposite of plants.
- **Genes:** Colonization Speed, Flush Count, Cap Color, Potency, Spore Load, Bioluminescence.
- **Machines:** Substrate Mixer, Steam Sterilizer, Colonization Rack, Fruiting Chamber, **Mycelial Mesh** (a network linking trays that shares humidity and nutrients and quietly displays nodes you never placed).
- **Risks:** Contamination (gentle, localized, cleanable).
- **Effect lines (fictional):** Rootsight (briefly sense ore and hidden containers), Hush (muffled sound, calm), Spore Sense (detect nearby clues).
- **Mystery payoff:** the facility is one living network; the Heart can “see” through the Mesh.

**35.5 Prism Wing (fictional psychedelic layer).**

- **Verbs:** split Prismatic Dew with **Refractors** and **Prism Lenses** at a **Spectrum Bench** into three color fractions, then recombine in recipes.
- **Prism Sight:** a timed, opt-in status that shifts the color palette and reveals **Echo Marks** (hidden clues and secret doors). Hallucinated figures are harmless clue-givers. Duration capped, intensity slider, no flashing, can be disabled.
- **Safety and scope:** entirely gamified and fictional, with no real-world chemistry or procedures. Herbal Mode renames it “Vision Dew” with a magical-tea theme.
- **Mystery payoff:** some Rule truths and Keeper echoes can only be confirmed under Prism Sight.

**35.6 Cadence.** One Wing per major update. Each Wing adds one Thread, one anomaly pack, 4-6 House Rules, 8-12 machines or items, and an Order template set, so a Wing refreshes the whole loop instead of bolting on an island.

---

## 36. Technical: the story engine and new day-one decisions

**Add to section 1.4 (confirm in your first reply).**

9. **Cultivar abstraction.** Do not hardcode “Plant”. Use a `Cultivar` interface (types: PLANT now, FUNGUS later) with pluggable gene schema, environment profile, process chain and effect map.
10. **Wing registry.** Wings register through a manifest and a loader. The base game is itself the first Wing.
11. **Event bus.** Gameplay events (harvest, delivery, rank-up, strain discovered, machine placed, time of day, near-block) are published on a bus that the story engine subscribes to.
12. **Story state.** Per-world saved data: flags, discovered clues, thread progress, verified rules, Attention, Standing, Keeper count. Versioned and migratable.
13. **Data-driven narrative.** Clues, directives, orders, anomalies, visitors, rules and endings are JSON. No story text in code; all text is lang strings.

**Examples (illustrative schemas).**

```json
{
  "id": "stonedew:clue/hatch_warm",
  "thread": "stonedew:hatch",
  "type": "observe",
  "trigger": { "event": "stonedew:near_block", "block": "stonedew:collection_hatch", "when": "hatch_warm" },
  "once": true,
  "board_text": "clue.hatch_warm",
  "raises": ["stonedew:q/hatch_who"],
  "grants": { "dew_xp": 15, "flag": "hatch_warm_seen" }
}
```

```json
{
  "id": "stonedew:directive/hatch_curiosity",
  "slot": "curiosity",
  "text": "directive.hatch_warm",
  "show_when": { "flag": "hatch_warm_seen", "not_flag": "hatch_pipe_found" },
  "hint_pos": "stonedew:collection_hatch"
}
```

---

## 37. Revised progression map (Cycles)

One Cycle is about 60 minutes at Grower pace, so Legacy lands around Cycle 40 `[TUNE]`. This table aligns the mystery with Rank and tier unlocks from Part I.

| Cycles | Mystery beat | New verb | Tier |
| --- | --- | --- | --- |
| 1 | First Ledger contact; the Hatch is warm; first delivery | Deliver at dusk | T0 |
| 2-3 | First anomaly; first rule verified; Mystery Board opens | Hand trim, read the forecast | T0 to T1 |
| 4-6 | First Night Visitor; carve K-7; the Hum begins | Respond to tells | T1 |
| 7-10 | Attention meter appears; Fen opens up; Spore hint | Choose Quiet or Greedy | T2 |
| 11-16 | Ledger voice strains; Keeper's Caches 1-3; first Heart reaction | Climate recipes, Hollow Runs (stretch) | T3 |
| 17-24 | Naming strains; the Tithe; trickier visitors; Dew thread | Rails, breeding | T4 to T5 |
| 25-32 | Heart Chamber glimpsed; Keepers 4-6 | Routines, Sprites | T6 |
| 33-40 | Greenhouse restoration; the Mother; ending choice | Legacy | T7 |
| Legacy | New rule set per ending; Wings unlock by path | Wing verbs | all |

Rule: a **new verb or new mystery beat arrives at least every hour of play**.

---

## 38. Tone controls and presentation

**Dread dial (config).** **Cozy** (no unsettling visuals, Ledger stays Formal, only friendly visitors), **Uneasy** (default, the full content with mild visuals), **Eerie** (more anomalies, darker lighting, Mimic nights, stronger audio). Separate sliders for visual wrongness and audio dread.

**Wrongness rules.** One thing is off at a time. The world is unreliable but fair: every strange rule is consistent once learned. No jump scares by default; the Eerie setting may add sudden sounds, and it can be turned off separately.

**Sound and look.** Tape hiss and low drones layered under the cozy music, a lamp that is a slightly wrong color, a mist that moves against the draft. Diegetic UI first (the Ledger, Rule Card, cassette player, Journal). Writing voice: deadpan, polite, specific.

**Safety.** No flashing, capped Prism effects, all intensity sliders, subtitles for every sound, and Herbal Mode retained for the consumable theme.

---

## 39. First hour script (revised with mystery hooks)

- **00:00** Wake on a cot in the cave. Lamp hum, a warm lantern, the Ledger glowing, a rusted Hatch that is warm to the touch. The Rule Card lists eight rules. Directive: “Plant the Wild Sprout. Water it. Await growth.”
- **02:00** Mail 1: “Welcome, Keeper. Your predecessor left in a hurry. Please disregard the scratches.”
- **03:00** Plant and water. First tooltip. A moth lands on the Ledger.
- **08:00** Stage-up sparkle. Mail: “Plants do not lean. Yours leaned. Note it.” The sprout visibly leans toward the Hatch. A `?` Directive appears: “The Hatch is warm. Find out why.”
- **15:00** Harvest snip, first hand trim. **Cycle 1 Orders accept dried (not cured) buds** so the first delivery lands inside the first hour.
- **Dusk** The Hatch opens, the buds vanish, payment appears with a pressed moth in wax. Standing +5, Rank 2, the Mystery Board opens with its first pinned clue.
- **Night** The Hermit appears at the door, says almost nothing, leaves a lantern for an hour. The Ledger prints: “The Ledger does not recognize this person.” Thread 6 begins.
- **Cycle 1 report (about 60 min)** “Output: 4 buds. Quality: Common. Note: the plant leaned.” A new `?`: “Why does the Hatch pay in moths?”

---

## 40. Roadmap deltas, Fun Gate and kickoff addendum

| Phase | Change from section 19 |
| --- | --- |
| P0 | Add Cultivar abstraction, event bus, story-state saved data, Wing registry skeleton |
| P1 | Add the Ledger stub (terminal block, first Directive); the Next Goal widget becomes the Directive stack |
| P2 | Add the Hollow Weather framework with two anomalies (Still Air, Dew Tide) |
| P3 | Add the Collection Hatch, Orders, Shift Cycle, Cycle Report and Standing; the Fun Gate is extended below |
| M1 (new, after A1) | Mystery Core: Mystery Board, Threads 1-3, 12 House Rules, Catalog, Surplus Crates |
| M2 (new, after A2) | Night Visitors (6), Attention meter, Machine Logs, Facility Memory |
| P6 | Merge with Threads 4-8, endings, Keeper's Caches |
| M3 (stretch) | Hollow Runs (short Annex expeditions with a lantern and limited light) |
| W1 (post-release) | Spore Wing |
| W2 | Prism Wing |
| W3+ | Apiary, Alchemy, Deep Wing |

**Extended Fun Gate (after P3).** A new player must (1) know what to do at every moment without outside help, (2) feel at least one `?` pull by minute 20, (3) finish Cycle 1 with a satisfying report and a hook, (4) have at least one “wait, what?” moment from the Hatch or Ledger, and (5) not feel that Cycles 2 and 3 are copies of Cycle 1.

**Cut order additions.** First to cut: Hollow Runs, Surplus Crates, visitor complexity. Never cut: the Ledger, Orders, Threads 1-3, House Rules, the Directive stack.

**Kickoff addendum (extends section 21).** Your first reply must also: (a) confirm you have read Part II, (b) confirm the new day-one decisions 9-13, (c) say where the Ledger, Hatch and Directive Engine land in P0-P3, (d) ask me for the default dread level and number of endings if unsure. Write no lore prose yourself beyond the clue beats; draft all Ledger, Mail and Directive text in a separate lang file in the voice from section 24.2 and keep it short.

---

# PART III: CONTENT BIBLE AND LOOSE ENDS

*Part II defined the systems. Part III writes the content those systems need so the developer is never left inventing story, rules or numbers. Everything here is data-driven source material for the JSON and lang files.*

---

## 41. Master map (what to read when)

| Part | Sections | Purpose | Use it for |
| --- | --- | --- | --- |
| I | 0-21 | The sim backbone: plants, genetics, processing, machines, tiers, UI, audio, roadmap | Building the core game |
| II | 22-40 | The directive layer: cycles, Ledger, mystery, rules, anomalies, visitors, Attention, Wings, story engine | Structure, stakes and curiosity |
| III | 41-50 | The content bible: Hatch, Catalog, Orders, rules pool, Ledger writing, Keepers, endings, Annex, Heart, integration | Filling the data and lang files |

Implementation order stays as in sections 19 and 40. Part III content is added phase by phase, never all at once.

---

## 42. The Collection Hatch, the Return Slot and the Catalog

**42.1 Hatch states.** **Dormant** (rusted plate, warm from day one), **Open** (the Dusk Delivery hour), **Warm** (glows at the seams: a special Order is waiting), **Quiet** (closed; accepts only Quiet Offerings). Delivery flow: interact to open a chute GUI, items slide in with a soft hiss, the Ledger confirms each (“Received.”), and after about 10 seconds payment appears.

**42.2 Returns (the item you never ordered).** Every payment includes Dew Coins plus one **Return** from this table (weights shift upward with Standing and Attention).

| Class | Weight | Examples |
| --- | --- | --- |
| Common | 50% | Pressed moth in wax (lore), seed packet, Glow Cell, compost bag |
| Uncommon | 30% | Recipe Card, Tolerance Break Tea, a cassette with a recording, Mutagen Dew |
| Rare | 15% | Heirloom seed, a Keeper's note, a lamp skin |
| Odd | 5% | A pocket watch that runs backward, a jar of dew that reflects another room, a postcard from the Annex, a key with no lock, a lantern wick that is still warm |

Odd items are collectible clues; each belongs to a Thread and pins itself to the Mystery Board.

**42.3 Hatch upgrades (Thread 1 payoff).** **Return Slot** (send one item back nightly), **Inspection Lamp** (see inside the Hatch), **Bell** (call the Collector early for a delivery), **Dumbwaiter** (T6: auto-delivery from the Export Port), **Window Pane** (peek through: more clues, more Attention).

**42.4 Return Slot.** Place one item in the slot at night. The next Shift the Heart reacts (section 49): affinity for that terpene or color grows, mood eases, and special Returns unlock at high affinity. Favorite items change over time, which gives the player something to learn.

**42.5 Catalog by Standing** (both Standing and Know-How must be met for blueprints).

| Standing | Catalog tier | Stock |
| --- | --- | --- |
| 0-19 | A: Basics | Dusty Seed Packet, Clay Pot, Tin Can, Bulb Lamp, Glow Cells, Rolling Paper, 4 Starter Jars, Pocket Meter |
| 20-39 | B | UV Tube Lamp, Planter Bed, Hand Dynamo, Loupe I, Steel Snips, nutrient base kit, Neem Soap, Clip Hygrometer, Cassette Player |
| 40-59 | C | Full-Spectrum Panel, Pump and Pipe kit, Tuning Fork, Copper Can, bulk Mold Spray, Display Case, Dewline Overalls (cosmetic) |
| 60-79 | D | Controller blueprint, Rail blueprint, Silver Micro-Snips, Loupe II, rotating rare seeds, Pager |
| 80-100 | E | Sequencer and Cross-Breeder blueprints, Console blueprint, Amethyst Array, rotating Heirloom seeds, Dew Sprite Lantern |

**Flavor text samples** (deadpan, one line, shown on the item): Tin Can: “Holds water. Has held other things.” Pocket Meter: “Measures what it can.” Cassette Player: “Play softly.” Tuning Fork: “Not for tuning.” Pager: “If it rings after the third bell, you did not hear it.” Dewline Overalls: “The previous owner kept them tidy.”

**42.6 Surplus Crates (variable-reward hook, transparent odds, never real money).**

| Crate | Price | Common | Uncommon | Rare | Notes |
| --- | --- | --- | --- | --- | --- |
| Dented Crate | 30 coins | 70% | 25% | 5% | Always in stock |
| Sealed Crate | 90 coins | 40% | 45% | 15% | Rotating stock |
| Hatch-Warm Crate | free | 0% | 60% | 40% | Appears only during a Warm Hatch; contains one Odd item |

Pity timer: 5 crates without a Rare guarantees at least an Uncommon on the next; 12 without a Rare guarantees a Rare. Odds are printed on the crate and in the Journal.

---

## 43. Orders: generator spec and the client roster

**43.1 Generator inputs.** The Journal (strains logged, best quality, terpenes and colors seen), current tier and estimated output per Cycle, Attention, Shortfall state, the Variation Budget (section 32), and active Threads.

**43.2 Order format.** `{ client, request, tiers: {bronze, silver, gold}, deadline (a Dusk Delivery), reward, flavor line, thread tag }`.

**43.3 Request types.** Count + Quality, Terpene, Color, Combo (terpene + color), Specific Strain Card, Vintage (cured N days), Mystery (Wildcard).

**43.4 Feasibility rule.** Bronze must be achievable at 85% of the player's estimated output using strains they already know. Silver needs good play (one quality tier higher or 50% more quantity). Gold needs mastery (both, or a client condition such as “burped at least five times”). Unknown traits are only requested by Wildcards, and always with a hint. A contract is never impossible.

**43.5 Rewards.** `Dew Coins = base * tierMult * (1 + AttentionBonus)`. Standing: Bronze +2, Silver +4, Gold +7. Gold completions also grant a small variable bonus (a Return upgrade or a Recipe Card).

**43.6 The client roster (12).** Each has a voice, so Orders read as people.

| Client | Voice | Typical request | Sample line |
| --- | --- | --- | --- |
| Mrs. Penhallow | Warm, rambling widow | Violet jar, any terpene | “He loved a violet one. Not too strong, dear.” |
| The Brass Brothers | Two merchants finishing each other's sentences | Large Count + Quality | “Forty buds, Fine or—” “—better. We are not fussy.” |
| Dr. Alder Quince | Precise, nervy apothecary | Exact terpene lines | “Linalool primary. Not myrcene. I cannot stress this.” |
| Marguerite of the Lantern Ridge Inn | Cheerful innkeeper | Hearty edibles and Hearth combos | “My guests eat well or they do not stay.” |
| Old Tamsin | Gentle, tired | Calm line for someone who sleeps badly | “Just something kind, please.” |
| The Surveyor | Terse, practical | Clarity for night work | “Night work. Pinene. Do not be late.” |
| Pip and Poppy | Whimsical twins | Pink or two-tone, Whimsy line | “We want one that looks like a sunrise!” |
| Mr. Vane | Cold, demanding | Gold-or-nothing, high pay | “Prime. Cured. Registered. Thank you.” |
| Sister Wick | Quiet monastery steward | Vintage jars | “The older the better. Time is the ingredient.” |
| Hollis Reed | Nervous courier from the next valley | Rush orders | “I have until dawn. Please.” |
| The Collector's Agent | Ledger-like formal voice | Collector (Strain Cards) | “The Collector requests the following card.” |
| \[REDACTED\] | No name; blank signature | Wildcards only | “You will know which.” |

**43.7 Wildcard templates (10, each tied to a Thread).**

1. “A jar that smells like rain.” Pinene or Linalool primary, cured, Fine+. (Thread 7)
2. “Something your predecessor never managed.” A Luminescent or Black strain. (Thread 8)
3. “A strain named for someone who is gone.” Register and name a strain. (Threads 6, 7)
4. “Two jars, identical. One must be older.” Vintage pair. (Thread 1)
5. “Deliver it at the wrong hour.” Deliver during a Warm Hatch at night. (Rule 3 test)
6. “A bud that hums.” A jar cured while the Heart is Hungry. (Thread 2)
7. “The color of the Hatch's glow.” A teal pigment strain. (Thread 5)
8. “What you grew on your first day.” A descendant of your first Wild strain. (Thread 3)
9. “Leave one jar unsealed.” A Return Slot test. (Thread 1)
10. “Count them. Again.” Pass the Count. (Rule 4 test)

---

## 44. House Rules pool, part 2 (rules 13-24)

Together with section 27 this completes the pool of 24. Each world draws 8 (default 5 true, 3 false).

| # | Rule text | Truth | Effect | Tell |
| --- | --- | --- | --- | --- |
| 13 | Never harvest at midnight | True | Midnight clusters carry the Hush: drying time doubles | Clusters are cold to the touch |
| 14 | Whisper to your plants | False | Nothing; the Ledger logs “Noted.” Busting it grants a cosmetic Talkative Fern | Ledger remark |
| 15 | Salt the doorstep | True | Mimics cannot enter; costs 1 Salt per Shift | Salt lines scatter at night |
| 16 | Do not read the Ledger after midnight | True | After midnight the forecast is right only 50% of the time | The screen text drifts |
| 17 | Never cure under a full moon | False | Full-moon cures get +5% quality | Jars glow faintly |
| 18 | Keep your boots by the door | True | The **Boot Mat**: if boots are moved overnight, a visitor passed; a free clue | Boots slightly out of place |
| 19 | Do not count the moths | False | Counting at the Moth Tally board gives a clue | Moths cluster in groups of three |
| 20 | The third lamp is the honest one | True | The third lamp you place shows the Heart's mood by color (the **Mood Lamp**) | That lamp's glow shifts hue |
| 21 | Water the empty pots too | True | 5% chance per watering that a Wild Sprout grows | Tiny green pinpricks in soil |
| 22 | Never sell what you cannot name | True | Unnamed strains count one tier lower on Gold orders | Ledger asks “Name?” |
| 23 | Fen has never left the valley | Unverifiable until Thread 6 | Cannot be tested early; resolves with a Thread 6 reveal | Fen deflects the question |
| 24 | There are only six of us | False | Revealed in Thread 8: the beams carry K-7 | A seventh carving, faint |

---

## 45. The Ledger's voice and Mail

**45.1 Style guide.** Short sentences. Passive and bureaucratic. Specific objects, never abstract fear. No exclamation marks. Never explain the strangeness. Understatement is the horror. It addresses the player as “Keeper”. The voice warms and cracks across four stages (Formal, Familiar, Strained, Candid).

**45.2 Voice samples by event.**

| Event | Formal | Familiar | Strained | Candid |
| --- | --- | --- | --- | --- |
| Order delivered | “Received.” | “Received. Thank you, Keeper.” | “Received. It was heavier than it looked.” | “Received. It was warm. It liked that one.” |
| Order late | “Order unfulfilled. Standing noted.” | “Order unfulfilled. It happens.” | “Order unfulfilled. The Hatch stayed warm all night.” | “Order unfulfilled. You were missed.” |
| Rank-up | “Facility Rank raised.” | “Facility Rank raised. Well done.” | “Facility Rank raised. Others reached this point.” | “Facility Rank raised. They always stop around here.” |
| First anomaly | “Conditions are irregular. Please continue.” | “Odd weather today. Keep your lamps on.” | “It is not weather.” | “It is paying attention.” |
| Naming a strain | “Name recorded.” | “Name recorded. A good one.” | “Name recorded. Names are heard.” | “Name recorded. It said it back.” |
| Cycle end | “End of Cycle. Compliance: satisfactory.” | “End of Cycle. Rest well.” | “End of Cycle. Please do not wait up.” | “End of Cycle. I am glad it was you.” |

**45.2a Voice stage drivers.** The stage is chosen by the higher of Standing band and Attention band, and is overridden to Formal by the Cozy dread setting.

**45.3 The first twelve Mail entries (trigger in brackets).**

1. “Welcome, Keeper. Your predecessor left in a hurry. Please disregard the scratches.” \[first load\]
2. “Plants do not lean. Yours leaned. Note it.” \[first stage-up\]
3. “The Hatch accepts dried product only until further notice.” \[Cycle 1 Orders\]
4. “Payment has been delivered. A small token is included. It is not ours.” \[first Return\]
5. “Visitors are not covered by your contract.” \[first Visitor\]
6. “Please do not annotate the Rule Card.” \[Rule Card first examined\]
7. “Keeper K-6 left some equipment. It is yours now.” \[Rank 3\]
8. “Your lamp count is correct. Thank you for counting.” \[first Count passed\]
9. “You have been noticed. This is not a complaint.” \[Attention reaches Noticed\]
10. “The Hermit is not on our payroll.” \[Hermit's second visit\]
11. “Please disregard the previous Mail.” \[the false-mail beat, Cycle 9\]
12. “If you are reading this twice, stop. The answer is in the margin.” \[Thread 3 clue 4\]

---

## 46. The Keepers and their Caches (Thread 8)

After the Circle sealed the Heart, the Collector hired **Keepers** to tend the facility. You are **K-7**. Each earlier Keeper hid a **Cache** (a locked tin box holding a tool and a short diary) and each seeded one of the House Rules. Caches are found by following physical clues (scratched initials, a misplaced beam, a warm brick), not by map markers.

| Keeper | Role | Cache tool | Location | Diary fragment | Rule origin |
| --- | --- | --- | --- | --- | --- |
| K-1 Marl Tibbet | Cave surveyor | **Annex Chalk** (marks safe routes in Hollow Runs) | Niche at the Annex door | “I mapped it twice. The second map did not match the first.” | Do not run in the Annex |
| K-2 Odalys Frenn | Cook | **Warm Ladle** (edibles last 25% longer, Hearty line boosted) | Behind the Reserve Shelf | “The Hatch returned my pot clean, with thanks written in wax.” | Leave one jar unsealed |
| K-3 Brannoch Pell | Tinkerer | **Tuning Fork** (answers the Hum; unlocks Thread 2) | Inside the first lamp's housing | “I hummed back. It was a good evening.” | The third lamp is the honest one |
| K-4 Ysolde Marrow | Naturalist | **Moth Jar** (collects Moth Silk) | The roof roost | “The moths are its eyes. I told everyone they were bad luck so they would leave them alone.” | Moths bring bad luck |
| K-5 Hob Larkin | Night watchman | **Hush Bell** (reveals visitor tells and calms Mimics) | Under the Hatch | “Someone is knocking in my voice.” | Do not answer the Pager after the third bell |
| K-6 Sable Quill | Ledger scribe | **Margin Pen** (lets you annotate the Ledger and read hidden margins) | Behind the Ledger's back panel | “I wrote it all down so that something would remember me.” | The Ledger is always right |

**K-6 twist (Thread 3).** The Ledger's Candid voice is partly Sable's handwriting and partly the Heart imitating her. Reading all six diaries unlocks the secret ending branch (section 47): you may choose to **Remember** the Keepers by carving their names where visitors can see them.

---

## 47. The Mother, the finale and the endings

**47.1 The Five-Fold Cross (the endgame breeding puzzle).** The five Founders' Lines (Ashgrove Loam, Quill's Cordial, Moorwick Frost, Harrow Spark, Duskmantle Glow) are bred in a tournament bracket using the Breeding Lab (section 10, T5).

1. **Round 1:** A x B gives a Half-Line AB; C x D gives CD. Each must be stabilized and Registered.
2. **Round 2:** AB x CD gives ABCD.
3. **Final:** ABCD x E gives the **Mother Seed candidate**. The Sequencer shows five **Founder Markers** per gene (one glyph per Line). The candidate qualifies only if the genome holds at least one allele from each Founder.
4. Stabilize and Register it to get a **Mythic** Mother Seed.

**47.2 Growing the Mother in the Valley Greenhouse.** The central bed needs five **Aspects**, one supplied by each restored Wing, held through a 3-Shift grow:

| Wing | Aspect | Requirement |
| --- | --- | --- |
| Nursery | Soil | Enriched Dewloam, Soil Quality 90+ |
| Apothecary | Tonic | A custom Founders' Tonic piped through the Mixing Station |
| Library and Lab | Recipe | The Mother's Recipe (5 fragments, one per Wing) loaded into the Controller |
| Workshop | Power | At least 300 W steady from combined sources |
| Observatory Dome | Light | The Dome's 14/10 Lume schedule with Luminescent lamps |

A failed Aspect only delays the grow. It never kills the plant (gentle failure).

**47.3 The Heart Chamber ritual (three stages).**

1. **Offer.** Deliver the Mother jar through the Dumbwaiter. The Hatch opens into a doorway to the Heart Chamber.
2. **Listen.** A short rhythm puzzle: reproduce a 6-note Hum pattern with the Tuning Fork and the Mood Lamp. The pattern is built from the player's own Order history (their terpene sequence), so every player's is personal. Assist mode reduces it to 3 notes.
3. **Choose.** The final decision: Feed, Seal or Free.

**47.4 The endings.**

| Ending | What happens | Permanent effects | Legacy path |
| --- | --- | --- | --- |
| **Feed (Tithe)** | You keep giving; the Heart thrives and glows through the valley. The Hatch never closes. Fen rests inside the lantern light. | Output value +100%, Attention floor 50, visitors x1.5 | **Tithe Run:** more rules are true, the Ledger starts Candid. Early Alchemy Wing |
| **Seal (Rest)** | You close it gently. Fen finally sleeps. The Dew recedes, then slowly returns. | Attention system disabled, gentler quotas, Dew growth bonus rising 1% per Cycle up to 20% | **Quiet Run:** fewer anomalies, a warm Formal Ledger. Early Apiary Wing |
| **Free (Wake)** | The Heart wakes; Mycelial Mesh nodes light across the valley; the Hatch becomes a doorway. The Ledger prints: “Thank you, Keeper. Please look up.” | Attention becomes **Affinity** (a positive meter), anomalies turn friendly and strange, House Rules become always-true Hints | **Wild Run:** early Spore and Prism Wings |
| **Remember** (overlay, needs all six diaries) | Carve the six Keepers' names where visitors can see them. Seven lanterns appear at the Hatch. | Keeper's Coat cosmetic, an extra epilogue | Combines with any ending |

Each ending has a short three-beat epilogue (a cinematic of about 30 seconds, skippable), then the world stays playable as a sandbox.

**47.5 Fen's arc (Thread 6, six beats).**

1. First visit: leaves a lantern, says almost nothing.
2. A story about the Circle's last harvest.
3. Asks you to name a strain after someone.
4. Slips: “The last Keeper said that too.”
5. Admits he is tired.
6. His fate depends on the ending (above).

**47.6 Your Cache (the Legacy hook).** At Legacy you choose one tool and write a short diary entry (player text, capped length). On a new run (and for other players in multiplayer) it appears as the previous Keeper's Cache, so every playthrough inherits a real trace of the last one. Your initials are carved as K-7 and the next run's player is **K-8**.

---

## 48. The Annex and Hollow Runs (fully specified, built last)

This is the Lethal-Company-style expedition loop. It is stretch milestone M3 and must be cuttable without breaking anything else.

**48.1 Entry and run flow.** The Annex Door unlocks at Rank 12 (or by finding K-1's Cache). At the Ledger you take a **Run Brief** (“Retrieve 3 Dew Samples and 1 cassette. Estimated time: 8 minutes.”). Runs last 8-12 minutes.

**48.2 The lantern.** The core resource. A **Glow meter** (8 minutes base) drains while you explore and the light radius shrinks as it drains. **Quiet Rooms** restore it. **Annex Chalk** marks safe paths.

**48.3 Layout.** 6-10 rooms assembled from handcrafted templates (below) with a different arrangement each run. Deeper rooms give more loot and add +2 Attention per room entered.

| Room | Purpose |
| --- | --- |
| Flooded Nursery | Ingredients |
| Collapsed Greenhouse | Seeds |
| Keeper's Cubby | Lore and cassettes |
| Lamp Gallery | A small light puzzle |
| Mirror Room | Mirror Dew: reveals hidden location clues |
| Pump House | Machine components |
| Quiet Room | Safe; restores the lantern |
| The Long Corridor | The Hum, and a Wanderer patrol |

**48.4 Wanderers (non-lethal).** Figures made of moths and dew that drift toward noise. Sprinting makes noise (this is House Rule 11). Holding still lets them pass. If one reaches you it **walks you back** to the entrance and you lose 10% of the run's loot. No health loss, no death, no gear loss.

**48.5 Failure and extraction.** If the lantern runs out you enter **Dim** (the screen narrows). After 30 seconds the Wanderers gather and walk you out, keeping 50% of the loot. You can leave at any time through the **Return Hatch** in every Quiet Room. Greed versus risk is the whole decision: go deeper for more loot and Attention, or leave early with what you have.

**48.6 Rewards.** Ingredients (Glowcap, Dew Samples, Moth Silk), Odd items, cassettes, blueprint fragments. **Every run contains one guaranteed clue** for the Thread with the least progress, so the Annex always moves the mystery forward.

**48.7 Annex Map.** Rooms discovered across runs appear as silhouettes. The layout changes each run, so the Map shows the kinds of rooms you have found, not a fixed floor plan.

**48.8 Co-op.** Up to 4 players share one lantern; any member can extinguish the group's Glow by sprinting, which makes teamwork a real mechanic.

**48.9 Technical plan.** A datapack dimension (`stonedew:annex`) using jigsaw template pools and a per-run seed, reset on exit. **Fallback:** if a custom dimension is too costly, build the run as an instanced structure far below the Overworld and clean it up afterward using the same template pools.

---

## 49. The Heart as a system (the mood engine)

The mystery needs a deterministic backbone so reactions feel consistent, not random. The Heart has three state variables.

**49.1 Variables.**

- **Hunger (0-100):** how much it wants. Rises +10 per Shift. Falls by `1 * qualityMult` per delivered bud, -4 per completed Order, -8 per Return Slot offering. A Shortfall adds +10.
- **Affinity (0-100 per terpene):** how much it likes each profile. +5 per Return Slot item of that terpene, +1 per delivered bud, -1 per Cycle decay.
- **Attention (0-100):** how closely it watches (section 30), driven by output and scale.

Attention is how much it **watches**; Hunger is how much it **wants**. Together they set the tone: Quiet + Content is cozy, Called + Restless is the strangest content in the game.

**49.2 Mood states and cues.** The Heart stays **Dormant** until Standing 10 or Cycle 3.

| Mood | Hunger | Cues the player perceives | Gameplay effect |
| --- | --- | --- | --- |
| Dormant | - | None | None |
| Content | under 20 | Low steady lamp hum; the Mood Lamp glows teal | Returns +10% value, anomalies -25% |
| Curious | 20-49 | Hum wavers; Mood Lamp amber-violet | Normal rewards, clue chance +20% |
| Hungry | 50-74 | Jars hum on the shelf; Mood Lamp deep violet | Wildcards pay +25%, anomalies +25%, Orders +10% |
| Restless | 75+ | Lamps stutter at dusk; Mood Lamp flickers magenta | Calling events, more Mimic nights, rewards +40%, Attention gain x1.5 |

**49.3 Affinity effects.** At Affinity 60 or higher for a terpene: its special Return pool unlocks, the Ledger comments on it, and Orders for that terpene gain a small bonus.

**49.4 Where the player reads it.** The Mood Lamp (House Rule 20), jar hum (rule 10), lamp pitch (Thread 2), Ledger voice stage (section 45), and the Hum reading on the Pocket Meter.

---

## 50. Integration and loose ends

**50.1 Reconciliation (where Parts conflict).**

| Part I item | Resolution |
| --- | --- |
| 12.2 Circle lore and 12.4 structures | Consistent. Added: the Collector is the Heart; Keepers K-1 to K-6 are the post-Circle watchers (section 46) |
| 12.6 Contracts | **Orders** at the Ledger are primary (section 43). The Contract Board stays for optional side jobs (Standard, Rush, Collector, Vintage); Chain contracts become Hermit Mail |
| 4 Macro loop (30-60 min) | Replaced by the 3-Shift Cycle (section 23) |
| 2 Next Goal widget | Replaced by the Directive stack (section 25) |
| 15.3 Random events | Merged into the Hollow Weather anomaly pool (section 28); Heatwave, Mite Outbreak, Lucky Mutation and others remain as pool entries |
| 12.5 Brisk Barrow, Judge Thistlewick | Stay as Night Visitors (section 29) and Strain Show NPCs |
| 9.2 Rank titles | Kept. Standing (section 24.3) is a separate meter that gates the Catalog and Mail |
| 19 Roadmap and 21 Kickoff | Use section 40 deltas and kickoff addendum |

**50.2 Pacing check.** One Cycle is about 60 minutes. Rank 5 (about 2 h) lands near Cycle 2-3; Legacy (about 40 h) lands near Cycle 40, as in section 37. Part I pacing targets in section 9.9 remain the reference for tier timing.

**50.3 Decisions that are yours (the developer should ask before building).**

1. **Default dread level:** Cozy, Uneasy (recommended) or Eerie.
2. **Number of endings:** three plus the Remember overlay (recommended) or fewer.
3. **Hollow Runs:** include (M3) or cut entirely.
4. **Mature theming:** keep the consumables as written or default to Herbal Mode.
5. **Title:** keep “Stonedew” or rename.

**50.4 What is intentionally not in this document.** Final prose beyond the samples, final art and audio, balance numbers beyond the starting values, and any real-world cultivation or chemistry content. Those are produced during the phases, with you approving each.

**50.5 Completion check.** The design now covers the sim backbone (Part I), the stakes, mystery and structure (Part II), and the writing, rules, characters, endings and expedition content (Part III), plus a plug-in expansion framework for mushrooms and the psychedelic-style layer. The remaining decisions are the five in section 50.3.
