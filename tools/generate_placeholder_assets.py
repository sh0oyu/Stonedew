#!/usr/bin/env python3
"""Deterministic 16x16 P0 textures. Standard library only; no reference image edits."""
from pathlib import Path
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1] / "src/main/resources/assets/stonedew/textures"
STONE = ("1B1226", "2C2038", "3E3050")
VIOLET = ("7A2BD6", "B04CFF", "D78BFF")
COPPER = ("4A2E24", "6B4332", "B8693A")


def rgba(hex_color):
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


def png(path, pixels):
    def chunk(kind, payload):
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload))
    raw = b"".join(b"\0" + bytes(channel for color in row for channel in color) for row in pixels)
    image = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 6, 0, 0, 0))
    image += chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(image)


def generate():
    stone = [[rgba(STONE[(x * 7 + y * 11 + x * y) % 3]) for x in range(16)] for y in range(16)]
    for x, y in ((3, 3), (10, 2), (6, 8), (12, 11), (2, 13)):
        stone[y][x] = rgba(VIOLET[2])
        stone[y + 1][x] = rgba(VIOLET[0])
        stone[y][x + 1] = rgba(VIOLET[1])
    png(ROOT / "block/dewstone.png", stone)
    cell = [[(0, 0, 0, 0) for _ in range(16)] for _ in range(16)]
    for y in range(2, 14):
        for x in range(4, 12):
            edge = x in (4, 11) or y in (2, 3, 12, 13)
            cell[y][x] = rgba(COPPER[(x + y) % 3] if edge else VIOLET[(x + y // 3) % 3])
    for y in range(5, 11):
        cell[y][6] = rgba("F2E8FF")
    png(ROOT / "item/glow_cell.png", cell)
    print("Generated 2 placeholder textures (16x16 RGBA).")


if __name__ == "__main__":
    generate()
