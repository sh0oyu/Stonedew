package dev.stonedew.core;

import net.neoforged.neoforge.common.ModConfigSpec;

public final class StonedewConfig {
  public enum Difficulty {
    CHILL,
    GROWER,
    CONNOISSEUR
  }

  public enum Dread {
    COZY,
    UNEASY,
    EERIE
  }

  public static final ModConfigSpec SERVER;
  public static final ModConfigSpec CLIENT;
  public static final ModConfigSpec.EnumValue<Difficulty> DIFFICULTY;
  public static final ModConfigSpec.EnumValue<Dread> DREAD;
  public static final ModConfigSpec.BooleanValue HERBAL_MODE;
  public static final ModConfigSpec.IntValue ROOM_VOLUME_CAP;
  public static final ModConfigSpec.BooleanValue ATMOSPHERE;
  public static final ModConfigSpec.BooleanValue CAMERA_MOMENTS;
  public static final ModConfigSpec.BooleanValue MINIGAMES;
  public static final ModConfigSpec.BooleanValue SCREEN_TINT;
  public static final ModConfigSpec.BooleanValue SUDDEN_SOUNDS;
  public static final ModConfigSpec.DoubleValue VISUAL_INTENSITY;
  public static final ModConfigSpec.DoubleValue AUDIO_DREAD;
  public static final ModConfigSpec.IntValue PARTICLE_BUDGET;

  static {
    var server = new ModConfigSpec.Builder();
    server
        .comment(
            "Authoritative world settings. Future gameplay systems consume these settings as their"
                + " phases arrive.")
        .push("gameplay");
    DIFFICULTY = server.defineEnum("difficulty", Difficulty.GROWER);
    DREAD = server.defineEnum("dread", Dread.UNEASY);
    HERBAL_MODE =
        server
            .comment(
                "Use the optional general-herb theme. No theme-dependent content exists in P0.")
            .define("herbalMode", false);
    ROOM_VOLUME_CAP = server.defineInRange("roomVolumeCap", 2000, 1, 32768);
    server.pop();
    SERVER = server.build();
    var client = new ModConfigSpec.Builder();
    client.push("accessibility");
    ATMOSPHERE = client.define("atmosphere", true);
    CAMERA_MOMENTS = client.define("cameraMoments", true);
    MINIGAMES = client.define("minigames", true);
    SCREEN_TINT = client.define("screenTint", true);
    SUDDEN_SOUNDS = client.define("suddenSounds", false);
    VISUAL_INTENSITY = client.defineInRange("visualIntensity", 0.5, 0.0, 1.0);
    AUDIO_DREAD = client.defineInRange("audioDread", 0.5, 0.0, 1.0);
    PARTICLE_BUDGET = client.defineInRange("particleBudget", 128, 0, 4096);
    client.pop();
    CLIENT = client.build();
  }

  private StonedewConfig() {}
}
