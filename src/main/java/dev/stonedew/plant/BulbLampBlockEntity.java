package dev.stonedew.plant;

import dev.stonedew.core.ModContent;
import dev.stonedew.core.StatusSource;
import dev.stonedew.data.DefinitionReloadListener;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;

public final class BulbLampBlockEntity extends BlockEntity implements StatusSource {
  private long fuelTicks, lastTime;

  public BulbLampBlockEntity(BlockPos pos, BlockState state) {
    super(ModContent.LAMP_ENTITY.get(), pos, state);
  }

  public void fuel() {
    advance();
    fuelTicks = Math.min(fuelTicks + profileFuel(), profileFuel() * 8);
    lastTime = dev.stonedew.core.GrowthClock.now(level);
    update();
    level.playSound(
        null, worldPosition, SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.BLOCKS, 0.6F, 1.1F);
  }

  private long profileFuel() {
    return DefinitionReloadListener.current().growthProfile("stonedew:herb").lampFuel();
  }

  public void advance() {
    if (!(level instanceof ServerLevel)) return;
    long now = dev.stonedew.core.GrowthClock.now(level);
    fuelTicks = Math.max(0, fuelTicks - Math.max(0, now - lastTime));
    lastTime = now;
    update();
  }

  private void update() {
    boolean lit = fuelTicks > 0;
    if (getBlockState().getValue(BulbLampBlock.LIT) != lit)
      level.setBlock(
          worldPosition, getBlockState().setValue(BulbLampBlock.LIT, lit), Block.UPDATE_ALL);
    setChanged();
    if (lit)
      level.scheduleTick(
          worldPosition,
          getBlockState().getBlock(),
          DefinitionReloadListener.current().growthProfile("stonedew:herb").updateInterval());
  }

  @Override
  public void onLoad() {
    super.onLoad();
    if (level instanceof ServerLevel) advance();
  }

  @Override
  protected void saveAdditional(CompoundTag tag, HolderLookup.Provider provider) {
    super.saveAdditional(tag, provider);
    tag.putInt("dataVersion", 1);
    tag.putLong("fuel", fuelTicks);
    tag.putLong("lastTime", lastTime);
  }

  @Override
  public CompoundTag getUpdateTag(HolderLookup.Provider provider) {
    var tag = new CompoundTag();
    saveAdditional(tag, provider);
    return tag;
  }

  @Override
  protected void loadAdditional(CompoundTag tag, HolderLookup.Provider provider) {
    super.loadAdditional(tag, provider);
    if (tag.getInt("dataVersion") != 1)
      throw new IllegalArgumentException("Unsupported lamp version");
    fuelTicks = Math.max(0, tag.getLong("fuel"));
    lastTime = tag.getLong("lastTime");
  }

  @Override
  public String getStatusReason() {
    return fuelTicks > 0 ? "status.stonedew.lamp_running" : "status.stonedew.lamp_empty";
  }
}
