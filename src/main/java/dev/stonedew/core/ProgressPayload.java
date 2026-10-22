package dev.stonedew.core;

import dev.stonedew.Stonedew;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;

public record ProgressPayload(int flags, String directive) implements CustomPacketPayload {
  public static final Type<ProgressPayload> TYPE = new Type<>(Stonedew.id("progress"));
  public static final StreamCodec<FriendlyByteBuf, ProgressPayload> CODEC =
      StreamCodec.of(
          (buffer, value) -> {
            buffer.writeVarInt(value.flags);
            buffer.writeUtf(value.directive, 256);
          },
          buffer -> new ProgressPayload(buffer.readVarInt(), buffer.readUtf(256)));

  @Override
  public Type<? extends CustomPacketPayload> type() {
    return TYPE;
  }

  public static void register(RegisterPayloadHandlersEvent event) {
    event
        .registrar("1")
        .playToClient(
            TYPE,
            CODEC,
            (payload, context) ->
                context.enqueueWork(
                    () ->
                        PlayerProgress.accept(
                            context.player(), payload.flags(), payload.directive())));
  }
}
