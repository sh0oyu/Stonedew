package dev.stonedew.plant;

import com.google.gson.JsonObject;
import java.util.List;
import java.util.Map;

/** All gameplay tuning is loaded from the cultivar's environment-profile JSON. */
public record GrowthProfile(
    List<Long> stageTicks,
    List<Map<String, Range>> stages,
    Map<String, Double> weights,
    int quantum,
    int updateInterval,
    long catchupCap,
    double waterDrain,
    double waterPerPour,
    int canPours,
    long lampFuel,
    int lampRadius,
    double lampOutput,
    double lampFalloff,
    double humidity,
    double temperature,
    double airflow,
    double tolerance,
    double minimumGrowth,
    double maximumGrowth,
    double meanWeight,
    Map<String, Double> difficulty) {
  public record Range(double min, double max) {
    public Range {
      if (!Double.isFinite(min) || !Double.isFinite(max) || min > max)
        throw new IllegalArgumentException("Invalid comfort range");
    }
  }

  public GrowthProfile {
    stageTicks = List.copyOf(stageTicks);
    stages = stages.stream().map(Map::copyOf).toList();
    weights = Map.copyOf(weights);
    difficulty = Map.copyOf(difficulty);
    if (stageTicks.size() != 4
        || stages.size() != 4
        || stageTicks.stream().anyMatch(v -> v < 1)
        || quantum < 20
        || updateInterval < 20
        || catchupCap < 1
        || catchupCap > 168000
        || canPours < 1
        || canPours > 1024
        || lampFuel < 1
        || lampRadius < 1
        || lampRadius > 16
        || lampOutput < 0
        || lampFalloff < 0
        || humidity < 0
        || humidity > 100
        || airflow < 0
        || airflow > 100
        || weights.values().stream().anyMatch(v -> !Double.isFinite(v) || v < 0 || v > 1)
        || waterDrain < 0
        || waterPerPour <= 0
        || tolerance <= 0
        || minimumGrowth <= 0
        || maximumGrowth < minimumGrowth
        || meanWeight < 0
        || meanWeight > 1
        || Math.abs(weights.values().stream().mapToDouble(Double::doubleValue).sum() - 1) > 0.0001)
      throw new IllegalArgumentException("Invalid growth profile");
    if (!weights
        .keySet()
        .equals(
            java.util.Set.of("water", "light", "humidity", "temperature", "nutrients", "schedule")))
      throw new IllegalArgumentException("Invalid Vigor weights");
    for (var stage : stages)
      for (String key : List.of("water", "light", "humidity", "temperature", "nutrients"))
        if (!stage.containsKey(key))
          throw new IllegalArgumentException("Missing stage range " + key);
    if (!difficulty.keySet().equals(java.util.Set.of("CHILL", "GROWER", "CONNOISSEUR"))
        || difficulty.values().stream().anyMatch(v -> !Double.isFinite(v) || v <= 0))
      throw new IllegalArgumentException("Invalid difficulty multipliers");
  }

  public static GrowthProfile read(JsonObject json) {
    var durations = json.getAsJsonObject("stage_ticks");
    var stages = new java.util.ArrayList<Map<String, Range>>();
    for (var value : json.getAsJsonArray("stages")) {
      var stage = new java.util.HashMap<String, Range>();
      value
          .getAsJsonObject()
          .entrySet()
          .forEach(
              entry -> {
                var array = entry.getValue().getAsJsonArray();
                if (array.size() != 2)
                  throw new IllegalArgumentException("Range must have two bounds");
                stage.put(
                    entry.getKey(),
                    new Range(array.get(0).getAsDouble(), array.get(1).getAsDouble()));
              });
      stages.add(stage);
    }
    return new GrowthProfile(
        List.of(
            durations.get("seedling").getAsBigDecimal().longValueExact(),
            durations.get("vegetative").getAsBigDecimal().longValueExact(),
            durations.get("flowering").getAsBigDecimal().longValueExact(),
            durations.get("ripe_window").getAsBigDecimal().longValueExact()),
        stages,
        doubles(json.getAsJsonObject("vigor_weights")),
        json.get("simulation_quantum").getAsInt(),
        json.get("update_interval").getAsInt(),
        json.get("catchup_cap_ticks").getAsLong(),
        n(json, "water_drain_per_day"),
        n(json, "water_per_pour"),
        json.get("can_pours").getAsInt(),
        json.get("lamp_fuel_ticks").getAsLong(),
        json.get("lamp_radius").getAsInt(),
        n(json, "lamp_output"),
        n(json, "lamp_falloff"),
        n(json, "ambient_humidity"),
        n(json, "ambient_temperature"),
        n(json, "ambient_airflow"),
        n(json, "comfort_tolerance"),
        n(json, "minimum_growth"),
        n(json, "maximum_growth"),
        n(json, "comfort_mean_weight"),
        doubles(json.getAsJsonObject("difficulty_growth")));
  }

  private static double n(JsonObject json, String key) {
    double value = json.get(key).getAsDouble();
    if (!Double.isFinite(value))
      throw new IllegalArgumentException("Nonfinite profile value: " + key);
    return value;
  }

  private static Map<String, Double> doubles(JsonObject json) {
    var map = new java.util.HashMap<String, Double>();
    json.entrySet().forEach(entry -> map.put(entry.getKey(), n(json, entry.getKey())));
    return map;
  }
}
