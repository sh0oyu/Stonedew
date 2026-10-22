# Stonedew datapacks — P0 schema 1

Place definitions at `data/<namespace>/stonedew/<category>/<id>.json`. The path, not an embedded field, establishes identity. For example, `data/stonedew/stonedew/wings/base.json` is Wing `stonedew:base`.

Every file must be a JSON object with numeric integer `"schema_version": 1`. Standard Minecraft datapack priority supplies overrides. `/reload` builds a fresh immutable index, verifies Wing/cultivar references, then publishes it atomically. Malformed input rejects the replacement. Existing readers keep the previous index. Input JSON and returned JSON cannot mutate a published index.

P0 categories: `wings`, `cultivars`, `gene_schemas`, `environment_profiles`, `process_chains`, `effect_maps`, `terpenes`, `pigments`, `nutrients`, `events`, `orders`, `contracts`, `grow_recipes`, `heirlooms`, `lore`, `routine_triggers`, `routine_actions`, `clues`, `directives`, `anomalies`, `visitors`, `rules`, `endings`.

**P0 implements identity/schema-envelope validation for these categories; it does not execute later gameplay or narrative definitions.** Only Wing identity/cultivar bindings and Cultivar profiles have typed runtime consumers now. Later phases add type-specific codecs, semantic checks and handlers before those categories become playable. Base profile files declare `implementation_phase` so placeholders are explicit. Base timings are design starting values, held in JSON rather than gameplay constants.

## Wing

```json
{
  "schema_version": 1,
  "display_name": "wing.example.garden",
  "unlock": {},
  "cultivars": ["stonedew:herb"],
  "content": {},
  "version_compatibility": {"minecraft": "1.21.1", "stonedew": "0.1"}
}
```

`display_name` is a language key, and every cultivar binding must exist. `unlock`, `content`, and version compatibility are reserved manifest payloads retained in the index, not enforced/unlocked by P0. A future Wing release adds those semantics and versioned codecs.

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

Localized text belongs in `assets/<namespace>/lang/en_us.json`. New story prose must have separate authoring inputs when introduced, merged into the generated language output during datagen. Do not put prose in Java handlers.
