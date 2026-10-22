"""Original reference-led hybrid plants: serrated flat foliage and stepped solid flowers.
Uses NeoForge's built-in OBJ loader. Coordinates are authored in sixteenths of a block.
Four branch layouts and three visible flower loads share deterministic baked meshes.
"""

import json
import math
import random


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

    def card(self, base, angle, length, width=None, pitch=.24, material="leaf"):
        """Painted, alpha-cutout fan on two hinged planes, with fixed world orientation."""
        width = width or length*1.10
        forward = (math.cos(angle), 0, math.sin(angle))
        sideways = (-math.sin(angle), 0, math.cos(angle))
        rows = []
        for t in (0, .50, 1):
            center = add(base, add(mul(forward, length*t*math.cos(pitch)),
                                   (0, length*t*math.sin(pitch) + .55*math.sin(math.pi*t), 0)))
            rows.append([add(center, mul(sideways, width*(u-.5))) for u in (0, 1)])
        for row in range(2):
            vertices = [rows[row][1], rows[row+1][1], rows[row+1][0], rows[row][0]]
            uv = [(1, 1-row*.5), (1, .5-row*.5), (0, .5-row*.5), (0, 1-row*.5)]
            # Upward foliage normals keep painted cards readable from either side.
            self.face(material, vertices, [(0, 1, 0)]*4, uv)
            self.face(material, list(reversed(vertices)), [(0, 1, 0)]*4, list(reversed(uv)))

    def block(self, lo, hi, material="bud"):
        x, y, z = lo
        X, Y, Z = hi
        for vertices in (
            [(x,y,z),(x,y,Z),(X,y,Z),(X,y,z)],
            [(x,Y,Z),(x,Y,z),(X,Y,z),(X,Y,Z)],
            [(X,y,z),(X,Y,z),(x,Y,z),(x,y,z)],
            [(x,y,Z),(x,Y,Z),(X,Y,Z),(X,y,Z)],
            [(x,y,z),(x,Y,z),(x,Y,Z),(x,y,Z)],
            [(X,y,Z),(X,Y,Z),(X,Y,z),(X,y,z)]):
            self.face(material, list(reversed(vertices)))

    def write(self, path, library="plants.mtl"):
        lines = ["# Original Stonedew organic plant art; tools/plant_art.py", "mtllib " + library, "o model"]
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


def flower(mesh, center, size, phase, lod=False):
    """Stepped, solid flower clusters: a tapered cola with individually offset bracts."""
    x, y, z = center
    if lod:
        mesh.block((x-size*.7,y-size*.5,z-size*.7), (x+size*.7,y+size*1.7,z+size*.7))
        return
    for tier, (width, bottom, top) in enumerate(((.82,-.4,.5),(.67,.4,1.25),(.43,1.2,1.8),(.22,1.75,2.12))):
        mesh.block((x-width*size,y+bottom*size,z-width*size),
                   (x+width*size,y+top*size,z+width*size), "bud_light" if tier == 3 else "bud")
    for i in range(6):
        angle = i*math.tau/6 + phase
        cx, cz = x+math.cos(angle)*size*.74, z+math.sin(angle)*size*.74
        cy = y + size*(.05+(i%3)*.36)
        r=size*(.26 if i%2 else .34)
        mesh.block((cx-r,cy-r,cz-r),(cx+r,cy+r*.95,cz+r), "bud_light" if i%3 == 1 else "bud")
    for i in range(3):
        angle=i*math.tau/3+phase
        cx, cz=x+math.cos(angle)*size*.63,z+math.sin(angle)*size*.63
        mesh.block((cx-size*.10,y+size*.9,cz-size*.1),
                   (cx+size*.1,y+size*1.15,cz+size*.1),"hair")


def plant(stage, shape, load=1, lod=False):
    mesh = Mesh()
    rng = random.Random(7701+shape*391)
    height = (2.2, 6.6, 10.8, 12.0)[stage] * (1, .94, 1.06, .98)[shape]
    wide = (1, 1.08, .88, 1.04)[shape]
    lean = ((.15,.1),(.9,-.5),(-.5,.6),(.6,.7))[shape]
    def stem(y): return (lean[0]*y/height, y, lean[1]*y/height)
    mesh.tube((0,0,0),stem(height),.16 if stage else .09,sides=4)
    if stage == 0:
        for i in range(2):
            mesh.card(stem(.85+i*.15), i*math.pi+shape*.65, 2.1, width=2.3, pitch=.30+i*.10)
        return mesh
    tiers = 4 if stage == 1 else 7
    if lod: tiers = 3
    for tier in range(tiers):
        fraction = (.10 + tier*(.78/(tiers-1)))
        y = height*fraction
        count = (3 if lod else (7 if stage >= 2 and tier < 4 else 5)) - (1 if tier == tiers-1 and not lod else 0)
        phase = shape*.51+tier*1.13+rng.uniform(-.20,.20)
        for i in range(count):
            angle = i*math.tau/count+phase+rng.uniform(-.20,.20)
            length = (7.8-5.7*fraction)*wide * rng.uniform(.88,1.12)
            if stage == 1: length *= .74
            base=stem(y+rng.uniform(-.22,.22))
            outward=(math.cos(angle)*(.7+tier*.05), .18, math.sin(angle)*(.7+tier*.05))
            tip=add(base,outward)
            if not lod: mesh.tube(base,tip,.08,sides=4)
            mesh.card(tip,angle,length,width=length*1.15,pitch=rng.uniform(.28,.65))
    if not lod:
        # Upright fill and crown fans bridge the gaps between skirts from a player's eye height.
        for fraction, length, count in ((.28,3.8,3),(.56,3.3,3),(.80,2.8,3),(.96,2.7,3)):
            for i in range(count):
                mesh.card(stem(height*fraction), i*math.tau/count+fraction*7+shape,
                          length*wide, pitch=.80 if fraction<.9 else .35)
    if stage >= 2:
        count=(5,9,13)[load]
        # Nested sites keep existing branch tips as new flowers fill in; no frame-time randomness.
        sites=[(*stem(height+.05),1.05)]
        for i in range(12):
            tier=i%3
            angle=i*2.39996+shape*.71
            fraction=(.27,.48,.69)[tier]+rng.uniform(-.035,.035)
            radius=(4.55,3.5,2.35)[tier]*wide*rng.uniform(.9,1.08)
            base=stem(height*fraction)
            sites.append((base[0]+math.cos(angle)*radius,base[1]+.7,
                          base[2]+math.sin(angle)*radius,rng.uniform(.63,.90)))
        for i,(x,y,z,size) in enumerate(sites[:count]):
            if lod and i >= (3,5,7)[load]: continue
            size *= .48 if stage == 2 else 1
            if not lod: mesh.tube(stem(y*.78),(x,y,z),.09,sides=4)
            flower(mesh,(x,y,z),size,shape+i*.7,lod)
    return mesh


def generate(root):
    directory = root / "models/block/plants"
    directory.mkdir(parents=True, exist_ok=True)
    # Obsolete habit meshes must not linger in the jar or the budget report.
    for pattern in ("*.obj", "*.json"):
        for path in directory.glob(pattern): path.unlink()
    materials = ["# Original Stonedew reference-led materials; tools/plant_art.py"]
    for name, texture, tint, color in [
        ("stem", "plant_stem", -1, (1, 1, 1)),
        ("leaf", "painted_leaf", 3, (1, 1, 1)),
        ("bud", "plant_bud", 1, (.78, .83, .73)),
        ("bud_light", "plant_bud", 1, (1, 1, .95)),
        ("hair", "plant_pistil", 2, (1, 1, 1)),
    ]:
        materials += [f"newmtl {name}", "Kd " + " ".join(map(str, color)),
                      f"map_Kd stonedew:block/{texture}", f"neoforge_TintIndex {tint}", ""]
    (directory / "plants.mtl").write_text("\n".join(materials))
    report=[]
    for stage in range(4):
        for shape in range(4):
            for load in range(3 if stage >= 2 else 1):
                for lod in (False,True):
                    mesh=plant(stage,shape,load,lod)
                    name=f"plant_{stage}_{shape}_{load}"+("_lod" if lod else "")
                    mesh.write(directory/f"{name}.obj")
                    data={"credit":"Original Stonedew reference-led art; tools/plant_art.py",
                          "loader":"neoforge:obj", "model":f"stonedew:models/block/plants/{name}.obj",
                          "automatic_culling":False,"shade_quads":True,"emissive_ambient":False,
                          "textures":{"particle":"stonedew:block/plant_leaf"}}
                    (directory/f"{name}.json").write_text(json.dumps(data,indent=2)+"\n")
                    report.append(dict(stage=stage,shape=shape,budLoad=load,buds=(5,9,13)[load] if stage>=2 else 0,
                                       lod=lod,faces=len(mesh.faces),vertices=sum(len(f[1]) for f in mesh.faces)))
    return report
