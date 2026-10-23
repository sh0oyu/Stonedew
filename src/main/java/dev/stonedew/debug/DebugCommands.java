package dev.stonedew.debug;

import com.mojang.brigadier.arguments.IntegerArgumentType;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import dev.stonedew.Stonedew;
import dev.stonedew.core.*;
import dev.stonedew.data.DefinitionReloadListener;
import dev.stonedew.genetics.Genome;
import dev.stonedew.plant.GrowTrayBlockEntity;
import dev.stonedew.world.story.GameplayEvent;
import dev.stonedew.world.story.StorySavedData;
import java.util.Map;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.BlockHitResult;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.RegisterCommandsEvent;

public final class DebugCommands {
  private record Target(GrowTrayBlockEntity tray, int slot) {}

  private static Target target(CommandSourceStack source) throws CommandSyntaxException {
    var player = source.getPlayerOrException();
    var foliage = dev.stonedew.plant.TrayTargeting.find(source.getLevel(), player, 8);
    if (foliage != null) return new Target(foliage.tray(), foliage.slot());
    if (player.pick(8, 0, false) instanceof BlockHitResult hit
        && source.getLevel().getBlockEntity(hit.getBlockPos()) instanceof GrowTrayBlockEntity tray)
      return new Target(tray, tray.slot(hit.getLocation()));
    throw new com.mojang.brigadier.exceptions.SimpleCommandExceptionType(
            Component.translatable("command.stonedew.target"))
        .create();
  }

  private static int deferred(CommandContext<CommandSourceStack> context) {
    context.getSource().sendFailure(Component.translatable("command.stonedew.deferred"));
    return 0;
  }

  private static int changed(CommandSourceStack source) {
    source.sendSuccess(() -> Component.translatable("command.stonedew.changed"), false);
    return 1;
  }

  public static void kit(net.minecraft.server.level.ServerPlayer player) {
    for (var block :
        java.util.List.of(
            ModContent.CLAY_POT_ITEM,
            ModContent.PLANTER_BED_ITEM,
            ModContent.BULB_LAMP_ITEM,
            ModContent.LEDGER_ITEM))
      player
          .getInventory()
          .placeItemBackInInventory(
              new ItemStack(block.get(), block == ModContent.CLAY_POT_ITEM ? 4 : 2));
    for (String color : java.util.List.of("violet", "teal", "amber", "green")) {
      var seed = new ItemStack(ModContent.WILD_SEED.get(), 4);
      seed.set(ModContent.GENOME.get(), Genome.wild(color, player.getRandom().nextLong()));
      player.getInventory().placeItemBackInInventory(seed);
    }
    var can = ModContent.WATERING_CAN.toStack();
    can.set(
        ModContent.WATER.get(),
        DefinitionReloadListener.current().growthProfile("stonedew:herb").canPours());
    can.set(
        ModContent.WATER_CAPACITY.get(),
        DefinitionReloadListener.current().growthProfile("stonedew:herb").canPours());
    player.getInventory().placeItemBackInInventory(can);
    player.getInventory().placeItemBackInInventory(new ItemStack(ModContent.GLOW_CELL.get(), 16));
  }

  public static void register(RegisterCommandsEvent event) {
    var debug =
        Commands.literal("debug")
            .requires(source -> source.hasPermission(2))
            .then(
                Commands.literal("status")
                    .executes(
                        context -> {
                          context
                              .getSource()
                              .sendSuccess(
                                  () ->
                                      Component.translatable(
                                          "command.stonedew.status",
                                          DefinitionReloadListener.current().size(),
                                          StonedewConfig.DIFFICULTY.get().name(),
                                          StonedewConfig.DREAD.get().name()),
                                  false);
                          return 1;
                        }))
            .then(
                Commands.literal("story")
                    .executes(
                        context -> {
                          var state =
                              StorySavedData.get(context.getSource().getServer()).snapshot();
                          context
                              .getSource()
                              .sendSuccess(
                                  () ->
                                      Component.translatable(
                                          "command.stonedew.story",
                                          state.keeperCount(),
                                          state.standing(),
                                          state.attention(),
                                          state
                                              .eventCounts()
                                              .getOrDefault("stonedew:debug_probe", 0L)),
                                  false);
                          return 1;
                        }))
            .then(
                Commands.literal("probe")
                    .executes(
                        context -> {
                          NeoForge.EVENT_BUS.post(
                              new GameplayEvent(
                                  context.getSource().getServer(),
                                  Stonedew.id("debug_probe"),
                                  null,
                                  Map.of()));
                          context
                              .getSource()
                              .sendSuccess(
                                  () -> Component.translatable("command.stonedew.probe"), false);
                          return 1;
                        }))
            .then(
                Commands.literal("givekit")
                    .executes(
                        context -> {
                          kit(context.getSource().getPlayerOrException());
                          context
                              .getSource()
                              .sendSuccess(
                                  () -> Component.translatable("command.stonedew.kit"), false);
                          return 1;
                        })
                    .then(
                        Commands.argument("tier", IntegerArgumentType.integer(0, 7))
                            .executes(
                                context -> {
                                  if (IntegerArgumentType.getInteger(context, "tier") != 0)
                                    return deferred(context);
                                  kit(context.getSource().getPlayerOrException());
                                  return changed(context.getSource());
                                })))
            .then(
                Commands.literal("grow")
                    .then(
                        Commands.argument("ticks", IntegerArgumentType.integer(0, 240000))
                            .executes(
                                context -> {
                                  var target = target(context.getSource());
                                  target
                                      .tray()
                                      .grow(IntegerArgumentType.getInteger(context, "ticks"));
                                  return changed(context.getSource());
                                })))
            .then(
                Commands.literal("setstage")
                    .then(
                        Commands.argument("stage", IntegerArgumentType.integer(0, 3))
                            .executes(
                                context -> {
                                  var target = target(context.getSource());
                                  target
                                      .tray()
                                      .setStage(
                                          target.slot(),
                                          IntegerArgumentType.getInteger(context, "stage"));
                                  return changed(context.getSource());
                                })))
            .then(
                Commands.literal("appearance")
                    .then(
                        Commands.argument(
                                "seed", com.mojang.brigadier.arguments.LongArgumentType.longArg())
                            .executes(
                                context -> {
                                  var target = target(context.getSource());
                                  target
                                      .tray()
                                      .setAppearance(
                                          target.slot(),
                                          com.mojang.brigadier.arguments.LongArgumentType.getLong(
                                              context, "seed"));
                                  var plant = target.tray().plant(target.slot());
                                  if (plant == null) return 0;
                                  context
                                      .getSource()
                                      .sendSuccess(
                                          () ->
                                              Component.literal(
                                                  "Appearance "
                                                      + plant.appearance()
                                                      + "; mature flower sites="
                                                      + plant.appearance().matureBudCount()),
                                          false);
                                  return 1;
                                })))
            .then(
                Commands.literal("genome")
                    .then(
                        Commands.literal("show")
                            .executes(
                                context -> {
                                  var target = target(context.getSource());
                                  var plant = target.tray().plant(target.slot());
                                  if (plant == null) return 0;
                                  context
                                      .getSource()
                                      .sendSuccess(
                                          () ->
                                              Component.literal(
                                                  new com.google.gson.Gson()
                                                      .toJson(plant.genome())),
                                          false);
                                  return 1;
                                }))
                    .then(
                        Commands.literal("random")
                            .executes(
                                context -> {
                                  var target = target(context.getSource());
                                  String[] colors = {"violet", "teal", "amber", "green"};
                                  target
                                      .tray()
                                      .setGenome(
                                          target.slot(),
                                          Genome.wild(
                                              colors[
                                                  context
                                                      .getSource()
                                                      .getLevel()
                                                      .random
                                                      .nextInt(colors.length)],
                                              context.getSource().getLevel().random.nextLong()));
                                  return changed(context.getSource());
                                }))
                    .then(
                        Commands.literal("set")
                            .then(
                                Commands.argument("gene", StringArgumentType.word())
                                    .then(
                                        Commands.argument("maternal", StringArgumentType.word())
                                            .then(
                                                Commands.argument(
                                                        "paternal", StringArgumentType.word())
                                                    .executes(
                                                        context -> {
                                                          var target = target(context.getSource());
                                                          var plant =
                                                              target.tray().plant(target.slot());
                                                          if (plant == null) return 0;
                                                          String
                                                              gene =
                                                                  StringArgumentType.getString(
                                                                      context, "gene"),
                                                              a =
                                                                  StringArgumentType.getString(
                                                                      context, "maternal"),
                                                              b =
                                                                  StringArgumentType.getString(
                                                                      context, "paternal");
                                                          if (!valid(gene, a) || !valid(gene, b)) {
                                                            context
                                                                .getSource()
                                                                .sendFailure(
                                                                    Component.translatable(
                                                                        "command.stonedew.invalid"));
                                                            return 0;
                                                          }
                                                          var genes =
                                                              new java.util.HashMap<>(
                                                                  plant.genome().genes());
                                                          genes.put(gene, new Genome.Alleles(a, b));
                                                          target
                                                              .tray()
                                                              .setGenome(
                                                                  target.slot(),
                                                                  new Genome(
                                                                      plant.genome().schema(),
                                                                      plant.genome().lineageSeed(),
                                                                      genes));
                                                          return changed(context.getSource());
                                                        }))))))
            .then(
                Commands.literal("timewarp")
                    .then(
                        Commands.argument("days", IntegerArgumentType.integer(1, 30))
                            .executes(
                                context -> {
                                  int days = IntegerArgumentType.getInteger(context, "days");
                                  GrowthClock.advance(
                                      context.getSource().getServer(), days * 24000L);
                                  context
                                      .getSource()
                                      .getLevel()
                                      .setDayTime(
                                          context.getSource().getLevel().getDayTime()
                                              + days * 24000L);
                                  context
                                      .getSource()
                                      .sendSuccess(
                                          () ->
                                              Component.translatable(
                                                  "command.stonedew.timewarp", days),
                                          false);
                                  return 1;
                                })))
            .then(Commands.literal("demo").executes(DebugShowcase::create))
            .then(Commands.literal("art").executes(ArtGallery::create));
    debug.then(
        Commands.literal("room").then(Commands.literal("info").executes(DebugCommands::deferred)));
    debug.then(
        Commands.literal("env")
            .then(
                Commands.literal("set")
                    .then(
                        Commands.argument("values", StringArgumentType.greedyString())
                            .executes(DebugCommands::deferred))));
    debug.then(
        Commands.literal("event")
            .then(
                Commands.literal("trigger")
                    .then(
                        Commands.argument("id", StringArgumentType.word())
                            .executes(DebugCommands::deferred))));
    for (String label : java.util.List.of("knowhow", "rank"))
      debug.then(
          Commands.literal(label)
              .then(
                  Commands.literal("set")
                      .then(
                          Commands.argument("value", StringArgumentType.greedyString())
                              .executes(DebugCommands::deferred))));
    debug.then(
        Commands.literal("contract")
            .then(Commands.literal("spawn").executes(DebugCommands::deferred)));
    debug.then(Commands.literal("unlockall").executes(DebugCommands::deferred));
    event.getDispatcher().register(Commands.literal(Stonedew.ID).then(debug));
  }

  private static boolean valid(String gene, String allele) {
    return switch (gene) {
      case "potency", "yield", "speed", "resilience" -> {
        try {
          int n = Integer.parseInt(allele);
          yield n >= 1 && n <= 10;
        } catch (NumberFormatException e) {
          yield false;
        }
      }
      case "pigment" -> java.util.Set.of("violet", "teal", "amber", "green").contains(allele);
      case "habit" -> java.util.Set.of("tall", "hybrid", "bushy").contains(allele);
      case "terpene" ->
          java.util.Set.of(
                  "myrcene",
                  "limonene",
                  "pinene",
                  "linalool",
                  "caryophyllene",
                  "humulene",
                  "terpinolene",
                  "ocimene")
              .contains(allele);
      case "luminescence" -> java.util.Set.of("dormant", "luminous").contains(allele);
      default -> false;
    };
  }

  private DebugCommands() {}
}
