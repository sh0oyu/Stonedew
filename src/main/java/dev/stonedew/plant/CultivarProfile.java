package dev.stonedew.plant;

import java.util.Objects;
import dev.stonedew.data.Identifiers;

public record CultivarProfile(String id, Type type, String geneSchema, String environmentProfile,
                              String processChain, String effectMap) implements Cultivar {
    public CultivarProfile {
        Objects.requireNonNull(type);
        Identifiers.require(id);
        Identifiers.require(geneSchema);
        Identifiers.require(environmentProfile);
        Identifiers.require(processChain);
        Identifiers.require(effectMap);
    }
}
