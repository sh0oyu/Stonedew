package dev.stonedew.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.stonedew.Stonedew;
import dev.stonedew.plant.GrowTrayBlockEntity;
import java.util.List;
import net.minecraft.client.Minecraft;
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

  private record Surface(BakedQuad quad, float[] x, float[] y, float[] z) {}

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
      if (!PlantSurfaceGeometry.hasArea(x, y, z)) continue;
      // The entity shader uses the original baked normals, including undersides.
      result.add(new Surface(quad, x, y, z));
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
    long profileStart = PlantRenderStats.ENABLED ? System.nanoTime() : 0;
    int profileFaces = 0;
    var level = (net.minecraft.client.multiplayer.ClientLevel) tray.getLevel();
    int grid = (int) Math.ceil(Math.sqrt(tray.capacity()));
    double distance =
        Minecraft.getInstance()
            .gameRenderer
            .getMainCamera()
            .getPosition()
            .distanceToSqr(tray.getBlockPos().getCenter());
    var illumination = GrowLightCache.sample(level, tray.getBlockPos(), grid);
    int[] levels = illumination.levels();
    for (int slot = 0; slot < tray.capacity(); slot++) {
      var plant = tray.view(slot);
      if (plant == null) continue;
      String detail = distance > 10 * 10 ? "_lod" : "";
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
      float soil =
          ((dev.stonedew.plant.GrowTrayBlock) tray.getBlockState().getBlock()).soilHeight();
      float grow = .93F + .07F * plant.progress() / 100F;
      float sx =
          (grid == 1 ? 1.25F : .48F)
              * grow
              * plant.spread()
              / 100F
              * (plant.habit().equals("tall") ? .86F : 1);
      float sy =
          (grid == 1 ? 1.30F : 1.05F)
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
        if (PlantRenderStats.ENABLED) profileFaces++;
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
          int height = Math.clamp((int) (soil + surface.y()[v] * sy + .25F), 1, 3);
          brightness[v] = 1;
          lighting[v] = levels[height];
          uv += illumination.uv()[slot * 4 + height] * .25F;
        }
        // Colored UV bounce remains conditional on actual fueled fixtures and obstruction checks.
        r = Math.min(1, r + .10F * uv);
        g *= 1 - .18F * uv;
        b = Math.min(1, b + .24F * uv);
        vertices.putBulkData(pose.last(), quad, brightness, r, g, b, 1, lighting, overlay, true);
      }
      pose.popPose();
    }
    if (PlantRenderStats.ENABLED)
      PlantRenderStats.tray(System.nanoTime() - profileStart, profileFaces);
  }
}
