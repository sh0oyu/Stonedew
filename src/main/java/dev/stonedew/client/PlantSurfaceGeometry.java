package dev.stonedew.client;

/** Headless geometry check shared by the tray renderer and shipped-mesh regression tests. */
final class PlantSurfaceGeometry {
  private PlantSurfaceGeometry() {}

  static boolean hasArea(float[] x, float[] y, float[] z) {
    float ax = x[1] - x[0], ay = y[1] - y[0], az = z[1] - z[0];
    float bx = x[2] - x[0], by = y[2] - y[0], bz = z[2] - z[0];
    float nx = ay * bz - az * by, ny = az * bx - ax * bz, nz = ax * by - ay * bx;
    // Model units are blocks. Thin pistils/resin are valid below the old 1e-5
    // cross-product length; reject only collapsed/numerically degenerate faces.
    return nx * nx + ny * ny + nz * nz >= 1.0e-16F;
  }
}
