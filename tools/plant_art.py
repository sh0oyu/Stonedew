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

    def fan(self, base, angle, length, pitch=.12, material="leaf", young=False):
        """Seven individually serrated, creased 2D leaflets; no alpha/mipmap erosion.

        All leaflets share a petiole, but spread radially in the fan's own plane.
        The underside is explicit geometry; two planes meet along each midrib.
        """
        forward=(math.cos(angle),0,math.sin(angle))
        across=(-math.sin(angle),0,math.cos(angle))
        def point(x,z,t):
            return add(base, add(mul(across,x), add(mul(forward,z*math.cos(pitch)),
                (0,z*math.sin(pitch)-.07*length*t*t,0))))
        for finger,(degrees,ratio) in enumerate(((-73,.48),(-48,.72),(-24,.91),(0,1),(24,.91),(48,.72),(73,.48))):
            theta=math.radians(degrees); reach=length*ratio
            # Broad tapered lobes, with six substantial forward-pointing teeth per edge.
            half=reach*(.115 if young else .125)
            rows=[]
            for segment in range(13):
                t=segment/12
                width=half*(math.sin(math.pi*t)**.70 if segment not in (0,12) else .035)
                if segment%2==0:width*=.70
                along=reach*t
                center=(math.sin(theta)*along,math.cos(theta)*along)
                row=[]
                for side in (-1,0,1):
                    x=center[0]+math.cos(theta)*width*side
                    z=center[1]-math.sin(theta)*width*side
                    v=point(x,z,t)
                    row.append(add(v,(0,.05*reach*math.sin(math.pi*t)*(1-abs(side)),0)))
                rows.append(row)
            for row in range(12):
                for side in range(2):
                    vertices=[rows[row][side+1],rows[row+1][side+1],rows[row+1][side],rows[row][side]]
                    mat=material+('_shade' if side else '')
                    u0,u1=(0,1) if side else (1,0)
                    uv=[(u1,row/12),(u1,(row+1)/12),(u0,(row+1)/12),(u0,row/12)]
                    self.face(mat,vertices,uv=uv)
                    self.face(mat,list(reversed(vertices)),uv=list(reversed(uv)))

    def cotyledon(self, base, angle):
        forward=(math.cos(angle),0,math.sin(angle));side=(-math.sin(angle),0,math.cos(angle))
        rows=[]
        for i in range(7):
            t=i/6;width=max(.025,math.sin(math.pi*t)**.65*.62)
            center=add(base,add(mul(forward,1.8*t),(0,.5*t,0)))
            rows.append([add(center,mul(side,-width)),add(center,(0,.05,0)),add(center,mul(side,width))])
        for i in range(6):
            for j in range(2):
                vertices=[rows[i][j+1],rows[i+1][j+1],rows[i+1][j],rows[i][j]]
                mat='leaf' if j==0 else 'leaf_shade'
                self.face(mat,vertices)
                self.face(mat,list(reversed(vertices)))

    def bevel(self, lo, hi, amount=.12, material="iron", edge=None):
        """Closed chamfered cuboid: six inset faces, twelve edge strips, eight corners."""
        amount=min(amount, min(b-a for a,b in zip(lo,hi))*.45)
        center=tuple((a+b)/2 for a,b in zip(lo,hi)); edge=edge or material
        def emit(vertices, mat):
            n=unit(cross(add(vertices[1],mul(vertices[0],-1)),add(vertices[2],mul(vertices[0],-1))))
            c=tuple(sum(v[i] for v in vertices)/len(vertices)-center[i] for i in range(3))
            if sum(a*b for a,b in zip(n,c))<0:vertices=list(reversed(vertices))
            self.face(mat,vertices)
        def v(coords):return tuple(coords)
        for axis in range(3):
            other=[i for i in range(3) if i!=axis]
            for sign in (0,1):
                vs=[]
                for a,b in ((0,0),(1,0),(1,1),(0,1)):
                    q=list(center);q[axis]=(lo,hi)[sign][axis]
                    q[other[0]]=(lo[other[0]]+amount,hi[other[0]]-amount)[a]
                    q[other[1]]=(lo[other[1]]+amount,hi[other[1]]-amount)[b];vs.append(v(q))
                emit(vs,material)
        for axis in range(3):
            a,b=[i for i in range(3) if i!=axis]
            for sa in (0,1):
                for sb in (0,1):
                    va=(lo,hi)[sa][a];vb=(lo,hi)[sb][b];da=amount*(1 if sa==0 else -1);db=amount*(1 if sb==0 else -1)
                    vs=[]
                    for t,side in ((0,0),(1,0),(1,1),(0,1)):
                        q=list(center);q[axis]=(lo[axis]+amount,hi[axis]-amount)[t]
                        q[a]=va+(da if side else 0);q[b]=vb+(0 if side else db);vs.append(v(q))
                    emit(vs,edge)
        for sx in (0,1):
            for sy in (0,1):
                for sz in (0,1):
                    c=[(lo,hi)[sign][axis] for axis,sign in enumerate((sx,sy,sz))];vs=[]
                    for axis in range(3):
                        q=[c[i]+amount*(1 if (sx,sy,sz)[i]==0 else -1) for i in range(3)]
                        q[axis]=c[axis];vs.append(v(q))
                    emit(vs,edge)

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
        # Share position / UV / normal indices; fully expanded OBJ duplicates most vertices.
        tables=[[],[],[]];indices=[{},{},{}];faces=[]
        def index(kind,value):
            key=tuple(round(v,6) for v in value)
            if key not in indices[kind]:
                indices[kind][key]=len(tables[kind])+1;tables[kind].append(key)
            return indices[kind][key]
        for material,vertices,normals,uvs in self.faces:
            face=[]
            for vertex,normal,uv in zip(vertices,normals,uvs):
                position=tuple((v+(8 if a!=1 else 0))/16 for a,v in enumerate(vertex))
                face.append((index(0,position),index(1,uv),index(2,normal)))
            faces.append((material,face))
        lines=["# Original Stonedew organic plant art; tools/plant_art.py", "mtllib "+library,"o model"]
        for tag,table in zip(('v','vt','vn'),tables):
            lines += [tag+' '+' '.join(f'{v:.6f}' for v in value) for value in table]
        previous=None
        for material,face in faces:
            if material!=previous:lines.append('usemtl '+material);previous=material
            lines.append('f '+' '.join('/'.join(map(str,v)) for v in face))
        path.write_text('\n'.join(lines)+'\n')


def flower(mesh, center, size, phase, lod=False):
    """Interlocking solid bracts around a fat heart, rather than an aligned voxel tower."""
    x,y,z=center
    if lod:
        mesh.block((x-size,y,z-size),(x+size,y+size*2.6,z+size),"bud")
        return
    rng=random.Random(round(phase*1000)+441)
    parts=[(0,1.3,0,.70,1.35,"bud_dark")]
    for tier,(height,radius,count,width) in enumerate(((.65,.68,5,.63),(1.48,.55,4,.58),(2.25,.30,3,.46))):
        for i in range(count):
            angle=phase+i*math.tau/count+tier*.67
            parts.append((math.cos(angle)*radius,height,math.sin(angle)*radius,width,rng.uniform(.49,.68),"bud_light" if tier==2 else "bud"))
    for i,(px,py,pz,w,h,mat) in enumerate(parts):
        first=len(mesh.faces)
        mesh.bevel((px-w,py-h,pz-w),(px+w,py+h,pz+w),.14,mat,"bud_light" if mat!="bud_dark" else "bud")
        # Misaligned bract facets make a puffy cluster and visible dark seams.
        angle=phase+i*.69; c=math.cos(angle);ss=math.sin(angle)
        for f in range(first,len(mesh.faces)):
            m,vertices,normals,uv=mesh.faces[f]
            def turn(v,normal=False):
                dx,dy,dz=v if normal else (v[0]-px,v[1]-py,v[2]-pz)
                out=(dx*c+dz*ss,dy,dz*c-dx*ss)
                return out if normal else (x+(out[0]+px)*size,y+(out[1]+py)*size,z+(out[2]+pz)*size)
            mesh.faces[f]=(m,[turn(v) for v in vertices],[turn(v,True) for v in normals],uv)
        if i in (1,3,6,9,12):
            # Small raised orange/lilac pistil at an exposed bract shoulder.
            cx=x+px*size;cz=z+pz*size;cy=y+(py+h)*size
            mesh.block((cx-.14*size,cy,cz-.14*size),(cx+.14*size,cy+.24*size,cz+.14*size),"hair")


def plant(stage, shape, load=1, lod=False):
    mesh=Mesh();rng=random.Random(7701+shape*391)
    height=(2.6,7.6,12.1,13.0)[stage]*(1,.97,1.04,.98)[shape]
    wide=(1,1.06,.92,1.03)[shape]
    lean=((.1,.1),(.7,-.4),(-.5,.5),(.5,.6))[shape]
    def stem(y):return(lean[0]*y/height,y,lean[1]*y/height)
    mesh.tube((0,0,0),stem(height if stage else 1.8),.18 if stage else .10,sides=4)
    if stage==0:
        for i in range(2):mesh.cotyledon(stem(1.8),i*math.pi+shape*.3)
        return mesh
    tiers=(.17,.48,.78) if stage==1 else (.12,.30,.48,.66,.84)
    if lod:tiers=(.16,.49,.80)
    for tier,fraction in enumerate(tiers):
        y=height*fraction
        count=3 if lod or stage>=2 else 2
        phase=shape*.49+tier*math.pi*.27
        for i in range(count):
            angle=i*math.tau/count+phase+rng.uniform(-.10,.10)
            length=(9.6-6.6*fraction)*wide*rng.uniform(.96,1.04)
            if stage==1:length*=.70
            base=stem(y)
            tip=add(base,(math.cos(angle)*.35,.1,math.sin(angle)*.35))
            if not lod:mesh.tube(base,tip,.08,sides=4)
            if lod:
                mesh.card(tip,angle,length,width=length*1.32,pitch=.12,simple=True,material="leaf_lod")
            else:
                mesh.fan(tip,angle,length,pitch=rng.uniform(-.02,.18)+fraction*.12,material="leaf_old" if fraction<.4 else "leaf",young=stage==1)
    if not lod and stage>=2:
        for i in range(3):mesh.fan(stem(height*.88),i*math.tau/3+shape*.6,3.8,pitch=.3)
    if not lod and stage>=2:
        for fraction,length in ((.42,3.6),):
            for i in range(3):mesh.fan(stem(height*fraction),i*math.tau/3+shape*.8+fraction, length, pitch=.65)
    if stage==1 and not lod:
        for i in range(2):mesh.fan(stem(height*.91),i*math.pi+shape*.6,2.6,pitch=.65,young=True)
    if stage>=2:
        count=(5,9,13)[load]
        sites=[(*stem(height-.3),1.13)]
        for i in range(12):
            tier=i%3
            angle=(i//3)*math.pi/2+tier*.95+shape*.5
            fraction=(.25,.48,.70)[tier]
            radius=(5.8,4.5,3.0)[tier]*wide
            root=stem(height*fraction)
            sites.append((root[0]+math.cos(angle)*radius,root[1]+.65,
                          root[2]+math.sin(angle)*radius,rng.uniform(.81,.95)))
        for i,(x,y,z,size) in enumerate(sites[:count]):
            if lod and i>=(3,5,7)[load]:continue
            size*=.48 if stage==2 else 1
            if not lod:mesh.tube(stem(y*.82),(x,y,z),.12,sides=4)
            if i and i<=4 and not lod:
                mesh.fan((x,y-.12,z),math.atan2(z,x),size*2.7,pitch=.16,material="leaf_old")
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
        ("leaf_lod", "leaf_fan", 3, (1,1,1)),
        ("leaf", "leaf_surface", 3, (1, 1, 1)),
        ("leaf_shade", "leaf_surface", 3, (.78, .86, .74)),
        ("leaf_old", "leaf_surface", 3, (.90, .99, .82)),
        ("leaf_old_shade", "leaf_surface", 3, (.72, .84, .60)),
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
