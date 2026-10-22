package dev.stonedew;

import com.mojang.logging.LogUtils;
import dev.stonedew.core.ModContent;
import dev.stonedew.core.StonedewConfig;
import dev.stonedew.data.DefinitionReloadListener;
import dev.stonedew.debug.DebugCommands;
import dev.stonedew.world.story.GameplayEvent;
import dev.stonedew.world.story.StorySavedData;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.AddReloadListenerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import org.slf4j.Logger;

@Mod(Stonedew.ID)
public final class Stonedew {
    public static final String ID = "stonedew";
    public static final Logger LOGGER = LogUtils.getLogger();

    public Stonedew(IEventBus modBus, ModContainer container) {
        ModContent.register(modBus);
        container.registerConfig(ModConfig.Type.SERVER, StonedewConfig.SERVER);
        container.registerConfig(ModConfig.Type.CLIENT, StonedewConfig.CLIENT);
        NeoForge.EVENT_BUS.addListener(DebugCommands::register);
        NeoForge.EVENT_BUS.addListener(this::reload);
        NeoForge.EVENT_BUS.addListener(this::started);
        NeoForge.EVENT_BUS.addListener(this::gameplay);
    }

    public static ResourceLocation id(String path) { return ResourceLocation.fromNamespaceAndPath(ID, path); }

    private void reload(AddReloadListenerEvent event) {
        event.addListener(new DefinitionReloadListener());
    }

    private void started(ServerStartedEvent event) {
        StorySavedData.get(event.getServer()).snapshot();
        LOGGER.info("Stonedew P0 ready: {} datapack definitions loaded", DefinitionReloadListener.current().size());
    }

    private void gameplay(GameplayEvent event) {
        // All producers must publish on the authoritative server thread.
        if (!event.server().isSameThread()) throw new IllegalStateException("Story events require the server thread");
        StorySavedData.get(event.server()).record(event.kind().toString());
    }
}
