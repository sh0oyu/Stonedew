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
    String habit,
    int shape,
    int budLoad,
    int height,
    int spread,
    int rotation) {
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
    tag.putInt("shape", shape);
    tag.putInt("budLoad", budLoad);
    tag.putInt("height", height);
    tag.putInt("spread", spread);
    tag.putInt("rotation", rotation);
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
        tag.getString("habit"),
        Math.clamp(tag.getInt("shape"), 0, 3),
        Math.clamp(tag.getInt("budLoad"), 0, 2),
        tag.contains("height") ? Math.clamp(tag.getInt("height"), 90, 110) : 100,
        tag.contains("spread") ? Math.clamp(tag.getInt("spread"), 90, 110) : 100,
        Math.floorMod(tag.getInt("rotation"), 360));
  }
}
