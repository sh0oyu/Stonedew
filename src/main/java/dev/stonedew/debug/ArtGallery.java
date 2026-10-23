package dev.stonedew.debug;

import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;

/** A checked, optional art exhibit. Display entities do not implement future-tier gameplay. */
public final class ArtGallery {
  public static int create(CommandContext<CommandSourceStack> context)
      throws CommandSyntaxException {
    var source = context.getSource();
    var player = source.getPlayerOrException();
    var level = source.getLevel();
    var origin = player.blockPosition().offset(4, 2, 4);
    for (BlockPos pos : BlockPos.betweenClosed(origin, origin.offset(17, 6, 13))) {
      if (!level.hasChunkAt(pos) || !level.getBlockState(pos).isAir()) {
        source.sendFailure(
            Component.literal(
                "Art gallery needs an empty, loaded 18 x 7 x 14 space starting four blocks"
                    + " east/south and two blocks above you."));
        return 0;
      }
    }
    for (int x = 0; x < 18; x++)
      for (int z = 0; z < 14; z++)
        level.setBlock(
            origin.offset(x, 0, z),
            (x == 0 || x == 17 || z == 0 || z == 13
                    ? Blocks.DARK_OAK_PLANKS
                    : Blocks.POLISHED_DEEPSLATE)
                .defaultBlockState(),
            Block.UPDATE_ALL);
    // Neutral backdrop allows inspecting the actual material colors without a shader pack.
    for (int x = 0; x < 18; x++)
      for (int y = 1; y <= 6; y++)
        level.setBlock(
            origin.offset(x, y, 13), Blocks.GRAY_CONCRETE.defaultBlockState(), Block.UPDATE_ALL);
    for (int tier = 0; tier < 4; tier++) {
      double x = origin.getX() + 14.5 - tier * 4;
      double y = origin.getY() + 1.5;
      double z = origin.getZ();
      // Working P1 pots keep their ordinary item models; future pots are labeled visual previews.
      display(
          source,
          x,
          y,
          z + 3.5,
          tier == 0
              ? "stonedew:clay_pot"
              : tier == 2 ? "stonedew:planter_bed" : "stonedew:glow_cell",
          tier == 1 ? 100 : tier == 3 ? 101 : -1);
      display(
          source, x, y + 2, z + 6.5, "stonedew:glow_cell", new int[] {102, 109, 103, 104}[tier]);
      display(source, x - .5, y, z + 9, "stonedew:glow_cell", 105 + tier);
      label(source, x, y + .1, z + 2.5, "POT " + (tier + 1));
      label(source, x, y + 1.3, z + 5.5, "UV " + (tier + 1));
      label(source, x + .3, y + .1, z + 8.4, "TENT " + (tier + 1) + " / ART PREVIEW");
    }
    label(
        source,
        origin.getX() + 8.5,
        origin.getY() + 1.7,
        origin.getZ() + .5,
        "REFERENCE ART GALLERY / Display models only; no automation");
    player.connection.teleport(origin.getX() + 8.5, origin.getY() + 3, origin.getZ() - 10.5, 0, 8);
    source.sendSuccess(
        () ->
            Component.literal(
                "Art gallery created. Future-tier pots, lamps and tents are display entities, not"
                    + " functional automation. Existing grow equipment remains in the Creative tab."
                    + " Gallery entities are tagged stonedew_art_preview."),
        false);
    return 1;
  }

  private static void display(
      CommandSourceStack source, double x, double y, double z, String item, int model) {
    String components =
        model < 0 ? "" : ",components:{\"minecraft:custom_model_data\":" + model + "}";
    run(
        source,
        "summon minecraft:item_display "
            + x
            + " "
            + y
            + " "
            + z
            + " {Tags:[\"stonedew_art_preview\"],view_range:2f,Rotation:[180f,0f],shadow_radius:0.65f,shadow_strength:0.75f,item_display:\"none\",item:{id:\""
            + item
            + "\",count:1"
            + components
            + "}}");
  }

  private static void label(CommandSourceStack source, double x, double y, double z, String text) {
    run(
        source,
        "summon minecraft:text_display "
            + x
            + " "
            + y
            + " "
            + z
            + " {Tags:[\"stonedew_art_preview\"],billboard:\"center\",alignment:\"center\",background:0,text:'{\"text\":\""
            + text
            + "\",\"color\":\"light_purple\"}',transformation:[0.32f,0f,0f,0f,0f,0.32f,0f,0f,0f,0f,0.32f,0f,0f,0f,0f,1f]}");
  }

  private static void run(CommandSourceStack source, String command) {
    source.getServer().getCommands().performPrefixedCommand(source.withSuppressedOutput(), command);
  }

  private ArtGallery() {}
}
