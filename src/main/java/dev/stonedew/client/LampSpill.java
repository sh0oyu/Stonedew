package dev.stonedew.client;

import com.mojang.blaze3d.vertex.PoseStack;
import dev.stonedew.Stonedew;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.Level;

/** Soft violet bounce on loaded receiving surfaces below a fueled UV fixture. */
final class LampSpill {
  private record Patch(float x, float y, float z, float alpha) {}

  private record Visit(long tick, List<Patch> patches) {}

  private static java.lang.ref.WeakReference<Level> currentLevel =
      new java.lang.ref.WeakReference<>(null);
  private static final java.util.Map<Long, Visit> CACHE = new java.util.HashMap<>();

  static void render(Level level, BlockPos lamp, PoseStack pose, MultiBufferSource buffers) {
    if (currentLevel.get() != level) {
      currentLevel = new java.lang.ref.WeakReference<>(level);
      CACHE.clear();
    }
    var visit = CACHE.get(lamp.asLong());
    if (visit == null || level.getGameTime() - visit.tick() >= 10) {
      visit = new Visit(level.getGameTime(), collect(level, lamp));
      if (CACHE.size() > 256) CACHE.clear();
      CACHE.put(lamp.asLong(), visit);
    }
    var vertices =
        buffers.getBuffer(
            RenderType.entityTranslucentEmissive(Stonedew.id("textures/effect/lamp_halo.png")));
    float radius = 1.65F;
    for (var patch : visit.patches()) {
      float x = patch.x(), z = patch.z(), y = patch.y();
      float[][] corners = {{x, y, z + 1}, {x + 1, y, z + 1}, {x + 1, y, z}, {x, y, z}};
      for (var c : corners) {
        float u = (c[0] - .5F) / (radius * 2) + .5F, v = (c[2] - .5F) / (radius * 2) + .5F;
        vertices
            .addVertex(pose.last(), c[0], c[1], c[2])
            .setColor(220, 175, 255, (int) (patch.alpha() * 255))
            .setUv(u, v)
            .setOverlay(OverlayTexture.NO_OVERLAY)
            .setLight(LightTexture.FULL_BRIGHT)
            .setNormal(pose.last(), 0, 1, 0);
      }
    }
  }

  private static List<Patch> collect(Level level, BlockPos lamp) {
    var result = new ArrayList<Patch>();
    for (int x = -1; x <= 1; x++)
      for (int z = -1; z <= 1; z++)
        for (int down = 1; down <= 5; down++) {
          var pos = lamp.offset(x, -down, z);
          if (!level.hasChunkAt(pos)) break;
          var state = level.getBlockState(pos);
          var shape = state.getCollisionShape(level, pos);
          if (shape.isEmpty()) continue;
          // Partial objects are shaded by the plant pass; project only onto actual full receiving
          // floors.
          if (shape.max(net.minecraft.core.Direction.Axis.Y) >= .99)
            result.add(new Patch(x, -down + 1.006F, z, .55F * (1 - down * .10F)));
          break;
        }
    return List.copyOf(result);
  }

  private LampSpill() {}
}
