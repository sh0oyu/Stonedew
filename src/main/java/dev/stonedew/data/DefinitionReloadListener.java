package dev.stonedew.data;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import dev.stonedew.Stonedew;
import java.util.Map;
import java.util.stream.Collectors;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.resources.FileToIdConverter;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.SimpleJsonResourceReloadListener;
import net.minecraft.util.profiling.ProfilerFiller;

public final class DefinitionReloadListener extends SimpleJsonResourceReloadListener {
    private static volatile DefinitionIndex current = DefinitionIndex.empty();
    public DefinitionReloadListener() { super(new Gson(), "stonedew"); }
    public static DefinitionIndex current() { return current; }

    @Override
    protected Map<ResourceLocation, JsonElement> prepare(ResourceManager manager, ProfilerFiller profiler) {
        // Vanilla's default JSON listener logs and skips malformed files. A partial content index is unsafe here.
        var converter = FileToIdConverter.json("stonedew");
        var definitions = new java.util.HashMap<ResourceLocation, JsonElement>();
        converter.listMatchingResources(manager).forEach((file, resource) -> {
            try (var reader = resource.openAsReader()) {
                definitions.put(converter.fileToId(file), JsonParser.parseReader(reader));
            } catch (java.io.IOException | RuntimeException exception) {
                throw new IllegalArgumentException("Cannot load Stonedew definition " + file, exception);
            }
        });
        return definitions;
    }

    @Override
    protected void apply(Map<ResourceLocation, JsonElement> resources, ResourceManager manager, ProfilerFiller profiler) {
        DefinitionIndex replacement = DefinitionIndex.load(resources.entrySet().stream()
                .collect(Collectors.toMap(entry -> entry.getKey().toString(), Map.Entry::getValue)));
        current = replacement;
        Stonedew.LOGGER.info("Loaded {} Stonedew definitions, {} Wings, {} cultivars", current.size(), current.wings().size(), current.cultivars().size());
    }
}
