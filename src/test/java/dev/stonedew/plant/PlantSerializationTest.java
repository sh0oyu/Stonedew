package dev.stonedew.plant;

import static org.junit.jupiter.api.Assertions.*;

import com.google.gson.JsonParser;
import dev.stonedew.genetics.Genome;
import java.util.HashMap;
import org.junit.jupiter.api.Test;

class PlantSerializationTest {
  private PlantState seed() {
    return PlantState.seed(Genome.wild("teal", 900), 100, "12345678-1234-1234-1234-123456789012");
  }

  @Test
  void genomeAndCareRoundTrip() {
    var state = new PlantState(seed().genome(), 2, 0.8, 65, 1400, 850, 1000, seed().owner());
    assertEquals(state, PlantSerialization.read(PlantSerialization.write(state)));
  }

  @Test
  void futureVersionIsRejected() {
    var json = JsonParser.parseString(PlantSerialization.write(seed())).getAsJsonObject();
    json.addProperty("dataVersion", 2);
    assertThrows(IllegalArgumentException.class, () -> PlantSerialization.read(json.toString()));
  }

  @Test
  void missingVersionIsRejected() {
    assertThrows(IllegalArgumentException.class, () -> PlantSerialization.read("{}"));
  }

  @Test
  void missingStateIsRejected() {
    var json = JsonParser.parseString(PlantSerialization.write(seed())).getAsJsonObject();
    json.remove("water");
    assertThrows(IllegalArgumentException.class, () -> PlantSerialization.read(json.toString()));
  }

  @Test
  void fractionalStageIsNotRounded() {
    var json = JsonParser.parseString(PlantSerialization.write(seed())).getAsJsonObject();
    json.addProperty("stage", 1.5);
    assertThrows(ArithmeticException.class, () -> PlantSerialization.read(json.toString()));
  }

  @Test
  void invalidStateCannotEnterSimulation() {
    assertThrows(
        IllegalArgumentException.class,
        () -> new PlantState(seed().genome(), 4, 0, 50, 0, 0, 0, ""));
    assertThrows(
        IllegalArgumentException.class,
        () -> new PlantState(seed().genome(), 0, Double.NaN, 50, 0, 0, 0, ""));
  }

  @Test
  void genomeIsAnImmutableValue() {
    var genes = new HashMap<>(seed().genome().genes());
    var genome = new Genome("stonedew:herb", 1, genes);
    genes.clear();
    assertEquals(8, genome.genes().size());
    assertThrows(UnsupportedOperationException.class, () -> genome.genes().clear());
    assertEquals(genome, new Genome(genome.schema(), genome.lineageSeed(), genome.genes()));
  }

  @Test
  void visibleChannelsFollowPigment() {
    assertNotEquals(Genome.wild("violet", 1).budColor(), Genome.wild("teal", 1).budColor());
    assertNotEquals(seed().genome().leafColor(), seed().genome().budColor());
  }
}
