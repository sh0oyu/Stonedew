package dev.stonedew.client;

import com.mojang.blaze3d.systems.RenderSystem;
import dev.stonedew.Stonedew;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.resources.ResourceLocation;

/** Shared painted wood, hardware and parchment used by the HUD and Ledger. */
public final class PaintedUi {
  private static final ResourceLocation MATERIALS = Stonedew.id("textures/art/materials_v6.png");
  private static final ResourceLocation LEAF = Stonedew.id("textures/block/leaf_emblem.png");

  public static void material(GuiGraphics graphics, int cell, int x, int y, int width, int height) {
    int tile =
        switch (cell) {
          case 0 -> 2;
          case 4 -> 9;
          case 8 -> 12;
          default -> cell;
        };
    // The same inset material windows as the equipment; the source painting is unchanged.
    graphics.blit(
        MATERIALS,
        x,
        y,
        width,
        height,
        tile % 4 * 100F + 9.25F,
        tile / 4 * 100F + 9.25F,
        82,
        82,
        400,
        400);
    if (cell == 0) graphics.fill(x, y, x + width, y + height, 0x40352119);
  }

  public static void panel(GuiGraphics graphics, int x, int y, int width, int height) {
    graphics.fill(x + 2, y + 3, x + width + 2, y + height + 3, 0x800F1B13);
    material(graphics, 0, x, y, width, height);
    material(graphics, 4, x + 2, y + 2, width - 4, height - 4);
    material(graphics, 8, x + 3, y + 3, width - 6, height - 6);
    // Keep the painted parchment quiet enough for the small HUD type.
    graphics.fill(x + 3, y + 3, x + width - 3, y + height - 3, 0xD0E8D3AD);
  }

  public static void leaf(GuiGraphics graphics, int x, int y, int size) {
    RenderSystem.enableBlend();
    RenderSystem.defaultBlendFunc();
    graphics.blit(LEAF, x, y, size, size, 0F, 0F, 1, 1, 1, 1);
    RenderSystem.disableBlend();
  }

  private PaintedUi() {}
}
