package dev.stonedew.plant;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public final class PlantSerialization {
  private static final Gson GSON = new Gson();
  public static final int DATA_VERSION = 1;

  public static String write(PlantState state) {
    JsonObject json = GSON.toJsonTree(state).getAsJsonObject();
    json.addProperty("dataVersion", DATA_VERSION);
    return json.toString();
  }

  public static PlantState read(String text) {
    JsonObject json = JsonParser.parseString(text).getAsJsonObject();
    if (!json.has("dataVersion")
        || !json.get("dataVersion").getAsJsonPrimitive().isNumber()
        || json.get("dataVersion").getAsBigDecimal().intValueExact() != DATA_VERSION)
      throw new IllegalArgumentException("Unsupported plant dataVersion");
    for (String field :
        java.util.List.of(
            "genome",
            "stage",
            "progress",
            "water",
            "lastSimTime",
            "careIntegral",
            "careTicks",
            "owner"))
      if (!json.has(field)) throw new IllegalArgumentException("Missing plant field: " + field);
    for (String field : java.util.List.of("stage", "lastSimTime", "careTicks")) {
      if (!json.get(field).isJsonPrimitive() || !json.get(field).getAsJsonPrimitive().isNumber())
        throw new IllegalArgumentException("Invalid numeric plant field");
      json.get(field).getAsBigDecimal().longValueExact();
    }
    // Version 1 saves predate visual identity. Derive it once without changing any genes.
    if (!json.has("appearanceSeed"))
      json.addProperty(
          "appearanceSeed", json.getAsJsonObject("genome").get("lineageSeed").getAsLong());
    if (!json.get("appearanceSeed").isJsonPrimitive()
        || !json.get("appearanceSeed").getAsJsonPrimitive().isNumber())
      throw new IllegalArgumentException("Invalid appearance seed");
    json.get("appearanceSeed").getAsBigDecimal().longValueExact();
    return GSON.fromJson(json, PlantState.class);
  }

  private PlantSerialization() {}
}
