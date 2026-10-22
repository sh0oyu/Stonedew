package dev.stonedew.plant;

import static org.junit.jupiter.api.Assertions.*;

import com.google.gson.JsonParser;
import dev.stonedew.genetics.Genome;
import java.nio.file.Files;
import java.nio.file.Path;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class PlantSimulationTest {
  private GrowthProfile profile;
  private PlantSimulation.Environment comfortable;

  @BeforeEach
  void setup() throws Exception {
    profile =
        GrowthProfile.read(
            JsonParser.parseString(
                    Files.readString(
                        Path.of(
                            "src/main/resources/data/stonedew/stonedew/environment_profiles/herb.json")))
                .getAsJsonObject());
    comfortable = new PlantSimulation.Environment(50, 75, 24, 50, 35, 1);
  }

  private PlantState seed() {
    return PlantState.seed(Genome.wild("violet", 45), 0, "").water(30);
  }

  @Test
  void perfectComfortScoresOne() {
    assertEquals(1, PlantSimulation.vigor(0, 70, comfortable, profile), 1e-9);
  }

  @Test
  void worstFactorPenalizesAnOtherwiseComfortablePlant() {
    assertTrue(PlantSimulation.vigor(0, 0, comfortable, profile) < 0.7);
  }

  @Test
  void comfortFallsLinearlyAndClamps() {
    var range = new GrowthProfile.Range(40, 60);
    assertEquals(1, PlantSimulation.comfort(50, range, 20));
    assertEquals(0.5, PlantSimulation.comfort(30, range, 20));
    assertEquals(0, PlantSimulation.comfort(0, range, 20));
  }

  @Test
  void hydratedLitPlantGrowsFaster() {
    var dark = new PlantSimulation.Environment(0, 75, 24, 50, 35, 1);
    assertTrue(
        PlantSimulation.advance(seed(), 8000, comfortable, profile, "GROWER").progress()
            > PlantSimulation.advance(seed(), 8000, dark, profile, "GROWER").progress());
  }

  @Test
  void poorCareSlowsGrowthWithoutDeletingPlant() {
    var state =
        PlantSimulation.advance(
            seed().water(-100),
            12000,
            new PlantSimulation.Environment(0, 0, 0, 0, 0, 0),
            profile,
            "GROWER");
    assertTrue(state.progress() > 0);
    assertEquals(0, state.water());
    assertEquals(seed().genome(), state.genome());
  }

  @Test
  void stageTransitionCarriesProgressForward() {
    var grown = PlantSimulation.advance(seed(), 16000, comfortable, profile, "GROWER");
    assertEquals(1, grown.stage());
    assertTrue(grown.progress() > 0);
  }

  @Test
  void chunkCatchupMatchesSmallStepsWithinOnePercent() {
    var one = PlantSimulation.advance(seed(), 16000, comfortable, profile, "GROWER");
    var many = seed();
    for (int tick = 20; tick <= 16000; tick += 20)
      many = PlantSimulation.advance(many, tick, comfortable, profile, "GROWER");
    assertEquals(one.stage(), many.stage());
    assertEquals(one.progress(), many.progress(), 0.01);
    assertEquals(one.water(), many.water(), 1e-8);
  }

  @Test
  void catchupCapCannotBeRepeatedForFreeGrowth() {
    var huge = PlantSimulation.advance(seed(), 500000, comfortable, profile, "GROWER");
    var capped =
        PlantSimulation.advance(seed(), profile.catchupCap(), comfortable, profile, "GROWER");
    assertEquals(capped.stage(), huge.stage());
    assertEquals(capped.progress(), huge.progress(), 1e-9);
    assertEquals(capped.water(), huge.water(), 1e-9);
    assertEquals(500000, huge.lastSimTime());
    assertEquals(huge, PlantSimulation.advance(huge, 500000, comfortable, profile, "GROWER"));
  }

  @Test
  void timeCannotRunBackward() {
    assertEquals(seed(), PlantSimulation.advance(seed(), -20, comfortable, profile, "GROWER"));
  }

  @Test
  void repeatedCareCanReachRipe() {
    var state = seed();
    for (int tick = 2000; tick <= 100000; tick += 2000) {
      var ranges = profile.stages().get(state.stage());
      double water = (ranges.get("water").min() + ranges.get("water").max()) / 2;
      var env =
          new PlantSimulation.Environment(
              (ranges.get("light").min() + ranges.get("light").max()) / 2,
              (ranges.get("humidity").min() + ranges.get("humidity").max()) / 2,
              (ranges.get("temperature").min() + ranges.get("temperature").max()) / 2,
              50,
              (ranges.get("nutrients").min() + ranges.get("nutrients").max()) / 2,
              1);
      state =
          PlantSimulation.advance(
              state.water(Math.max(0, water - state.water())), tick, env, profile, "GROWER");
    }
    assertEquals(3, state.stage());
    assertEquals(1, state.progress());
  }

  @Test
  void ripePlantsRemainPresentDuringCatchup() {
    var state = PlantSimulation.advance(seed().stage(3), 40000, comfortable, profile, "GROWER");
    assertEquals(3, state.stage());
    assertEquals(1, state.progress());
  }

  @Test
  void wateringIsBounded() {
    assertEquals(100, seed().water(1000).water());
    assertEquals(0, seed().water(-1000).water());
  }

  @Test
  void difficultyChangesGrowthRate() {
    var chill = PlantSimulation.advance(seed(), 5000, comfortable, profile, "CHILL");
    var hard = PlantSimulation.advance(seed(), 5000, comfortable, profile, "CONNOISSEUR");
    assertTrue(chill.progress() > hard.progress());
  }

  @Test
  void nonfiniteEnvironmentIsRejected() {
    assertThrows(
        IllegalArgumentException.class,
        () -> new PlantSimulation.Environment(Double.NaN, 60, 24, 50, 50, 1));
  }

  @Test
  void invalidRangesAndWeightsAreRejected() throws Exception {
    assertThrows(IllegalArgumentException.class, () -> new GrowthProfile.Range(80, 20));
    var json =
        JsonParser.parseString(
                Files.readString(
                    Path.of(
                        "src/main/resources/data/stonedew/stonedew/environment_profiles/herb.json")))
            .getAsJsonObject();
    json.getAsJsonObject("vigor_weights").addProperty("water", -0.25);
    json.getAsJsonObject("vigor_weights").addProperty("light", 0.75);
    assertThrows(IllegalArgumentException.class, () -> GrowthProfile.read(json));
  }
}
