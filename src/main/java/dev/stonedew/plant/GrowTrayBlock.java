package dev.stonedew.plant;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BaseEntityBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

public final class GrowTrayBlock extends BaseEntityBlock {
  public static final MapCodec<GrowTrayBlock> CODEC =
      simpleCodec(properties -> new GrowTrayBlock(properties, 1));
  public static final BooleanProperty WET = BooleanProperty.create("wet");
  private final int slots;

  public GrowTrayBlock(Properties properties, int slots) {
    super(properties);
    this.slots = slots;
    registerDefaultState(stateDefinition.any().setValue(WET, false));
  }

  public int slots() {
    return slots;
  }

  @Override
  protected MapCodec<? extends BaseEntityBlock> codec() {
    return CODEC;
  }

  @Override
  protected RenderShape getRenderShape(BlockState state) {
    return RenderShape.MODEL;
  }

  @Override
  protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
    builder.add(WET);
  }

  @Override
  public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
    return new GrowTrayBlockEntity(pos, state);
  }

  @Override
  protected VoxelShape getShape(
      BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
    return slots == 1 ? Block.box(3, 0, 3, 13, 9, 13) : Block.box(0, 0, 0, 16, 14.7, 16);
  }

  @Override
  protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
    if (level.getBlockEntity(pos) instanceof GrowTrayBlockEntity tray) {
      tray.advance();
      if (tray.hasPlants()) level.scheduleTick(pos, this, tray.profile().updateInterval());
    }
  }

  @Override
  protected InteractionResult useWithoutItem(
      BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
    if (!player.getMainHandItem().isEmpty()) return InteractionResult.PASS;
    if (!level.isClientSide && level.getBlockEntity(pos) instanceof GrowTrayBlockEntity tray)
      tray.inspect(player, tray.slot(hit.getLocation()));
    return InteractionResult.sidedSuccess(level.isClientSide);
  }

  @Override
  protected void onRemove(
      BlockState state, Level level, BlockPos pos, BlockState replacement, boolean moving) {
    if (!state.is(replacement.getBlock())
        && !level.isClientSide
        && level.getBlockEntity(pos) instanceof GrowTrayBlockEntity tray) tray.dropSeeds();
    super.onRemove(state, level, pos, replacement, moving);
  }
}
