package dev.stonedew.plant;

import com.google.gson.JsonParser;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public final class PlantTuning {
  private static final GrowthProfile DEFAULT = readDefault();

  private static GrowthProfile readDefault() {
    try (var input =
        PlantTuning.class.getResourceAsStream(
            "/data/stonedew/stonedew/environment_profiles/herb.json")) {
      if (input == null) throw new IllegalStateException("Bundled plant tuning is missing");
      return GrowthProfile.read(
          JsonParser.parseReader(new InputStreamReader(input, StandardCharsets.UTF_8))
              .getAsJsonObject());
    } catch (java.io.IOException e) {
      throw new java.io.UncheckedIOException(e);
    }
  }

  public static GrowthProfile defaults() {
    return DEFAULT;
  }

  private PlantTuning() {}
}
