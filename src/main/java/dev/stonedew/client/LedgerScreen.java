package dev.stonedew.client;

import dev.stonedew.core.ModContent;
import dev.stonedew.core.PlayerProgress;
import dev.stonedew.world.ledger.LedgerMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.narration.NarrationElementOutput;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;

public final class LedgerScreen extends AbstractContainerScreen<LedgerMenu> {
  private int page;
  private static final String[] PAGES = {"overview", "growing", "equipment"};

  public LedgerScreen(LedgerMenu menu, Inventory inventory, Component title) {
    super(menu, inventory, title);
    imageWidth = 324;
    imageHeight = 216;
    inventoryLabelY = 1000;
  }

  @Override
  protected void init() {
    super.init();
    for (int i = 0; i < 3; i++) {
      final int tab = i;
      addRenderableWidget(
          new AbstractButton(
              leftPos + 15,
              topPos + 52 + i * 43,
              65,
              31,
              Component.translatable("ui.stonedew." + PAGES[i])) {
            @Override
            public void onPress() {
              page = tab;
            }

            @Override
            protected void renderWidget(GuiGraphics g, int mx, int my, float partial) {
              boolean active = page == tab;
              if (active || isHoveredOrFocused()) {
                g.fill(
                    getX(),
                    getY(),
                    getX() + width,
                    getY() + height,
                    active ? 0xD04C365B : 0x9042354D);
                g.fill(
                    getX(), getY(), getX() + 2, getY() + height, active ? 0xFFB7D67B : 0xFFAD8ACB);
              }
              g.drawString(
                  font,
                  getMessage(),
                  getX() + 6,
                  getY() + 11,
                  active ? PaintedUi.GREEN : PaintedUi.CREAM,
                  false);
            }

            @Override
            protected void updateWidgetNarration(NarrationElementOutput out) {
              defaultButtonNarrationText(out);
            }
          });
    }
  }

  private void text(GuiGraphics g, String key, int x, int y, int color) {
    g.drawString(font, Component.translatable(key), x, y, color, false);
  }

  @Override
  protected void renderBg(GuiGraphics g, float partial, int mx, int my) {
    int x = leftPos, y = topPos, cx = x + 98, cw = 205;
    PaintedUi.journal(g, x, y, imageWidth, imageHeight);
    g.pose().pushPose();
    g.pose().translate(x + 49, y + 15, 0);
    g.pose().scale(1.35F, 1.35F, 1);
    text(g, "ui.stonedew.brand", 0, 0, PaintedUi.CREAM);
    g.pose().popPose();
    text(g, "ui.stonedew.journal", x + 49, y + 30, 0xC4A77F);
    String keeper = font.plainSubstrByWidth(minecraft.player.getName().getString(), cw - 75);
    g.drawString(font, keeper, cx, y + 49, 0x64503F, false);
    text(g, "ui.stonedew." + PAGES[page], cx, y + 64, 0x38582E);
    g.fill(cx, y + 78, cx + cw, y + 79, 0xFFBBA17A);
    if (page == 0) {
      text(g, "ui.stonedew.next", cx, y + 88, 0x806C53);
      g.drawWordWrap(
          font,
          Component.translatable(PlayerProgress.clientDirective(minecraft.player)),
          cx,
          y + 102,
          cw,
          PaintedUi.INK);
      text(g, "ui.stonedew.progress", cx, y + 133, 0x806C53);
      int flags = PlayerProgress.flags(minecraft.player);
      for (int i = 0; i < 4; i++) {
        int px = cx + i * 51;
        boolean done = (flags & (1 << i)) != 0;
        g.fill(px, y + 148, px + 43, y + 151, done ? 0xFF6F9250 : 0xFFB6A58A);
        text(
            g,
            "ui.stonedew." + new String[] {"plant", "water", "light", "grow"}[i],
            px,
            y + 158,
            done ? 0x406337 : 0x806D58);
      }
      text(g, "ui.stonedew.journal_hint", cx, y + 181, 0x816B51);
    } else if (page == 1) {
      g.drawWordWrap(
          font, Component.translatable("ui.stonedew.care"), cx, y + 89, cw, PaintedUi.INK);
      ItemStack[] items = {
        ModContent.WILD_SEED.toStack(),
        ModContent.WATERING_CAN.toStack(),
        ModContent.BULB_LAMP.toStack()
      };
      for (int i = 0; i < 3; i++) {
        int px = cx + i * 67;
        g.fill(px, y + 151, px + 57, y + 182, 0x3087664C);
        g.renderItem(items[i], px + 20, y + 155);
        text(
            g,
            "ui.stonedew." + new String[] {"plant", "water", "light"}[i],
            px + 12,
            y + 183,
            PaintedUi.INK);
      }
    } else {
      g.drawWordWrap(
          font, Component.translatable("ui.stonedew.workshop"), cx, y + 88, cw, PaintedUi.INK);
      g.drawWordWrap(
          font, Component.translatable("ui.stonedew.tent_note"), cx, y + 133, cw, 0x806C53);
      ItemStack[] items = {
        ModContent.FABRIC_POT.toStack(),
        ModContent.REINFORCED_POT.toStack(),
        ModContent.UV_PANEL_4.toStack(),
        ModContent.TENT_2.toStack(),
        ModContent.TENT_4.toStack()
      };
      for (int i = 0; i < items.length; i++) g.renderItem(items[i], cx + 6 + i * 40, y + 179);
    }
    text(g, "ui.stonedew.close", x + 98, y + 202, 0xCBB58D);
  }

  @Override
  protected void renderLabels(GuiGraphics g, int mx, int my) {}
}
