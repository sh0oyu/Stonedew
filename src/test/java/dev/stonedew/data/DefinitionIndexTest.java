package dev.stonedew.data;

import static org.junit.jupiter.api.Assertions.*;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import dev.stonedew.plant.Cultivar;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.Test;

class DefinitionIndexTest {
    private Map<String, JsonElement> bundled() throws IOException {
        Path root = Path.of("src/main/resources/data/stonedew/stonedew");
        var map = new HashMap<String, JsonElement>();
        try (var paths = Files.walk(root)) {
            for (Path path : paths.filter(p -> p.toString().endsWith(".json")).toList()) {
                String key = "stonedew:" + root.relativize(path).toString().replace('\\', '/').replaceFirst("\\.json$", "");
                map.put(key, JsonParser.parseString(Files.readString(path)));
            }
        }
        return map;
    }
    @Test void bundledWingAndCultivarResolve() throws IOException {
        var index = DefinitionIndex.load(bundled());
        assertEquals(6, index.size());
        assertEquals(Cultivar.Type.PLANT, index.cultivars().get("stonedew:herb").type());
        assertEquals(java.util.List.of("stonedew:herb"), index.wings().get("stonedew:base").cultivars());
    }
    @Test void addonNamespaceCanRegisterWing() throws IOException {
        var definitions = bundled();
        definitions.put("addon:wings/extra", JsonParser.parseString("{\"schema_version\":1,\"display_name\":\"wing.addon.extra\",\"cultivars\":[\"stonedew:herb\"]}"));
        assertTrue(DefinitionIndex.load(definitions).wings().containsKey("addon:extra"));
    }
    @Test void brokenProfileReferenceRejectsReload() throws IOException {
        var definitions = bundled();
        definitions.remove("stonedew:process_chains/herb");
        assertThrows(IllegalArgumentException.class, () -> DefinitionIndex.load(definitions));
    }
    @Test void brokenWingBindingRejectsReload() throws IOException {
        var definitions = bundled();
        definitions.remove("stonedew:cultivars/herb");
        assertThrows(IllegalArgumentException.class, () -> DefinitionIndex.load(definitions));
    }
    @Test void unsupportedSchemaRejectsReload() throws IOException {
        var definitions = bundled();
        definitions.get("stonedew:wings/base").getAsJsonObject().addProperty("schema_version", 99);
        assertThrows(IllegalArgumentException.class, () -> DefinitionIndex.load(definitions));
    }
    @Test void fractionalAndStringSchemaAreRejected() throws IOException {
        for (var schema : java.util.List.of("1.5", "\"1\"")) {
            var definitions = bundled();
            definitions.get("stonedew:wings/base").getAsJsonObject().add("schema_version", JsonParser.parseString(schema));
            assertThrows(IllegalArgumentException.class, () -> DefinitionIndex.load(definitions));
        }
    }
    @Test void unknownCategoryIsRejected() {
        assertThrows(IllegalArgumentException.class, () -> DefinitionIndex.load(Map.of("addon:typo/x", JsonParser.parseString("{\"schema_version\":1}"))));
    }
    @Test void nonObjectDefinitionsAreRejected() {
        assertThrows(IllegalArgumentException.class, () -> DefinitionIndex.load(Map.of("addon:wings/x", JsonParser.parseString("[]"))));
    }
    @Test void callersCannotMutatePublishedDefinitions() throws IOException {
        var source = bundled();
        var index = DefinitionIndex.load(source);
        source.get("stonedew:wings/base").getAsJsonObject().addProperty("display_name", "changed");
        index.definition("wings", "stonedew:base").addProperty("display_name", "also changed");
        assertEquals("wing.stonedew.base", index.definition("wings", "stonedew:base").get("display_name").getAsString());
        assertThrows(UnsupportedOperationException.class, () -> index.wings().clear());
    }
    @Test void cultivarAbstractionAcceptsFungusWithoutPlantSubclass() throws IOException {
        var definitions = bundled();
        var fungus = definitions.get("stonedew:cultivars/herb").deepCopy();
        fungus.getAsJsonObject().addProperty("type", "FUNGUS");
        definitions.put("addon:cultivars/fungus", fungus);
        assertEquals(Cultivar.Type.FUNGUS, DefinitionIndex.load(definitions).cultivars().get("addon:fungus").type());
    }
    @Test void invalidNamespacedReferencesAreRejected() throws IOException {
        var definitions = bundled();
        definitions.get("stonedew:cultivars/herb").getAsJsonObject().addProperty("gene_schema", "not a resource id");
        assertThrows(IllegalArgumentException.class, () -> DefinitionIndex.load(definitions));
    }
}
