# Current painted sources — 0.2.9

Five new original paintings provide the complete fan, equipment palette, botanical surfaces, journal and Dewstone. See [source inventory](sources/README.md) and [recorded hashes](painted-sources.json). Runtime copies retain their original bytes. Four native atlas sources expose 22 named sprites at mip level 4; the journal is a direct UI texture. Python reads the source alpha to author geometry and does not edit paintings.

The notes below document historical source acquisition for rejected earlier versions.

---

# Painted sources

The current original paintings are `sources/materials-v6.png` and `sources/cannabis-leaflet-v8.png`. See [its provenance](sources/README.md) and [current bindings/rendering notes](ART_DIRECTION.md). It is packaged unchanged and exposed through native atlas UV windows; its dimensions/hash are in `authored-sources.json`.

The fan and material sheet used in 0.2.3 were rejected. They remain unchanged under `archive/0.2.3`; their original hashes, dimensions and creation method remain in `painted-sources.json`. They are not current art references or runtime assets.

Individual cannabis fingers use the unchanged new painting and read-only alpha measurements. The full-fan v7 painting was rejected and is preserved in documentation only. Distant foliage silhouettes, small sugar leaves/cotyledons, seed printing, material masks and local effects come from original authoring code. The owner's CODEX_REFERENCE_NEW uploads are unchanged visual targets, not textures extracted for the mod.
