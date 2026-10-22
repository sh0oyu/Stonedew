package dev.stonedew.client;

import dev.stonedew.plant.BulbLampBlock;
import dev.stonedew.plant.BulbLampBlockEntity;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/** Client visual light query. Only already-loaded chunks are inspected, at most twice/second. */
final class GrowLightCache {
  private static java.lang.ref.WeakReference<ClientLevel> cachedLevel =
      new java.lang.ref.WeakReference<>(null);
  private static long visit = Long.MIN_VALUE;
  private static final java.util.Map<Long, List<Vec3>> CACHE = new java.util.HashMap<>();

  static List<Vec3> near(ClientLevel level, BlockPos tray) {
    if (level != cachedLevel.get() || level.getGameTime() / 10 != visit) {
      cachedLevel = new java.lang.ref.WeakReference<>(level);
      visit = level.getGameTime() / 10;
      CACHE.clear();
    }
    return CACHE.computeIfAbsent(tray.asLong(), ignored -> find(level, tray));
  }

  private static List<Vec3> find(ClientLevel level, BlockPos tray) {
    var lights = new ArrayList<Vec3>();
    Vec3 target = tray.getCenter().add(0, .6, 0);
    for (int x = (tray.getX() - 5) >> 4; x <= (tray.getX() + 5) >> 4; x++) {
      for (int z = (tray.getZ() - 5) >> 4; z <= (tray.getZ() + 5) >> 4; z++) {
        var chunk = level.getChunkSource().getChunk(x, z, false);
        if (chunk == null) continue;
        for (var entity : chunk.getBlockEntities().values()) {
          if (!(entity instanceof BulbLampBlockEntity)
              || !entity.getBlockState().getValue(BulbLampBlock.LIT)) continue;
          Vec3 source = entity.getBlockPos().getCenter().add(0, -.24, 0);
          if (source.y <= target.y || source.distanceToSqr(target) > 30) continue;
          // The fixture's selection/collision hull encloses its tubes and chain.
          // Begin below that hull; otherwise every ray immediately hits its own emitter.
          Vec3 rayStart = new Vec3(source.x, entity.getBlockPos().getY() - .01, source.z);
          var ray =
              level.clip(
                  new ClipContext(
                      rayStart,
                      target,
                      ClipContext.Block.COLLIDER,
                      ClipContext.Fluid.NONE,
                      net.minecraft.world.phys.shapes.CollisionContext.empty()));
          if (ray.getType() == HitResult.Type.MISS) lights.add(source);
        }
      }
    }
    return List.copyOf(lights);
  }

  static float strength(List<Vec3> lights, double x, double y, double z) {
    float sum = 0;
    for (var light : lights) {
      double dy = light.y - y;
      if (dy < -.2) continue;
      double radial = (light.x - x) * (light.x - x) + (light.z - z) * (light.z - z);
      double cone = Math.max(0, 1 - radial / (1.1 + dy * dy * .8));
      sum += (float) (cone * Math.max(0, 1 - (radial + dy * dy) / 30));
    }
    return Math.min(1, sum);
  }
}
