package dev.stonedew.client;

import com.mojang.blaze3d.platform.NativeImage;
import com.mojang.serialization.MapCodec;
import dev.stonedew.Stonedew;
import net.minecraft.client.renderer.texture.MissingTextureAtlasSprite;
import net.minecraft.client.renderer.texture.SpriteContents;
import net.minecraft.client.renderer.texture.atlas.SpriteSource;
import net.minecraft.client.renderer.texture.atlas.SpriteSourceType;
import net.minecraft.client.renderer.texture.atlas.sources.LazyLoadedImage;
import net.minecraft.client.resources.metadata.animation.FrameSize;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.ResourceMetadata;
import net.neoforged.neoforge.client.event.RegisterSpriteSourceTypesEvent;

/** Imports the painted material sheet as ordinary mip-safe Minecraft sprites. */
public record PaintedMaterialSource(ResourceLocation resource) implements SpriteSource {
  public static final MapCodec<PaintedMaterialSource> CODEC =
      ResourceLocation.CODEC
          .fieldOf("resource")
          .xmap(PaintedMaterialSource::new, PaintedMaterialSource::resource);
  public static final SpriteSourceType TYPE = new SpriteSourceType(CODEC);
  private static final String[] MATERIALS = {
    "wood",
    "wood_edge",
    "ceramic",
    "teal",
    "copper",
    "iron",
    "soil",
    "soil_wet",
    "paper",
    "glow",
    "glass",
    "dewstone",
    "plant_bud",
    "plant_leaf",
    "plant_stem",
    "plant_pistil",
    "leaf",
    "bud",
    "hair",
    "stem"
  };
  private static final int[] CELLS = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 13, 12, 15, 14
  };

  public static void register(RegisterSpriteSourceTypesEvent event) {
    event.register(Stonedew.id("painted_materials"), TYPE);
  }

  @Override
  public SpriteSourceType type() {
    return TYPE;
  }

  @Override
  public void run(ResourceManager resources, Output output) {
    var file = TEXTURE_ID_CONVERTER.idToFile(resource);
    var source = resources.getResource(file);
    if (source.isEmpty()) {
      Stonedew.LOGGER.error("Missing painted material sheet {}", file);
      return;
    }
    var image = new LazyLoadedImage(file, source.get(), MATERIALS.length);
    for (int index = 0; index < MATERIALS.length; index++) {
      var sprite = Stonedew.id("block/" + MATERIALS[index]);
      int cell = CELLS[index];
      output.add(
          sprite,
          new SpriteSupplier() {
            @Override
            public SpriteContents apply(
                net.minecraft.client.renderer.texture.atlas.SpriteResourceLoader loader) {
              NativeImage tile = null;
              try {
                var original = image.get();
                // Native texture import normalizes each tile, preserving the source artwork.
                // Power-of-two sprites retain the world's requested mip level; a small inset
                // prevents neighboring paint swatches from bleeding into a material.
                int x = (int) ((cell % 4 + .02) * original.getWidth() / 4);
                int y = (int) ((cell / 4 + .02) * original.getHeight() / 4);
                int width = (int) (original.getWidth() * .96 / 4);
                int height = (int) (original.getHeight() * .96 / 4);
                tile = new NativeImage(256, 256, false);
                original.resizeSubRectTo(x, y, width, height, tile);
                return new SpriteContents(
                    sprite, new FrameSize(256, 256), tile, ResourceMetadata.EMPTY);
              } catch (Exception exception) {
                if (tile != null) tile.close();
                Stonedew.LOGGER.error("Cannot import painted material {}", sprite, exception);
                return MissingTextureAtlasSprite.create();
              } finally {
                image.release();
              }
            }

            @Override
            public void discard() {
              image.release();
            }
          });
    }
    var leafFile = Stonedew.id("textures/art/leaf_fan.png");
    var leaf = resources.getResource(leafFile);
    if (leaf.isPresent()) {
      var id = Stonedew.id("block/painted_leaf");
      output.add(
          id,
          loader -> {
            NativeImage tile = null;
            try (var input = leaf.get().open();
                var original = NativeImage.read(input)) {
              tile = new NativeImage(512, 512, false);
              original.resizeSubRectTo(0, 0, original.getWidth(), original.getHeight(), tile);
              return new SpriteContents(id, new FrameSize(512, 512), tile, ResourceMetadata.EMPTY);
            } catch (Exception exception) {
              if (tile != null) tile.close();
              Stonedew.LOGGER.error("Cannot import painted foliage {}", leafFile, exception);
              return MissingTextureAtlasSprite.create();
            }
          });
    } else Stonedew.LOGGER.error("Missing painted foliage {}", leafFile);
  }
}
