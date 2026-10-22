package dev.stonedew.world.story;

import static org.junit.jupiter.api.Assertions.*;
import com.google.gson.JsonParser;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.Test;

class StorySerializationTest {
    @Test void initialStateRoundTrips() {
        assertEquals(StorySnapshot.initial(), StorySerialization.read(StorySerialization.write(StorySnapshot.initial())));
    }
    @Test void populatedProgressSurvivesSave() {
        var state = new StorySnapshot(Set.of("hatch_warm"), Set.of("stonedew:hatch"), Map.of("stonedew:hatch", 3),
                Set.of("stonedew:count"), 42, 65, 8, Map.of("stonedew:harvest", 15L));
        assertEquals(state, StorySerialization.read(StorySerialization.write(state)));
    }
    @Test void prototypeMigrationRenamesCluesAndSuppliesNewFields() {
        var state = StorySerialization.read("{\"dataVersion\":0,\"knownClues\":[\"stonedew:hatch\"],\"standing\":12}");
        assertEquals(Set.of("stonedew:hatch"), state.discoveredClues());
        assertEquals(12, state.standing());
        assertEquals(7, state.keeperCount());
        assertTrue(state.eventCounts().isEmpty());
        assertEquals(StorySerialization.DATA_VERSION, JsonParser.parseString(StorySerialization.write(state)).getAsJsonObject().get("dataVersion").getAsInt());
    }
    @Test void unversionedPrototypeMigrates() { assertEquals(StorySnapshot.initial(), StorySerialization.read("{}")); }
    @Test void futureAndNegativeVersionsAreRejected() {
        assertThrows(IllegalArgumentException.class, () -> StorySerialization.read("{\"dataVersion\":99}"));
        assertThrows(IllegalArgumentException.class, () -> StorySerialization.read("{\"dataVersion\":-1}"));
    }
    @Test void fractionalVersionIsRejected() {
        assertThrows(ArithmeticException.class, () -> StorySerialization.read("{\"dataVersion\":1.5}"));
    }
    @Test void stringVersionAndTruncatedMetersAreRejected() {
        assertThrows(IllegalArgumentException.class, () -> StorySerialization.read("{\"dataVersion\":\"1\"}"));
        var object = JsonParser.parseString(StorySerialization.write(StorySnapshot.initial())).getAsJsonObject();
        object.remove("standing");
        assertThrows(IllegalArgumentException.class, () -> StorySerialization.read(object.toString()));
    }
    @Test void fractionalProgressIsNotSilentlyRounded() {
        var object = JsonParser.parseString(StorySerialization.write(StorySnapshot.initial())).getAsJsonObject();
        object.addProperty("standing", 1.5);
        assertThrows(ArithmeticException.class, () -> StorySerialization.read(object.toString()));
    }
    @Test void malformedCurrentSaveDoesNotBecomeEmptyProgress() {
        assertThrows(RuntimeException.class, () -> StorySerialization.read("{\"dataVersion\":1}"));
        assertThrows(RuntimeException.class, () -> StorySerialization.read("not json"));
    }
    @Test void invalidProgressIsRejected() {
        assertThrows(IllegalArgumentException.class, () -> new StorySnapshot(Set.of(), Set.of(), Map.of(), Set.of(), 101, 0, 7, Map.of()));
        assertThrows(IllegalArgumentException.class, () -> new StorySnapshot(Set.of(), Set.of(), Map.of("x", -1), Set.of(), 0, 0, 7, Map.of()));
        assertThrows(IllegalArgumentException.class, () -> new StorySnapshot(Set.of(), Set.of(), Map.of(), Set.of(), 0, 0, 0, Map.of()));
    }
    @Test void snapshotsDoNotAliasMutableCollections() {
        var flags = new HashSet<>(Set.of("first"));
        var state = new StorySnapshot(flags, Set.of(), Map.of(), Set.of(), 0, 0, 7, Map.of());
        flags.add("later");
        assertEquals(Set.of("first"), state.flags());
        assertThrows(UnsupportedOperationException.class, () -> state.flags().add("third"));
    }
    @Test void eventCountsPersistWithoutMutatingPriorSnapshot() {
        var initial = StorySnapshot.initial();
        var recorded = initial.record("stonedew:harvest").record("stonedew:harvest").record("stonedew:delivery");
        assertTrue(initial.eventCounts().isEmpty());
        assertEquals(Map.of("stonedew:harvest", 2L, "stonedew:delivery", 1L), StorySerialization.read(StorySerialization.write(recorded)).eventCounts());
    }
    @Test void overflowDoesNotWrapIntoNegativeCounts() {
        var state = new StorySnapshot(Set.of(), Set.of(), Map.of(), Set.of(), 0, 0, 7, Map.of("x", Long.MAX_VALUE));
        assertThrows(ArithmeticException.class, () -> state.record("x"));
    }
}
