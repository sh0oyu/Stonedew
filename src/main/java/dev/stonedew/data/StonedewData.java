package dev.stonedew.data;

import dev.stonedew.Stonedew;
import dev.stonedew.core.ModContent;
import java.util.List;
import java.util.Set;
import java.util.concurrent.CompletableFuture;
import net.minecraft.advancements.Advancement;
import net.minecraft.advancements.AdvancementType;
import net.minecraft.advancements.critereon.InventoryChangeTrigger;
import net.minecraft.core.HolderLookup;
import net.minecraft.data.PackOutput;
import net.minecraft.data.advancements.AdvancementProvider;
import net.minecraft.data.loot.BlockLootSubProvider;
import net.minecraft.data.loot.LootTableProvider;
import net.minecraft.data.recipes.RecipeCategory;
import net.minecraft.data.recipes.RecipeOutput;
import net.minecraft.data.recipes.RecipeProvider;
import net.minecraft.data.recipes.ShapelessRecipeBuilder;
import net.minecraft.network.chat.Component;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.storage.loot.parameters.LootContextParamSets;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.model.generators.BlockStateProvider;
import net.neoforged.neoforge.client.model.generators.ItemModelProvider;
import net.neoforged.neoforge.common.data.BlockTagsProvider;
import net.neoforged.neoforge.common.data.ExistingFileHelper;
import net.neoforged.neoforge.common.data.LanguageProvider;
import net.neoforged.neoforge.data.event.GatherDataEvent;

@EventBusSubscriber(modid = Stonedew.ID)
public final class StonedewData {
    @SubscribeEvent
    public static void gather(GatherDataEvent event) {
        var generator = event.getGenerator();
        var output = generator.getPackOutput();
        var lookup = event.getLookupProvider();
        var files = event.getExistingFileHelper();
        generator.addProvider(event.includeClient(), new BlockStateProvider(output, Stonedew.ID, files) {
            @Override protected void registerStatesAndModels() { simpleBlockWithItem(ModContent.DEWSTONE.get(), cubeAll(ModContent.DEWSTONE.get())); }
        });
        generator.addProvider(event.includeClient(), new ItemModelProvider(output, Stonedew.ID, files) {
            @Override protected void registerModels() { basicItem(ModContent.GLOW_CELL.get()); }
        });
        generator.addProvider(event.includeClient(), new English(output));
        generator.addProvider(event.includeServer(), new LootTableProvider(output, Set.of(), List.of(
                new LootTableProvider.SubProviderEntry(Drops::new, LootContextParamSets.BLOCK)), lookup));
        generator.addProvider(event.includeServer(), new Tags(output, lookup, files));
        generator.addProvider(event.includeServer(), new Recipes(output, lookup));
        generator.addProvider(event.includeServer(), new AdvancementProvider(output, lookup, List.of((registries, writer) ->
                Advancement.Builder.advancement()
                        .display(ModContent.DEWSTONE.get(), Component.translatable("advancement.stonedew.root.title"),
                                Component.translatable("advancement.stonedew.root.description"), Stonedew.id("textures/block/dewstone.png"),
                                AdvancementType.TASK, true, true, false)
                        .addCriterion("dewstone", InventoryChangeTrigger.TriggerInstance.hasItems(ModContent.DEWSTONE.get()))
                        .save(writer, "stonedew:root"))));
    }

    private static final class Drops extends BlockLootSubProvider {
        Drops(HolderLookup.Provider lookup) { super(Set.of(), FeatureFlags.DEFAULT_FLAGS, lookup); }
        @Override protected void generate() { dropSelf(ModContent.DEWSTONE.get()); }
        @Override protected Iterable<Block> getKnownBlocks() { return List.of(ModContent.DEWSTONE.get()); }
    }
    private static final class Tags extends BlockTagsProvider {
        Tags(PackOutput output, CompletableFuture<HolderLookup.Provider> lookup, ExistingFileHelper files) { super(output, lookup, Stonedew.ID, files); }
        @Override protected void addTags(HolderLookup.Provider lookup) { tag(BlockTags.MINEABLE_WITH_PICKAXE).add(ModContent.DEWSTONE.get()); }
    }
    private static final class Recipes extends RecipeProvider {
        Recipes(PackOutput output, CompletableFuture<HolderLookup.Provider> lookup) { super(output, lookup); }
        @Override protected void buildRecipes(RecipeOutput output, HolderLookup.Provider registries) {
            // P0 developer recipe. Data packs may replace it; progression balancing arrives with gameplay.
            ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, ModContent.GLOW_CELL.get())
                    .requires(Items.AMETHYST_SHARD).requires(Items.COPPER_INGOT)
                    .unlockedBy("has_amethyst", has(Items.AMETHYST_SHARD)).save(output);
        }
    }
    private static final class English extends LanguageProvider {
        English(PackOutput output) { super(output, Stonedew.ID, "en_us"); }
        @Override protected void addTranslations() {
            add("itemGroup.stonedew", "Stonedew");
            add(ModContent.DEWSTONE.get(), "Dewstone");
            add(ModContent.GLOW_CELL.get(), "Glow Cell");
            add("wing.stonedew.base", "Stonedew");
            add("advancement.stonedew.root.title", "Stonedew");
            add("advancement.stonedew.root.description", "Obtain Dewstone.");
            add("command.stonedew.status", "Stonedew P0 | definitions: %s | difficulty: %s | dread: %s");
            add("command.stonedew.story", "Keeper K-%s | Standing: %s | Attention: %s | debug probes: %s");
            add("command.stonedew.probe", "Recorded one debug probe. Use /stonedew debug story to inspect persistence.");
            add("status.stonedew.foundation", "Foundation build: plant gameplay arrives in P1");
            add("stonedew.configuration.gameplay", "Gameplay");
            add("stonedew.configuration.accessibility", "Accessibility");
            add("stonedew.configuration.difficulty", "Difficulty");
            add("stonedew.configuration.dread", "Dread");
            add("stonedew.configuration.herbalMode", "Herbal Mode");
            add("stonedew.configuration.roomVolumeCap", "Room volume cap");
            add("stonedew.configuration.atmosphere", "Atmospheric effects");
            add("stonedew.configuration.cameraMoments", "Camera moments");
            add("stonedew.configuration.minigames", "Minigames");
            add("stonedew.configuration.screenTint", "Screen tint");
            add("stonedew.configuration.suddenSounds", "Sudden sounds");
            add("stonedew.configuration.visualIntensity", "Visual intensity");
            add("stonedew.configuration.audioDread", "Audio dread");
            add("stonedew.configuration.particleBudget", "Particle budget");
        }
    }
    private StonedewData() {}
}
