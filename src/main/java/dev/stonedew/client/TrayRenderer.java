package dev.stonedew.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.stonedew.Stonedew;
import dev.stonedew.plant.GrowTrayBlockEntity;
import java.util.List;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.LevelRenderer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.block.model.BakedQuad;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.client.resources.model.ModelResourceLocation;
import net.minecraft.util.RandomSource;

public final class TrayRenderer implements BlockEntityRenderer<GrowTrayBlockEntity> {
  private final RandomSource random = RandomSource.create(0);
  private final java.util.Map<BakedModel, List<Surface>> meshCache = new java.util.WeakHashMap<>();

  private record Surface(
      BakedQuad quad, float nx, float ny, float nz, float[] x, float[] y, float[] z) {}

  private List<Surface> unpack(BakedModel model) {
    var result = new java.util.ArrayList<Surface>();
    for (var quad : model.getQuads(null, null, random)) {
      int[] data = quad.getVertices();
      int stride = data.length / 4;
      float[] x = new float[4], y = new float[4], z = new float[4];
      for (int i = 0; i < 4; i++) {
        x[i] = Float.intBitsToFloat(data[i * stride]) - .5F;
        y[i] = Float.intBitsToFloat(data[i * stride + 1]);
        z[i] = Float.intBitsToFloat(data[i * stride + 2]) - .5F;
      }
      // Use geometric normals, including folded leaf undersides and tilted colas.
      float ax = x[1] - x[0], ay = y[1] - y[0], az = z[1] - z[0];
      float bx = x[2] - x[0], by = y[2] - y[0], bz = z[2] - z[0];
      float nx = ay * bz - az * by, ny = az * bx - ax * bz, nz = ax * by - ay * bx;
      float length = (float) Math.sqrt(nx * nx + ny * ny + nz * nz);
      if (length < .00001F) continue;
      result.add(new Surface(quad, nx / length, ny / length, nz / length, x, y, z));
    }
    return List.copyOf(result);
  }

  public TrayRenderer(BlockEntityRendererProvider.Context context) {}

  @Override
  public net.minecraft.world.phys.AABB getRenderBoundingBox(GrowTrayBlockEntity tray) {
    return new net.minecraft.world.phys.AABB(tray.getBlockPos()).inflate(.85, 2, .85);
  }

  @Override
  public int getViewDistance() {
    return 48;
  }

  private static void contact(PoseStack pose, MultiBufferSource buffers, float radius, int light) {
    var vertices =
        buffers.getBuffer(
            RenderType.entityTranslucent(Stonedew.id("textures/effect/contact_shadow.png")));
    float y = .012F;
    float[][] corners = {
      {-radius, y, radius}, {radius, y, radius}, {radius, y, -radius}, {-radius, y, -radius}
    };
    float[][] uv = {{0, 1}, {1, 1}, {1, 0}, {0, 0}};
    for (int i = 0; i < 4; i++)
      vertices
          .addVertex(pose.last(), corners[i][0], y, corners[i][2])
          .setColor(255, 255, 255, 185)
          .setUv(uv[i][0], uv[i][1])
          .setOverlay(net.minecraft.client.renderer.texture.OverlayTexture.NO_OVERLAY)
          .setLight(light)
          .setNormal(pose.last(), 0, 1, 0);
  }

  private static void foliageShadow(
      PoseStack pose,
      MultiBufferSource buffers,
      dev.stonedew.plant.PlantView plant,
      float offsetX,
      float offsetZ,
      int grid,
      float spread,
      float cos,
      float sin,
      int light) {
    var vertices =
        buffers.getBuffer(
            RenderType.entityTranslucent(
                Stonedew.id(
                    "textures/effect/plant_shadow_"
                        + plant.stage()
                        + "_"
                        + plant.shape()
                        + "_"
                        + (plant.stage() >= 2 ? plant.budLoad() : 0)
                        + ".png")));
    float lo = grid == 1 ? 3.75F / 16 : 1.4F / 16;
    float hi = grid == 1 ? 12.25F / 16 : 14.6F / 16;
    float radius = grid == 1 ? .5F : .25F;
    float x0 = Math.max(-radius, lo - offsetX), x1 = Math.min(radius, hi - offsetX);
    float z0 = Math.max(-radius, lo - offsetZ), z1 = Math.min(radius, hi - offsetZ);
    float[][] corners = {{x0, z1}, {x1, z1}, {x1, z0}, {x0, z0}};
    for (var corner : corners) {
      float x = corner[0], z = corner[1];
      vertices
          .addVertex(pose.last(), x, .015F, z)
          .setColor(255, 255, 255, 200)
          .setUv(
              .5F + (x * cos - z * sin) / spread * (2F / 3),
              .5F + (x * sin + z * cos) / spread * (2F / 3))
          .setOverlay(net.minecraft.client.renderer.texture.OverlayTexture.NO_OVERLAY)
          .setLight(light)
          .setNormal(pose.last(), 0, 1, 0);
    }
  }

  @Override
  public void render(
      GrowTrayBlockEntity tray,
      float partial,
      PoseStack pose,
      MultiBufferSource buffers,
      int light,
      int overlay) {
    var level = (net.minecraft.client.multiplayer.ClientLevel) tray.getLevel();
    var lights = GrowLightCache.near(level, tray.getBlockPos());
    int grid = (int) Math.ceil(Math.sqrt(tray.capacity()));
    double distance =
        Minecraft.getInstance()
            .gameRenderer
            .getMainCamera()
            .getPosition()
            .distanceToSqr(tray.getBlockPos().getCenter());
    int[] levels = new int[4];
    for (int i = 0; i < 4; i++)
      levels[i] = LevelRenderer.getLightColor(level, tray.getBlockPos().above(Math.max(1, i)));
    for (int slot = 0; slot < tray.capacity(); slot++) {
      var plant = tray.view(slot);
      if (plant == null) continue;
      String detail = distance > 14 * 14 ? "_lod" : "";
      var model =
          Minecraft.getInstance()
              .getModelManager()
              .getModel(
                  ModelResourceLocation.standalone(
                      Stonedew.id(
                          "block/plants/plant_"
                              + plant.stage()
                              + "_"
                              + plant.shape()
                              + "_"
                              + (plant.stage() >= 2 ? plant.budLoad() : 0)
                              + detail)));
      float offsetX = (slot % grid + .5F) / grid, offsetZ = (slot / grid + .5F) / grid;
      float soil = grid == 1 ? 7.5F / 16 : 13.6F / 16;
      float grow = .93F + .07F * plant.progress() / 100F;
      float sx =
          (grid == 1 ? 1.0F : .62F)
              * grow
              * plant.spread()
              / 100F
              * (plant.habit().equals("tall") ? .86F : 1);
      float sy =
          (grid == 1 ? 1.10F : .94F)
              * grow
              * plant.height()
              / 100F
              * (plant.habit().equals("tall") ? 1.15F : 1);
      float rotation = (float) Math.toRadians(plant.rotation());
      float cos = (float) Math.cos(rotation), sin = (float) Math.sin(rotation);
      pose.pushPose();
      pose.translate(offsetX, soil, offsetZ);
      contact(pose, buffers, grid == 1 ? (plant.stage() == 0 ? .13F : .23F) : .13F, levels[1]);
      foliageShadow(pose, buffers, plant, offsetX, offsetZ, grid, sx, cos, sin, levels[1]);
      float sway =
          (float) Math.sin((level.getGameTime() + partial) * .025 + plant.rotation()) * .8F;
      pose.mulPose(Axis.ZP.rotationDegrees(sway));
      pose.mulPose(Axis.YP.rotationDegrees(plant.rotation()));
      pose.scale(sx, sy, sx);
      pose.translate(-.5, 0, -.5);
      var vertices = buffers.getBuffer(Sheets.cutoutBlockSheet());
      float[] brightness = new float[4];
      int[] lighting = new int[4];
      for (var surface : meshCache.computeIfAbsent(model, this::unpack)) {
        var quad = surface.quad();
        boolean leaf = quad.getTintIndex() == 3;
        int color =
            switch (quad.getTintIndex()) {
              case 0 -> plant.leaf();
              case 1 -> plant.bud();
              case 2 -> plant.hair();
              case 4 -> {
                int bud = plant.bud();
                int red = ((bud >> 16) & 255), green = ((bud >> 8) & 255), blue = (bud & 255);
                yield ((red + (255 - red) / 3) << 16)
                    | ((green + (255 - green) / 3) << 8)
                    | (blue + (255 - blue) / 3);
              }
              default -> 0xFFFFFF;
            };
        float r = leaf ? 1.0F : ((color >> 16) & 255) / 255F;
        float g = leaf ? 1.0F : ((color >> 8) & 255) / 255F;
        float b = leaf ? 1.0F : (color & 255) / 255F;
        if (quad.getTintIndex() == 1 || quad.getTintIndex() == 4) {
          r = Math.min(1, r * 1.12F);
          g = Math.min(1, g * 1.12F);
          b = Math.min(1, b * 1.12F);
        }
        float uv = 0;
        for (int v = 0; v < 4; v++) {
          float x = surface.x()[v], y = surface.y()[v], z = surface.z()[v];
          // The entity shader already lights the transformed geometric normal.
          // Keep baked occlusion, without applying a second diffuse-light pass.
          brightness[v] = 1;
          lighting[v] = levels[Math.clamp((int) (soil + y * sy + .25F), 1, 3)];
          uv +=
              GrowLightCache.strength(
                      lights,
                      tray.getBlockPos().getX() + offsetX + (x * cos + z * sin) * sx,
                      tray.getBlockPos().getY() + soil + y * sy,
                      tray.getBlockPos().getZ() + offsetZ + (z * cos - x * sin) * sx)
                  * .25F
                  * (1
                      - .65F
                          * Math.max(
                              0,
                              net.minecraft.client.renderer.LightTexture.sky(lighting[v])
                                  - level.getSkyDarken())
                          / 15F);
        }
        // Colored UV bounce remains conditional on actual fueled fixtures and obstruction checks.
        r = Math.min(1, r + .10F * uv);
        g *= 1 - .18F * uv;
        b = Math.min(1, b + .24F * uv);
        vertices.putBulkData(pose.last(), quad, brightness, r, g, b, 1, lighting, overlay, true);
      }
      pose.popPose();
    }
  }
}
