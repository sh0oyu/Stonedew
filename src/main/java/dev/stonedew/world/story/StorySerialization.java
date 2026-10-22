package dev.stonedew.world.story;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

/**
 * Schema 0 is a documented pre-release format; future versions fail instead of silently losing
 * progress.
 */
public final class StorySerialization {
  public static final int DATA_VERSION = 1;
  private static final Gson GSON = new Gson();

  public static String write(StorySnapshot state) {
    JsonObject object = GSON.toJsonTree(state).getAsJsonObject();
    object.addProperty("dataVersion", DATA_VERSION);
    return object.toString();
  }

  public static StorySnapshot read(String json) {
    JsonObject object = JsonParser.parseString(json).getAsJsonObject().deepCopy();
    int version = object.has("dataVersion") ? integer(object, "dataVersion") : 0;
    if (version < 0 || version > DATA_VERSION)
      throw new IllegalArgumentException("Unsupported Stonedew story dataVersion " + version);
    if (version == 0) {
      if (object.has("knownClues") && !object.has("discoveredClues"))
        object.add("discoveredClues", object.remove("knownClues"));
      // Prototype saves lacked these collections and the Keeper number.
      JsonObject defaults = GSON.toJsonTree(StorySnapshot.initial()).getAsJsonObject();
      defaults
          .entrySet()
          .forEach(
              entry -> {
                if (!object.has(entry.getKey())) object.add(entry.getKey(), entry.getValue());
              });
      object.addProperty("dataVersion", DATA_VERSION);
    }
    return new StorySnapshot(
        strings(object, "flags"),
        strings(object, "discoveredClues"),
        intMap(object, "threadProgress"),
        strings(object, "verifiedRules"),
        integer(object, "attention"),
        integer(object, "standing"),
        integer(object, "keeperCount"),
        longMap(object, "eventCounts"));
  }

  private static int integer(JsonObject object, String key) {
    return number(object.get(key)).intValueExact();
  }

  private static java.math.BigDecimal number(com.google.gson.JsonElement value) {
    if (value == null || !value.isJsonPrimitive() || !value.getAsJsonPrimitive().isNumber())
      throw new IllegalArgumentException("Expected numeric story field");
    return value.getAsBigDecimal();
  }

  private static java.util.Set<String> strings(JsonObject object, String key) {
    var values = new java.util.HashSet<String>();
    for (var value : object.getAsJsonArray(key)) {
      if (!value.isJsonPrimitive() || !value.getAsJsonPrimitive().isString())
        throw new IllegalArgumentException("Expected story string: " + key);
      values.add(value.getAsString());
    }
    return values;
  }

  private static java.util.Map<String, Integer> intMap(JsonObject object, String key) {
    var values = new java.util.HashMap<String, Integer>();
    object
        .getAsJsonObject(key)
        .entrySet()
        .forEach(entry -> values.put(entry.getKey(), number(entry.getValue()).intValueExact()));
    return values;
  }

  private static java.util.Map<String, Long> longMap(JsonObject object, String key) {
    var values = new java.util.HashMap<String, Long>();
    object
        .getAsJsonObject(key)
        .entrySet()
        .forEach(entry -> values.put(entry.getKey(), number(entry.getValue()).longValueExact()));
    return values;
  }

  private StorySerialization() {}
}
