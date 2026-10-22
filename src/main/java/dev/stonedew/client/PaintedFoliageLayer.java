package dev.stonedew.client;

import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.VertexFormat;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.texture.TextureAtlas;

/** Vanilla entity lighting with mip filtering for painted alpha foliage. No custom shader. */
public final class PaintedFoliageLayer extends RenderType {
  public static final RenderType LAYER =
      create(
          "stonedew_painted_foliage",
          DefaultVertexFormat.NEW_ENTITY,
          VertexFormat.Mode.QUADS,
          1536,
          true,
          false,
          CompositeState.builder()
              .setShaderState(RENDERTYPE_ENTITY_CUTOUT_SHADER)
              .setTextureState(new TextureStateShard(TextureAtlas.LOCATION_BLOCKS, false, true))
              .setTransparencyState(NO_TRANSPARENCY)
              .setLightmapState(LIGHTMAP)
              .setOverlayState(OVERLAY)
              .createCompositeState(true));

  private PaintedFoliageLayer() {
    super(
        "stonedew_foliage_factory",
        DefaultVertexFormat.NEW_ENTITY,
        VertexFormat.Mode.QUADS,
        1536,
        false,
        false,
        () -> {},
        () -> {});
  }
}
