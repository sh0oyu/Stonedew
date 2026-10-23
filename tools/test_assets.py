"""Validate shipped geometry, materials and OBJ references before client loading."""
from pathlib import Path
import json
import math
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/assets/stonedew"


def atlas_regions():
    path=ROOT / 'src/main/resources/assets/minecraft/atlases/blocks.json'
    if not path.exists():return {}
    return {region['sprite']:region for source in json.loads(path.read_text())['sources']
            for region in source.get('regions',[])}


def texture_exists(texture):
    return (ASSETS / 'textures' / (texture.split(':',1)[1]+'.png')).is_file() or texture in atlas_regions()


def read_obj(path):
    result = {"v": [], "vn": [], "vt": [], "vc": [], "f": [], "usemtl": [], "mtllib": []}
    for line in path.read_text().splitlines():
        parts = line.split()
        if not parts or parts[0].startswith("#"):
            continue
        kind = parts[0]
        if kind in ("v", "vn", "vt", "vc"):
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
                            if not detail:self.assertTrue(mesh["vc"], "Near meshes require a successful AO bake")
                            self.assertLessEqual(len(mesh["f"]), 100 if detail else 14000)
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
                for uv in mesh["vt"]:
                    self.assertTrue(all(0 <= value <= 1 for value in uv), "Atlas UVs must never sample adjacent sprites")
                for normal in mesh["vn"]:
                    self.assertAlmostEqual(sum(v*v for v in normal), 1, places=4)
                for color in mesh["vc"]:
                    self.assertEqual(len(color), 4)
                    self.assertTrue(all(0 <= channel <= 1 for channel in color))
                for face in mesh["f"]:
                    self.assertIn(len(face), (3, 4))
                    for indices in face:
                        for index, kind in zip(indices, ("v", "vt", "vn", "vc")):
                            self.assertGreater(index, 0)
                            self.assertLessEqual(index, len(mesh[kind]))
                    self.assertGreaterEqual(len({mesh["v"][v[0]-1] for v in face}), 3)

    def test_models_and_materials_reference_present_textures(self):
        for path in (ASSETS / "models").rglob("*.json"):
            model = json.loads(path.read_text())
            for texture in model.get("textures", {}).values():
                if texture.startswith("stonedew:"):
                    self.assertTrue(texture_exists(texture),texture)
            for override in model.get("overrides", []):
                if override["model"].startswith("stonedew:"):
                    self.assertTrue((ASSETS/"models"/(override["model"].split(":",1)[1]+".json")).is_file())
            for element in model.get("elements", []):
                for face in element["faces"].values():
                    self.assertIn(face["texture"][1:], model["textures"])
                    self.assertTrue(all(0 <= value <= 16 for value in face["uv"]))
        for path in (ASSETS / "models").rglob("*.mtl"):
            for line in path.read_text().splitlines():
                if line.startswith("map_Kd "):
                    texture = line.split()[1]
                    if texture.startswith("stonedew:"):
                        self.assertTrue(texture_exists(texture),texture)

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
                expected = 128 if path.parent.name == "gui" else 64 if path.name.startswith('plant_shadow_') or path.name in ("leaf_fan.png", "leaf_emblem.png", "lamp_halo.png", "seed_packet.png", "uv_beam.png", "fixture_halo.png", "fixture_aura.png") else 32 if path.parent.name == "block" or path.name == "contact_shadow.png" else 16
                self.assertEqual((width, height), (expected, expected), path)
        self.assertTrue((ASSETS / "textures/block/leaf_fan.png").is_file())
        self.assertTrue((ASSETS / "textures/gui/materials.png").is_file())

    def test_painted_sprite_source_and_card_binding_are_packaged(self):
        # Painting windows have distinct IDs: never overwrite ordinary 32px sprites,
        # import the non-power-of-two source as a block sprite, or lower global mips.
        atlas=json.loads((ROOT/'src/main/resources/assets/minecraft/atlases/blocks.json').read_text())
        self.assertEqual(len(atlas['sources']),1)
        source=atlas['sources'][0]
        self.assertEqual(source['type'],'minecraft:unstitch')
        self.assertEqual(source['resource'],'stonedew:art/materials_v6')
        original=(ROOT/'docs/art/sources/materials-v6.png').read_bytes()
        self.assertEqual(original,(ASSETS/'textures/art/materials_v6.png').read_bytes())
        width,height=struct.unpack('>II',original[16:24])
        self.assertEqual((source['divisor_x'],source['divisor_y']),(width,height))
        self.assertEqual(len(atlas_regions()),16)
        for region in source['regions']:
            self.assertTrue(region['sprite'].startswith('stonedew:block/painted/'))
            self.assertEqual((region['width'],region['height']),(256,256))
            self.assertTrue(0<=region['x']<=width-256 and 0<=region['y']<=height-256)
        materials = (ASSETS / "models/block/plants/plants.mtl").read_text()
        self.assertIn("map_Kd stonedew:block/leaf_fan", materials)
        self.assertIn("neoforge_TintIndex 3", materials)
        near = read_obj(ASSETS / "models/block/plants/plant_3_0_0.obj")
        self.assertTrue(any(n[1] < -.5 for n in near["vn"]), "undersides need their own normals")
        self.assertTrue(any(.1 < abs(n[0]) < .9 for n in near["vn"]), "folded fans need directional normals")
        provenance = json.loads((ROOT / "docs/art/painted-sources.json").read_text())
        import hashlib
        for entry in provenance + json.loads((ROOT / "docs/art/authored-sources.json").read_text()):
            path = ROOT / entry["path"]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry["sha256"])

    def test_bud_load_and_branch_layouts_have_distinct_geometry(self):
        from plant_art import plant
        for stage in (3,):
            for shape in range(4):
                counts = [len(plant(stage, shape, load).faces) for load in range(3)]
                self.assertLess(counts[0], counts[1])
                self.assertLess(counts[1], counts[2])
        meshes = [str(plant(3, shape, 1).faces) for shape in range(4)]
        self.assertEqual(len(set(meshes)), 4)
        for stage in (0, 1, 2):
            self.assertFalse(any(material.startswith('bud') or material == 'hair'
                                 for material, *_ in plant(stage, 0).faces),
                             'The reference progression flowers only at maturity')

    def test_equipment_is_bounded_and_uses_outward_closed_surfaces(self):
        from plant_art import Mesh
        mesh = Mesh()
        mesh.block((-1,-1,-1),(1,1,1))
        for _, vertices, normals, _ in mesh.faces:
            center = [sum(v[a] for v in vertices)/len(vertices) for a in range(3)]
            self.assertGreater(sum(center[a]*normals[0][a] for a in range(3)), 0)
        for path in (ASSETS / "models/block/equipment").glob("*.obj"):
            mesh = read_obj(path)
            self.assertLessEqual(len(mesh["f"]), 1400)
            self.assertTrue(all(-.1 <= value <= 1.05 for vertex in mesh["v"] for value in vertex))

    def test_pistil_caps_are_on_exposed_bract_tops(self):
        from plant_art import Mesh, flower
        mesh = Mesh()
        flower(mesh, (0,0,0), 1, 0)
        hairs = [face for face in mesh.faces if face[0] == "hair"]
        self.assertEqual(len(hairs), 30)
        tops = [face[1] for face in mesh.faces if face[0].startswith("bud") and face[2][0][1] > .5]
        for offset in range(0, len(hairs), 6):
            vertices = [vertex for face in hairs[offset:offset+6] for vertex in face[1]]
            x = (min(v[0] for v in vertices)+max(v[0] for v in vertices))/2
            z = (min(v[2] for v in vertices)+max(v[2] for v in vertices))/2
            y = min(v[1] for v in vertices)
            self.assertTrue(any(abs(top[0][1]-y)<1e-6
                and min(v[0] for v in top)<=x<=max(v[0] for v in top)
                and min(v[2] for v in top)<=z<=max(v[2] for v in top) for top in tops))

    def test_thin_chamfers_preserve_closed_outward_surfaces(self):
        from plant_art import Mesh
        mesh=Mesh()
        mesh.bevel((-2,-2,-.11),(2,2,.11),.11)
        for _,vertices,normals,_ in mesh.faces:
            self.assertGreaterEqual(len(set(vertices)),3)
            center=tuple(sum(v[i] for v in vertices)/len(vertices) for i in range(3))
            self.assertGreater(sum(center[i]*normals[0][i] for i in range(3)),0)

    def test_emissive_passes_do_not_make_entire_props_unlit(self):
        found=0
        for path in (ASSETS/"models").rglob("*.json"):
            model=json.loads(path.read_text())
            if model.get("loader")!="neoforge:composite":continue
            found+=1
            self.assertIn("particle",model["textures"])
            body=model["children"]["body"];light=model["children"]["light"]
            self.assertEqual(light["render_type"],"stonedew:emissive")
            self.assertNotEqual(body["render_type"],light["render_type"])
            body_mesh=read_obj(ASSETS/body["model"].split(":",1)[1])
            self.assertTrue(all("emission" not in material for material in body_mesh["usemtl"]), "Diffuse body must not overwrite the luminous pass")
            mesh=read_obj(ASSETS/light["model"].split(":",1)[1])
            self.assertTrue(all("emission" in material for material in mesh["usemtl"]))
            self.assertTrue(all(color==(1,1,1,1) for color in mesh["vc"]))
        self.assertGreater(found,0)

    def test_source_attribution_is_present(self):
        for path in (ASSETS / "models").rglob("*.json"):
            self.assertIn("Original Stonedew", json.loads(path.read_text())["credit"])
        for path in (ASSETS / "models").rglob("*.obj"):
            self.assertTrue(path.read_text().startswith("# Original Stonedew organic plant art"))


if __name__ == "__main__":
    unittest.main()
