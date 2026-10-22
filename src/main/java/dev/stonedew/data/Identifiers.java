package dev.stonedew.data;

import java.util.regex.Pattern;

public final class Identifiers {
  private static final Pattern ID = Pattern.compile("[a-z0-9_.-]+:[a-z0-9/._-]+");

  public static String require(String value) {
    if (value == null || !ID.matcher(value).matches())
      throw new IllegalArgumentException("Invalid namespaced id: " + value);
    return value;
  }

  private Identifiers() {}
}
