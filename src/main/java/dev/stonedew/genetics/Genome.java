package dev.stonedew.genetics;

import dev.stonedew.data.Identifiers;
import java.util.Map;

/** Schema-neutral immutable diploid value. Full inheritance arrives in P5. */
public record Genome(String schema, long lineageSeed, Map<String, Alleles> genes) {
  public record Alleles(String maternal, String paternal) {
    public Alleles {
      if (maternal == null
          || paternal == null
          || maternal.isBlank()
          || paternal.isBlank()
          || maternal.length() > 32
          || paternal.length() > 32) throw new IllegalArgumentException("Invalid allele pair");
    }
  }

  public Genome {
    Identifiers.require(schema);
    genes = Map.copyOf(genes);
    if (genes.isEmpty() || genes.size() > 16)
      throw new IllegalArgumentException("Invalid genome size");
  }

  public static Genome wild(String pigment, long seed) {
    return new Genome(
        "stonedew:herb",
        seed,
        Map.of(
            "potency",
            new Alleles("5", "5"),
            "yield",
            new Alleles("5", "5"),
            "speed",
            new Alleles("5", "5"),
            "resilience",
            new Alleles("5", "5"),
            "terpene",
            new Alleles("linalool", "pinene"),
            "pigment",
            new Alleles(pigment, pigment),
            "habit",
            new Alleles("bushy", "bushy"),
            "luminescence",
            new Alleles("dormant", "dormant")));
  }

  public String pigment() {
    return genes.getOrDefault("pigment", new Alleles("green", "green")).maternal();
  }

  public String habit() {
    return genes.getOrDefault("habit", new Alleles("hybrid", "hybrid")).maternal();
  }

  public int leafColor() {
    return switch (pigment()) {
      case "teal" -> 0x45B999;
      case "amber" -> 0x64AE49;
      case "violet" -> 0x54A749;
      default -> 0x4FBF5A;
    };
  }

  public int budColor() {
    return switch (pigment()) {
      case "teal" -> 0x4FE8E0;
      case "amber" -> 0xFFC247;
      case "violet" -> 0xB642FF;
      default -> 0xB9D953;
    };
  }

  public int hairColor() {
    return switch (pigment()) {
      case "teal" -> 0xD0FCF1;
      case "violet" -> 0xD5A0EF;
      default -> 0xF5BA3A;
    };
  }
}
