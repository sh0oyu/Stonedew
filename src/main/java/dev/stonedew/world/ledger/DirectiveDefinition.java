package dev.stonedew.world.ledger;

import com.google.gson.JsonObject;
import java.util.List;

/** Most-specific completed flag set selects the next concrete instruction. */
public record DirectiveDefinition(List<Step> steps) {
  public record Step(int requiredFlags, String text) {
    public Step {
      if (requiredFlags < 0
          || requiredFlags > 65535
          || text == null
          || !text.matches("[a-z0-9_.-]+"))
        throw new IllegalArgumentException("Invalid Directive step");
    }
  }

  public DirectiveDefinition {
    steps = List.copyOf(steps);
    if (steps.isEmpty()
        || steps.stream().noneMatch(step -> step.requiredFlags() == 0)
        || steps.stream().map(Step::requiredFlags).distinct().count() != steps.size())
      throw new IllegalArgumentException("Directive requires a unique initial step");
  }

  public String select(int flags) {
    return steps.stream()
        .filter(step -> (flags & step.requiredFlags()) == step.requiredFlags())
        .max(java.util.Comparator.comparingInt(step -> Integer.bitCount(step.requiredFlags())))
        .orElseThrow()
        .text();
  }

  public static DirectiveDefinition read(JsonObject json) {
    var steps = new java.util.ArrayList<Step>();
    for (var value : json.getAsJsonArray("steps")) {
      var step = value.getAsJsonObject();
      steps.add(
          new Step(
              step.get("required_flags").getAsBigDecimal().intValueExact(),
              step.get("text").getAsString()));
    }
    return new DirectiveDefinition(steps);
  }
}
