package dev.stonedew.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import dev.stonedew.Stonedew;
import dev.stonedew.plant.GrowTrayBlockEntity;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.Sheets;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.resources.model.ModelResourceLocation;
import net.minecraft.util.RandomSource;

public final class TrayRenderer implements BlockEntityRenderer<GrowTrayBlockEntity> {
  private final RandomSource random = RandomSource.create(0);

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
      String habit =
          switch (plant.habit()) {
            case "tall" -> "tall";
            case "hybrid" -> "hybrid";
            default -> "bushy";
          };
      String detail = distance > 24 * 24 ? "_lod" : "";
      var model =
          Minecraft.getInstance()
              .getModelManager()
              .getModel(
                  ModelResourceLocation.standalone(
                      Stonedew.id("block/plants/" + habit + "_" + plant.stage() + detail)));
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
      pose.mulPose(Axis.YP.rotationDegrees(slot * 83 + tray.getBlockPos().asLong() % 17));
      float grow = 0.93F + 0.07F * plant.progress() / 100F;
      pose.scale(scale * grow, (grid == 1 ? 1.35F : 1.12F) * grow, scale * grow);
      pose.translate(-0.5, 0, -0.5);
      var vertices = buffers.getBuffer(Sheets.cutoutBlockSheet());
      var quads = model.getQuads(null, null, random);
      for (var quad : quads) {
        int color =
            switch (quad.getTintIndex()) {
              case 0 -> plant.leaf();
              case 1 -> plant.bud();
              case 2 -> plant.hair();
              default -> 0xFFFFFF;
            };
        float shade =
            switch (quad.getDirection()) {
              case DOWN -> 0.5F;
              case NORTH, SOUTH -> 0.8F;
              case EAST, WEST -> 0.65F;
              default -> 1F;
            };
        vertices.putBulkData(
            pose.last(),
            quad,
            ((color >> 16) & 255) / 255F * shade,
            ((color >> 8) & 255) / 255F * shade,
            (color & 255) / 255F * shade,
            1F,
            net.minecraft.client.renderer.LevelRenderer.getLightColor(
                tray.getLevel(), tray.getBlockPos().above(plant.stage() >= 2 ? 2 : 1)),
            overlay);
      }
      pose.popPose();
    }
  }
}
