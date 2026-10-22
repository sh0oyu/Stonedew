package dev.stonedew.plant;

import net.minecraft.nbt.CompoundTag;

/** Compact presentation snapshot; no hidden genetics, quality history or owner is sent. */
public record PlantView(
    int stage,
    int progress,
    int water,
    int vigor,
    int light,
    int humidity,
    int leaf,
    int bud,
    int hair,
    String pigment,
    String habit) {
  public CompoundTag save() {
    var tag = new CompoundTag();
    tag.putInt("stage", stage);
    tag.putInt("progress", progress);
    tag.putInt("water", water);
    tag.putInt("vigor", vigor);
    tag.putInt("light", light);
    tag.putInt("humidity", humidity);
    tag.putInt("leaf", leaf);
    tag.putInt("bud", bud);
    tag.putInt("hair", hair);
    tag.putString("pigment", pigment);
    tag.putString("habit", habit);
    return tag;
  }

  public static PlantView load(CompoundTag tag) {
    return new PlantView(
        Math.clamp(tag.getInt("stage"), 0, 3),
        tag.getInt("progress"),
        tag.getInt("water"),
        tag.getInt("vigor"),
        tag.getInt("light"),
        tag.getInt("humidity"),
        tag.getInt("leaf"),
        tag.getInt("bud"),
        tag.getInt("hair"),
        tag.getString("pigment"),
        tag.getString("habit"));
  }
}
