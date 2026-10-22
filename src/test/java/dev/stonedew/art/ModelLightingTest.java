package dev.stonedew.art;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class ModelLightingTest {
  @Test
  void flowerFacesHaveDirectionalContrast() {
    float top = ModelLighting.diffuse(0, 1, 0, 0);
    float lit = ModelLighting.diffuse(-1, 0, 0, 0);
    float shadow = ModelLighting.diffuse(1, 0, 0, 0);
    assertTrue(top > lit);
    assertTrue(lit > shadow + .15F);
    assertTrue(shadow >= .5F);
  }

  @Test
  void rotatingAPlantRotatesItsShadingWithItsSurfaces() {
    assertEquals(
        ModelLighting.diffuse(-1, 0, 0, 0), ModelLighting.diffuse(1, 0, 0, (float) Math.PI), 1e-6F);
    assertEquals(ModelLighting.diffuse(0, 1, 0, 0), ModelLighting.diffuse(0, 1, 0, 2), 1e-6F);
  }

  @Test
  void UndersidesAndInnerCanopyRemainDarkerThanExposedTips() {
    assertTrue(ModelLighting.diffuse(0, -1, 0, 0) < ModelLighting.diffuse(0, 1, 0, 0));
    assertTrue(ModelLighting.canopy(.1F, .05F, true) < ModelLighting.canopy(.8F, .45F, true));
    for (float y = -1; y < 2; y += .1F)
      for (float r = 0; r < 1; r += .1F) {
        float value = ModelLighting.canopy(y, r, true);
        assertTrue(value >= .65F && value <= 1);
      }
  }
}
