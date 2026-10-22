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
        for stage in range(4):
            for shape in range(4):
                for load in range(3 if stage >= 2 else 1):
                    for detail in ("", "_lod"):
                        path = ASSETS / "models/block/plants" / f"plant_{stage}_{shape}_{load}{detail}.json"
                        with self.subTest(model=path.name):
                            model = json.loads(path.read_text())
                            self.assertEqual(model["loader"], "neoforge:obj")
                            mesh = read_obj(path.with_suffix(".obj"))
                            self.assertGreater(len(mesh["f"]), 0)
                            self.assertLessEqual(len(mesh["f"]), 100 if detail else 1800)
                            for vertex in mesh["v"]:
                                self.assertTrue(all(math.isfinite(value) and -1 <= value <= 2 for value in vertex))

    def test_obj_indices_normals_and_materials_are_valid(self):
        for path in (ASSETS / "models").rglob("*.obj"):
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
                    texture = line.split()[1]
                    if texture == "stonedew:block/painted_leaf":
                        self.assertTrue((ASSETS / "textures/art/leaf_fan.png").is_file())
                    elif texture.startswith("stonedew:"):
                        self.assertTrue((ASSETS / "textures" / (texture.split(":", 1)[1]+".png")).is_file())

    def test_texture_dimensions_and_painted_sources(self):
        for path in (ASSETS / "textures").rglob("*.png"):
            data = path.read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", data[16:24])
            if path.parent.name == "art":
                for dimension in (width, height):
                    self.assertGreaterEqual(dimension, 256)
                    self.assertLessEqual(dimension, 2048)
                if path.name == "painted_materials.png": self.assertEqual(width, height)
                else: self.assertTrue(.75 <= width/height <= 1.5)
                if path.name == "leaf_fan.png":
                    self.assertEqual(data[25], 6, "Leaf cards must preserve alpha")
                else:
                    self.assertIn(data[25], (2, 6))
            else:
                self.assertEqual((width, height), (16, 16), path)
        for name in ("leaf_fan", "painted_materials"):
            self.assertTrue((ASSETS / "textures/art" / (name+".png")).is_file())

    def test_painted_sprite_source_and_card_binding_are_packaged(self):
        source_path = ROOT / "src/main/resources/assets/minecraft/atlases/blocks.json"
        sources = json.loads(source_path.read_text())["sources"]
        self.assertIn({"type": "stonedew:painted_materials", "resource": "stonedew:art/painted_materials"}, sources)
        materials = (ASSETS / "models/block/plants/plants.mtl").read_text()
        self.assertIn("map_Kd stonedew:block/painted_leaf", materials)
        self.assertIn("neoforge_TintIndex 3", materials)
        provenance = json.loads((ROOT / "docs/art/painted-sources.json").read_text())
        import hashlib
        for entry in provenance:
            path = ROOT / entry["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry["sha256"])

    def test_bud_load_and_branch_layouts_have_distinct_geometry(self):
        from plant_art import plant
        for stage in (2, 3):
            for shape in range(4):
                counts = [len(plant(stage, shape, load).faces) for load in range(3)]
                self.assertLess(counts[0], counts[1])
                self.assertLess(counts[1], counts[2])
        meshes = [str(plant(3, shape, 1).faces) for shape in range(4)]
        self.assertEqual(len(set(meshes)), 4)

    def test_equipment_is_bounded_and_uses_outward_closed_surfaces(self):
        from plant_art import Mesh
        mesh = Mesh()
        mesh.block((-1,-1,-1),(1,1,1))
        for _, vertices, normals, _ in mesh.faces:
            center = [sum(v[a] for v in vertices)/len(vertices) for a in range(3)]
            self.assertGreater(sum(center[a]*normals[0][a] for a in range(3)), 0)
        for path in (ASSETS / "models/block/equipment").glob("*.obj"):
            mesh = read_obj(path)
            self.assertLess(len(mesh["f"]), 1000)
            self.assertTrue(all(-.1 <= value <= 1.05 for vertex in mesh["v"] for value in vertex))

    def test_source_attribution_is_present(self):
        for path in (ASSETS / "models").rglob("*.json"):
            self.assertIn("Original Stonedew", json.loads(path.read_text())["credit"])
        for path in (ASSETS / "models").rglob("*.obj"):
            self.assertTrue(path.read_text().startswith("# Original Stonedew organic plant art"))


if __name__ == "__main__":
    unittest.main()
