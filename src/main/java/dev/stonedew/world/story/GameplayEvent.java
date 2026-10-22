package dev.stonedew.world.story;

import java.util.Map;
import java.util.UUID;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.neoforged.bus.api.Event;

/**
 * Server-only bridge for harvest, delivery, rank, time and observation producers in later phases.
 */
public final class GameplayEvent extends Event {
  private final MinecraftServer server;
  private final ResourceLocation kind;
  private final UUID player;
  private final Map<String, String> context;

  public GameplayEvent(
      MinecraftServer server, ResourceLocation kind, UUID player, Map<String, String> context) {
    this.server = java.util.Objects.requireNonNull(server);
    this.kind = java.util.Objects.requireNonNull(kind);
    this.player = player;
    this.context = Map.copyOf(context);
  }

  public MinecraftServer server() {
    return server;
  }

  public ResourceLocation kind() {
    return kind;
  }

  public UUID player() {
    return player;
  }

  public Map<String, String> context() {
    return context;
  }
}
