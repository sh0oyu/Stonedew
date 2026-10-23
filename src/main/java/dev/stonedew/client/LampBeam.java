package dev.stonedew.client;

import com.mojang.blaze3d.vertex.PoseStack;
import dev.stonedew.Stonedew;
import dev.stonedew.core.StonedewConfig;
import java.util.HashMap;
import java.util.Map;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;

/** Subtle, bounded light shaft; respects receiving geometry and the atmosphere setting. */
final class LampBeam {
  private record Depth(long tick, float distance) {}

  private static final Map<Long, Depth> CACHE = new HashMap<>();
  private static java.lang.ref.WeakReference<Level> current =
      new java.lang.ref.WeakReference<>(null);

  static void render(Level level, BlockPos lamp, PoseStack pose, MultiBufferSource buffers) {
    if (current.get() != level) {
      current = new java.lang.ref.WeakReference<>(level);
      CACHE.clear();
    }
    Depth depth = CACHE.get(lamp.asLong());
    if (depth == null || level.getGameTime() - depth.tick() >= 10) {
      float distance = 4;
      for (int down = 1; down <= 4; down++) {
        var pos = lamp.below(down);
        if (!level.hasChunkAt(pos)) {
          distance = down - .75F;
          break;
        }
        var shape = level.getBlockState(pos).getCollisionShape(level, pos);
        if (!shape.isEmpty()) {
          distance = down + .25F - (float) shape.max(Direction.Axis.Y);
          break;
        }
      }
      depth = new Depth(level.getGameTime(), distance);
      if (CACHE.size() > 256) CACHE.clear();
      CACHE.put(lamp.asLong(), depth);
    }
    var camera = Minecraft.getInstance().gameRenderer.getMainCamera().getPosition();
    double dx = camera.x - lamp.getX() - .5, dz = camera.z - lamp.getZ() - .5;
    double length = Math.sqrt(dx * dx + dz * dz);
    if (length < .01) return;
    float x = (float) (-dz / length), z = (float) (dx / length);
    float bottom = .25F - depth.distance();
    float spread = Math.min(.95F, .38F + depth.distance() * .15F);
    var consumer =
        buffers.getBuffer(
            RenderType.entityTranslucentEmissive(Stonedew.id("textures/effect/uv_beam.png")));
    float[][] points = {
      {.5F - x * spread, bottom, .5F - z * spread, 0, 1},
      {.5F + x * spread, bottom, .5F + z * spread, 1, 1},
      {.5F + x * .38F, .25F, .5F + z * .38F, 1, 0},
      {.5F - x * .38F, .25F, .5F - z * .38F, 0, 0}
    };
    int alpha = (int) (StonedewConfig.VISUAL_INTENSITY.get() * 160);
    for (float[] p : points)
      consumer
          .addVertex(pose.last(), p[0], p[1], p[2])
          .setColor(255, 255, 255, alpha)
          .setUv(p[3], p[4])
          .setOverlay(OverlayTexture.NO_OVERLAY)
          .setLight(LightTexture.FULL_BRIGHT)
          .setNormal(pose.last(), 0, 0, 1);
  }

  private LampBeam() {}
}
