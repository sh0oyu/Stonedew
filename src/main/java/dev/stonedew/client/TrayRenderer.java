package dev.stonedew.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.stonedew.Stonedew;
import dev.stonedew.plant.GrowTrayBlockEntity;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.block.model.BakedQuad;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.client.resources.model.ModelResourceLocation;
import net.minecraft.util.RandomSource;

public final class TrayRenderer implements BlockEntityRenderer<GrowTrayBlockEntity> {
  private static final float[] BRIGHTNESS = {1, 1, 1, 1};
  private final RandomSource random = RandomSource.create(0);
  private final java.util.Map<BakedModel, Parts> meshCache = new java.util.WeakHashMap<>();

  private record Parts(java.util.List<BakedQuad> flowers, java.util.List<BakedQuad> cards) {}

  private Parts unpack(BakedModel model) {
    var flowers = new java.util.ArrayList<BakedQuad>();
    var cards = new java.util.ArrayList<BakedQuad>();
    for (var quad : model.getQuads(null, null, random)) {
      if (quad.getTintIndex() != 3) {
        flowers.add(quad);
        continue;
      }
      cards.add(quad);
    }
    return new Parts(java.util.List.copyOf(flowers), java.util.List.copyOf(cards));
  }

  public TrayRenderer(BlockEntityRendererProvider.Context context) {}

  @Override
  public net.minecraft.world.phys.AABB getRenderBoundingBox(GrowTrayBlockEntity tray) {
    return new net.minecraft.world.phys.AABB(tray.getBlockPos()).inflate(0.7, 2, 0.7);
  }

  @Override
  public int getViewDistance() {
    return 48;
  }

  @Override
  public void render(
      GrowTrayBlockEntity tray,
      float partial,
      PoseStack pose,
      MultiBufferSource buffers,
      int light,
      int overlay) {
    int grid = (int) Math.ceil(Math.sqrt(tray.capacity()));
    double distance =
        Minecraft.getInstance()
            .gameRenderer
            .getMainCamera()
            .getPosition()
            .distanceToSqr(tray.getBlockPos().getCenter());
    for (int slot = 0; slot < tray.capacity(); slot++) {
      var plant = tray.view(slot);
      if (plant == null) continue;
      String detail = distance > 24 * 24 ? "_lod" : "";
      var model =
          Minecraft.getInstance()
              .getModelManager()
              .getModel(
                  ModelResourceLocation.standalone(
                      Stonedew.id(
                          "block/plants/"
                              + "plant_"
                              + plant.stage()
                              + "_"
                              + plant.shape()
                              + "_"
                              + (plant.stage() >= 2 ? plant.budLoad() : 0)
                              + detail)));
      pose.pushPose();
      pose.translate(
          (slot % grid + 0.5) / grid,
          tray.capacity() == 1 ? 7.5 / 16.0 : 6.25 / 16.0,
          (slot / grid + 0.5) / grid);
      float scale = grid == 1 ? 0.95F : 0.65F;
      float sway =
          (float)
                  Math.sin(
                      (tray.getLevel().getGameTime() + partial) * 0.035
                          + tray.getBlockPos().asLong() % 31
                          + slot)
              * 1.2F;
      pose.mulPose(Axis.ZP.rotationDegrees(sway));
      pose.mulPose(Axis.YP.rotationDegrees(plant.rotation()));
      float grow = 0.93F + 0.07F * plant.progress() / 100F;
      float height = plant.height() / 100F * (plant.habit().equals("tall") ? 1.15F : 1F);
      float spread = plant.spread() / 100F * (plant.habit().equals("tall") ? .86F : 1F);
      pose.scale(
          scale * grow * spread,
          (grid == 1 ? 1.35F : 1.12F) * grow * height,
          scale * grow * spread);
      pose.translate(-0.5, 0, -0.5);
      var vertices = buffers.getBuffer(Sheets.cutoutBlockSheet());
      int sampledLight =
          net.minecraft.client.renderer.LevelRenderer.getLightColor(
              tray.getLevel(), tray.getBlockPos().above(plant.stage() >= 2 ? 2 : 1));
      int[] lighting = {sampledLight, sampledLight, sampledLight, sampledLight};
      var parts = meshCache.computeIfAbsent(model, this::unpack);
      for (var quad : parts.flowers()) {
        int color =
            switch (quad.getTintIndex()) {
              case 0 -> plant.leaf();
              case 1 -> plant.bud();
              case 2 -> plant.hair();
              default -> 0xFFFFFF;
            };
        // OBJ vertex normals and baked material colors preserve the curved forms.
        vertices.putBulkData(
            pose.last(),
            quad,
            BRIGHTNESS,
            ((color >> 16) & 255) / 255F,
            ((color >> 8) & 255) / 255F,
            (color & 255) / 255F,
            1F,
            lighting,
            overlay,
            true);
      }
      var foliage = buffers.getBuffer(PaintedFoliageLayer.LAYER);
      float leafR = .78F + .22F * ((plant.leaf() >> 16) & 255) / 255F;
      float leafG = .78F + .22F * ((plant.leaf() >> 8) & 255) / 255F;
      float leafB = .78F + .22F * (plant.leaf() & 255) / 255F;
      for (var card : parts.cards()) {
        foliage.putBulkData(
            pose.last(), card, BRIGHTNESS, leafR, leafG, leafB, 1F, lighting, overlay, true);
      }
      pose.popPose();
    }
  }
}
