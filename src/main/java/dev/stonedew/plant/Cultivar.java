package dev.stonedew.plant;

/**
 * Organism-neutral binding. Profiles refer to datapack identifiers, not hardcoded plant classes.
 */
public interface Cultivar {
  enum Type {
    PLANT,
    FUNGUS
  }

  String id();

  Type type();

  String geneSchema();

  String environmentProfile();

  String processChain();

  String effectMap();
}
