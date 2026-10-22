package dev.stonedew.plant;

import dev.stonedew.core.ModContent;
import dev.stonedew.genetics.Genome;
import java.util.List;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;

public final class SeedItem extends Item {
  public SeedItem(Properties properties) {
    super(properties);
  }

  private InteractionResult sow(
      Level level, Player player, ItemStack stack, TrayTargeting.Target target) {
    if (target == null) return InteractionResult.PASS;
    var pos = target.tray().getBlockPos();
    if (!level.mayInteract(player, pos)
        || !player.mayUseItemAt(pos, net.minecraft.core.Direction.UP, stack))
      return InteractionResult.FAIL;
    if (!level.isClientSide) {
      var genome = stack.getOrDefault(ModContent.GENOME.get(), Genome.wild("violet", 0));
      if (!target.tray().plant(player, target.slot(), genome)) {
        player.displayClientMessage(Component.translatable("hint.stonedew.occupied"), true);
        return InteractionResult.FAIL;
      }
      if (!player.getAbilities().instabuild) stack.shrink(1);
      level.playSound(null, pos, SoundEvents.CROP_PLANTED, SoundSource.BLOCKS, 0.7F, 1.1F);
    }
    return InteractionResult.sidedSuccess(level.isClientSide);
  }

  @Override
  public InteractionResult useOn(UseOnContext context) {
    if (context.getPlayer() == null) return InteractionResult.PASS;
    TrayTargeting.Target target =
        context.getLevel().getBlockEntity(context.getClickedPos())
                instanceof GrowTrayBlockEntity tray
            ? new TrayTargeting.Target(tray, tray.slot(context.getClickLocation()))
            : TrayTargeting.find(context.getLevel(), context.getPlayer());
    return sow(context.getLevel(), context.getPlayer(), context.getItemInHand(), target);
  }

  @Override
  public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
    var stack = player.getItemInHand(hand);
    var target = TrayTargeting.find(level, player);
    if (target == null) return InteractionResultHolder.pass(stack);
    var result = sow(level, player, stack, target);
    return new InteractionResultHolder<>(result, stack);
  }

  @Override
  public void appendHoverText(
      ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
    var genome = stack.getOrDefault(ModContent.GENOME.get(), Genome.wild("violet", 0));
    lines.add(
        Component.translatable("pigment.stonedew." + genome.pigment())
            .withColor(genome.budColor()));
    lines.add(Component.translatable("hint.stonedew.seed"));
  }
}
