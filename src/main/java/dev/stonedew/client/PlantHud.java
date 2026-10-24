package dev.stonedew.client;

import dev.stonedew.core.PlayerProgress;
import net.minecraft.client.Minecraft;
import net.minecraft.network.chat.Component;
import net.neoforged.neoforge.client.event.RenderGuiEvent;

public final class PlantHud {
  private static long nextTargetQuery;
  private static java.lang.ref.WeakReference<net.minecraft.world.level.Level> targetLevel =
      new java.lang.ref.WeakReference<>(null);
  private static dev.stonedew.plant.TrayTargeting.Target cachedTarget;

  public static void render(RenderGuiEvent.Post event) {
    PlantRenderStats.frame();
    var c = Minecraft.getInstance();
    if (c.player == null || c.level == null || c.options.hideGui || c.screen != null) return;
    var g = event.getGuiGraphics();
    var f = c.font;
    Component goal = Component.translatable(PlayerProgress.clientDirective(c.player));
    int gw = Math.min(190, Math.min(g.guiWidth() - 20, Math.max(142, f.width(goal) + 28)));
    int lines = f.split(goal, gw - 30).size();
    PaintedUi.panel(g, 8, 8, gw, 20 + lines * 9);
    PaintedUi.leaf(g, 14, 13, 14);
    g.drawString(f, Component.translatable("ui.stonedew.brand"), 32, 13, PaintedUi.GREEN, false);
    g.drawWordWrap(f, goal, 16, 27, gw - 24, PaintedUi.CREAM);
    long now = System.nanoTime();
    if (targetLevel.get() != c.level || now >= nextTargetQuery) {
      cachedTarget = dev.stonedew.plant.TrayTargeting.find(c.level, c.player);
      targetLevel = new java.lang.ref.WeakReference<>(c.level);
      nextTargetQuery = now + 100_000_000L;
    }
    var target = cachedTarget;
    if (target == null) return;
    var p = target.tray().view(target.slot());
    if (p == null) return;
    int w = 178, x = g.guiWidth() - w - 8, y = g.guiHeight() - 112;
    PaintedUi.panel(g, x, y, w, 82);
    PaintedUi.leaf(g, x + 7, y + 7, 16);
    var name =
        Component.translatable(
            "plant.stonedew.wild", Component.translatable("pigment.stonedew." + p.pigment()));
    g.drawString(
        f, f.plainSubstrByWidth(name.getString(), w - 38), x + 28, y + 8, PaintedUi.GREEN, false);
    g.drawString(
        f,
        Component.translatable(
            "hud.stonedew.stage",
            Component.translatable("stage.stonedew." + p.stage()),
            p.progress()),
        x + 9,
        y + 24,
        PaintedUi.CREAM,
        false);
    PaintedUi.bar(g, x + 9, y + 36, w - 18, p.progress(), 0x9C79CC);
    int[] values = {p.water(), p.light(), p.vigor()};
    String[] labels = {"water", "light", "vigor"};
    int[] colors = {0x63BFC6, 0xB18BE1, 0x9DCC67};
    for (int i = 0; i < 3; i++) {
      int cx = x + 9 + i * 54;
      g.drawString(
          f, Component.translatable("ui.stonedew." + labels[i]), cx, y + 46, 0xC8B9A4, false);
      g.drawString(f, Integer.toString(values[i]), cx + 32, y + 46, colors[i], false);
      PaintedUi.bar(g, cx, y + 57, 48, values[i], colors[i]);
    }
    String status = p.water() < 20 ? "thirsty" : p.stage() == 3 ? "ripe" : "growing";
    g.drawString(
        f,
        Component.translatable("status.stonedew." + status),
        x + 9,
        y + 68,
        p.water() < 20 ? 0xEDAD6A : PaintedUi.CREAM,
        false);
    g.drawString(
        f,
        Component.translatable("hud.stonedew.humidity", p.humidity()),
        x + 99,
        y + 68,
        0xAA9DAD,
        false);
  }

  private PlantHud() {}
}
