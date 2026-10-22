package dev.stonedew.plant;

import dev.stonedew.Stonedew;
import dev.stonedew.core.ModContent;
import dev.stonedew.core.PlayerProgress;
import dev.stonedew.core.StatusSource;
import dev.stonedew.core.StonedewConfig;
import dev.stonedew.data.DefinitionReloadListener;
import dev.stonedew.genetics.Genome;
import dev.stonedew.world.story.GameplayEvent;
import java.util.Arrays;
import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.common.NeoForge;

public final class GrowTrayBlockEntity extends BlockEntity implements StatusSource {
  private final PlantState[] plants;
  private final PlantView[] views;
  private final Map<Integer, CompoundTag> pending = new java.util.HashMap<>();

  public GrowTrayBlockEntity(BlockPos pos, BlockState state) {
    super(ModContent.GROW_TRAY.get(), pos, state);
    int size = ((GrowTrayBlock) state.getBlock()).slots();
    plants = new PlantState[size];
    views = new PlantView[size];
  }

  public boolean hasDisplayPlants() {
    return Arrays.stream(views).anyMatch(java.util.Objects::nonNull);
  }

  public int capacity() {
    return plants.length;
  }

  public PlantState plant(int slot) {
    return plants[Math.clamp(slot, 0, plants.length - 1)];
  }

  public PlantView view(int slot) {
    return views[Math.clamp(slot, 0, views.length - 1)];
  }

  public GrowthProfile profile() {
    return DefinitionReloadListener.current().growthProfile("stonedew:herb");
  }

  public int slot(Vec3 hit) {
    if (plants.length == 1) return 0;
    int grid = (int) Math.ceil(Math.sqrt(plants.length));
    return Math.clamp(
        Math.clamp((int) ((hit.x - worldPosition.getX()) * grid), 0, grid - 1)
            + grid * Math.clamp((int) ((hit.z - worldPosition.getZ()) * grid), 0, grid - 1),
        0,
        plants.length - 1);
  }

  public boolean hasPlants() {
    return Arrays.stream(plants).anyMatch(java.util.Objects::nonNull);
  }

  public long now() {
    return level == null ? 0 : dev.stonedew.core.GrowthClock.now(level);
  }

  public PlantSimulation.Environment environment() {
    double light =
        level.canSeeSky(worldPosition.above()) ? Math.max(0, 100 - level.getSkyDarken() * 8) : 0;
    GrowthProfile p = profile();
    for (BlockPos lamp :
        BlockPos.betweenClosed(
            worldPosition.offset(-p.lampRadius(), 1, -p.lampRadius()),
            worldPosition.offset(p.lampRadius(), p.lampRadius() + 2, p.lampRadius()))) {
      // Check loaded blocks only: a grow tray must never force neighboring chunks to load.
      if (level.hasChunkAt(lamp)
          && level.getBlockState(lamp).is(ModContent.BULB_LAMP.get())
          && level.getBlockState(lamp).getValue(BulbLampBlock.LIT))
        light += p.lampOutput() / (1 + p.lampFalloff() * lamp.distSqr(worldPosition));
    }
    return new PlantSimulation.Environment(
        Math.min(120, light), p.humidity(), p.temperature(), p.airflow(), 50, 1);
  }

  public void advance() {
    if (!(level instanceof ServerLevel server) || !hasPlants()) return;
    var env = environment();
    var p = profile();
    boolean changed = false;
    for (int i = 0; i < plants.length; i++)
      if (plants[i] != null) {
        PlantState old = plants[i],
            next =
                PlantSimulation.advance(old, now(), env, p, StonedewConfig.DIFFICULTY.get().name());
        plants[i] = next;
        changed |= !next.equals(old);
        if (old.stage() != next.stage()) {
          server.sendParticles(
              ParticleTypes.HAPPY_VILLAGER,
              worldPosition.getX() + 0.5,
              worldPosition.getY() + 1,
              worldPosition.getZ() + 0.5,
              8,
              0.3,
              0.3,
              0.3,
              0.01);
          level.playSound(
              null,
              worldPosition,
              SoundEvents.AMETHYST_BLOCK_CHIME,
              SoundSource.BLOCKS,
              0.5F,
              1.25F);
          NeoForge.EVENT_BUS.post(
              new GameplayEvent(
                  server.getServer(),
                  Stonedew.id("stage_up"),
                  null,
                  Map.of("stage", Integer.toString(next.stage()))));
        }
        if (next.stage() == 3 && !next.owner().isEmpty()) {
          var owner =
              server.getServer().getPlayerList().getPlayer(java.util.UUID.fromString(next.owner()));
          if (owner != null) PlayerProgress.mark(owner, PlayerProgress.RIPE);
        }
      }
    if (changed) setChanged();
    sync(env);
  }

  public boolean plant(Player player, int slot, Genome genome) {
    advance();
    if (plants[slot] != null) return false;
    plants[slot] =
        PlantState.seed(genome, now(), player.getUUID().toString(), level.random.nextLong());
    PlayerProgress.mark(player, PlayerProgress.PLANTED);
    NeoForge.EVENT_BUS.post(
        new GameplayEvent(
            ((ServerLevel) level).getServer(), Stonedew.id("planted"), player.getUUID(), Map.of()));
    changed();
    level.scheduleTick(worldPosition, getBlockState().getBlock(), profile().updateInterval());
    return true;
  }

  public boolean water(Player player, int slot) {
    advance();
    if (plants[slot] == null || plants[slot].water() >= 99) return false;
    plants[slot] = plants[slot].water(profile().waterPerPour());
    PlayerProgress.mark(player, PlayerProgress.WATERED);
    changed();
    ((ServerLevel) level)
        .sendParticles(
            ParticleTypes.SPLASH,
            worldPosition.getX() + 0.5,
            worldPosition.getY() + 0.65,
            worldPosition.getZ() + 0.5,
            12,
            0.25,
            0.1,
            0.25,
            0.06);
    level.playSound(null, worldPosition, SoundEvents.BUCKET_EMPTY, SoundSource.BLOCKS, 0.45F, 1.3F);
    return true;
  }

  public void inspect(Player player, int slot) {
    advance();
    var plant = plants[slot];
    if (plant == null)
      player.displayClientMessage(
          net.minecraft.network.chat.Component.translatable("hint.stonedew.empty_tray"), true);
    else
      player.displayClientMessage(
          net.minecraft.network.chat.Component.translatable(
              "hint.stonedew.plant",
              net.minecraft.network.chat.Component.translatable("stage.stonedew." + plant.stage()),
              Math.round(plant.water())),
          true);
  }

  public void setStage(int slot, int stage) {
    advance();
    if (plants[slot] != null) {
      plants[slot] = plants[slot].stage(stage);
      changed();
    }
  }

  public void setAppearance(int slot, long seed) {
    if (plants[slot] != null) {
      plants[slot] = plants[slot].withAppearanceSeed(seed);
      changed();
    }
  }

  public void setGenome(int slot, Genome genome) {
    if (plants[slot] != null) {
      plants[slot] = plants[slot].genome(genome);
      changed();
    }
  }

  public void grow(long ticks) {
    var env = environment();
    for (int i = 0; i < plants.length; i++)
      if (plants[i] != null) {
        var old = plants[i];
        long remaining = ticks;
        while (remaining > 0) {
          long step = Math.min(remaining, profile().catchupCap());
          var advanced =
              PlantSimulation.advance(
                  old,
                  old.lastSimTime() + step,
                  env,
                  profile(),
                  StonedewConfig.DIFFICULTY.get().name());
          old = advanced;
          remaining -= step;
        }
        plants[i] =
            new PlantState(
                old.genome(),
                old.stage(),
                old.progress(),
                old.water(),
                now(),
                old.careIntegral(),
                old.careTicks(),
                old.owner(),
                old.appearanceSeed());
      }
    changed();
  }

  public void dropSeeds() {
    for (var plant : plants)
      if (plant != null) {
        var seed = new ItemStack(ModContent.WILD_SEED.get());
        seed.set(ModContent.GENOME.get(), plant.genome());
        Block.popResource(level, worldPosition, seed);
      }
  }

  private void changed() {
    setChanged();
    sync(environment());
  }

  private void sync(PlantSimulation.Environment env) {
    var changes = new ListTag();
    boolean wet = false;
    for (int i = 0; i < plants.length; i++) {
      PlantState plant = plants[i];
      PlantView view =
          plant == null
              ? null
              : new PlantView(
                  plant.stage(),
                  (int) Math.round(plant.progress() * 100),
                  (int) Math.round(plant.water()),
                  (int)
                      Math.round(
                          PlantSimulation.vigor(plant.stage(), plant.water(), env, profile())
                              * 100),
                  (int) Math.round(env.light()),
                  (int) Math.round(env.humidity()),
                  plant.genome().leafColor(),
                  plant.genome().budColor(),
                  plant.genome().hairColor(),
                  plant.genome().pigment(),
                  plant.genome().habit(),
                  plant.appearance().shape(),
                  plant.appearance().budLoad(),
                  plant.appearance().height(),
                  plant.appearance().spread(),
                  plant.appearance().rotation());
      wet |= plant != null && plant.water() > 45;
      if (!java.util.Objects.equals(view, views[i])) {
        var tag = view == null ? new CompoundTag() : view.save();
        tag.putInt("slot", i);
        tag.putBoolean("empty", view == null);
        changes.add(tag);
        pending.put(i, tag);
        views[i] = view;
      }
    }
    if (getBlockState().getValue(GrowTrayBlock.WET) != wet)
      level.setBlock(
          worldPosition, getBlockState().setValue(GrowTrayBlock.WET, wet), Block.UPDATE_CLIENTS);
    if (!changes.isEmpty())
      level.sendBlockUpdated(worldPosition, getBlockState(), getBlockState(), Block.UPDATE_CLIENTS);
  }

  @Override
  public void onLoad() {
    super.onLoad();
    if (level instanceof ServerLevel) {
      advance();
      if (hasPlants())
        level.scheduleTick(worldPosition, getBlockState().getBlock(), profile().updateInterval());
    }
  }

  @Override
  protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
    super.saveAdditional(tag, registries);
    tag.putInt("dataVersion", 1);
    var slots = new ListTag();
    for (int i = 0; i < plants.length; i++)
      if (plants[i] != null) {
        var entry = new CompoundTag();
        entry.putInt("slot", i);
        entry.putString("plant", PlantSerialization.write(plants[i]));
        slots.add(entry);
      }
    tag.put("plants", slots);
  }

  @Override
  protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
    super.loadAdditional(tag, registries);
    if (tag.getInt("dataVersion") != 1)
      throw new IllegalArgumentException("Unsupported tray save version");
    Arrays.fill(plants, null);
    for (var entry : tag.getList("plants", Tag.TAG_COMPOUND)) {
      var slot = (CompoundTag) entry;
      int index = slot.getInt("slot");
      if (index < 0 || index >= plants.length)
        throw new IllegalArgumentException("Invalid tray slot");
      String saved = slot.getString("plant");
      plants[index] = PlantSerialization.read(saved);
      if (!com.google.gson.JsonParser.parseString(saved).getAsJsonObject().has("appearanceSeed")) {
        // Stable migration also differentiates older identical seed stacks in existing worlds.
        plants[index] =
            plants[index].withAppearanceSeed(
                plants[index].genome().lineageSeed()
                    ^ worldPosition.asLong()
                    ^ ((long) index * 0x9E3779B97F4A7C15L));
      }
    }
  }

  @Override
  public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
    var tag = new CompoundTag();
    var list = new ListTag();
    for (int i = 0; i < views.length; i++) {
      var entry = views[i] == null ? new CompoundTag() : views[i].save();
      entry.putInt("slot", i);
      entry.putBoolean("empty", views[i] == null);
      list.add(entry);
    }
    tag.put("views", list);
    return tag;
  }

  @Override
  public ClientboundBlockEntityDataPacket getUpdatePacket() {
    var tag = new CompoundTag();
    var entries = new ListTag();
    pending.values().forEach(value -> entries.add(value.copy()));
    pending.clear();
    tag.put("views", entries);
    return ClientboundBlockEntityDataPacket.create(this, (ignored, registries) -> tag);
  }

  @Override
  public void onDataPacket(
      net.minecraft.network.Connection connection,
      ClientboundBlockEntityDataPacket packet,
      HolderLookup.Provider registries) {
    handleUpdateTag(packet.getTag(), registries);
  }

  @Override
  public void handleUpdateTag(CompoundTag tag, HolderLookup.Provider registries) {
    for (var value : tag.getList("views", Tag.TAG_COMPOUND)) {
      var entry = (CompoundTag) value;
      int slot = entry.getInt("slot");
      if (slot >= 0 && slot < views.length)
        views[slot] = entry.getBoolean("empty") ? null : PlantView.load(entry);
    }
  }

  @Override
  public String getStatusReason() {
    if (!hasPlants()) return "status.stonedew.empty";
    for (var plant : plants)
      if (plant != null && plant.water() < 20) return "status.stonedew.thirsty";
    return "status.stonedew.growing";
  }
}
