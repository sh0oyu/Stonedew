# Current painted material source

`materials-v6.png` is a new original imagegen painting, created on 2026-10-23 with the owner's unchanged pot/tent and UV sheets as visual guidance. The request was a flat 4×4 atlas of stylized pixel materials: terracotta/rim, wood/end grain, dark/light steel, cloth/lining, blue-gray enamel, hardware, dry/wet soil, parchment, violet/cyan glass and dark recesses. It contains no copied reference scenes or other game's artwork.

The returned image is 1254×1254. Keep it unchanged. Native Minecraft atlas windows select inset 256px material swatches; the whole original is also packaged unchanged. Source hashes/dimensions are recorded in ../authored-sources.json. This fixed painting is copied during deterministic resource generation; running Python does not reproduce image generation.

Original execution output: `/workspace/generated_images/exec-0ab95d92-3ab3-4df4-a5f6-687ffcc3f73a.png`. Rejected 0.2.3 originals remain separately archived and are not used.

## Cannabis fan source — 0.2.7

`cannabis-fan-v7.png` is a new original imagegen painting made with the owner's unchanged banner and kush sheet as visual guidance. It depicts one seven-finger cannabis leaf: separate narrow serrated leaflets, green veins, short petiole, transparent background and painted light/dark green facets. The original 1254×1254 RGBA output is preserved unchanged here and in the packaged resources. Original execution output: `/workspace/generated_images/exec-d296fe8a-e5bf-4528-94d3-a49d0a8aa307.png`.

`tools/botanical_leaf.py` uses Pillow and NumPy only to **read** alpha coverage and author a conservative, compact leaf mesh. It never edits, crops, resizes or saves the image. Twenty-five native 256px Minecraft atlas windows cover the complete original painting, including the outer finger tips and petiole; partial final cells use overlapping source windows with adjusted mesh UVs. The native atlas retains global mip level 4. The painting is fixed input to reproducible asset generation, not recreated by Python.
