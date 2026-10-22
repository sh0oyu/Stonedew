package dev.stonedew.data;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import dev.stonedew.plant.Cultivar;
import dev.stonedew.plant.CultivarProfile;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** A reload is validated completely before publication. JSON returned to callers is always a copy. */
public final class DefinitionIndex {
    public static final Set<String> CATEGORIES = Set.of("wings", "cultivars", "gene_schemas", "environment_profiles",
            "process_chains", "effect_maps", "terpenes", "pigments", "nutrients", "events", "orders", "contracts",
            "grow_recipes", "heirlooms", "lore", "routine_triggers", "routine_actions", "clues", "directives",
            "anomalies", "visitors", "rules", "endings");
    private final Map<String, String> json;
    private final Map<String, WingManifest> wings;
    private final Map<String, CultivarProfile> cultivars;

    private DefinitionIndex(Map<String, String> json, Map<String, WingManifest> wings, Map<String, CultivarProfile> cultivars) {
        this.json = Map.copyOf(json);
        this.wings = Map.copyOf(wings);
        this.cultivars = Map.copyOf(cultivars);
    }
    public static DefinitionIndex empty() { return new DefinitionIndex(Map.of(), Map.of(), Map.of()); }
    public int size() { return json.size(); }
    public Map<String, WingManifest> wings() { return wings; }
    public Map<String, CultivarProfile> cultivars() { return cultivars; }
    public JsonObject definition(String category, String id) {
        String text = json.get(category + "/" + id);
        if (text == null) throw new IllegalArgumentException("Missing " + category + "/" + id);
        return JsonParser.parseString(text).getAsJsonObject();
    }

    /** Input keys are reload resource IDs such as stonedew:wings/base. */
    public static DefinitionIndex load(Map<String, JsonElement> resources) {
        Map<String, String> definitions = new HashMap<>();
        Map<String, WingManifest> wings = new HashMap<>();
        Map<String, CultivarProfile> cultivars = new HashMap<>();
        resources.forEach((resource, element) -> {
            Identifiers.require(resource);
            int colon = resource.indexOf(':');
            int slash = resource.indexOf('/', colon);
            if (slash < 0) throw new IllegalArgumentException("Definition needs a category: " + resource);
            String category = resource.substring(colon + 1, slash);
            if (!CATEGORIES.contains(category)) throw new IllegalArgumentException("Unknown content category: " + resource);
            String id = resource.substring(0, colon + 1) + resource.substring(slash + 1);
            if (!element.isJsonObject()) throw new IllegalArgumentException("Expected object: " + resource);
            JsonObject object = element.getAsJsonObject();
            JsonElement schema = object.get("schema_version");
            if (schema == null || !schema.isJsonPrimitive() || !schema.getAsJsonPrimitive().isNumber()
                    || !schema.getAsString().equals("1")) throw new IllegalArgumentException("Unsupported schema_version: " + resource);
            definitions.put(category + "/" + id, object.toString());
            if (category.equals("wings")) {
                var ids = object.getAsJsonArray("cultivars");
                if (ids == null) throw new IllegalArgumentException("Wing needs cultivars: " + id);
                List<String> bindings = java.util.stream.StreamSupport.stream(ids.spliterator(), false).map(JsonElement::getAsString).toList();
                wings.put(id, new WingManifest(id, string(object, "display_name"), bindings));
            } else if (category.equals("cultivars")) {
                cultivars.put(id, new CultivarProfile(id, Cultivar.Type.valueOf(string(object, "type")), string(object, "gene_schema"),
                        string(object, "environment_profile"), string(object, "process_chain"), string(object, "effect_map")));
            }
        });
        wings.values().forEach(wing -> wing.cultivars().forEach(id -> {
            if (!cultivars.containsKey(id)) throw new IllegalArgumentException("Wing " + wing.id() + " references missing cultivar " + id);
        }));
        cultivars.values().forEach(profile -> {
            requireReference(definitions, "gene_schemas", profile.geneSchema());
            requireReference(definitions, "environment_profiles", profile.environmentProfile());
            requireReference(definitions, "process_chains", profile.processChain());
            requireReference(definitions, "effect_maps", profile.effectMap());
        });
        return new DefinitionIndex(definitions, wings, cultivars);
    }
    private static String string(JsonObject object, String key) {
        JsonElement value = object.get(key);
        if (value == null || !value.isJsonPrimitive() || !value.getAsJsonPrimitive().isString() || value.getAsString().isBlank())
            throw new IllegalArgumentException("Expected nonempty string: " + key);
        return value.getAsString();
    }
    private static void requireReference(Map<String, String> definitions, String category, String id) {
        if (!definitions.containsKey(category + "/" + id)) throw new IllegalArgumentException("Missing " + category + "/" + id);
    }
}
