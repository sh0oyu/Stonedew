#!/usr/bin/env python3
"""Original Stonedew equipment and organic plant art. Reproducible geometry and materials.

Model sources are these authored shape recipes; no third-party art is bundled.
The reference images guide silhouette, material hierarchy and color.
"""
from pathlib import Path
import json
import math
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/assets/stonedew"
FACES = ("down", "up", "north", "south", "west", "east")
PALETTES = {
    "ceramic": ("693E33", "975944", "BC7859"),
    "wood": ("38251F", "4A2E24", "6B4332"),
    "wood_edge": ("291F1D", "3F2A23", "80533B"),
    "copper": ("72442D", "B8693A", "DEA568"),
    "iron": ("232634", "3C4050", "686579"),
    "soil": ("241B24", "33242A", "4A3231"),
    "soil_wet": ("181520", "251B26", "352634"),
    "leaf": ("80977B", "C1D1B8", "E3F2D6"),
    "bud": ("8B8A9C", "C9BFDD", "F0E2FA"),
    "hair": ("B3A299", "EADCD2", "FFF2E2"),
    "stem": ("3A5F31", "557F3D", "8BA45B"),
    "glow": ("7A2BD6", "B04CFF", "D78BFF"),
    "glass": ("264359", "47758A", "A8DAE2"),
    "paper": ("907459", "C7AA80", "E6CFAB"),
    "teal": ("153E3D", "235C56", "43897A"),
    "dewstone": ("211B2C", "30263B", "493852"),
}


def write_json(relative, content):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, indent=2) + "\n")


def png(name, pixels):
    def chunk(kind, payload):
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload))
    raw = b"".join(b"\0" + bytes(c for pixel in row for c in pixel) for row in pixels)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 6, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    path = ROOT / "textures" / (name + ".png")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def textures():
    for name, palette in PALETTES.items():
        pixels = []
        for y in range(16):
            row = []
            for x in range(16):
                # Restrained material marks; low-frequency grain rather than checkerboard noise.
                value = 1
                if name.startswith("wood"):
                    value = 0 if x in (0, 8, 15) else 2 if x in (2, 10) and y % 7 < 4 else 1
                elif name in ("soil", "soil_wet", "dewstone"):
                    value = 0 if (x + y // 4) % 9 == 0 else 2 if (x * 3 + y * 5) % 31 == 0 else 1
                elif name in ("leaf", "bud"):
                    value = 2 if x == y or x == 8 else 0 if (x + 2 * y) % 11 == 0 else 1
                else:
                    value = 2 if x in (1, 2) or y == 1 else 0 if x == 15 or y == 15 else 1
                color = palette[value]
                row.append(tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) + (255,))
            pixels.append(row)
        if name == "dewstone":
            for x, y in ((3, 5), (4, 5), (5, 6), (11, 12), (12, 12)):
                pixels[y][x] = (155, 89, 193, 255)
        png("block/" + name, pixels)
    halo=[]
    for y in range(16):
        row=[]
        for x in range(16):
            radius=math.sqrt(((x-7.5)/7.5)**2+((y-7.5)/7.5)**2)
            alpha=round(max(0,1-radius)**2*150)
            row.append((176,76,255,alpha))
        halo.append(row)
    png("effect/lamp_halo",halo)
    # Organic foliage materials. The leaf's central vein follows the modeled ridge;
    # the bud uses soft grouped bracts and small resin glints, not voxel stripes.
    for material in ("plant_leaf", "plant_bud", "plant_stem", "plant_pistil"):
        pixels = []
        for y in range(16):
            row = []
            for x in range(16):
                if material == "plant_leaf":
                    ridge = max(0, 1-abs(x-7.5)/7.5)
                    vein = x in (7, 8) or (y+int(abs(x-7.5)*.6)) % 5 == 0
                    value = int(161 + ridge*55 + (14 if vein else 0))
                    color = (min(255,value), min(255,value+13), max(0,value-10))
                elif material == "plant_bud":
                    puff = (math.sin(x*1.4+y*.6)+math.cos(y*1.7-x*.4))*.5
                    value = int(207 + puff*19)
                    if (x*7+y*11) % 43 == 0: value = 251
                    color = (value, min(255,value+6), max(0,value-7))
                elif material == "plant_stem":
                    color = (91+x%3*8, 126+x%3*8, 52+x%3*5)
                else:
                    color = (255, 234, 199)
                row.append(tuple(color)+(255,))
            pixels.append(row)
        png("block/"+material, pixels)
    # Legacy item texture remains a particle fallback, while the item itself is volumetric.
    png("item/glow_cell", [[(176, 76, 255, 255) for _ in range(16)] for _ in range(16)])


def box(lo, hi, material, tint=None, faces=FACES, emissive=False):
    face = {"texture": "#" + material, "uv": [0, 0, 16, 16]}
    if tint is not None:
        face["tintindex"] = tint
    if emissive:
        face["neoforge_data"] = {"block_light": 15, "sky_light": 15}
    return {"from": list(lo), "to": list(hi), "faces": {side: dict(face) for side in faces}}


def model(name, elements, item=False, particle="wood", display=None):
    data = {"credit": "Original Stonedew voxel art; tools/generate_game_assets.py", "ambientocclusion": True,
            "textures": {key: "stonedew:block/" + key for key in PALETTES}, "elements": elements}
    data["textures"]["particle"] = "stonedew:block/" + particle
    if item:
        data["gui_light"] = "front"
    data["display"] = display or {
        "gui": {"rotation": [25, 225, 0], "translation": [0, 1, 0], "scale": [0.8, 0.8, 0.8]},
        "ground": {"translation": [0, 3, 0], "scale": [0.5, 0.5, 0.5]},
        "fixed": {"rotation": [0, 180, 0], "scale": [0.8, 0.8, 0.8]},
        "firstperson_righthand": {"rotation": [0, 45, 0], "translation": [0, 1.5, 0], "scale": [0.7, 0.7, 0.7]},
        "firstperson_lefthand": {"rotation": [0, -45, 0], "translation": [0, 1.5, 0], "scale": [0.7, 0.7, 0.7]},
        "thirdperson_righthand": {"rotation": [75, 45, 0], "translation": [0, 2.5, 0], "scale": [0.5, 0.5, 0.5]}}
    write_json("models/" + ("item/" if item else "block/") + name + ".json", data)


def containers():
    for wet in (False, True):
        soil = "soil_wet" if wet else "soil"
        pot = [box((4, 0, 4), (12, 1, 12), "ceramic"), box((4, 1, 4), (12, 2, 12), "ceramic")]
        for a, b in [((3.5, 2, 3.5), (5, 7, 12.5)), ((11, 2, 3.5), (12.5, 7, 12.5)),
                     ((5, 2, 3.5), (11, 7, 5)), ((5, 2, 11), (11, 7, 12.5)),
                     ((3, 7, 3), (5, 9, 13)), ((11, 7, 3), (13, 9, 13)),
                     ((5, 7, 3), (11, 9, 5)), ((5, 7, 11), (11, 9, 13))]:
            pot.append(box(a, b, "ceramic"))
        pot.append(box((5, 6.5, 5), (11, 7.5, 11), soil))
        pot.append(box((6, 3.5, 3.1), (10, 5, 3.5), "copper"))
        model("clay_pot" + ("_wet" if wet else ""), pot, particle="ceramic")
        bed = [box((1, 0.5, 1), (15, 1.5, 15), "wood"), box((1, 5.5, 1), (15, 6.25, 15), soil)]
        for lo, hi in [((0, 1, 0), (1.5, 7, 16)), ((14.5, 1, 0), (16, 7, 16)),
                       ((1.5, 1, 0), (14.5, 7, 1.5)), ((1.5, 1, 14.5), (14.5, 7, 16))]:
            bed.append(box(lo, hi, "wood"))
        for x in (0, 14.5):
            for z in (0, 14.5):
                bed.append(box((x, 0, z), (x + 1.5, 8, z + 1.5), "wood_edge"))
                for y in (2, 6):
                    bed.append(box((x - .1, y, z - .1), (x + 1.6, y + .6, z + 1.6), "copper"))
        model("planter_bed" + ("_wet" if wet else ""), bed)


def equipment():
    for lit in (False, True):
        lamp = [box((1, 5, 5), (15, 7, 11), "iron"), box((0.5, 3, 5.5), (3, 7.5, 10.5), "copper"),
                box((13, 3, 5.5), (15.5, 7.5, 10.5), "copper"),
                box((3, 3.5, 6), (13, 5, 10), "glow" if lit else "glass", emissive=lit)]
        for x in (3, 12):
            for y in (8, 11, 14):
                lamp += [box((x, y, 7.5), (x + 1, y + 2, 8.5), "iron"), box((x - .25, y, 7.25), (x + 1.25, y + .5, 8.75), "iron")]
        model("bulb_lamp" + ("_lit" if lit else ""), lamp, particle="iron")
    cell = [box((5, 2, 5), (11, 4, 11), "copper"), box((5, 12, 5), (11, 14, 11), "copper"),
            box((5.5, 4, 5.5), (10.5, 12, 10.5), "glow", emissive=True), box((6, 4, 5.1), (7, 12, 5.5), "glass")]
    for x in (5, 10):
        for z in (5, 10): cell.append(box((x, 4, z), (x+1, 12, z+1), "copper"))
    model("glow_cell", cell, item=True, particle="glow")
    can = [box((5, 2, 5), (11, 9, 12), "teal"), box((4.5, 1.5, 4.5), (11.5, 2.5, 12.5), "copper"),
           box((5, 9, 5), (11, 10, 12), "copper"), box((6, 10, 6), (10, 10.7, 11), "teal"),
           box((10.5, 5, 7), (12, 10.5, 9), "teal"), box((12, 10, 7), (14, 11.5, 9), "teal"),
           box((13, 4.5, 7), (14.5, 10, 9), "teal"), box((11, 4, 7), (14, 5.5, 9), "copper"),
           box((3, 4, 7), (5, 6, 10), "teal"), box((1.5, 5, 7), (3.5, 8, 10), "teal"),
           box((0, 7.5, 6), (2, 9, 11), "copper")]
    for z in (6.5, 8, 9.5):can.append(box((-.05, 7.8, z), (.15, 8.5, z+.5), "iron"))
    model("watering_can", can, item=True, particle="teal")
    can_path=ROOT / "models/item/watering_can.json"
    can_model=json.loads(can_path.read_text())
    for hand,angle in (("righthand",-45),("lefthand",45)):
        can_model["display"]["firstperson_"+hand]={"rotation":[0,angle,0],"translation":[-1,4,0],"scale":[.55,.55,.55]}
    can_path.write_text(json.dumps(can_model,indent=2)+"\n")
    packet = [box((4, 1, 7), (12, 13, 9), "paper"), box((3.8, 12, 6.8), (12.2, 14, 9.2), "copper"),
              box((5.5, 4, 6.7), (10.5, 9, 7), "bud", tint=0), box((7.5, 3, 6.5), (8.5, 10, 6.8), "stem")]
    model("wild_seed", packet, item=True, particle="paper")
    ledger = [box((1, 0, 2), (15, 2, 14), "wood_edge"), box((2, 2, 3), (14, 10, 13), "wood"),
              box((1.5, 9, 2.5), (14.5, 10.5, 13.5), "copper"), box((3, 10.5, 4), (13, 11, 12), "paper"),
              box((4, 11, 5), (12, 11.3, 6), "iron"), box((4, 11, 7), (11, 11.3, 7.5), "iron"),
              box((4, 11, 8.5), (9, 11.3, 9), "iron"), box((12.8, 4, 6), (14, 8, 10), "glow", emissive=True)]
    model("ledger", ledger)



def generate():
    textures();containers();equipment()
    from plant_art import generate as generate_plants
    stats = generate_plants(ROOT)
    report=Path(__file__).resolve().parents[1]/"docs/art/mesh-budget.json"
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(stats,indent=2)+"\n")
    print("Generated original equipment, 20 material textures and 24 organic plant meshes.")
    print("Maximum plant faces (near / distant):", max(row["faces"] for row in stats if not row["lod"]), "/", max(row["faces"] for row in stats if row["lod"]))


if __name__=="__main__":generate()
