package dev.stonedew.debug;

import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import dev.stonedew.core.ModContent;
import dev.stonedew.genetics.Genome;
import dev.stonedew.plant.*;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;

/**
 * Optional developer exhibit, built only in a verified clear, loaded volume. Never replaces
 * existing builds.
 */
public final class DebugShowcase {
  public static int create(CommandContext<CommandSourceStack> context)
      throws CommandSyntaxException {
    var source = context.getSource();
    var player = source.getPlayerOrException();
    var level = source.getLevel();
    BlockPos origin = player.blockPosition().offset(4, 2, 4);
    for (BlockPos pos : BlockPos.betweenClosed(origin, origin.offset(13, 6, 9)))
      if (!level.hasChunkAt(pos) || !level.getBlockState(pos).isAir()) {
        source.sendFailure(Component.translatable("command.stonedew.demo_space"));
        return 0;
      }
    for (int x = 0; x < 14; x++)
      for (int z = 0; z < 10; z++) {
        level.setBlock(
            origin.offset(x, 0, z),
            (x % 4 == 0 ? Blocks.DARK_OAK_PLANKS : Blocks.POLISHED_DEEPSLATE).defaultBlockState(),
            Block.UPDATE_ALL);
        level.setBlock(
            origin.offset(x, 6, z), Blocks.DEEPSLATE_TILES.defaultBlockState(), Block.UPDATE_ALL);
      }
    for (int y = 1; y < 6; y++)
      for (int x = 0; x < 14; x++)
        for (int z = 0; z < 10; z++)
          if (x == 0 || x == 13 || z == 0 || z == 9) {
            boolean doorway = z == 0 && x >= 6 && x <= 7 && y <= 3;
            if (doorway) continue;
            var block =
                (x == 0 || x == 13) && (z == 0 || z == 9)
                    ? Blocks.STRIPPED_DARK_OAK_LOG
                    : y >= 2 && y <= 4 && (x == 0 || x == 13) && z >= 2 && z <= 7
                        ? Blocks.GLASS
                        : Blocks.DEEPSLATE_BRICKS;
            level.setBlock(origin.offset(x, y, z), block.defaultBlockState(), Block.UPDATE_ALL);
          }
    for (int z : new int[] {2, 5, 8})
      for (int x = 0; x < 14; x++)
        level.setBlock(
            origin.offset(x, 5, z),
            Blocks.STRIPPED_DARK_OAK_LOG
                .defaultBlockState()
                .setValue(
                    net.minecraft.world.level.block.RotatedPillarBlock.AXIS,
                    net.minecraft.core.Direction.Axis.X),
            Block.UPDATE_ALL);
    for (int z : new int[] {0, 4, 9})
      for (int x : new int[] {0, 13})
        for (int y = 1; y <= 5; y++)
          level.setBlock(
              origin.offset(x, y, z),
              Blocks.STRIPPED_DARK_OAK_LOG.defaultBlockState(),
              Block.UPDATE_ALL);
    for (int x : new int[] {3, 6, 10})
      for (int z : new int[] {3, 7}) {
        BlockPos pos = origin.offset(x, 1, z);
        boolean bed = z == 7;
        level.setBlock(
            pos,
            (bed ? ModContent.PLANTER_BED : ModContent.CLAY_POT).get().defaultBlockState(),
            Block.UPDATE_ALL);
        var tray = (GrowTrayBlockEntity) level.getBlockEntity(pos);
        for (int slot = 0; slot < tray.capacity(); slot++) {
          String color = x == 3 ? "violet" : x == 6 ? "amber" : "teal";
          tray.plant(player, slot, Genome.wild(color, x * 100L + slot));
          tray.water(player, slot);
          tray.setStage(slot, bed ? 2 + (slot % 2) : x == 3 ? 0 : x == 6 ? 1 : 3);
        }
        BlockPos lamp = origin.offset(x, 4, z);
        level.setBlock(lamp, ModContent.BULB_LAMP.get().defaultBlockState(), Block.UPDATE_ALL);
        ((BulbLampBlockEntity) level.getBlockEntity(lamp)).fuel();
        level.setBlock(lamp.above(), Blocks.CHAIN.defaultBlockState(), Block.UPDATE_ALL);
      }
    level.setBlock(
        origin.offset(2, 1, 1), ModContent.LEDGER.get().defaultBlockState(), Block.UPDATE_ALL);
    level.setBlock(
        origin.offset(11, 1, 1),
        Blocks.WATER_CAULDRON
            .defaultBlockState()
            .setValue(net.minecraft.world.level.block.LayeredCauldronBlock.LEVEL, 3),
        Block.UPDATE_ALL);
    level.setBlock(origin.offset(1, 4, 1), Blocks.LANTERN.defaultBlockState(), Block.UPDATE_ALL);
    level.setBlock(origin.offset(12, 4, 8), Blocks.LANTERN.defaultBlockState(), Block.UPDATE_ALL);
    DebugCommands.kit(player);
    player.connection.teleport(origin.getX() + 6.5, origin.getY() + 1, origin.getZ() + 1.5, 0, 8);
    source.sendSuccess(() -> Component.translatable("command.stonedew.demo_ready"), false);
    return 1;
  }

  private DebugShowcase() {}
}
