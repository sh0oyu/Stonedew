"""Checks that authored voxel assets remain valid, bounded and reasonably sized."""
from pathlib import Path
import json
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/assets/stonedew"


class AssetTests(unittest.TestCase):
    def test_all_plant_stages_and_habits_have_bounded_meshes(self):
        for habit in ("bushy", "hybrid", "tall"):
            for stage in range(4):
                for detail in ("", "_lod"):
                    path = ASSETS / "models/block/plants" / f"{habit}_{stage}{detail}.json"
                    with self.subTest(model=path.name):
                        model = json.loads(path.read_text())
                        quads = sum(len(element["faces"]) for element in model["elements"])
                        self.assertGreater(quads, 0)
                        self.assertLessEqual(quads, 40 if detail else 1000)
                        for element in model["elements"]:
                            for lo, hi in zip(element["from"], element["to"]):
                                self.assertGreaterEqual(lo, -16)
                                self.assertLessEqual(hi, 32)
                                self.assertLessEqual(lo, hi)

    def test_models_only_reference_present_material_textures(self):
        for path in (ASSETS / "models").rglob("*.json"):
            model = json.loads(path.read_text())
            for texture in model.get("textures", {}).values():
                if texture.startswith("stonedew:"):
                    local = texture.split(":", 1)[1]
                    self.assertTrue((ASSETS / "textures" / f"{local}.png").is_file(), (path, texture))
            for element in model.get("elements", []):
                for face in element["faces"].values():
                    self.assertIn(face["texture"][1:], model["textures"])
                    self.assertTrue(all(0 <= value <= 16 for value in face["uv"]))

    def test_material_textures_keep_vanilla_pixel_density(self):
        for path in (ASSETS / "textures").rglob("*.png"):
            data = path.read_bytes()
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", data[16:24]), (16, 16), path)

    def test_source_attribution_is_present(self):
        for path in (ASSETS / "models").rglob("*.json"):
            self.assertIn("Original Stonedew voxel art", json.loads(path.read_text())["credit"])


if __name__ == "__main__":
    unittest.main()
