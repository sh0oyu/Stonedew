package dev.stonedew.client;

import dev.stonedew.Stonedew;
import java.util.Arrays;

/** Opt-in developer measurement; no timers or allocations in ordinary play. */
final class PlantRenderStats {
  static final boolean ENABLED = Boolean.getBoolean("stonedew.profileRender");
  private static final long[] SAMPLES = new long[4096];
  private static long start = System.nanoTime(), nanos, faces, trays, frameNanos;
  private static int frames;

  static void tray(long elapsed, int surfaces) {
    nanos += elapsed;
    frameNanos += elapsed;
    faces += surfaces;
    trays++;
  }

  static void frame() {
    if (!ENABLED) return;
    SAMPLES[frames % SAMPLES.length] = frameNanos;
    frameNanos = 0;
    frames++;
    long now = System.nanoTime();
    if (now - start < 10_000_000_000L) return;
    var sorted = Arrays.copyOf(SAMPLES, Math.min(frames, SAMPLES.length));
    Arrays.sort(sorted);
    Stonedew.LOGGER.info(
        "Plant render profile: frames={} fps={} trays/frame={} faces/frame={} CPU mean={}ms"
            + " p95={}ms",
        frames,
        net.minecraft.client.Minecraft.getInstance().getFps(),
        (double) trays / frames,
        (double) faces / frames,
        nanos / (frames * 1_000_000.0),
        sorted[(int) ((sorted.length - 1) * .95)] / 1_000_000.0);
    frames = 0;
    nanos = faces = trays = 0;
    start = now;
  }
}
