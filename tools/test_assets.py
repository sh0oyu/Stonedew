"""Validate shipped geometry, materials and OBJ references before client loading."""
from pathlib import Path
import json
import math
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/assets/stonedew"


def read_obj(path):
    result = {"v": [], "vn": [], "vt": [], "f": [], "usemtl": [], "mtllib": []}
    for line in path.read_text().splitlines():
        parts = line.split()
        if not parts or parts[0].startswith("#"):
            continue
        kind = parts[0]
        if kind in ("v", "vn", "vt"):
            result[kind].append(tuple(map(float, parts[1:])))
        elif kind == "f":
            result[kind].append([tuple(map(int, ref.split("/"))) for ref in parts[1:]])
        elif kind in result:
            result[kind].append(parts[1])
    return result


class AssetTests(unittest.TestCase):
    def test_all_stages_and_habits_have_bounded_meshes(self):
        for habit in ("bushy", "hybrid", "tall"):
            for stage in range(4):
                for detail in ("", "_lod"):
                    path = ASSETS / "models/block/plants" / f"{habit}_{stage}{detail}.json"
                    with self.subTest(model=path.name):
                        model = json.loads(path.read_text())
                        self.assertEqual(model["loader"], "neoforge:obj")
                        mesh = read_obj(path.with_suffix(".obj"))
                        self.assertGreater(len(mesh["f"]), 0)
                        self.assertLessEqual(len(mesh["f"]), 100 if detail else 3000)
                        for vertex in mesh["v"]:
                            self.assertTrue(all(math.isfinite(value) and -1 <= value <= 2 for value in vertex))

    def test_obj_indices_normals_and_materials_are_valid(self):
        for path in (ASSETS / "models/block/plants").glob("*.obj"):
            mesh = read_obj(path)
            with self.subTest(model=path.name):
                material_file = path.parent / mesh["mtllib"][0]
                materials = {line.split()[1] for line in material_file.read_text().splitlines()
                             if line.startswith("newmtl ")}
                self.assertTrue(set(mesh["usemtl"]).issubset(materials))
                for normal in mesh["vn"]:
                    self.assertAlmostEqual(sum(v*v for v in normal), 1, places=4)
                for face in mesh["f"]:
                    self.assertIn(len(face), (3, 4))
                    for indices in face:
                        for index, kind in zip(indices, ("v", "vt", "vn")):
                            self.assertGreater(index, 0)
                            self.assertLessEqual(index, len(mesh[kind]))
                    self.assertGreaterEqual(len({mesh["v"][v[0]-1] for v in face}), 3)

    def test_models_and_materials_reference_present_textures(self):
        for path in (ASSETS / "models").rglob("*.json"):
            model = json.loads(path.read_text())
            for texture in model.get("textures", {}).values():
                if texture.startswith("stonedew:"):
                    self.assertTrue((ASSETS / "textures" / (texture.split(":", 1)[1]+".png")).is_file())
            for element in model.get("elements", []):
                for face in element["faces"].values():
                    self.assertIn(face["texture"][1:], model["textures"])
                    self.assertTrue(all(0 <= value <= 16 for value in face["uv"]))
        for path in (ASSETS / "models").rglob("*.mtl"):
            for line in path.read_text().splitlines():
                if line.startswith("map_Kd "):
                    texture = line.split()[1].split(":", 1)[1]
                    self.assertTrue((ASSETS / "textures" / (texture+".png")).is_file())

    def test_material_textures_keep_vanilla_pixel_density(self):
        for path in (ASSETS / "textures").rglob("*.png"):
            data = path.read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", data[16:24]), (16, 16), path)

    def test_source_attribution_is_present(self):
        for path in (ASSETS / "models").rglob("*.json"):
            self.assertIn("Original Stonedew", json.loads(path.read_text())["credit"])
        for path in (ASSETS / "models/block/plants").glob("*.obj"):
            self.assertTrue(path.read_text().startswith("# Original Stonedew organic plant art"))


if __name__ == "__main__":
    unittest.main()
