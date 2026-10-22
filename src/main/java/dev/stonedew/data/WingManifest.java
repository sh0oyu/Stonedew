package dev.stonedew.data;

import java.util.List;

/**
 * P0 manifest identity and cultivar bindings; remaining content stays in the validated JSON index.
 */
public record WingManifest(String id, String displayName, List<String> cultivars) {
  public WingManifest {
    Identifiers.require(id);
    if (displayName == null || displayName.isBlank())
      throw new IllegalArgumentException("Wing requires a language key");
    cultivars = List.copyOf(cultivars);
    cultivars.forEach(Identifiers::require);
  }
}
