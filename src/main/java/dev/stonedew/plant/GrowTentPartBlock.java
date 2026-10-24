package dev.stonedew.plant;

import com.mojang.serialization.MapCodec;
import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.RenderShape;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/** Invisible shell cells share one model and one dropped tent item. No block entities. */
public final class GrowTentPartBlock extends HorizontalDirectionalBlock {
  public static final MapCodec<GrowTentPartBlock> CODEC = simpleCodec(GrowTentPartBlock::new);
  public static final IntegerProperty INDEX = IntegerProperty.create("part", 1, 26);
  public static final IntegerProperty TIER = IntegerProperty.create("tier", 1, 4);

  public GrowTentPartBlock(Properties p) {
    super(p);
  }

  @Override
  protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
    return CODEC;
  }

  @Override
  protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> b) {
    b.add(FACING, INDEX, TIER);
  }

  @Override
  protected RenderShape getRenderShape(BlockState s) {
    return RenderShape.INVISIBLE;
  }

  @Override
  protected VoxelShape getShape(BlockState s, BlockGetter l, BlockPos p, CollisionContext c) {
    return GrowTentBlock.shape(s.getValue(TIER), s.getValue(INDEX), s.getValue(FACING));
  }

  private static BlockPos anchor(BlockState s, BlockPos p) {
    return p.subtract(GrowTentBlock.offset(s.getValue(INDEX), s.getValue(FACING)));
  }

  @Override
  public BlockState playerWillDestroy(Level l, BlockPos p, BlockState s, Player player) {
    if (!l.isClientSide && player.isCreative()) l.destroyBlock(anchor(s, p), false, player);
    return super.playerWillDestroy(l, p, s, player);
  }

  @Override
  protected void onRemove(BlockState s, Level l, BlockPos p, BlockState next, boolean moving) {
    if (!s.is(next.getBlock()) && !l.isClientSide) {
      BlockPos a = anchor(s, p);
      if (l.getBlockState(a).getBlock() instanceof GrowTentBlock) l.destroyBlock(a, true);
    }
    super.onRemove(s, l, p, next, moving);
  }

  @Override
  public ItemStack getCloneItemStack(
      BlockState s,
      HitResult target,
      net.minecraft.world.level.LevelReader l,
      BlockPos p,
      Player player) {
    BlockState root = l.getBlockState(anchor(s, p));
    return root.getBlock() instanceof GrowTentBlock
        ? new ItemStack(root.getBlock())
        : ItemStack.EMPTY;
  }
}
