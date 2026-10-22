"""Original organic plant meshes: curved leaf fans and clustered, lobed flower heads.

Uses NeoForge's built-in OBJ loader, so leaves and buds need not be cuboids.
Coordinates are authored in sixteenths of a block, with the stem at (0, 0, 0).
"""

import json
import math


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(a, scale):
    return tuple(x * scale for x in a)


def unit(a):
    length = math.sqrt(sum(x * x for x in a))
    return mul(a, 1 / length) if length else (0, 1, 0)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


class Mesh:
    def __init__(self):
        self.faces = []

    def face(self, material, vertices, normals=None, uv=None):
        if normals is None:
            normal = unit(cross(add(vertices[1], mul(vertices[0], -1)),
                                add(vertices[2], mul(vertices[0], -1))))
            normals = [normal] * len(vertices)
        self.faces.append((material, vertices, normals, uv or [(0, 0), (1, 0), (1, 1), (0, 1)][:len(vertices)]))

    def tube(self, start, end, radius=.13, material="stem", sides=5):
        direction = unit(add(end, mul(start, -1)))
        side = unit(cross(direction, (0, 0, 1)))
        across = unit(cross(direction, side))
        rings = []
        for center, taper in ((start, 1), (end, .65)):
            rings.append([add(center, add(mul(side, radius*taper*math.cos(i*math.tau/sides)),
                                          mul(across, radius*taper*math.sin(i*math.tau/sides))))
                          for i in range(sides)])
        for i in range(sides):
            j = (i + 1) % sides
            self.face(material, [rings[0][i], rings[0][j], rings[1][j], rings[1][i]])

    def puff(self, center, radii, phase=0, material="bud", sides=8, bands=4):
        """A soft lumpy ellipsoid, with smooth normals and a gently irregular outline."""
        rings, normals = [], []
        for band in range(bands + 1):
            latitude = math.pi * band / bands
            ring, normal_ring = [], []
            for i in range(sides):
                angle = i * math.tau / sides
                lobe = 1 + .12 * math.cos(angle*3 + phase + band*.8)
                radial = math.sin(latitude)
                direction = (radial*math.cos(angle), -math.cos(latitude), radial*math.sin(angle))
                offset = tuple(direction[a]*radii[a]*(lobe if a != 1 else 1) for a in range(3))
                ring.append(add(center, offset))
                normal_ring.append(unit(tuple(direction[a]/radii[a] for a in range(3))))
            rings.append(ring)
            normals.append(normal_ring)
        for band in range(bands):
            for i in range(sides):
                j = (i + 1) % sides
                corners = [(band, i), (band, j), (band+1, j), (band+1, i)]
                if band == 0:
                    corners = corners[1:]
                elif band == bands - 1:
                    corners = corners[:3]
                corners = list(reversed(corners))
                self.face(material, [rings[b][k] for b, k in corners],
                          [normals[b][k] for b, k in corners],
                          [(k/sides, b/bands) for b, k in corners])

    def blade(self, base, angle, length, width, lift=.8, material="leaf", simple=False):
        """Folded, arched leaf with a pointed tip and serrated outer edges."""
        forward = (math.cos(angle), 0, math.sin(angle))
        sideways = (-math.sin(angle), 0, math.cos(angle))
        steps = 2 if simple else 5
        rows = []
        for i in range(steps + 1):
            t = i / steps
            belly = math.sin(math.pi*t)**.8
            tooth = 1 if simple or i % 2 else .70
            spread = width*belly*tooth
            center = add(base, add(mul(forward, length*t),
                                   (0, lift*math.sin(math.pi*t)-length*.22*t*t, 0)))
            fold = .24*belly
            rows.append([add(center, add(mul(sideways, -spread), (0, -fold, 0))),
                         add(center, (0, fold, 0)),
                         add(center, add(mul(sideways, spread), (0, -fold, 0)))])
        for i in range(steps):
            for side in range(2):
                vertices = [rows[i][side], rows[i+1][side], rows[i+1][side+1], rows[i][side+1]]
                # Explicit back faces retain foliage when viewed from below.
                uv = [(side/2, i/steps), (side/2, (i+1)/steps),
                      ((side+1)/2, (i+1)/steps), ((side+1)/2, i/steps)]
                if i == 0:
                    vertices, uv = vertices[:3], uv[:3]
                elif i == steps - 1:
                    vertices, uv = [vertices[k] for k in (0, 1, 3)], [uv[k] for k in (0, 1, 3)]
                self.face(material, vertices, uv=uv)
                self.face(material, list(reversed(vertices)), uv=list(reversed(uv)))

    def fan(self, center, angle, size, simple=False, sugar=False):
        joint = add(center, (math.cos(angle)*1.35, .35, math.sin(angle)*1.35))
        self.tube(center, joint, .10 if sugar else .13)
        fingers = (-.78, -.38, 0, .38, .78) if not simple else (-.5, 0, .5)
        for finger in fingers:
            length = size * (1 - abs(finger)*.58)
            self.blade(joint, angle+finger, length, length*.14,
                       lift=length*.16, material="sugar" if sugar else "leaf", simple=simple)

    def write(self, path):
        lines = ["# Original Stonedew organic plant art; tools/plant_art.py", "mtllib plants.mtl", "o plant"]
        index = 1
        previous = None
        for material, vertices, normals, uv in self.faces:
            if material != previous:
                lines.append("usemtl " + material)
                previous = material
            for vertex in vertices:
                lines.append("v " + " ".join(f"{(v + (8 if a != 1 else 0))/16:.6f}" for a, v in enumerate(vertex)))
            for u, v in uv:
                lines.append(f"vt {u:.6f} {v:.6f}")
            for normal in normals:
                lines.append("vn " + " ".join(f"{v:.6f}" for v in normal))
            lines.append("f " + " ".join(f"{i}/{i}/{i}" for i in range(index, index+len(vertices))))
            index += len(vertices)
        path.write_text("\n".join(lines) + "\n")


def plant(stage, habit, lod=False):
    mesh = Mesh()
    height = (3.2, 8.8, 12.3, 14.2)[stage]
    tall = 1.18 if habit == "tall" else .92 if habit == "bushy" else 1
    wide = .84 if habit == "tall" else 1.08 if habit == "bushy" else 1
    height *= tall
    lean = .65 if habit == "tall" else .35
    mesh.tube((0, 0, 0), (lean, height, -.15), .17 if stage else .12, sides=5)
    if stage == 0:
        for angle in (.3, math.pi+.3):
            mesh.blade((0, 2.3, 0), angle, 2.5, .65, lift=.6, simple=lod)
        if not lod:
            for angle in (1.9, 5):
                mesh.blade((0, 3, 0), angle, 1.4, .27, lift=.5)
        return mesh
    if lod:
        for tier, y in enumerate((height*.3, height*.65)):
            for i in range(3):
                angle = i*math.tau/3 + tier*.9
                mesh.blade((0, y, 0), angle, (6.3-tier*1.7)*wide, 1.15, simple=True)
        if stage >= 2:
            for x, y, z in ((lean, height, 0), (2.8, height*.64, 1), (-2.8, height*.62, -1)):
                mesh.puff((x, y, z), (1.7, 2.0, 1.7), material="bud", sides=5, bands=3)
        return mesh
    tiers = [(height*.24, 4, 5.8*wide), (height*.53, 3, 4.7*wide)]
    if stage >= 2:
        tiers += [(height*.74, 3, 4.5*wide), (height*.89, 3, 3.5*wide)]
    for tier, (y, count, size) in enumerate(tiers):
        for i in range(count):
            angle = i*math.tau/count + tier*1.1 + .35
            mesh.fan((lean*y/height, y, 0), angle, size)
    if stage >= 2:
        sites = [(lean, height-.25, 0, 2.0)]
        for i in range(4):
            angle = i*math.tau/4 + .4
            radius = 3.5*wide
            sites.append((math.cos(angle)*radius, height*.66 + (i%2)*.9,
                          math.sin(angle)*radius, 1.55))
        for i in range(3):
            angle = i*math.tau/3 + 1.2
            sites.append((math.cos(angle)*4.7*wide, height*.39,
                          math.sin(angle)*4.7*wide, 1.25))
        for i, (x, y, z, size) in enumerate(sites):
            size *= .68 if stage == 2 else .90
            mesh.tube((lean*.6, y*.65, 0), (x, y, z), .13)
            # Green bracts cradle the colored flower, rather than a single solid column.
            mesh.puff((x, y-.65, z), (size*.82, size*.45, size*.82), i, "bract", sides=6, bands=3)
            mesh.puff((x, y+.25, z), (size*.86, size*.98, size*.86), i*.7,
                      "bud", sides=8, bands=3)
            for tuft in range(5):
                angle = tuft*math.tau/5 + i
                center = (x+math.cos(angle)*size*.65, y+.30+math.sin(tuft*1.7)*size*.20, z+math.sin(angle)*size*.65)
                mesh.puff(center, (size*.36, size*.46, size*.36), i+tuft,
                          "bud_light" if tuft == 1 else "bud", sides=6, bands=3)
            mesh.puff((x+.12*size, y+size*1.05, z),
                      (size*.60, size*.57, size*.58), i, "bud_light", sides=6, bands=3)
            for tip in range(2):
                angle = i + tip*2.8
                base = (x+math.cos(angle)*size*.65, y+size*.8, z+math.sin(angle)*size*.65)
                mesh.blade(base, angle, .4, .06, lift=.25, material="hair", simple=True)
            if i < 8:
                mesh.fan((x, y-.5, z), i*1.9, 3.3*wide, simple=True, sugar=True)
    return mesh


def generate(root):
    directory = root / "models/block/plants"
    directory.mkdir(parents=True, exist_ok=True)
    materials = ["# Original Stonedew organic plant materials; tools/plant_art.py"]
    for name, texture, tint, color in [
        ("stem", "plant_stem", -1, (1, 1, 1)),
        ("leaf", "plant_leaf", 0, (1, 1, 1)),
        ("sugar", "plant_leaf", 0, (.88, .97, .88)),
        ("bract", "plant_bud", 0, (.82, .92, .73)),
        ("bud", "plant_bud", 1, (.83, .92, .88)),
        ("bud_light", "plant_bud", 1, (1, 1, 1)),
        ("hair", "plant_pistil", 2, (1, 1, 1)),
    ]:
        materials += [f"newmtl {name}", "Kd " + " ".join(map(str, color)),
                      f"map_Kd stonedew:block/{texture}", f"neoforge_TintIndex {tint}", ""]
    (directory / "plants.mtl").write_text("\n".join(materials))
    report = []
    for habit in ("bushy", "hybrid", "tall"):
        for stage in range(4):
            for lod in (False, True):
                mesh = plant(stage, habit, lod)
                name = f"{habit}_{stage}" + ("_lod" if lod else "")
                mesh.write(directory / f"{name}.obj")
                data = {
                    "credit": "Original Stonedew organic plant art; tools/plant_art.py",
                    "loader": "neoforge:obj",
                    "model": f"stonedew:models/block/plants/{name}.obj",
                    "automatic_culling": False, "shade_quads": True, "emissive_ambient": False,
                    "textures": {"particle": "stonedew:block/plant_leaf"},
                }
                (directory / f"{name}.json").write_text(json.dumps(data, indent=2) + "\n")
                report.append(dict(habit=habit, stage=stage, lod=lod,
                                   faces=len(mesh.faces), vertices=sum(len(f[1]) for f in mesh.faces)))
    return report
