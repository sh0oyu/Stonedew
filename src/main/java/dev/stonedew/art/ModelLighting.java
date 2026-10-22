package dev.stonedew.art;

/** Directional surface light and soft canopy occlusion; independent of render buffers. */
public final class ModelLighting {
  public static float diffuse(float nx, float ny, float nz, float rotationRadians) {
    float cos = (float) Math.cos(rotationRadians), sin = (float) Math.sin(rotationRadians);
    float x = nx * cos + nz * sin, z = nz * cos - nx * sin;
    float dot = x * -.45F + ny * .82F + z * -.35F;
    return .55F + .45F * Math.max(0, dot);
  }

  public static float canopy(float height, float radius, boolean leaf) {
    float outer = Math.clamp(radius / .48F, 0, 1);
    float top = Math.clamp(height / .95F, 0, 1);
    return Math.clamp((leaf ? .70F : .78F) + .17F * top + .16F * outer, .65F, 1);
  }

  private ModelLighting() {}
}
