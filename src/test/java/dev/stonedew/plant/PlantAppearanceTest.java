package dev.stonedew.plant;

import static org.junit.jupiter.api.Assertions.*;

import com.google.gson.JsonParser;
import dev.stonedew.genetics.Genome;
import java.util.HashSet;
import org.junit.jupiter.api.Test;

class PlantAppearanceTest {
  @Test
  void samePacketCanProduceDistinctPlantsWithoutChangingItsGenes() {
    var genome = Genome.wild("violet", 19);
    var shapes = new HashSet<Integer>();
    var loads = new HashSet<Integer>();
    var identities = new HashSet<PlantAppearance>();
    for (long seed = 0; seed < 256; seed++) {
      var plant = PlantState.seed(genome, 100, "", seed);
      assertEquals(genome, plant.genome());
      shapes.add(plant.appearance().shape());
      loads.add(plant.appearance().budLoad());
      identities.add(plant.appearance());
      assertTrue(plant.appearance().height() >= 90 && plant.appearance().height() <= 110);
      assertTrue(plant.appearance().spread() >= 90 && plant.appearance().spread() <= 110);
    }
    assertEquals(4, shapes.size());
    assertEquals(3, loads.size());
    assertTrue(identities.size() > 240);
  }

  @Test
  void identitySurvivesCareGrowthGenomeChangesAndSaveReload() throws Exception {
    var plant = PlantState.seed(Genome.wild("green", 7), 100, "", -839174621L);
    var original = plant.appearance();
    plant = plant.water(30).stage(2).genome(Genome.wild("violet", 99));
    var profile =
        GrowthProfile.read(
            JsonParser.parseString(
                    java.nio.file.Files.readString(
                        java.nio.file.Path.of(
                            "src/main/resources/data/stonedew/stonedew/environment_profiles/herb.json")))
                .getAsJsonObject());
    plant =
        PlantSimulation.advance(
            plant, 1000, new PlantSimulation.Environment(50, 75, 24, 50, 35, 1), profile, "GROWER");
    assertEquals(original, plant.appearance());
    var reloaded = PlantSerialization.read(PlantSerialization.write(plant));
    assertEquals(plant, reloaded);
    assertEquals(original, reloaded.appearance());
  }

  @Test
  void legacyPlantSavesMigrateWithoutLosingCareOrGenes() {
    var plant = PlantState.seed(Genome.wild("teal", 319), 100, "").water(25).stage(2);
    var json = JsonParser.parseString(PlantSerialization.write(plant)).getAsJsonObject();
    json.remove("appearanceSeed");
    var migrated = PlantSerialization.read(json.toString());
    assertEquals(plant, migrated);
    assertEquals(migrated, PlantSerialization.read(PlantSerialization.write(migrated)));
  }

  @Test
  void fractionalVisualIdentityIsRejectedRatherThanTruncated() {
    var json =
        JsonParser.parseString(
                PlantSerialization.write(PlantState.seed(Genome.wild("teal", 1), 0, "")))
            .getAsJsonObject();
    json.addProperty("appearanceSeed", 1.5);
    assertThrows(ArithmeticException.class, () -> PlantSerialization.read(json.toString()));
  }
}
