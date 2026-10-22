package dev.stonedew.plant;

/**
 * Stable visual identity, independent of genetics, care, position and frame time. Bud load
 * describes visible flower sites only; harvest yield is introduced in P3.
 */
public record PlantAppearance(int shape, int budLoad, int height, int spread, int rotation) {
  public static final int SHAPES = 4;
  public static final int BUD_LOADS = 3;

  public static PlantAppearance fromSeed(long seed) {
    var random = new java.util.Random(Long.rotateLeft(seed * 0x9E3779B97F4A7C15L, 23));
    return new PlantAppearance(
        random.nextInt(SHAPES),
        random.nextInt(BUD_LOADS),
        90 + random.nextInt(21),
        90 + random.nextInt(21),
        random.nextInt(360));
  }

  public int matureBudCount() {
    return switch (budLoad) {
      case 0 -> 5;
      case 1 -> 9;
      default -> 13;
    };
  }
}
