package dev.stonedew.client;

import com.mojang.blaze3d.vertex.PoseStack;
import dev.stonedew.Stonedew;
import dev.stonedew.core.StonedewConfig;
import dev.stonedew.plant.BulbLampBlock;
import dev.stonedew.plant.BulbLampBlockEntity;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.LightTexture;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.blockentity.BlockEntityRendererProvider;
import net.minecraft.client.renderer.texture.OverlayTexture;

/** Fuel-gated local radiance using Minecraft's unlit additive material. */
public final class LampRenderer implements BlockEntityRenderer<BulbLampBlockEntity> {
  public LampRenderer(BlockEntityRendererProvider.Context context) {}

  @Override
  public net.minecraft.world.phys.AABB getRenderBoundingBox(BulbLampBlockEntity lamp) {
    return new net.minecraft.world.phys.AABB(lamp.getBlockPos()).inflate(2, 5, 2);
  }

  @Override
  public int getViewDistance() {
    return 24;
  }

  @Override
  public void render(
      BulbLampBlockEntity lamp,
      float partial,
      PoseStack pose,
      MultiBufferSource buffers,
      int light,
      int overlay) {
    if (!lamp.getBlockState().getValue(BulbLampBlock.LIT) || !StonedewConfig.ATMOSPHERE.get())
      return;
    LampSpill.render(lamp.getLevel(), lamp.getBlockPos(), pose, buffers);
    LampBeam.render(lamp.getLevel(), lamp.getBlockPos(), pose, buffers);
    pose.pushPose();
    pose.translate(0.5, 0.27, 0.5);
    pose.mulPose(Minecraft.getInstance().gameRenderer.getMainCamera().rotation());
    var vertices =
        buffers.getBuffer(RenderType.eyes(Stonedew.id("textures/block/fixture_aura.png")));
    var frame = pose.last();
    int radiance = (int) (255 * Math.min(1, StonedewConfig.VISUAL_INTENSITY.get() * 1.5));
    vertices
        .addVertex(frame, -0.65F, -0.45F, 0)
        .setColor(radiance, radiance, radiance, 255)
        .setUv(0, 1)
        .setOverlay(OverlayTexture.NO_OVERLAY)
        .setLight(LightTexture.FULL_BRIGHT)
        .setNormal(frame, 0, 0, 1);
    vertices
        .addVertex(frame, 0.65F, -0.45F, 0)
        .setColor(radiance, radiance, radiance, 255)
        .setUv(1, 1)
        .setOverlay(OverlayTexture.NO_OVERLAY)
        .setLight(LightTexture.FULL_BRIGHT)
        .setNormal(frame, 0, 0, 1);
    vertices
        .addVertex(frame, 0.65F, 0.45F, 0)
        .setColor(radiance, radiance, radiance, 255)
        .setUv(1, 0)
        .setOverlay(OverlayTexture.NO_OVERLAY)
        .setLight(LightTexture.FULL_BRIGHT)
        .setNormal(frame, 0, 0, 1);
    vertices
        .addVertex(frame, -0.65F, 0.45F, 0)
        .setColor(radiance, radiance, radiance, 255)
        .setUv(0, 0)
        .setOverlay(OverlayTexture.NO_OVERLAY)
        .setLight(LightTexture.FULL_BRIGHT)
        .setNormal(frame, 0, 0, 1);
    pose.popPose();
  }
}
