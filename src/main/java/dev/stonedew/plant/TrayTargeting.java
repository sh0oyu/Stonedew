package dev.stonedew.plant;

import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/** Bounded ray selection for foliage above its tray, respecting walls and server reach. */
public final class TrayTargeting {
  public record Target(GrowTrayBlockEntity tray, int slot) {}

  public static Target find(Level level, Player player) {
    return find(level, player, Math.min(6, player.blockInteractionRange()));
  }

  public static Target find(Level level, Player player, double reach) {
    Vec3 eye = player.getEyePosition(), end = eye.add(player.getViewVector(1).scale(reach));
    var obstruction =
        level.clip(
            new ClipContext(eye, end, ClipContext.Block.OUTLINE, ClipContext.Fluid.NONE, player));
    double closest =
        obstruction.getType() == HitResult.Type.MISS
            ? reach * reach
            : eye.distanceToSqr(obstruction.getLocation()) + 0.0001;
    var search = new AABB(eye, end).inflate(0.6, 0, 0.6).expandTowards(0, -2.3, 0);
    Target result = null;
    for (BlockPos pos :
        BlockPos.betweenClosed(
            BlockPos.containing(search.minX, search.minY, search.minZ),
            BlockPos.containing(search.maxX, search.maxY, search.maxZ))) {
      if (!level.hasChunkAt(pos)
          || !(level.getBlockEntity(pos) instanceof GrowTrayBlockEntity tray)) continue;
      int grid = (int) Math.ceil(Math.sqrt(tray.capacity()));
      for (int slot = 0; slot < tray.capacity(); slot++) {
        var view = level.isClientSide ? tray.view(slot) : null;
        var state = level.isClientSide ? null : tray.plant(slot);
        if (view == null && state == null) continue;
        int stage = view != null ? view.stage() : state.stage();
        String habit = view != null ? view.habit() : state.genome().habit();
        double centerX = pos.getX() + (slot % grid + 0.5) / grid;
        double centerZ = pos.getZ() + (slot / grid + 0.5) / grid;
        double radius = (grid == 1 ? 0.32 : 0.24) * (stage == 0 ? 0.5 : 1);
        double height =
            switch (stage) {
              case 0 -> 0.3;
              case 1 -> 0.7;
              case 2 -> 1.1;
              default -> 1.3;
            };
        height *= grid == 1 ? 1 : 0.83;
        if (habit.equals("tall")) height *= 1.25;
        var bounds =
            new AABB(
                centerX - radius,
                pos.getY() + 0.35,
                centerZ - radius,
                centerX + radius,
                pos.getY() + 0.5 + height,
                centerZ + radius);
        var hit = bounds.clip(eye, end);
        if (hit.isPresent() && eye.distanceToSqr(hit.get()) < closest) {
          closest = eye.distanceToSqr(hit.get());
          result = new Target(tray, slot);
        }
      }
    }
    return result;
  }

  private TrayTargeting() {}
}
