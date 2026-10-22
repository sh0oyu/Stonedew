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
    graphics.fill(goalX, 6, goalX + goalWidth, 23, 0xC91E1528);
    graphics.fill(goalX, 6, goalX + 2, 23, 0xFFB8693A);
    graphics.drawString(font, primary, goalX + 8, 11, 0xF2E8FF, false);
    var target = dev.stonedew.plant.TrayTargeting.find(client.level, client.player);
    if (target == null) return;
    var plant = target.tray().view(target.slot());
    if (plant == null) return;
    int x = width / 2 - 104, y = 29;
    graphics.fill(x - 1, y - 1, x + 209, y + 65, 0xB05A3A7A);
    graphics.fill(x, y, x + 208, y + 64, 0xEF1E1528);
    graphics.drawString(
        font,
        Component.translatable(
            "plant.stonedew.wild", Component.translatable("pigment.stonedew." + plant.pigment())),
        x + 8,
        y + 6,
        plant.bud(),
        false);
    graphics.drawString(
        font,
        Component.translatable(
            "hud.stonedew.stage",
            Component.translatable("stage.stonedew." + plant.stage()),
            plant.progress()),
        x + 8,
        y + 20,
        0xF2E8FF,
        false);
    graphics.fill(x + 8, y + 34, x + 200, y + 37, 0xFF3E3050);
    graphics.fill(x + 8, y + 34, x + 8 + 192 * plant.water() / 100, y + 37, 0xFF4FE8E0);
    graphics.drawString(
        font,
        Component.translatable("hud.stonedew.metrics", plant.water(), plant.light(), plant.vigor()),
        x + 8,
        y + 43,
        plant.water() < 20 ? 0xFFB347 : 0xBEAEC8,
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
        plant.water() < 20 ? 0xFFB347 : 0xBEAEC8,
        false);
  }

  private PlantHud() {}
}
