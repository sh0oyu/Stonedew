package dev.stonedew.client;

import dev.stonedew.Stonedew;
import dev.stonedew.core.ModContent;
import dev.stonedew.genetics.Genome;
import net.minecraft.client.resources.model.ModelResourceLocation;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.neoforged.neoforge.client.event.ModelEvent;
import net.neoforged.neoforge.client.event.RegisterColorHandlersEvent;
import net.neoforged.neoforge.client.event.RegisterMenuScreensEvent;

public final class ClientRegistration {
  public static void renderTypes(
      net.neoforged.neoforge.client.event.RegisterNamedRenderTypesEvent event) {
    event.register(
        Stonedew.id("emissive"),
        net.minecraft.client.renderer.RenderType.translucent(),
        net.minecraft.client.renderer.RenderType.eyes(
            net.minecraft.client.renderer.texture.TextureAtlas.LOCATION_BLOCKS));
  }

  public static void models(ModelEvent.RegisterAdditional event) {
    for (int stage = 0; stage < 4; stage++)
      for (int shape = 0; shape < dev.stonedew.plant.PlantAppearance.SHAPES; shape++)
        for (int load = 0; load < (stage >= 2 ? 3 : 1); load++)
          for (String detail : java.util.List.of("", "_lod"))
            event.register(
                ModelResourceLocation.standalone(
                    Stonedew.id(
                        "block/plants/plant_" + stage + "_" + shape + "_" + load + detail)));
  }

  public static void renderers(EntityRenderersEvent.RegisterRenderers event) {
    event.registerBlockEntityRenderer(ModContent.GROW_TRAY.get(), TrayRenderer::new);
    event.registerBlockEntityRenderer(ModContent.LAMP_ENTITY.get(), LampRenderer::new);
  }

  public static void screens(RegisterMenuScreensEvent event) {
    event.register(ModContent.LEDGER_MENU.get(), LedgerScreen::new);
  }

  public static void colors(RegisterColorHandlersEvent.Item event) {
    event.register(
        (stack, tint) ->
            tint == 0
                ? 0xFF000000
                    | stack
                        .getOrDefault(ModContent.GENOME.get(), Genome.wild("violet", 0))
                        .budColor()
                : -1,
        ModContent.WILD_SEED);
  }

  public static void extensions(
      net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent event) {
    event.registerItem(
        new net.neoforged.neoforge.client.extensions.common.IClientItemExtensions() {
          @Override
          public boolean applyForgeHandTransform(
              com.mojang.blaze3d.vertex.PoseStack pose,
              net.minecraft.client.player.LocalPlayer player,
              net.minecraft.world.entity.HumanoidArm arm,
              net.minecraft.world.item.ItemStack stack,
              float partial,
              float equip,
              float swing) {
            if (player.isUsingItem() && player.getUseItem().is(ModContent.WATERING_CAN.get())) {
              boolean main =
                  player.getUsedItemHand() == net.minecraft.world.InteractionHand.MAIN_HAND;
              var usedArm = main ? player.getMainArm() : player.getMainArm().getOpposite();
              if (arm == usedArm) {
                float elapsed = 16 - player.getUseItemRemainingTicks() + partial;
                float tilt = (float) Math.sin(Math.clamp(elapsed / 16F, 0, 1) * Math.PI) * 32;
                float sign = arm == net.minecraft.world.entity.HumanoidArm.RIGHT ? 1 : -1;
                pose.translate(sign * 0.56F, -0.52F - equip * 0.6F, -0.72F);
                pose.mulPose(com.mojang.math.Axis.ZP.rotationDegrees(sign * tilt));
                return true;
              }
            }
            return false;
          }
        },
        ModContent.WATERING_CAN);
  }

  private ClientRegistration() {}
}
