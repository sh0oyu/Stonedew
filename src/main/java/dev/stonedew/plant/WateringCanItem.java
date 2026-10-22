package dev.stonedew.plant;

import dev.stonedew.core.ModContent;
import dev.stonedew.data.DefinitionReloadListener;
import java.util.List;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.FluidTags;
import net.minecraft.world.*;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.*;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LayeredCauldronBlock;
import net.minecraft.world.phys.HitResult;

public final class WateringCanItem extends Item {
  public WateringCanItem(Properties properties) {
    super(properties);
  }

  private InteractionResult pour(
      Level level,
      Player player,
      ItemStack stack,
      InteractionHand hand,
      TrayTargeting.Target target) {
    if (target == null) return InteractionResult.PASS;
    var pos = target.tray().getBlockPos();
    if (!level.mayInteract(player, pos)
        || !player.mayUseItemAt(pos, net.minecraft.core.Direction.UP, stack))
      return InteractionResult.FAIL;
    int pours = stack.getOrDefault(ModContent.WATER.get(), 0);
    if (pours <= 0) {
      if (!level.isClientSide)
        player.displayClientMessage(Component.translatable("hint.stonedew.refill"), true);
      return InteractionResult.FAIL;
    }
    if (!level.isClientSide) {
      if (!target.tray().water(player, target.slot())) {
        player.displayClientMessage(
            Component.translatable(
                target.tray().plant(target.slot()) == null
                    ? "hint.stonedew.empty_tray"
                    : "hint.stonedew.already_wet"),
            true);
        return InteractionResult.FAIL;
      }
      if (!player.getAbilities().instabuild) stack.set(ModContent.WATER.get(), pours - 1);
    }
    player.startUsingItem(hand);
    return InteractionResult.sidedSuccess(level.isClientSide);
  }

  @Override
  public InteractionResult useOn(UseOnContext context) {
    var player = context.getPlayer();
    if (player == null) return InteractionResult.PASS;
    var level = context.getLevel();
    var pos = context.getClickedPos();
    if (level.getBlockState(pos).is(Blocks.WATER_CAULDRON)) {
      if (!level.mayInteract(player, pos)) return InteractionResult.FAIL;
      if (!level.isClientSide && isFull(context.getItemInHand())) return InteractionResult.FAIL;
      if (!level.isClientSide) {
        fill(context.getItemInHand());
        if (!player.getAbilities().instabuild)
          LayeredCauldronBlock.lowerFillLevel(level.getBlockState(pos), level, pos);
        level.playSound(null, pos, SoundEvents.BUCKET_FILL, SoundSource.BLOCKS, 0.7F, 1.1F);
      }
      return InteractionResult.sidedSuccess(level.isClientSide);
    }
    var target =
        level.getBlockEntity(pos) instanceof GrowTrayBlockEntity tray
            ? new TrayTargeting.Target(tray, tray.slot(context.getClickLocation()))
            : TrayTargeting.find(level, player);
    return pour(level, player, context.getItemInHand(), context.getHand(), target);
  }

  @Override
  public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
    var stack = player.getItemInHand(hand);
    var target = TrayTargeting.find(level, player);
    if (target != null)
      return new InteractionResultHolder<>(pour(level, player, stack, hand, target), stack);
    var hit = getPlayerPOVHitResult(level, player, ClipContext.Fluid.SOURCE_ONLY);
    if (hit.getType() == HitResult.Type.BLOCK
        && level.getFluidState(hit.getBlockPos()).is(FluidTags.WATER)) {
      if (!level.mayInteract(player, hit.getBlockPos())) return InteractionResultHolder.fail(stack);
      if (!level.isClientSide && isFull(stack)) return InteractionResultHolder.fail(stack);
      if (!level.isClientSide) {
        fill(stack);
        level.playSound(
            null, player.blockPosition(), SoundEvents.BUCKET_FILL, SoundSource.PLAYERS, 0.7F, 1.1F);
      }
      return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
    }
    return InteractionResultHolder.pass(stack);
  }

  private static boolean isFull(ItemStack stack) {
    return stack.getOrDefault(ModContent.WATER.get(), 0)
        >= DefinitionReloadListener.current().growthProfile("stonedew:herb").canPours();
  }

  private static void fill(ItemStack stack) {
    int capacity = DefinitionReloadListener.current().growthProfile("stonedew:herb").canPours();
    stack.set(ModContent.WATER_CAPACITY.get(), capacity);
    stack.set(ModContent.WATER.get(), capacity);
  }

  @Override
  public boolean shouldCauseReequipAnimation(
      ItemStack previous, ItemStack next, boolean slotChanged) {
    return slotChanged || !ItemStack.isSameItem(previous, next);
  }

  @Override
  public UseAnim getUseAnimation(ItemStack stack) {
    return UseAnim.NONE;
  }

  @Override
  public int getUseDuration(ItemStack stack, LivingEntity entity) {
    return 16;
  }

  @Override
  public void appendHoverText(
      ItemStack stack, TooltipContext context, List<Component> lines, TooltipFlag flag) {
    lines.add(
        Component.translatable("hint.stonedew.can", stack.getOrDefault(ModContent.WATER.get(), 0)));
    lines.add(Component.translatable("hint.stonedew.can_use"));
  }

  @Override
  public boolean isBarVisible(ItemStack stack) {
    return true;
  }

  @Override
  public int getBarWidth(ItemStack stack) {
    return Math.clamp(
        stack.getOrDefault(ModContent.WATER.get(), 0)
            * 13
            / stack.getOrDefault(
                ModContent.WATER_CAPACITY.get(), PlantTuning.defaults().canPours()),
        0,
        13);
  }

  @Override
  public int getBarColor(ItemStack stack) {
    return 0x4FE8E0;
  }
}
