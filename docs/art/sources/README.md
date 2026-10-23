# Current painted material source

`materials-v6.png` is a new original imagegen painting, created on 2026-10-23 with the owner's unchanged pot/tent and UV sheets as visual guidance. The request was a flat 4×4 atlas of stylized pixel materials: terracotta/rim, wood/end grain, dark/light steel, cloth/lining, blue-gray enamel, hardware, dry/wet soil, parchment, violet/cyan glass and dark recesses. It contains no copied reference scenes or other game's artwork.

The returned image is 1254×1254. Keep it unchanged. Native Minecraft atlas windows select inset 256px material swatches; the whole original is also packaged unchanged. Source hashes/dimensions are recorded in ../authored-sources.json. This fixed painting is copied during deterministic resource generation; running Python does not reproduce image generation.

Original execution output: `/workspace/generated_images/exec-0ab95d92-3ab3-4df4-a5f6-687ffcc3f73a.png`. Rejected 0.2.3 originals remain separately archived and are not used.

## Rejected full-fan source — 0.2.7

`cannabis-fan-v7.png` is a new original imagegen painting made with the owner's unchanged banner and kush sheet as visual guidance. It depicts one seven-finger cannabis leaf: separate narrow serrated leaflets, green veins, short petiole, transparent background and painted light/dark green facets. The original 1254×1254 RGBA output is preserved unchanged here and in the packaged resources. Original execution output: `/workspace/generated_images/exec-d296fe8a-e5bf-4528-94d3-a49d0a8aa307.png`.

`tools/botanical_leaf.py` uses Pillow and NumPy only to **read** alpha coverage and author a conservative, compact leaf mesh. It never edits, crops, resizes or saves the image. Twenty-five native 256px Minecraft atlas windows cover the complete original painting, including the outer finger tips and petiole; partial final cells use overlapping source windows with adjusted mesh UVs. The native atlas retains global mip level 4. The painting is fixed input to reproducible asset generation, not recreated by Python.

## Current individual leaflet — 0.2.8

`cannabis-leaflet-v8.png` is a new original single-finger painting created with the user's warm Stonedew banner as art-direction guidance. An initial imagegen draft (`/workspace/generated_images/exec-cd73d0a0-8144-4797-9728-eb9cb1c61550.png`) was too noisy/yellow in-game. Imagegen then simplified it to quiet green facets, restrained veins and broad serrations. The final original output is `/workspace/generated_images/exec-ef782906-6335-4a89-b814-b6a3f0189a4e.png`; its bytes are copied unchanged here and into runtime resources. Both execution outputs remain intact.

`tools/botanical_leaf.py` only reads alpha measurements with Pillow/NumPy. It selects one native power-of-two UV window and six conservative longitudinal bands; seven separately bent/folded copies form a fan. The complete painted finger and stalk fit the native window. No Python image editing, resampling or texture export occurs. Native mip level 4 remains. The rejected v7 full-fan painting stays unchanged in this documentation, outside the runtime package.
