package dev.stonedew.world.ledger;

import static org.junit.jupiter.api.Assertions.*;

import com.google.gson.JsonParser;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;

class DirectiveDefinitionTest {
  private DirectiveDefinition definition() throws Exception {
    return DirectiveDefinition.read(
        JsonParser.parseString(
                Files.readString(
                    Path.of(
                        "src/main/resources/data/stonedew/stonedew/directives/first_grow.json")))
            .getAsJsonObject());
  }

  @Test
  void firstGrowDirectivesFollowCompletedActions() throws Exception {
    var d = definition();
    assertEquals("directive.stonedew.plant", d.select(0));
    assertEquals("directive.stonedew.water", d.select(1));
    assertEquals("directive.stonedew.light", d.select(3));
    assertEquals("directive.stonedew.grow", d.select(7));
    assertEquals("directive.stonedew.ripe", d.select(15));
  }

  @Test
  void CompletingLightFirstDoesNotSkipWater() throws Exception {
    assertEquals("directive.stonedew.water", definition().select(5));
  }

  @Test
  void missingInitialInstructionIsRejected() {
    assertThrows(
        IllegalArgumentException.class,
        () -> new DirectiveDefinition(List.of(new DirectiveDefinition.Step(1, "text.x"))));
  }

  @Test
  void duplicateConditionsAreRejected() {
    assertThrows(
        IllegalArgumentException.class,
        () ->
            new DirectiveDefinition(
                List.of(
                    new DirectiveDefinition.Step(0, "text.a"),
                    new DirectiveDefinition.Step(0, "text.b"))));
  }

  @Test
  void proseCannotReplaceLanguageKey() {
    assertThrows(
        IllegalArgumentException.class, () -> new DirectiveDefinition.Step(0, "Go plant a seed!"));
  }
}
