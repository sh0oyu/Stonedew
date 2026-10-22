# Stonedew datapacks — P1, schema 1

Place definitions at `data/<namespace>/stonedew/<category>/<id>.json`. The path, not an embedded field, establishes identity. For example, `data/stonedew/stonedew/wings/base.json` is Wing `stonedew:base`.

Every file must be a JSON object with numeric integer `"schema_version": 1`. Standard Minecraft datapack priority supplies overrides. `/reload` builds a fresh immutable index, verifies Wing/cultivar references, then publishes it atomically. Malformed input rejects the replacement. Existing readers keep the previous index. Input JSON and returned JSON cannot mutate a published index.

Recognized categories: `wings`, `cultivars`, `gene_schemas`, `environment_profiles`, `process_chains`, `effect_maps`, `terpenes`, `pigments`, `nutrients`, `events`, `orders`, `contracts`, `grow_recipes`, `heirlooms`, `lore`, `routine_triggers`, `routine_actions`, `clues`, `directives`, `anomalies`, `visitors`, `rules`, `endings`.

**P1 has typed runtime consumers for Wings, cultivars, the base growth/environment profile and introductory directive.** Other categories retain envelope/identity validation until their gameplay phases. The base index contains seven definitions. `stonedew:herb` environment profile and `stonedew:first_grow` directive are required; removing them rejects reload instead of causing a later interaction/login failure.

## Growth profile

`environment_profiles/herb.json` contains stage durations/comfort ranges, Vigor weights/tolerance, growth bounds, difficulty multipliers, update/integration intervals, catch-up cap, water drain/pour/can capacity, lamp fuel/output/range/falloff and baseline environment. Values are finite and range-checked; weights sum to one. The exact bundled file is the complete P1 example. Reload applies to subsequent simulation visits. P2 will replace baseline environment sampling with room measurements.

## Introductory directive

`directives/first_grow.json` contains ordered steps with `required_flags` and localized `text` keys. Flags are planted=1, watered=2, lamp fueled=4, ripe=8. The highest satisfied step selects the current directive. An initial zero-mask step is required; duplicate masks and invalid text keys reject loading. This P1 introductory sequence does not implement the later narrative scheduler.

## Wing

```json
{
  "schema_version": 1,
  "display_name": "wing.example.garden",
  "unlock": {},
  "cultivars": ["stonedew:herb"],
  "content": {},
  "version_compatibility": {"minecraft": "1.21.1", "stonedew": "0.2"}
}
```

`display_name` is a language key, and every cultivar binding must exist. `unlock`, `content`, and version compatibility are reserved manifest payloads retained in the index, not enforced/unlocked by P1. A future Wing release adds those semantics and versioned codecs.

## Cultivar

```json
{
  "schema_version": 1,
  "type": "PLANT",
  "gene_schema": "stonedew:herb",
  "environment_profile": "stonedew:herb",
  "process_chain": "stonedew:herb",
  "effect_map": "stonedew:herb"
}
```

`type` is `PLANT` or `FUNGUS`; all four references must exist in their corresponding categories. Adding a fungus profile demonstrates the abstraction; mushroom gameplay remains a later Wing.

Localized text belongs in `assets/<namespace>/lang/en_us.json`. Stonedew authors directive prose separately in `src/main/narrative/en_us.json`; `runData` merges it with generated labels. Do not put narrative prose in Java handlers.
