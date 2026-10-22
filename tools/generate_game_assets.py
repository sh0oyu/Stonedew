#!/usr/bin/env python3
"""Stonedew equipment and hybrid plants: deterministic geometry and fallback materials.

Geometry is authored here and in plant_art.py. Painted source PNGs in textures/art are retained.
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


def generate():
    textures()
    from equipment_art import generate as generate_equipment
    equipment_stats = generate_equipment(ROOT)
    from plant_art import generate as generate_plants
    stats = generate_plants(ROOT)
    report=Path(__file__).resolve().parents[1]/"docs/art/mesh-budget.json"
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(stats,indent=2)+"\n")
    (report.parent / "equipment-budget.json").write_text(json.dumps(equipment_stats, indent=2)+"\n")
    print("Generated rebuilt equipment, fallback materials and 64 varied plant meshes; painted source PNGs retained.")
    print("Maximum plant faces (near / distant):", max(row["faces"] for row in stats if not row["lod"]), "/", max(row["faces"] for row in stats if row["lod"]))


if __name__=="__main__":generate()
