package dev.stonedew.client;

import com.mojang.blaze3d.systems.RenderSystem;
import dev.stonedew.Stonedew;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.resources.ResourceLocation;

/** A quiet, shared walnut / violet / copper identity. Text always has a flat backdrop. */
public final class PaintedUi {
  public static final int INK = 0x503C36, CREAM = 0xF4E4C3, GREEN = 0xA8CE68, VIOLET = 0xA783CF;
  private static final ResourceLocation LEAF = Stonedew.id("textures/block/leaf_emblem.png");
  private static final ResourceLocation JOURNAL = Stonedew.id("textures/art/journal_v9.png");

  public static void journal(GuiGraphics g, int x, int y, int w, int h) {
    g.blit(JOURNAL, x, y, w, h, 0, 0, 1, 1, 1, 1);
  }

  public static void panel(GuiGraphics g, int x, int y, int w, int h) {
    g.fill(x + 2, y + 3, x + w + 2, y + h + 3, 0x780C111D);
    g.fill(x, y, x + w, y + h, 0xF01D1929);
    g.fill(x + 1, y + 1, x + w - 1, y + 2, 0xFFAF89D0);
    g.fill(x + 1, y + 2, x + w - 1, y + h - 1, 0xEB302638);
    g.fill(x + 3, y + 4, x + w - 3, y + h - 3, 0xEB252331);
    for (int dx : new int[] {2, w - 4})
      for (int dy : new int[] {2, h - 4})
        g.fill(x + dx, y + dy, x + dx + 2, y + dy + 2, 0xFFBD905A);
  }

  public static void bar(GuiGraphics g, int x, int y, int w, int value, int color) {
    g.fill(x, y, x + w, y + 4, 0xFF171720);
    g.fill(
        x + 1, y + 1, x + 1 + (w - 2) * Math.clamp(value, 0, 100) / 100, y + 3, 0xFF000000 | color);
  }

  public static void leaf(GuiGraphics g, int x, int y, int size) {
    RenderSystem.enableBlend();
    RenderSystem.defaultBlendFunc();
    g.blit(LEAF, x, y, size, size, 0, 0, 1, 1, 1, 1);
    RenderSystem.disableBlend();
  }

  private PaintedUi() {}
}
