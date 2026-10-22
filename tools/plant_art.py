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

    def card(self, base, angle, length, width=None, pitch=.16, material="leaf", simple=False):
        """Broad, lightly creased fan with geometric front AND underside normals."""
        width = width or length*1.32
        if simple:
            forward=(math.cos(angle),0,math.sin(angle))
            across=(-math.sin(angle),0,math.cos(angle))
            tip=add(base,add(mul(forward,length*math.cos(pitch)),(0,length*math.sin(pitch),0)))
            vertices=[add(base,mul(across,width*.5)),add(tip,mul(across,width*.5)),
                      add(tip,mul(across,-width*.5)),add(base,mul(across,-width*.5))]
            uv=[(1,1),(1,0),(0,0),(0,1)]
            self.face(material,vertices,uv=uv)
            self.face(material,list(reversed(vertices)),uv=list(reversed(uv)))
            return
        forward=(math.cos(angle),0,math.sin(angle))
        across=(-math.sin(angle),0,math.cos(angle))
        rows=[]
        for t in (0,.5,1):
            center=add(base,add(mul(forward,length*t*math.cos(pitch)),
                                (0,length*(t*math.sin(pitch)-.10*t*t),0)))
            rows.append([add(center,add(mul(across,width*(u-.5)),
                         (0,.045*length*math.sin(math.pi*t)*(1-2*abs(u-.5)),0))) for u in (0,.5,1)])
        for row in range(2):
            for side in range(2):
                vertices=[rows[row][side+1],rows[row+1][side+1],rows[row+1][side],rows[row][side]]
                uv=[((side+1)/2,1-row*.5),((side+1)/2,.5-row*.5),(side/2,.5-row*.5),(side/2,1-row*.5)]
                self.face(material,vertices,uv=uv)
                self.face(material,list(reversed(vertices)),uv=list(reversed(uv)))

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
    """Bulging stepped flower, with recessed seams and individually visible bracts.
    Emit only the exposed faces of the cluster; interior voxel faces are discarded.
    """
    x,y,z=center
    if lod:
        mesh.block((x-size,y,z-size),(x+size,y+size*2.4,z+size),"bud")
        return
    cells=set()
    radii=(.9,1.13,1.06,.90,.68,.35)
    for tier,radius in enumerate(radii):
        for xx in range(-2,3):
            for zz in range(-2,3):
                # Slight deterministic asymmetry prevents a mechanically repeated pyramid.
                perturb=.045*math.sin(xx*3+zz*5+phase+tier)
                if math.hypot(xx/2,zz/2)<=radius+perturb:cells.add((xx,tier,zz))
    step=size*.58
    neighbors=((0,-1,0),(0,1,0),(0,0,-1),(0,0,1),(-1,0,0),(1,0,0))
    for xx,yy,zz in sorted(cells):
        lo=(x+(xx-.5)*step,y+yy*step,z+(zz-.5)*step)
        hi=(lo[0]+step,lo[1]+step,lo[2]+step)
        material="bud_light" if yy>=4 or (xx*7+yy*3+zz*11)%9==0 else "bud_dark" if yy==0 else "bud"
        voxel=Mesh();voxel.block(lo,hi,material)
        for face,delta in zip(voxel.faces,neighbors):
            if (xx+delta[0],yy+delta[1],zz+delta[2]) not in cells:
                mat,vertices,normals,uv=face
                if normals[0][1]>.5: mat="bud_light"
                mesh.faces.append((mat,vertices,normals,uv))
    # Put colored pistils ON exposed bracts, rather than burying them inside the cluster.
    caps=[cell for cell in sorted(cells) if (cell[0],cell[1]+1,cell[2]) not in cells
          and 1<=cell[1]<=3 and (cell[0] or cell[2])]
    random.Random(round(phase*1000)).shuffle(caps)
    caps=caps[:4]+[(0,5,0)]
    for xx,yy,zz in caps:
        cx,cz=x+xx*step,z+zz*step
        cy=y+(yy+1)*step
        mesh.block((cx-step*.22,cy,cz-step*.22),(cx+step*.22,cy+step*.35,cz+step*.22),"hair")


def plant(stage, shape, load=1, lod=False):
    mesh=Mesh();rng=random.Random(7701+shape*391)
    height=(2.6,7.6,12.1,13.0)[stage]*(1,.97,1.04,.98)[shape]
    wide=(1,1.06,.92,1.03)[shape]
    lean=((.1,.1),(.7,-.4),(-.5,.5),(.5,.6))[shape]
    def stem(y):return(lean[0]*y/height,y,lean[1]*y/height)
    mesh.tube((0,0,0),stem(height),.18 if stage else .10,sides=4)
    if stage==0:
        for i in range(2):mesh.card(stem(1.1),i*math.pi+shape*.3,2.2,width=2.7,pitch=.3)
        return mesh
    tiers=(.17,.48,.78) if stage==1 else (.12,.30,.48,.66,.84)
    if lod:tiers=(.16,.49,.80)
    for tier,fraction in enumerate(tiers):
        y=height*fraction
        count=3 if lod else 4
        phase=shape*.49+tier*math.pi*.27
        for i in range(count):
            angle=i*math.tau/count+phase+rng.uniform(-.10,.10)
            length=(8.8-5.5*fraction)*wide*rng.uniform(.96,1.04)
            if stage==1:length*=.70
            base=stem(y)
            tip=add(base,(math.cos(angle)*.35,.1,math.sin(angle)*.35))
            if not lod:mesh.tube(base,tip,.08,sides=4)
            mesh.card(tip,angle,length,width=length*1.32,pitch=rng.uniform(-.04,.21)+fraction*.12,simple=lod,material="leaf_old" if fraction<.4 else "leaf")
    if not lod:
        for i in range(4):mesh.card(stem(height*.91),i*math.tau/4+shape*.6,3.6,pitch=.25)
    if not lod:
        for fraction,length in ((.42,4.0),(.67,3.0)):
            for i in range(3):mesh.card(stem(height*fraction),i*math.tau/3+shape*.8+fraction, length, pitch=.65)
    if stage>=2:
        count=(5,9,13)[load]
        sites=[(*stem(height-.3),1.2)]
        for i in range(12):
            tier=i%3
            angle=(i//3)*math.pi/2+tier*.95+shape*.5
            fraction=(.25,.48,.70)[tier]
            radius=(5.8,4.5,3.0)[tier]*wide
            root=stem(height*fraction)
            sites.append((root[0]+math.cos(angle)*radius,root[1]+.65,
                          root[2]+math.sin(angle)*radius,rng.uniform(.72,.85)))
        for i,(x,y,z,size) in enumerate(sites[:count]):
            if lod and i>=(3,5,7)[load]:continue
            size*=.48 if stage==2 else 1
            if not lod:mesh.tube(stem(y*.82),(x,y,z),.12,sides=4)
            if i and not lod:
                mesh.card((x,y-.12,z),math.atan2(z,x),size*2.8,width=size*3.5,pitch=.12,material="leaf_old")
            first=len(mesh.faces)
            flower(mesh,(x,y,z),size,shape+i*.7,lod)
            # Side colas lean out from their branch; the central leader remains upright.
            if i and not lod:
                tilt=.27;angle=math.atan2(z,x)
                for face in range(first,len(mesh.faces)):
                    mat,vertices,normals,uv=mesh.faces[face]
                    def rotate(v,normal=False):
                        dx,dy,dz=v if normal else (v[0]-x,v[1]-y,v[2]-z)
                        radial=dx*math.cos(angle)+dz*math.sin(angle)
                        along=-radial*math.sin(tilt)+dy*math.cos(tilt)
                        out=radial*math.cos(tilt)+dy*math.sin(tilt)-radial
                        result=(dx+out*math.cos(angle),along,dz+out*math.sin(angle))
                        return result if normal else (x+result[0],y+result[1],z+result[2])
                    mesh.faces[face]=(mat,[rotate(v) for v in vertices],[rotate(v,True) for v in normals],uv)
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
        ("leaf", "leaf_fan", 3, (1, 1, 1)),
        ("leaf_old", "leaf_fan", 3, (.83, .92, .86)),
        ("bud", "plant_bud", 1, (.90, .90, .90)),
        ("bud_dark", "plant_bud", 1, (.69, .69, .74)),
        ("bud_light", "plant_bud", 4, (1, 1, 1)),
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
