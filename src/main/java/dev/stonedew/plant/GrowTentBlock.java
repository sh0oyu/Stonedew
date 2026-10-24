package dev.stonedew.plant;

import com.mojang.serialization.MapCodec;
import dev.stonedew.core.ModContent;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.HorizontalDirectionalBlock;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/** A static, chunk-baked walk-in enclosure. Its interior remains available for pots. */
public final class GrowTentBlock extends HorizontalDirectionalBlock {
  public static final MapCodec<GrowTentBlock> CODEC = simpleCodec(p -> new GrowTentBlock(p, 1));
  private final int tier;

  public GrowTentBlock(Properties properties, int tier) {
    super(properties);
    this.tier = tier;
    registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH));
  }

  @Override
  protected MapCodec<? extends HorizontalDirectionalBlock> codec() {
    return CODEC;
  }

  @Override
  protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> b) {
    b.add(FACING);
  }

  @Override
  protected BlockState rotate(BlockState s, Rotation r) {
    return s.setValue(FACING, r.rotate(s.getValue(FACING)));
  }

  @Override
  protected BlockState mirror(BlockState s, Mirror m) {
    return rotate(s, m.getRotation(s.getValue(FACING)));
  }

  public static BlockPos offset(int index, Direction facing) {
    int x = index % 3, y = index / 9, z = index / 3 % 3;
    return switch (facing) {
      case EAST -> new BlockPos(-z, y, x);
      case SOUTH -> new BlockPos(-x, y, -z);
      case WEST -> new BlockPos(z, y, -x);
      default -> new BlockPos(x, y, z);
    };
  }

  public static boolean reserved(int index) {
    int x = index % 3, y = index / 9, z = index / 3 % 3;
    return !(x == 1 && z == 1) && (y == 2 || x != 1 || z != 0);
  }

  @Override
  public BlockState getStateForPlacement(BlockPlaceContext context) {
    Direction facing = context.getHorizontalDirection().getOpposite();
    for (int i = 0; i < 27; i++) {
      if (!reserved(i)) continue;
      BlockPos p = context.getClickedPos().offset(offset(i, facing));
      if (!context.getLevel().isInWorldBounds(p)
          || !context.getLevel().hasChunkAt(p)
          || !context.getLevel().getWorldBorder().isWithinBounds(p)
          || !context.getLevel().getBlockState(p).canBeReplaced()) return null;
    }
    return defaultBlockState().setValue(FACING, facing);
  }

  @Override
  public void setPlacedBy(
      Level level, BlockPos pos, BlockState state, LivingEntity player, ItemStack stack) {
    if (level.isClientSide) return;
    for (int i = 1; i < 27; i++)
      if (reserved(i))
        level.setBlock(
            pos.offset(offset(i, state.getValue(FACING))),
            ModContent.TENT_PART
                .get()
                .defaultBlockState()
                .setValue(GrowTentPartBlock.INDEX, i)
                .setValue(GrowTentPartBlock.TIER, tier)
                .setValue(FACING, state.getValue(FACING)),
            Block.UPDATE_ALL);
  }

  @Override
  protected void onRemove(
      BlockState state, Level level, BlockPos pos, BlockState replacement, boolean moving) {
    if (!state.is(replacement.getBlock()) && !level.isClientSide) {
      for (int i = 1; i < 27; i++) {
        BlockPos p = pos.offset(offset(i, state.getValue(FACING)));
        BlockState part = level.getBlockState(p);
        if (part.is(ModContent.TENT_PART.get())
            && part.getValue(GrowTentPartBlock.INDEX) == i
            && part.getValue(FACING) == state.getValue(FACING)) level.removeBlock(p, false);
      }
    }
    super.onRemove(state, level, pos, replacement, moving);
  }

  @Override
  protected VoxelShape getShape(
      BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
    return shape(tier, 0, state.getValue(FACING));
  }

  private static final java.util.Map<Integer, VoxelShape> SHAPES =
      new java.util.concurrent.ConcurrentHashMap<>();

  static VoxelShape shape(int tier, int index, Direction facing) {
    int key = tier * 108 + index * 4 + facing.get2DDataValue();
    return SHAPES.computeIfAbsent(key, ignored -> buildShape(tier, index, facing));
  }

  private static VoxelShape buildShape(int tier, int index, Direction facing) {
    // Cell-local collision follows the painted shell, never a solid 3x3 cube.
    double w = new double[] {0, 18, 24, 29, 34}[tier] / 16.0;
    double d = new double[] {0, 18, 20, 23, 26}[tier] / 16.0;
    double h = new double[] {0, 36, 37, 40, 43}[tier] / 16.0;
    double x = (3 - w) / 2, z = (3 - d) / 2, t = .10;
    List<AABB> walls =
        List.of(
            new AABB(x, 0, z, x + t, h, z + d), new AABB(x + w - t, 0, z, x + w, h, z + d),
            new AABB(x, 0, z + d - t, x + w, h, z + d), new AABB(x, h - .15, z, x + w, h, z + d),
            new AABB(x, 0, z, x + w, .12, z + d), new AABB(x, h - .35, z, x + w, h, z + t));
    int ox = index % 3, oy = index / 9, oz = index / 3 % 3;
    AABB cell = new AABB(ox, oy, oz, ox + 1, oy + 1, oz + 1);
    var shapes = new ArrayList<VoxelShape>();
    for (AABB wall : walls)
      if (wall.intersects(cell)) {
        AABB a = wall.intersect(cell).move(-ox, -oy, -oz);
        AABB r =
            switch (facing) {
              case EAST -> new AABB(1 - a.maxZ, a.minY, a.minX, 1 - a.minZ, a.maxY, a.maxX);
              case SOUTH ->
                  new AABB(1 - a.maxX, a.minY, 1 - a.maxZ, 1 - a.minX, a.maxY, 1 - a.minZ);
              case WEST -> new AABB(a.minZ, a.minY, 1 - a.maxX, a.maxZ, a.maxY, 1 - a.minX);
              default -> a;
            };
        shapes.add(Shapes.create(r));
      }
    return Shapes.or(Shapes.empty(), shapes.toArray(VoxelShape[]::new));
  }
}
