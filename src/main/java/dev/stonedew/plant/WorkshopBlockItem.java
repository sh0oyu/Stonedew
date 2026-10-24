package dev.stonedew.plant;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.block.Block;

/** Short, honest descriptions for the newly available workshop equipment. */
public final class WorkshopBlockItem extends BlockItem {
  public WorkshopBlockItem(Block block, Properties properties) {
    super(block, properties);
  }

  @Override
  public void appendHoverText(
      ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flags) {
    super.appendHoverText(stack, context, lines, flags);
    if (getBlock() instanceof GrowTentBlock) {
      lines.add(Component.translatable("tooltip.stonedew.tent").withStyle(ChatFormatting.GREEN));
      lines.add(
          Component.translatable("tooltip.stonedew.tent_light").withStyle(ChatFormatting.GRAY));
    } else if (getBlock() instanceof GrowTrayBlock) {
      lines.add(Component.translatable("tooltip.stonedew.pot").withStyle(ChatFormatting.GRAY));
    } else if (getBlock() instanceof BulbLampBlock) {
      lines.add(Component.translatable("tooltip.stonedew.lamp").withStyle(ChatFormatting.GRAY));
    }
  }
}
