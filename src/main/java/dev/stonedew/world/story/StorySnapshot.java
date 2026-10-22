package dev.stonedew.world.story;

import java.util.Map;
import java.util.Set;

/**
 * Immutable per-world narrative state; per-player progress and facility permissions are separate
 * future systems.
 */
public record StorySnapshot(
    Set<String> flags,
    Set<String> discoveredClues,
    Map<String, Integer> threadProgress,
    Set<String> verifiedRules,
    int attention,
    int standing,
    int keeperCount,
    Map<String, Long> eventCounts) {
  public StorySnapshot {
    flags = Set.copyOf(flags);
    discoveredClues = Set.copyOf(discoveredClues);
    threadProgress = Map.copyOf(threadProgress);
    verifiedRules = Set.copyOf(verifiedRules);
    eventCounts = Map.copyOf(eventCounts);
    if (attention < 0 || attention > 100 || standing < 0 || standing > 100 || keeperCount < 1)
      throw new IllegalArgumentException("Invalid story meters");
    if (threadProgress.values().stream().anyMatch(value -> value < 0)
        || eventCounts.values().stream().anyMatch(value -> value < 0))
      throw new IllegalArgumentException("Negative story progress");
  }

  public static StorySnapshot initial() {
    return new StorySnapshot(Set.of(), Set.of(), Map.of(), Set.of(), 0, 0, 7, Map.of());
  }

  public StorySnapshot record(String event) {
    var counts = new java.util.HashMap<>(eventCounts);
    counts.merge(event, 1L, Math::addExact);
    return new StorySnapshot(
        flags,
        discoveredClues,
        threadProgress,
        verifiedRules,
        attention,
        standing,
        keeperCount,
        counts);
  }
}
