package dev.stonedew.core;

import dev.stonedew.Stonedew;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModContent {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(Stonedew.ID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(Stonedew.ID);
    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, Stonedew.ID);
    public static final DeferredBlock<Block> DEWSTONE = BLOCKS.registerSimpleBlock("dewstone", BlockBehaviour.Properties.of()
            .mapColor(MapColor.COLOR_PURPLE).strength(1.5F, 6F).sound(SoundType.AMETHYST).lightLevel(state -> 4));
    public static final DeferredItem<BlockItem> DEWSTONE_ITEM = ITEMS.registerSimpleBlockItem(DEWSTONE);
    public static final DeferredItem<Item> GLOW_CELL = ITEMS.registerSimpleItem("glow_cell");
    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> TAB = TABS.register("main", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.stonedew"))
            .icon(() -> GLOW_CELL.get().getDefaultInstance())
            .displayItems((parameters, output) -> { output.accept(DEWSTONE_ITEM); output.accept(GLOW_CELL); })
            .build());

    public static void register(IEventBus bus) { BLOCKS.register(bus); ITEMS.register(bus); TABS.register(bus); }
    private ModContent() {}
}
