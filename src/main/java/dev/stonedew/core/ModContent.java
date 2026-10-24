package dev.stonedew.core;

import com.mojang.serialization.Codec;
import dev.stonedew.Stonedew;
import dev.stonedew.genetics.Genome;
import dev.stonedew.genetics.GenomeCodecs;
import dev.stonedew.plant.*;
import dev.stonedew.world.ledger.*;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.world.flag.FeatureFlags;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.item.*;
import net.minecraft.world.level.block.*;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.*;

public final class ModContent {
  public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(Stonedew.ID);
  public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(Stonedew.ID);
  public static final DeferredRegister<CreativeModeTab> TABS =
      DeferredRegister.create(Registries.CREATIVE_MODE_TAB, Stonedew.ID);
  public static final DeferredRegister<DataComponentType<?>> COMPONENTS =
      DeferredRegister.create(Registries.DATA_COMPONENT_TYPE, Stonedew.ID);
  public static final DeferredRegister<BlockEntityType<?>> ENTITIES =
      DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, Stonedew.ID);
  public static final DeferredRegister<MenuType<?>> MENUS =
      DeferredRegister.create(Registries.MENU, Stonedew.ID);
  public static final DeferredHolder<DataComponentType<?>, DataComponentType<Genome>> GENOME =
      COMPONENTS.register(
          "genome",
          () ->
              DataComponentType.<Genome>builder()
                  .persistent(GenomeCodecs.CODEC)
                  .networkSynchronized(GenomeCodecs.STREAM_CODEC)
                  .build());
  public static final DeferredHolder<DataComponentType<?>, DataComponentType<Integer>> WATER =
      COMPONENTS.register(
          "water",
          () ->
              DataComponentType.<Integer>builder()
                  .persistent(Codec.intRange(0, 1024))
                  .networkSynchronized(ByteBufCodecs.VAR_INT)
                  .build());
  public static final DeferredHolder<DataComponentType<?>, DataComponentType<Integer>>
      WATER_CAPACITY =
          COMPONENTS.register(
              "water_capacity",
              () ->
                  DataComponentType.<Integer>builder()
                      .persistent(Codec.intRange(1, 1024))
                      .networkSynchronized(ByteBufCodecs.VAR_INT)
                      .build());
  public static final DeferredBlock<Block> DEWSTONE =
      BLOCKS.registerSimpleBlock(
          "dewstone",
          BlockBehaviour.Properties.of()
              .mapColor(MapColor.COLOR_PURPLE)
              .strength(1.5F, 6F)
              .sound(SoundType.AMETHYST)
              .lightLevel(state -> 4));
  public static final DeferredBlock<GrowTrayBlock> CLAY_POT =
      BLOCKS.register(
          "clay_pot",
          () ->
              new GrowTrayBlock(
                  BlockBehaviour.Properties.of()
                      .mapColor(MapColor.TERRACOTTA_ORANGE)
                      .strength(1.0F)
                      .sound(SoundType.DECORATED_POT)
                      .noOcclusion(),
                  1));
  public static final DeferredBlock<GrowTrayBlock> PLANTER_BED =
      BLOCKS.register(
          "planter_bed",
          () ->
              new GrowTrayBlock(
                  BlockBehaviour.Properties.of()
                      .mapColor(MapColor.WOOD)
                      .strength(2.0F)
                      .sound(SoundType.WOOD)
                      .noOcclusion(),
                  4));
  public static final DeferredBlock<BulbLampBlock> BULB_LAMP =
      BLOCKS.register(
          "bulb_lamp",
          () ->
              new BulbLampBlock(
                  BlockBehaviour.Properties.of()
                      .mapColor(MapColor.COLOR_PURPLE)
                      .strength(1.5F)
                      .sound(SoundType.LANTERN)
                      .noOcclusion()
                      .lightLevel(state -> state.getValue(BulbLampBlock.LIT) ? 12 : 0)));
  public static final DeferredBlock<LedgerBlock> LEDGER =
      BLOCKS.register(
          "ledger",
          () ->
              new LedgerBlock(
                  BlockBehaviour.Properties.of()
                      .mapColor(MapColor.COLOR_BROWN)
                      .strength(2F)
                      .sound(SoundType.WOOD)
                      .noOcclusion()));
  public static final DeferredBlock<GrowTrayBlock> WOODEN_PLANTER =
      BLOCKS.register(
          "wooden_planter",
          () ->
              new GrowTrayBlock(
                  BlockBehaviour.Properties.of()
                      .mapColor(MapColor.WOOD)
                      .strength(2F)
                      .sound(SoundType.WOOD)
                      .noOcclusion(),
                  1,
                  13.6F / 16));
  public static final DeferredBlock<GrowTrayBlock> FABRIC_POT =
      BLOCKS.register(
          "fabric_pot",
          () ->
              new GrowTrayBlock(
                  BlockBehaviour.Properties.of().strength(1F).sound(SoundType.WOOL).noOcclusion(),
                  1,
                  10F / 16));
  public static final DeferredBlock<GrowTrayBlock> REINFORCED_POT =
      BLOCKS.register(
          "reinforced_pot",
          () ->
              new GrowTrayBlock(
                  BlockBehaviour.Properties.of().strength(2F).sound(SoundType.METAL).noOcclusion(),
                  1,
                  12.4F / 16));
  public static final DeferredBlock<BulbLampBlock> UV_PENDANT = catalogLamp("uv_pendant");
  public static final DeferredBlock<BulbLampBlock> UV_PANEL_4 = catalogLamp("uv_panel_4");
  public static final DeferredBlock<BulbLampBlock> UV_PANEL_6 = catalogLamp("uv_panel_6");
  public static final DeferredBlock<GrowTentBlock> TENT_1 = tent("grow_tent_1", 1);
  public static final DeferredBlock<GrowTentBlock> TENT_2 = tent("grow_tent_2", 2);
  public static final DeferredBlock<GrowTentBlock> TENT_3 = tent("grow_tent_3", 3);
  public static final DeferredBlock<GrowTentBlock> TENT_4 = tent("grow_tent_4", 4);
  public static final DeferredBlock<GrowTentPartBlock> TENT_PART =
      BLOCKS.register(
          "grow_tent_part",
          () ->
              new GrowTentPartBlock(
                  BlockBehaviour.Properties.of()
                      .strength(1.5F)
                      .sound(SoundType.WOOL)
                      .noOcclusion()
                      .noLootTable()));
  public static final java.util.List<DeferredBlock<? extends Block>> CATALOG =
      java.util.List.of(
          WOODEN_PLANTER,
          FABRIC_POT,
          REINFORCED_POT,
          UV_PENDANT,
          UV_PANEL_4,
          UV_PANEL_6,
          TENT_1,
          TENT_2,
          TENT_3,
          TENT_4);
  private static final java.util.List<DeferredItem<BlockItem>> CATALOG_ITEMS =
      CATALOG.stream()
          .map(
              block ->
                  ITEMS.<BlockItem>register(
                      block.getId().getPath(),
                      () -> new WorkshopBlockItem(block.get(), new Item.Properties())))
          .toList();

  private static DeferredBlock<BulbLampBlock> catalogLamp(String name) {
    return BLOCKS.register(
        name,
        () ->
            new BulbLampBlock(
                BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(1.5F)
                    .sound(SoundType.LANTERN)
                    .noOcclusion()
                    .lightLevel(state -> state.getValue(BulbLampBlock.LIT) ? 12 : 0),
                switch (name) {
                  case "uv_pendant" -> Block.box(4, 0, 4, 12, 12, 12);
                  case "uv_panel_4" -> Block.box(-1, 4, 1, 17, 13, 15);
                  default -> Block.box(-3.5, 4, -1, 19.5, 13, 17);
                }));
  }

  private static DeferredBlock<GrowTentBlock> tent(String name, int tier) {
    return BLOCKS.register(
        name,
        () ->
            new GrowTentBlock(
                BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(1.5F)
                    .sound(SoundType.WOOL)
                    .noOcclusion(),
                tier));
  }

  public static final DeferredItem<BlockItem> DEWSTONE_ITEM =
      ITEMS.registerSimpleBlockItem(DEWSTONE);
  public static final DeferredItem<BlockItem> CLAY_POT_ITEM =
      ITEMS.registerSimpleBlockItem(CLAY_POT);
  public static final DeferredItem<BlockItem> PLANTER_BED_ITEM =
      ITEMS.registerSimpleBlockItem(PLANTER_BED);
  public static final DeferredItem<BlockItem> BULB_LAMP_ITEM =
      ITEMS.registerSimpleBlockItem(BULB_LAMP);
  public static final DeferredItem<BlockItem> LEDGER_ITEM = ITEMS.registerSimpleBlockItem(LEDGER);
  public static final DeferredItem<Item> GLOW_CELL = ITEMS.registerSimpleItem("glow_cell");
  public static final DeferredItem<SeedItem> WILD_SEED =
      ITEMS.register(
          "wild_seed",
          () ->
              new SeedItem(
                  new Item.Properties().component(GENOME.get(), Genome.wild("violet", 0))));
  public static final DeferredItem<WateringCanItem> WATERING_CAN =
      ITEMS.register(
          "watering_can",
          () ->
              new WateringCanItem(
                  new Item.Properties()
                      .stacksTo(1)
                      .component(WATER.get(), 0)
                      .component(WATER_CAPACITY.get(), PlantTuning.defaults().canPours())));
  public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<GrowTrayBlockEntity>>
      GROW_TRAY =
          ENTITIES.register(
              "grow_tray",
              () ->
                  BlockEntityType.Builder.of(
                          GrowTrayBlockEntity::new,
                          CLAY_POT.get(),
                          PLANTER_BED.get(),
                          WOODEN_PLANTER.get(),
                          FABRIC_POT.get(),
                          REINFORCED_POT.get())
                      .build(null));
  public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<BulbLampBlockEntity>>
      LAMP_ENTITY =
          ENTITIES.register(
              "bulb_lamp",
              () ->
                  BlockEntityType.Builder.of(
                          BulbLampBlockEntity::new,
                          BULB_LAMP.get(),
                          UV_PENDANT.get(),
                          UV_PANEL_4.get(),
                          UV_PANEL_6.get())
                      .build(null));
  public static final DeferredHolder<MenuType<?>, MenuType<LedgerMenu>> LEDGER_MENU =
      MENUS.register("ledger", () -> new MenuType<>(LedgerMenu::new, FeatureFlags.DEFAULT_FLAGS));
  public static final DeferredHolder<CreativeModeTab, CreativeModeTab> TAB =
      TABS.register(
          "main",
          () ->
              CreativeModeTab.builder()
                  .title(Component.translatable("itemGroup.stonedew"))
                  .icon(() -> CLAY_POT_ITEM.get().getDefaultInstance())
                  .displayItems(
                      (parameters, output) -> {
                        output.accept(CLAY_POT_ITEM);
                        output.accept(PLANTER_BED_ITEM);
                        output.accept(BULB_LAMP_ITEM);
                        output.accept(LEDGER_ITEM);
                        CATALOG_ITEMS.forEach(item -> output.accept(item));
                        for (String pigment :
                            java.util.List.of("violet", "teal", "amber", "green")) {
                          var seed = WILD_SEED.toStack();
                          seed.set(GENOME.get(), Genome.wild(pigment, 0));
                          output.accept(seed);
                        }
                        var can = WATERING_CAN.toStack();
                        can.set(WATER.get(), PlantTuning.defaults().canPours());
                        output.accept(can);
                        output.accept(GLOW_CELL);
                        output.accept(DEWSTONE_ITEM);
                      })
                  .build());

  public static void register(IEventBus bus) {
    COMPONENTS.register(bus);
    BLOCKS.register(bus);
    ITEMS.register(bus);
    ENTITIES.register(bus);
    MENUS.register(bus);
    TABS.register(bus);
  }

  private ModContent() {}
}
