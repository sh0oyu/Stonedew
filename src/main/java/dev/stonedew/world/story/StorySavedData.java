package dev.stonedew.world.story;

import net.minecraft.core.HolderLookup;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.saveddata.SavedData;

public final class StorySavedData extends SavedData {
    private StorySnapshot snapshot;
    private StorySavedData(StorySnapshot snapshot) { this.snapshot = snapshot; }
    public static StorySavedData get(MinecraftServer server) {
        var failure = new java.util.concurrent.atomic.AtomicReference<RuntimeException>();
        return server.overworld().getDataStorage().computeIfAbsent(new Factory<>(() -> {
            // Vanilla catches read exceptions. Do not let its fallback overwrite an unreadable/future save.
            if (failure.get() != null) throw new IllegalStateException("Stonedew story save could not be loaded", failure.get());
            var created = new StorySavedData(StorySnapshot.initial());
            created.setDirty();
            return created;
        }, (tag, registries) -> {
            try { return load(tag, registries); }
            catch (RuntimeException exception) { failure.set(exception); throw exception; }
        }, null), "stonedew_story");
    }
    private static StorySavedData load(CompoundTag tag, HolderLookup.Provider registries) {
        int version = tag.getInt("dataVersion");
        if (version < 0 || version > StorySerialization.DATA_VERSION) throw new IllegalArgumentException("Unsupported story dataVersion " + version);
        return new StorySavedData(StorySerialization.read(tag.getString("story")));
    }
    @Override
    public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
        tag.putInt("dataVersion", StorySerialization.DATA_VERSION);
        tag.putString("story", StorySerialization.write(snapshot));
        return tag;
    }
    public StorySnapshot snapshot() { return snapshot; }
    public void record(String event) { snapshot = snapshot.record(event); setDirty(); }
}
