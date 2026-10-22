package dev.stonedew.genetics;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;

/** Serialization adapter kept separate so domain math tests need no game bootstrap. */
public final class GenomeCodecs {
  public static final Codec<Genome.Alleles> ALLELES =
      RecordCodecBuilder.create(
          instance ->
              instance
                  .group(
                      Codec.STRING.fieldOf("maternal").forGetter(Genome.Alleles::maternal),
                      Codec.STRING.fieldOf("paternal").forGetter(Genome.Alleles::paternal))
                  .apply(instance, Genome.Alleles::new));
  public static final Codec<Genome> CODEC =
      RecordCodecBuilder.create(
          instance ->
              instance
                  .group(
                      Codec.STRING.fieldOf("schema").forGetter(Genome::schema),
                      Codec.LONG.fieldOf("lineageSeed").forGetter(Genome::lineageSeed),
                      Codec.unboundedMap(Codec.STRING, ALLELES)
                          .fieldOf("genes")
                          .forGetter(Genome::genes))
                  .apply(instance, Genome::new));
  public static final StreamCodec<ByteBuf, Genome> STREAM_CODEC = ByteBufCodecs.fromCodec(CODEC);

  private GenomeCodecs() {}
}
