package dev.stonedew.client;

import dev.stonedew.core.ModContent;
import dev.stonedew.core.PlayerProgress;
import dev.stonedew.world.ledger.LedgerMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;

public final class LedgerScreen extends AbstractContainerScreen<LedgerMenu> {
  public LedgerScreen(LedgerMenu menu, Inventory inventory, Component title) {
    super(menu, inventory, title);
    imageWidth = 248;
    imageHeight = 186;
    titleLabelX = 46;
    titleLabelY = 15;
    inventoryLabelY = 1000;
  }

  @Override
  protected void renderBg(GuiGraphics graphics, float partial, int mouseX, int mouseY) {
    int x = leftPos, y = topPos;
    PaintedUi.panel(graphics, x - 3, y - 3, imageWidth + 6, imageHeight + 6);
    PaintedUi.material(graphics, 0, x + 3, y + 3, imageWidth - 6, 30);
    PaintedUi.leaf(graphics, x + 13, y + 6, 24);
    graphics.fill(x + 8, y + 33, x + imageWidth - 8, y + 34, 0xFF86522E);
    for (int dx : new int[] {5, imageWidth - 7})
      for (int dy : new int[] {5, imageHeight - 7})
        graphics.fill(x + dx, y + dy, x + dx + 2, y + dy + 2, 0xFFFFC247);
    graphics.drawString(
        font, Component.translatable("ui.stonedew.directive"), x + 18, y + 44, 0x315630, false);
    String directive = PlayerProgress.clientDirective(minecraft.player);
    graphics.drawWordWrap(
        font, Component.translatable(directive), x + 18, y + 62, imageWidth - 36, 0x503C29);
    graphics.fill(x + 18, y + 101, x + imageWidth - 18, y + 102, 0xFFBA965E);
    for (int dx : new int[] {14, 82, 150}) PaintedUi.panel(graphics, x + dx, y + 109, 64, 40);
    graphics.renderItem(ModContent.WILD_SEED.toStack(), x + 24, y + 114);
    graphics.renderItem(ModContent.WATERING_CAN.toStack(), x + 91, y + 114);
    graphics.renderItem(ModContent.BULB_LAMP.toStack(), x + 161, y + 114);
    graphics.drawString(
        font, Component.translatable("ui.stonedew.plant"), x + 20, y + 136, 0x503C29, false);
    graphics.drawString(
        font, Component.translatable("ui.stonedew.water"), x + 87, y + 136, 0x503C29, false);
    graphics.drawString(
        font, Component.translatable("ui.stonedew.light"), x + 160, y + 136, 0x503C29, false);
    graphics.drawString(
        font, Component.translatable("ui.stonedew.close"), x + 18, y + 160, 0x80664A, false);
  }

  @Override
  protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
    graphics.drawString(font, title, titleLabelX, titleLabelY, 0xFFE3AC, false);
  }
}
