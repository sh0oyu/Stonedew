package dev.stonedew.core;

import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.saveddata.SavedData;
import net.neoforged.neoforge.event.level.SleepFinishedTimeEvent;

/**
 * Monotonic world time including skipped sleep hours. Does not advance while the server is stopped.
 */
public final class GrowthClock extends SavedData {
  private long offset;

  private static GrowthClock get(MinecraftServer server) {
    var failure = new java.util.concurrent.atomic.AtomicReference<RuntimeException>();
    return server
        .overworld()
        .getDataStorage()
        .computeIfAbsent(
            new Factory<>(
                () -> {
                  if (failure.get() != null)
                    throw new IllegalStateException(
                        "Growth clock could not be loaded", failure.get());
                  return new GrowthClock();
                },
                (tag, registries) -> {
                  try {
                    if (tag.getInt("dataVersion") != 1 || tag.getLong("offset") < 0)
                      throw new IllegalArgumentException("Invalid growth clock save");
                    var clock = new GrowthClock();
                    clock.offset = tag.getLong("offset");
                    return clock;
                  } catch (RuntimeException e) {
                    failure.set(e);
                    throw e;
                  }
                },
                null),
            "stonedew_growth_clock");
  }

  public static long now(Level level) {
    return level.isClientSide
        ? level.getGameTime()
        : Math.addExact(level.getGameTime(), get(level.getServer()).offset);
  }

  public static void advance(MinecraftServer server, long ticks) {
    if (ticks < 0) throw new IllegalArgumentException("Negative time jump");
    var clock = get(server);
    clock.offset = Math.addExact(clock.offset, ticks);
    clock.setDirty();
  }

  public static void slept(SleepFinishedTimeEvent event) {
    if (event.getLevel() instanceof net.minecraft.server.level.ServerLevel level)
      advance(level.getServer(), Math.max(0, event.getNewTime() - level.getDayTime()));
  }

  @Override
  public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
    tag.putInt("dataVersion", 1);
    tag.putLong("offset", offset);
    return tag;
  }
}
