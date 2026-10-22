package dev.stonedew.core;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.network.PacketDistributor;

/** Per-player introductory flags. Never used as the authoritative plant state. */
public final class PlayerProgress {
  public static final int PLANTED = 1, WATERED = 2, LIT = 4, RIPE = 8;

  private static CompoundTag data(Player player) {
    CompoundTag root = player.getPersistentData();
    if (!root.contains("stonedew_progress")) {
      var created = new CompoundTag();
      created.putInt("dataVersion", 1);
      created.putInt("flags", 0);
      root.put("stonedew_progress", created);
    }
    var data = root.getCompound("stonedew_progress");
    if (data.getInt("dataVersion") != 1)
      throw new IllegalStateException("Unsupported player progress version");
    return data;
  }

  public static int flags(Player player) {
    return data(player).getInt("flags");
  }

  public static void mark(Player player, int flag) {
    if (player instanceof ServerPlayer server) {
      int old = flags(player), updated = old | flag;
      if (old != updated) {
        data(player).putInt("flags", updated);
        sync(server);
      }
    }
  }

  public static String directive(int flags) {
    if ((flags & PLANTED) == 0) return "directive.stonedew.plant";
    if ((flags & WATERED) == 0) return "directive.stonedew.water";
    if ((flags & LIT) == 0) return "directive.stonedew.light";
    return (flags & RIPE) == 0 ? "directive.stonedew.grow" : "directive.stonedew.ripe";
  }

  public static void sync(ServerPlayer player) {
    PacketDistributor.sendToPlayer(
        player,
        new ProgressPayload(
            flags(player),
            dev.stonedew.data.DefinitionReloadListener.current().directive(flags(player))));
  }

  public static void login(PlayerEvent.PlayerLoggedInEvent event) {
    if (event.getEntity() instanceof ServerPlayer player) sync(player);
  }

  public static void clone(PlayerEvent.Clone event) {
    event
        .getEntity()
        .getPersistentData()
        .put("stonedew_progress", data(event.getOriginal()).copy());
  }

  public static void respawn(PlayerEvent.PlayerRespawnEvent event) {
    if (event.getEntity() instanceof ServerPlayer player) sync(player);
  }

  public static String clientDirective(Player player) {
    String key = data(player).getString("directive");
    return key.isEmpty() ? directive(flags(player)) : key;
  }

  public static void datapackSync(net.neoforged.neoforge.event.OnDatapackSyncEvent event) {
    if (event.getPlayer() != null) sync(event.getPlayer());
    else event.getPlayerList().getPlayers().forEach(PlayerProgress::sync);
  }

  public static void accept(Player player, int flags, String directive) {
    data(player).putInt("flags", flags);
    data(player).putString("directive", directive);
  }

  private PlayerProgress() {}
}
