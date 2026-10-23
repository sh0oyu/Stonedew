package dev.stonedew.client;

import dev.stonedew.Stonedew;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.gui.ConfigurationScreen;
import net.neoforged.neoforge.client.gui.IConfigScreenFactory;

@Mod(value = Stonedew.ID, dist = Dist.CLIENT)
public final class StonedewClient {
  public StonedewClient(ModContainer container, net.neoforged.bus.api.IEventBus bus) {
    bus.addListener(ClientRegistration::models);
    bus.addListener(ClientRegistration::renderTypes);
    bus.addListener(ClientRegistration::renderers);
    bus.addListener(ClientRegistration::screens);
    bus.addListener(ClientRegistration::colors);
    bus.addListener(ClientRegistration::extensions);
    net.neoforged.neoforge.common.NeoForge.EVENT_BUS.addListener(PlantHud::render);
    container.registerExtensionPoint(IConfigScreenFactory.class, ConfigurationScreen::new);
  }
}
