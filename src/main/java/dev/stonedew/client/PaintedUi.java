package dev.stonedew.client;

import com.mojang.blaze3d.systems.RenderSystem;
import dev.stonedew.Stonedew;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.resources.ResourceLocation;

/** Shared painted wood, copper and parchment used by the HUD and Ledger. */
public final class PaintedUi {
  private static final ResourceLocation MATERIALS =
      Stonedew.id("textures/art/painted_materials.png");
  private static final ResourceLocation LEAF = Stonedew.id("textures/art/leaf_fan.png");

  public static void material(GuiGraphics graphics, int cell, int x, int y, int width, int height) {
    // UV coordinate units are normalized to the 4x4 sheet, independent of source resolution.
    graphics.blit(
        MATERIALS, x, y, width, height, cell % 4 * 100F + 2, cell / 4 * 100F + 2, 96, 96, 400, 400);
  }

  public static void panel(GuiGraphics graphics, int x, int y, int width, int height) {
    graphics.fill(x + 2, y + 3, x + width + 2, y + height + 3, 0x800F1B13);
    material(graphics, 0, x, y, width, height);
    material(graphics, 4, x + 2, y + 2, width - 4, height - 4);
    material(graphics, 8, x + 3, y + 3, width - 6, height - 6);
  }

  public static void leaf(GuiGraphics graphics, int x, int y, int size) {
    RenderSystem.enableBlend();
    RenderSystem.defaultBlendFunc();
    graphics.blit(LEAF, x, y, size, size, 0F, 0F, 1, 1, 1, 1);
    RenderSystem.disableBlend();
  }

  private PaintedUi() {}
}
