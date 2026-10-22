package dev.stonedew.debug;

import dev.stonedew.Stonedew;
import dev.stonedew.core.StonedewConfig;
import dev.stonedew.data.DefinitionReloadListener;
import dev.stonedew.world.story.GameplayEvent;
import dev.stonedew.world.story.StorySavedData;
import java.util.Map;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.RegisterCommandsEvent;

public final class DebugCommands {
    public static void register(RegisterCommandsEvent event) {
        event.getDispatcher().register(Commands.literal(Stonedew.ID)
                .then(Commands.literal("debug").requires(source -> source.hasPermission(2))
                        .then(Commands.literal("status").executes(context -> {
                            context.getSource().sendSuccess(() -> Component.translatable("command.stonedew.status",
                                    DefinitionReloadListener.current().size(), StonedewConfig.DIFFICULTY.get().name(), StonedewConfig.DREAD.get().name()), false);
                            return 1;
                        }))
                        .then(Commands.literal("story").executes(context -> {
                            var snapshot = StorySavedData.get(context.getSource().getServer()).snapshot();
                            context.getSource().sendSuccess(() -> Component.translatable("command.stonedew.story", snapshot.keeperCount(),
                                    snapshot.standing(), snapshot.attention(), snapshot.eventCounts().getOrDefault("stonedew:debug_probe", 0L)), false);
                            return 1;
                        }))
                        .then(Commands.literal("probe").executes(context -> {
                            NeoForge.EVENT_BUS.post(new GameplayEvent(context.getSource().getServer(), Stonedew.id("debug_probe"),
                                    context.getSource().getPlayer() == null ? null : context.getSource().getPlayer().getUUID(), Map.of()));
                            context.getSource().sendSuccess(() -> Component.translatable("command.stonedew.probe"), false);
                            return 1;
                        }))));
    }
    private DebugCommands() {}
}
