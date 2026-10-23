package dev.stonedew.client;

import static org.junit.jupiter.api.Assertions.*;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import org.junit.jupiter.api.Test;

class PlantSurfaceGeometryTest {
  @Test
  void retainsShippedPistilsAndResinButRejectsCollapsedFaces() throws Exception {
    var positions = new ArrayList<float[]>();
    String material = "";
    int checked = 0;
    for (String line :
        Files.readAllLines(
            Path.of("src/main/resources/assets/stonedew/models/block/plants/plant_3_0_0.obj"))) {
      String[] parts = line.split(" ");
      if (line.startsWith("v ")) {
        positions.add(
            new float[] {
              Float.parseFloat(parts[1]), Float.parseFloat(parts[2]), Float.parseFloat(parts[3])
            });
      } else if (line.startsWith("usemtl ")) {
        material = parts[1];
      } else if (line.startsWith("f ") && (material.equals("hair") || material.equals("resin"))) {
        float[][] axis = new float[3][4];
        for (int vertex = 0; vertex < 4; vertex++) {
          String ref = parts[Math.min(vertex + 1, parts.length - 1)];
          float[] point = positions.get(Integer.parseInt(ref.split("/")[0]) - 1);
          for (int a = 0; a < 3; a++) axis[a][vertex] = point[a];
        }
        assertTrue(PlantSurfaceGeometry.hasArea(axis[0], axis[1], axis[2]), material + ": " + line);
        checked++;
      }
    }
    assertTrue(checked > 100, "Exercise the real shipped detail geometry");
    assertFalse(PlantSurfaceGeometry.hasArea(new float[4], new float[4], new float[4]));
  }
}
