package dev.stonedew.world.ledger;

import dev.stonedew.core.PlayerProgress;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.ContainerLevelAccess;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

public final class LedgerBlock extends Block {
  public LedgerBlock(Properties properties) {
    super(properties);
  }

  @Override
  protected InteractionResult useWithoutItem(
      BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
    if (player instanceof ServerPlayer server) {
      PlayerProgress.sync(server);
      server.openMenu(
          new SimpleMenuProvider(
              (id, inventory, who) ->
                  new LedgerMenu(id, inventory, ContainerLevelAccess.create(level, pos)),
              Component.translatable("block.stonedew.ledger")));
    }
    return InteractionResult.sidedSuccess(level.isClientSide);
  }
}
