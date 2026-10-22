package dev.stonedew.plant;

import dev.stonedew.genetics.Genome;
import java.util.Objects;

public record PlantState(
    Genome genome,
    int stage,
    double progress,
    double water,
    long lastSimTime,
    double careIntegral,
    long careTicks,
    String owner,
    long appearanceSeed) {
  public PlantState {
    Objects.requireNonNull(genome);
    Objects.requireNonNull(owner);
    if (stage < 0
        || stage > 3
        || !Double.isFinite(progress)
        || progress < 0
        || progress > 1
        || !Double.isFinite(water)
        || water < 0
        || water > 100
        || !Double.isFinite(careIntegral)
        || careIntegral < 0
        || careTicks < 0
        || lastSimTime < 0
        || careIntegral > careTicks + 0.000001)
      throw new IllegalArgumentException("Invalid plant state");
  }

  /** Compatibility constructor for callers and legacy saves; planting supplies a fresh seed. */
  public PlantState(
      Genome genome,
      int stage,
      double progress,
      double water,
      long lastSimTime,
      double careIntegral,
      long careTicks,
      String owner) {
    this(
        genome,
        stage,
        progress,
        water,
        lastSimTime,
        careIntegral,
        careTicks,
        owner,
        genome.lineageSeed());
  }

  public static PlantState seed(Genome genome, long now, String owner) {
    return seed(genome, now, owner, genome.lineageSeed());
  }

  public static PlantState seed(Genome genome, long now, String owner, long appearanceSeed) {
    return new PlantState(genome, 0, 0, 40, now, 0, 0, owner, appearanceSeed);
  }

  public PlantAppearance appearance() {
    return PlantAppearance.fromSeed(appearanceSeed);
  }

  public PlantState withAppearanceSeed(long seed) {
    return new PlantState(
        genome, stage, progress, water, lastSimTime, careIntegral, careTicks, owner, seed);
  }

  public PlantState water(double amount) {
    return new PlantState(
        genome,
        stage,
        progress,
        Math.clamp(water + amount, 0, 100),
        lastSimTime,
        careIntegral,
        careTicks,
        owner,
        appearanceSeed);
  }

  public PlantState stage(int value) {
    return new PlantState(
        genome,
        value,
        value == 3 ? 1 : 0,
        water,
        lastSimTime,
        careIntegral,
        careTicks,
        owner,
        appearanceSeed);
  }

  public PlantState genome(Genome value) {
    return new PlantState(
        value, stage, progress, water, lastSimTime, careIntegral, careTicks, owner, appearanceSeed);
  }
}
