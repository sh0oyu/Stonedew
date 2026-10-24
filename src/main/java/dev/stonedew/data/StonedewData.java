package dev.stonedew.data;

import dev.stonedew.Stonedew;
import dev.stonedew.core.ModContent;
import dev.stonedew.plant.BulbLampBlock;
import dev.stonedew.plant.GrowTrayBlock;
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
import net.minecraft.data.recipes.ShapedRecipeBuilder;
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
import net.neoforged.neoforge.client.model.generators.ConfiguredModel;
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
    generator.addProvider(
        event.includeClient(),
        new BlockStateProvider(output, Stonedew.ID, files) {
          @Override
          protected void registerStatesAndModels() {
            files.trackGenerated(
                modLoc("block/painted/dewstone"),
                net.minecraft.server.packs.PackType.CLIENT_RESOURCES,
                ".png",
                "textures");
            simpleBlockWithItem(
                ModContent.DEWSTONE.get(),
                models().cubeAll("dewstone", modLoc("block/painted/dewstone")));
            for (var tray : List.of(ModContent.CLAY_POT, ModContent.PLANTER_BED)) {
              getVariantBuilder(tray.get())
                  .forAllStates(
                      state ->
                          ConfiguredModel.builder()
                              .modelFile(
                                  models()
                                      .getExistingFile(
                                          modLoc(
                                              "block/"
                                                  + tray.getId().getPath()
                                                  + (state.getValue(GrowTrayBlock.WET)
                                                      ? "_wet"
                                                      : ""))))
                              .build());
              simpleBlockItem(
                  tray.get(), models().getExistingFile(modLoc("block/" + tray.getId().getPath())));
            }
            getVariantBuilder(ModContent.BULB_LAMP.get())
                .forAllStates(
                    state ->
                        ConfiguredModel.builder()
                            .modelFile(
                                models()
                                    .getExistingFile(
                                        modLoc(
                                            "block/bulb_lamp"
                                                + (state.getValue(BulbLampBlock.LIT)
                                                    ? "_lit"
                                                    : ""))))
                            .build());
            simpleBlockItem(
                ModContent.BULB_LAMP.get(), models().getExistingFile(modLoc("block/bulb_lamp")));
            simpleBlockWithItem(
                ModContent.LEDGER.get(), models().getExistingFile(modLoc("block/ledger")));
          }
        });

    generator.addProvider(event.includeClient(), new English(output));
    generator.addProvider(
        event.includeServer(),
        new LootTableProvider(
            output,
            Set.of(),
            List.of(new LootTableProvider.SubProviderEntry(Drops::new, LootContextParamSets.BLOCK)),
            lookup));
    generator.addProvider(event.includeServer(), new Tags(output, lookup, files));
    generator.addProvider(event.includeServer(), new Recipes(output, lookup));
    generator.addProvider(
        event.includeServer(),
        new AdvancementProvider(
            output,
            lookup,
            List.of(
                (registries, writer) ->
                    Advancement.Builder.advancement()
                        .display(
                            ModContent.DEWSTONE.get(),
                            Component.translatable("advancement.stonedew.root.title"),
                            Component.translatable("advancement.stonedew.root.description"),
                            Stonedew.id("textures/block/dewstone.png"),
                            AdvancementType.TASK,
                            true,
                            true,
                            false)
                        .addCriterion(
                            "dewstone",
                            InventoryChangeTrigger.TriggerInstance.hasItems(
                                ModContent.DEWSTONE.get()))
                        .save(writer, "stonedew:root"))));
  }

  private static final class Drops extends BlockLootSubProvider {
    Drops(HolderLookup.Provider lookup) {
      super(Set.of(), FeatureFlags.DEFAULT_FLAGS, lookup);
    }

    @Override
    protected void generate() {
      for (var block : ModContent.BLOCKS.getEntries())
        if (block.get() != ModContent.TENT_PART.get()) dropSelf(block.get());
    }

    @Override
    protected Iterable<Block> getKnownBlocks() {
      return ModContent.BLOCKS.getEntries().stream()
          .map(entry -> (Block) entry.get())
          .filter(block -> block != ModContent.TENT_PART.get())
          .toList();
    }
  }

  private static final class Tags extends BlockTagsProvider {
    Tags(
        PackOutput output,
        CompletableFuture<HolderLookup.Provider> lookup,
        ExistingFileHelper files) {
      super(output, lookup, Stonedew.ID, files);
    }

    @Override
    protected void addTags(HolderLookup.Provider lookup) {
      tag(BlockTags.MINEABLE_WITH_PICKAXE)
          .add(ModContent.DEWSTONE.get(), ModContent.BULB_LAMP.get());
      tag(BlockTags.MINEABLE_WITH_AXE).add(ModContent.PLANTER_BED.get(), ModContent.LEDGER.get());
    }
  }

  private static final class Recipes extends RecipeProvider {
    Recipes(PackOutput output, CompletableFuture<HolderLookup.Provider> lookup) {
      super(output, lookup);
    }

    @Override
    protected void buildRecipes(RecipeOutput output, HolderLookup.Provider registries) {
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.WOODEN_PLANTER.get())
          .pattern("S S")
          .pattern("SCS")
          .pattern("III")
          .define('S', Items.OAK_SLAB)
          .define('C', ModContent.CLAY_POT.get())
          .define('I', Items.IRON_NUGGET)
          .unlockedBy("has_pot", has(ModContent.CLAY_POT.get()))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.FABRIC_POT.get())
          .pattern("S S")
          .pattern("W W")
          .pattern("DDD")
          .define('S', Items.STRING)
          .define('W', Items.BLACK_WOOL)
          .define('D', Items.DIRT)
          .unlockedBy("has_wool", has(Items.BLACK_WOOL))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.REINFORCED_POT.get())
          .pattern("I I")
          .pattern("ICI")
          .pattern("III")
          .define('I', Items.IRON_INGOT)
          .define('C', ModContent.CLAY_POT.get())
          .unlockedBy("has_pot", has(ModContent.CLAY_POT.get()))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.UV_PENDANT.get())
          .pattern(" I ")
          .pattern(" G ")
          .pattern("III")
          .define('I', Items.IRON_INGOT)
          .define('G', ModContent.GLOW_CELL.get())
          .unlockedBy("has_cell", has(ModContent.GLOW_CELL.get()))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.UV_PANEL_4.get())
          .pattern("III")
          .pattern("L L")
          .pattern("III")
          .define('I', Items.IRON_INGOT)
          .define('L', ModContent.BULB_LAMP.get())
          .unlockedBy("has_lamp", has(ModContent.BULB_LAMP.get()))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.UV_PANEL_6.get())
          .pattern("ALA")
          .pattern("IPI")
          .define('A', Items.AMETHYST_SHARD)
          .define('L', ModContent.BULB_LAMP.get())
          .define('I', Items.IRON_INGOT)
          .define('P', ModContent.UV_PANEL_4.get())
          .unlockedBy("has_panel", has(ModContent.UV_PANEL_4.get()))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.TENT_1.get())
          .pattern("WWW")
          .pattern("ISI")
          .pattern("I I")
          .define('W', Items.PURPLE_WOOL)
          .define('S', Items.STRING)
          .define('I', Items.IRON_INGOT)
          .unlockedBy("has_iron", has(Items.IRON_INGOT))
          .save(output);
      var tents =
          List.of(ModContent.TENT_1, ModContent.TENT_2, ModContent.TENT_3, ModContent.TENT_4);
      var trim = List.of(Items.LEATHER, Items.COPPER_INGOT, Items.AMETHYST_SHARD);
      for (int i = 1; i < 4; i++)
        ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, tents.get(i).get())
            .pattern("WTW")
            .pattern("ICI")
            .pattern("III")
            .define('W', Items.PURPLE_WOOL)
            .define('T', trim.get(i - 1))
            .define('I', Items.IRON_INGOT)
            .define('C', tents.get(i - 1).get())
            .unlockedBy("has_tent", has(tents.get(i - 1).get()))
            .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.CLAY_POT.get())
          .pattern("B B")
          .pattern(" B ")
          .define('B', Items.BRICK)
          .unlockedBy("has_brick", has(Items.BRICK))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.PLANTER_BED.get())
          .pattern("S S")
          .pattern("SDS")
          .define('S', Items.SPRUCE_SLAB)
          .define('D', Items.DIRT)
          .unlockedBy("has_slab", has(Items.SPRUCE_SLAB))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.TOOLS, ModContent.WATERING_CAN.get())
          .pattern("I I")
          .pattern("III")
          .define('I', Items.IRON_INGOT)
          .unlockedBy("has_iron", has(Items.IRON_INGOT))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.BULB_LAMP.get())
          .pattern("C C")
          .pattern("AGA")
          .define('C', Items.CHAIN)
          .define('A', Items.COPPER_INGOT)
          .define('G', Items.AMETHYST_SHARD)
          .unlockedBy("has_amethyst", has(Items.AMETHYST_SHARD))
          .save(output);
      ShapedRecipeBuilder.shaped(RecipeCategory.DECORATIONS, ModContent.LEDGER.get())
          .pattern(" P ")
          .pattern("CAC")
          .pattern("SSS")
          .define('P', Items.PAPER)
          .define('C', Items.COPPER_INGOT)
          .define('A', Items.AMETHYST_SHARD)
          .define('S', Items.SPRUCE_SLAB)
          .unlockedBy("has_paper", has(Items.PAPER))
          .save(output);
      ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, ModContent.WILD_SEED.get(), 2)
          .requires(Items.WHEAT_SEEDS)
          .requires(Items.GLOW_BERRIES)
          .unlockedBy("has_berries", has(Items.GLOW_BERRIES))
          .save(output);
      // P0 developer recipe. Data packs may replace it; progression balancing arrives with
      // gameplay.
      ShapelessRecipeBuilder.shapeless(RecipeCategory.MISC, ModContent.GLOW_CELL.get())
          .requires(Items.AMETHYST_SHARD)
          .requires(Items.COPPER_INGOT)
          .unlockedBy("has_amethyst", has(Items.AMETHYST_SHARD))
          .save(output);
    }
  }

  private static final class English extends LanguageProvider {
    English(PackOutput output) {
      super(output, Stonedew.ID, "en_us");
    }

    @Override
    protected void addTranslations() {
      add("itemGroup.stonedew", "Stonedew");
      add(ModContent.CLAY_POT.get(), "Clay Pot");
      add(ModContent.PLANTER_BED.get(), "Planter Bed");
      add(ModContent.BULB_LAMP.get(), "Bulb Lamp");
      add(ModContent.LEDGER.get(), "The Ledger");
      add(ModContent.WILD_SEED.get(), "Wild Seed");
      add(ModContent.WATERING_CAN.get(), "Tin Watering Can");
      add("pigment.stonedew.violet", "Violet");
      add("pigment.stonedew.teal", "Teal");
      add("pigment.stonedew.amber", "Amber");
      add("pigment.stonedew.green", "Green");
      add("stage.stonedew.0", "Seedling");
      add("stage.stonedew.1", "Vegetative");
      add("stage.stonedew.2", "Flowering");
      add("stage.stonedew.3", "Ripe");
      add("plant.stonedew.wild", "Wild %s");
      add("hud.stonedew.stage", "%s · %s%%");
      add("hud.stonedew.metrics", "Water %s · Lume %s · Vigor %s");
      add("hud.stonedew.condition", "Humidity %s%% · %s");
      add("hint.stonedew.seed", "Plant in a Clay Pot or Planter Bed.");
      add("hint.stonedew.empty_tray", "Plant a Wild Seed in this soil.");
      add("hint.stonedew.occupied", "This slot already holds a plant.");
      add("hint.stonedew.already_wet", "The soil is already wet enough.");
      add("hint.stonedew.refill", "Empty can. Right-click a water source to refill.");
      add("hint.stonedew.can", "Water: %s pours");
      add("hint.stonedew.can_use", "Refill at water; pour onto planted soil.");
      add("hint.stonedew.plant", "%s · Water %s%%");
      add("status.stonedew.empty", "Ready for a seed");
      add("status.stonedew.thirsty", "Needs water");
      add("status.stonedew.growing", "Growing");
      add("status.stonedew.ripe", "Ripe");
      add("status.stonedew.lamp_running", "Lamp is running");
      add("status.stonedew.lamp_empty", "Insert a Glow Cell");
      add(ModContent.WOODEN_PLANTER.get(), "Wooden Grow Crate");
      add(ModContent.FABRIC_POT.get(), "Canvas Grow Pot");
      add(ModContent.REINFORCED_POT.get(), "Reinforced Grow Pot");
      add(ModContent.UV_PENDANT.get(), "UV Pendant");
      add(ModContent.UV_PANEL_4.get(), "Four-Tube Grow Panel");
      add(ModContent.UV_PANEL_6.get(), "Six-Tube Grow Panel");
      add(ModContent.TENT_1.get(), "Seedling Grow Tent");
      add(ModContent.TENT_2.get(), "Keeper's Grow Tent");
      add(ModContent.TENT_3.get(), "Botanist's Grow Tent");
      add(ModContent.TENT_4.get(), "Master Grow Tent");
      add("ui.stonedew.vigor", "Vigor");
      add("ui.stonedew.grow", "Grow");
      add("hud.stonedew.humidity", "RH %s%%");
      add("ui.stonedew.journal", "KEEPER'S FIELD JOURNAL");
      add("ui.stonedew.brand", "STONEDEW");
      add("ui.stonedew.overview", "My garden");
      add("ui.stonedew.growing", "Plant care");
      add("ui.stonedew.equipment", "Workshop");
      add("ui.stonedew.next", "YOUR NEXT STEP");
      add("ui.stonedew.progress", "FIRST GARDEN");
      add("ui.stonedew.journal_hint", "Small steps. Healthy roots.");
      add(
          "ui.stonedew.care",
          "Plant a seed in a pot or bed. Water with the can; refill it at a water source. A fueled"
              + " lamp keeps your indoor garden growing.");
      add(
          "ui.stonedew.workshop",
          "Tents are placeable enclosures with room for your pots. Allow a clear 3 x 3 x 3 space."
              + " All grow lamps accept Glow Cells; one cell lasts 20 minutes.");
      add(
          "ui.stonedew.tent_note",
          "Fit a lamp in the upper center space. Tend your plants by hand and keep the lamp fueled"
              + " with Glow Cells.");
      add("ui.stonedew.no_automation", "Reinforced pots are watered by hand.");
      add("tooltip.stonedew.pot", "Plant one seed. Water by hand.");
      add("tooltip.stonedew.lamp", "Fuel with Glow Cells. 20 minutes per cell.");
      add("tooltip.stonedew.tent", "Place in a clear 3 x 3 x 3 space. Opening faces you.");
      add("tooltip.stonedew.tent_light", "Enclosure only — add your own fueled lamp.");
      add("ui.stonedew.directive", "CURRENT DIRECTIVE");
      add("ui.stonedew.plant", "Plant");
      add("ui.stonedew.water", "Water");
      add("ui.stonedew.light", "Light");
      add("ui.stonedew.close", "Esc — close the Ledger");
      add(
          "command.stonedew.demo_space",
          "The exhibit needs a clear 14 × 10 × 7 space nearby. Fly to an open area first; no"
              + " existing blocks were replaced.");
      add(
          "command.stonedew.demo_ready",
          "Grow room exhibit built nearby. Example plants show different stages; use your kit to"
              + " plant a fresh pot.");
      add(
          "command.stonedew.kit",
          "Starter kit supplied. Plant a seed, water it and fuel a hanging lamp.");
      add("command.stonedew.target", "Look at a planted pot or bed first.");
      add("command.stonedew.changed", "Updated the targeted tray.");
      add(
          "command.stonedew.deferred",
          "This debug operation requires a later gameplay system; no state was changed.");
      add("command.stonedew.invalid", "Invalid debug value.");
      add(
          "command.stonedew.timewarp",
          "Advanced the growth clock by %s day(s). Loaded plants update on their next scheduled"
              + " visit.");
      try {
        var narrative =
            com.google.gson.JsonParser.parseString(
                    java.nio.file.Files.readString(
                        java.nio.file.Path.of(System.getProperty("stonedew.narrativeSource"))))
                .getAsJsonObject();
        narrative.entrySet().forEach(entry -> add(entry.getKey(), entry.getValue().getAsString()));
      } catch (java.io.IOException e) {
        throw new java.io.UncheckedIOException(e);
      }
      add(ModContent.DEWSTONE.get(), "Dewstone");
      add(ModContent.GLOW_CELL.get(), "Glow Cell");
      add("wing.stonedew.base", "Stonedew");
      add("advancement.stonedew.root.title", "Stonedew");
      add("advancement.stonedew.root.description", "Obtain Dewstone.");
      add("command.stonedew.status", "Stonedew P1 | definitions: %s | difficulty: %s | dread: %s");
      add(
          "command.stonedew.story",
          "Keeper K-%s | Standing: %s | Attention: %s | debug probes: %s");
      add(
          "command.stonedew.probe",
          "Recorded one debug probe. Use /stonedew debug story to inspect persistence.");
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
