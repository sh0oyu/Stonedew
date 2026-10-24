package dev.stonedew.plant;

import com.mojang.serialization.MapCodec;
import dev.stonedew.core.ModContent;
import dev.stonedew.core.PlayerProgress;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
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

public final class BulbLampBlock extends BaseEntityBlock {
  public static final MapCodec<BulbLampBlock> CODEC = simpleCodec(BulbLampBlock::new);
  public static final BooleanProperty LIT = BooleanProperty.create("lit");

  private final VoxelShape hull;

  public BulbLampBlock(Properties properties) {
    this(properties, Block.box(1, 1, 5, 15, 16, 11));
  }

  public BulbLampBlock(Properties properties, VoxelShape hull) {
    super(properties);
    this.hull = hull;
    registerDefaultState(stateDefinition.any().setValue(LIT, false));
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
    builder.add(LIT);
  }

  @Override
  public BlockEntity newBlockEntity(BlockPos pos, BlockState state) {
    return new BulbLampBlockEntity(pos, state);
  }

  @Override
  protected VoxelShape getShape(
      BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
    return hull;
  }

  @Override
  protected ItemInteractionResult useItemOn(
      ItemStack stack,
      BlockState state,
      Level level,
      BlockPos pos,
      Player player,
      InteractionHand hand,
      BlockHitResult hit) {
    if (!stack.is(ModContent.GLOW_CELL.get()))
      return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
    if (!level.isClientSide && level.getBlockEntity(pos) instanceof BulbLampBlockEntity lamp) {
      lamp.fuel();
      if (!player.getAbilities().instabuild) stack.shrink(1);
      PlayerProgress.mark(player, PlayerProgress.LIT);
    }
    return ItemInteractionResult.sidedSuccess(level.isClientSide);
  }

  @Override
  protected net.minecraft.world.InteractionResult useWithoutItem(
      BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
    if (!level.isClientSide)
      player.displayClientMessage(
          net.minecraft.network.chat.Component.translatable(
              state.getValue(LIT) ? "status.stonedew.lamp_running" : "status.stonedew.lamp_empty"),
          true);
    return net.minecraft.world.InteractionResult.sidedSuccess(level.isClientSide);
  }

  @Override
  protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
    if (level.getBlockEntity(pos) instanceof BulbLampBlockEntity lamp) lamp.advance();
  }

  @Override
  public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
    if (state.getValue(LIT)
        && dev.stonedew.core.StonedewConfig.ATMOSPHERE.get()
        && dev.stonedew.core.StonedewConfig.PARTICLE_BUDGET.get() > 0
        && random.nextInt(4) == 0)
      level.addParticle(
          new DustParticleOptions(new org.joml.Vector3f(0.69F, 0.3F, 1F), 0.65F),
          pos.getX() + 0.2 + random.nextDouble() * 0.6,
          pos.getY() + 0.2,
          pos.getZ() + 0.5,
          0,
          -0.005,
          0);
  }
}
