package dev.stonedew.plant;

import java.util.Map;

/** Bounded integration on demand. No world scanning or per-tick plant loop. */
public final class PlantSimulation {
  public record Environment(
      double light,
      double humidity,
      double temperature,
      double airflow,
      double nutrients,
      double schedule) {
    public Environment {
      for (double value : new double[] {light, humidity, temperature, airflow, nutrients, schedule})
        if (!Double.isFinite(value)) throw new IllegalArgumentException("Nonfinite environment");
    }
  }

  public static double comfort(double value, GrowthProfile.Range range, double tolerance) {
    if (value >= range.min() && value <= range.max()) return 1;
    return Math.clamp(1 - Math.max(range.min() - value, value - range.max()) / tolerance, 0, 1);
  }

  public static double vigor(int stage, double water, Environment env, GrowthProfile profile) {
    Map<String, Double> values =
        Map.of(
            "water",
            water,
            "light",
            env.light(),
            "humidity",
            env.humidity(),
            "temperature",
            env.temperature(),
            "nutrients",
            env.nutrients());
    double mean = 0, worst = 1;
    for (var entry : profile.weights().entrySet()) {
      double score =
          entry.getKey().equals("schedule")
              ? env.schedule()
              : comfort(
                  values.get(entry.getKey()),
                  profile.stages().get(stage).get(entry.getKey()),
                  profile.tolerance());
      mean += score * entry.getValue();
      worst = Math.min(worst, score);
    }
    return profile.meanWeight() * mean + (1 - profile.meanWeight()) * worst;
  }

  public static PlantState advance(
      PlantState initial, long now, Environment env, GrowthProfile profile, String difficulty) {
    if (now <= initial.lastSimTime()) return initial;
    long elapsed = Math.min(now - initial.lastSimTime(), profile.catchupCap());
    long remaining = elapsed;
    int stage = initial.stage();
    double progress = initial.progress(), water = initial.water(), care = initial.careIntegral();
    long careTicks = initial.careTicks();
    while (remaining > 0) {
      long step = Math.min(remaining, profile.quantum());
      double drained = profile.waterDrain() * step / 24000.0;
      double vigor = vigor(stage, Math.max(0, water - drained / 2), env, profile);
      if (stage < 3) {
        double rate =
            (profile.minimumGrowth() + (profile.maximumGrowth() - profile.minimumGrowth()) * vigor)
                / profile.difficulty().get(difficulty);
        double amount = step * rate;
        while (stage < 3 && amount > 0) {
          double required = (1 - progress) * profile.stageTicks().get(stage);
          if (amount < required) {
            progress += amount / profile.stageTicks().get(stage);
            amount = 0;
          } else {
            amount -= required;
            stage++;
            progress = stage == 3 ? 1 : 0;
          }
        }
        care += vigor * step;
        careTicks += step;
      }
      water = Math.max(0, water - drained);
      remaining -= step;
    }
    return new PlantState(
        initial.genome(),
        stage,
        Math.clamp(progress, 0, 1),
        water,
        now,
        care,
        careTicks,
        initial.owner());
  }

  private PlantSimulation() {}
}
