package dev.stonedew.client;

import dev.stonedew.core.PlayerProgress;
import net.minecraft.client.Minecraft;
import net.minecraft.network.chat.Component;
import net.neoforged.neoforge.client.event.RenderGuiEvent;

public final class PlantHud {
  public static void render(RenderGuiEvent.Post event) {
    var client = Minecraft.getInstance();
    if (client.player == null
        || client.level == null
        || client.options.hideGui
        || client.screen != null) return;
    var graphics = event.getGuiGraphics();
    var font = client.font;
    int width = graphics.guiWidth();
    Component primary = Component.translatable(PlayerProgress.clientDirective(client.player));
    int goalWidth = Math.min(width - 20, font.width(primary) + 24), goalX = 8;
    PaintedUi.material(graphics, 0, goalX, 6, goalWidth, 17);
    graphics.fill(goalX, 6, goalX + 2, 23, 0xFFCA9854);
    graphics.drawString(font, primary, goalX + 8, 11, 0xFFEAC6, false);
    var target = dev.stonedew.plant.TrayTargeting.find(client.level, client.player);
    if (target == null) return;
    var plant = target.tray().view(target.slot());
    if (plant == null) return;
    int x = width - 216, y = 30;
    PaintedUi.panel(graphics, x, y, 208, 68);
    PaintedUi.leaf(graphics, x + 7, y + 4, 16);
    graphics.drawString(
        font,
        Component.translatable(
            "plant.stonedew.wild", Component.translatable("pigment.stonedew." + plant.pigment())),
        x + 27,
        y + 6,
        0x315630,
        false);
    graphics.drawString(
        font,
        Component.translatable(
            "hud.stonedew.stage",
            Component.translatable("stage.stonedew." + plant.stage()),
            plant.progress()),
        x + 8,
        y + 20,
        0x503C29,
        false);
    graphics.fill(x + 8, y + 34, x + 200, y + 37, 0xFF96784E);
    graphics.fill(x + 8, y + 34, x + 8 + 192 * plant.water() / 100, y + 37, 0xFF2A9585);
    graphics.drawString(
        font,
        Component.translatable("hud.stonedew.metrics", plant.water(), plant.light(), plant.vigor()),
        x + 8,
        y + 43,
        plant.water() < 20 ? 0xA23E26 : 0x624B34,
        false);
    graphics.drawString(
        font,
        Component.translatable(
            "hud.stonedew.condition",
            plant.humidity(),
            Component.translatable(
                plant.water() < 20
                    ? "status.stonedew.thirsty"
                    : plant.stage() == 3 ? "status.stonedew.ripe" : "status.stonedew.growing")),
        x + 8,
        y + 54,
        plant.water() < 20 ? 0xA23E26 : 0x624B34,
        false);
  }

  private PlantHud() {}
}
