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
        """Flat palmate fans with deliberately stepped, square-ended silhouettes.

        The leaflet outline is authored on a small grid, like the reference's cut
        paper foliage. There is no smooth sine taper or sagging needle tip. Each
        half is almost planar; its very shallow fold keeps the midrib readable.
        """
        forward=(math.cos(angle),0,math.sin(angle))
        across=(-math.sin(angle),0,math.cos(angle))
        profile=(1,1,2,2,3,2,3,3,4,3,4,3,4,3,4,3,3,2,3,2,2,1,1,1)
        for finger,(degrees,ratio) in enumerate(((-78,.36),(-53,.62),(-27,.86),(0,1),(27,.86),(53,.62),(78,.36))):
            theta=math.radians(degrees); reach=length*ratio
            rows=max(8,round(24*ratio))
            half=reach*(.14 if young else .18)
            def point(along,side):
                x=math.sin(theta)*along+math.cos(theta)*side
                z=math.cos(theta)*along-math.sin(theta)*side
                return add(base,add(mul(across,x),add(mul(forward,z*math.cos(pitch)),
                    (0,z*math.sin(pitch)-abs(side)*.11,0))))
            spans=[]
            for row in range(rows):
                width=half*profile[min(23,int((row+.5)*24/rows))]/4
                if spans and spans[-1][2]==width:spans[-1]=(spans[-1][0],row+1,width)
                else:spans.append((row,row+1,width))
            for first,last,width in spans:
                start=reach*first/rows;end=reach*last/rows
                for side in range(2):
                    edge=width*(-1 if side else 1)
                    vertices=[point(start,0),point(end,0),point(end,edge),point(start,edge)]
                    if side:vertices.reverse()
                    mat=material+('_shade' if side else '')
                    uv=[(0,first/rows),(0,last/rows),(width/half,last/rows),(width/half,first/rows)]
                    if side:uv.reverse()
                    self.face(mat,vertices,uv=uv)
                    self.face(mat,list(reversed(vertices)),uv=list(reversed(uv)))

    def cotyledon(self, base, angle):
        forward=(math.cos(angle),0,math.sin(angle));side=(-math.sin(angle),0,math.cos(angle))
        profile=(.15,.40,.60,.60,.45,.25,.12)
        for i,width in enumerate(profile):
            a=i/len(profile);b=(i+1)/len(profile)
            for j in (-1,1):
                def point(t,w):return add(base,add(mul(forward,1.8*t),add(mul(side,w),(0,.5*t-abs(w)*.08,0))))
                vertices=[point(a,0),point(b,0),point(b,width*j),point(a,width*j)]
                mat='leaf' if j<0 else 'leaf_shade'
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
    """A compact stepped cluster: blocky bracts, recessed seams and lit shoulders."""
    x,y,z=center
    if lod:
        mesh.block((x-size,y,z-size),(x+size,y+size*2.6,z+size),"bud")
        return
    rng=random.Random(round(phase*1000)+441)
    # An irregular solid egg made of small voxel bracts. Only exposed faces are
    # emitted; there is no stack of large boxes or repeated cylindrical rings.
    cell=.38
    radii=(2.3,3.05,3.22,3.04,2.72,2.26,1.72,1.02)
    occupied=set()
    for layer,radius in enumerate(radii):
        for a in range(-3,4):
            for b in range(-3,4):
                if math.hypot(a,b)<radius+rng.uniform(-.18,.18):occupied.add((a,layer,b))
    directions=((0,-1,0),(0,1,0),(0,0,-1),(0,0,1),(-1,0,0),(1,0,0))
    shoulders=[]
    for a,layer,b in sorted(occupied):
        lo=((a-.5)*cell,layer*cell,(b-.5)*cell)
        hi=((a+.5)*cell,(layer+1)*cell,(b+.5)*cell)
        part=Mesh();part.block(lo,hi)
        roll=rng.random()
        side_material='bud_dark' if roll<.12 else 'bud_light' if roll>.84 else 'bud'
        for direction,(_,vertices,normals,uv) in zip(directions,part.faces):
            if (a+direction[0],layer+direction[1],b+direction[2]) in occupied:continue
            material='bud_light' if direction[1]>0 else 'bud_dark' if direction[1]<0 else side_material
            mesh.face(material,[(x+px*size,y+py*size,z+pz*size) for px,py,pz in vertices],normals,uv)
            if direction[1]>0:shoulders.append((a*cell,(layer+1)*cell,b*cell))
    # Five short colored pistil clusters sit on exposed upper bract shoulders.
    shoulders.sort(key=lambda p:(p[1],p[0],p[2]))
    for index in (0,len(shoulders)//4,len(shoulders)//2,3*len(shoulders)//4,len(shoulders)-1):
        px,py,pz=shoulders[index];cx=x+px*size;cz=z+pz*size;cy=y+py*size
        mesh.block((cx-.105*size,cy,cz-.105*size),(cx+.105*size,cy+.15*size,cz+.105*size),'hair')


def plant(stage, shape, load=1, lod=False):
    mesh=Mesh();rng=random.Random(7701+shape*391)
    height=(2.6,7.6,12.1,13.0)[stage]*(1,.97,1.04,.98)[shape]
    wide=(1,1.06,.92,1.03)[shape]
    lean=((.1,.1),(.7,-.4),(-.5,.5),(.5,.6))[shape]
    def stem(y):return(lean[0]*y/height,y,lean[1]*y/height)
    mesh.tube((0,0,0),stem(height if stage else 1.8),(.30 if stage>=2 else .18) if stage else .10,sides=4)
    if stage==0:
        for i in range(2):mesh.cotyledon(stem(1.8),i*math.pi+shape*.3)
        return mesh
    tiers=(.18,.51,.79) if stage==1 else (.13,.31,.49,.67,.85)
    if lod:tiers=(.16,.49,.80)
    for tier,fraction in enumerate(tiers):
        y=height*fraction
        count=3 if lod or stage>=2 else 2
        phase=shape*.49+tier*math.pi*.27
        for i in range(count):
            angle=i*math.tau/count+phase+rng.uniform(-.10,.10)
            length=(9.4-4.7*fraction)*wide*rng.uniform(.94,1.06)
            if stage==1:length*=.70
            base=stem(y)
            petiole=length*.19
            tip=add(base,(math.cos(angle)*petiole,.16,math.sin(angle)*petiole))
            if not lod:mesh.tube(base,tip,.08,sides=4)
            if lod:
                mesh.card(tip,angle,length,width=length*1.32,pitch=.12,simple=True,material="leaf_lod")
            else:
                mesh.fan(tip,angle,length*.81,pitch=rng.uniform(-.26,.30)+fraction*.08,material="leaf_old" if fraction<.4 else "leaf",young=stage==1)
    if stage>=2 and not lod:
        for i in range(3):
            mesh.fan(stem(height-.10),i*math.tau/3+shape*.6,5.0,pitch=.18)
        # Secondary branch fans occupy the spaces between the main whorls. Their
        # different inclinations make a full cone rather than flat separated shelves.
        for tier,(fraction,length,pitch) in enumerate(((.23,4.6,-.33),(.42,4.0,.45),(.62,3.2,-.30),(.80,2.8,.35))):
            for i in range(2):
                angle=shape*.49+tier*1.04+i*math.pi+.5
                root=stem(height*fraction)
                base=add(root,(math.cos(angle)*1.7,.1,math.sin(angle)*1.7))
                mesh.tube(root,base,.09,sides=4)
                mesh.fan(base,angle,length*wide,pitch=pitch,material='leaf_old' if tier==0 else 'leaf')
        # Upright interior fans fill the trunk gap without enlarging the outline.
        for i,(fraction,length) in enumerate(((.35,5.0),(.57,4.5),(.77,3.5))):
            mesh.fan(stem(height*fraction),shape*.6+i*2.1,length,pitch=.95,material='leaf_old')
    if stage==1 and not lod:
        for i in range(2):mesh.fan(stem(height*.91),i*math.pi+shape*.6,2.6,pitch=.65,young=True)
    if stage==3:
        count=(5,9,13)[load]
        sites=[(*stem(height-.3),1.13)]
        for i in range(12):
            tier=i//4
            angle=(i%4)*math.pi/2+tier*.78+shape*.5
            fraction=(.55,.33,.76)[tier]
            radius=(4.8,6.0,2.8)[tier]*wide
            root=stem(height*fraction)
            sites.append((root[0]+math.cos(angle)*radius,root[1]+.65,
                          root[2]+math.sin(angle)*radius,rng.uniform(.67,.83)))
        for i,(x,y,z,size) in enumerate(sites[:count]):
            if lod and i>=(3,5,7)[load]:continue
            if not lod:mesh.tube(stem(y*.82),(x,y,z),.12,sides=4)
            first=len(mesh.faces)
            flower(mesh,(x,y,z),size,shape+i*.7,lod)
            # Side colas lean out from their branch; the central leader remains upright.
            if i and not lod:
                tilt=.20;angle=math.atan2(z,x)
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


def soil_shadow(mesh, path):
    """Author a soft foliage silhouette from the mesh, on the soil's UV plane.

    This is original geometry rasterization, not processing any reference image.
    Union coverage prevents overlapping leaf faces from making opaque black blobs.
    """
    from stylized_textures import write_png
    size=128;covered=[bytearray(size) for _ in range(size)]
    for material,vertices,normals,_ in mesh.faces:
        if normals[0][1]<.05:continue
        polygon=[((x+y*.45/.82+12)*size/24,(z+y*.35/.82+12)*size/24) for x,y,z in vertices]
        for row in range(max(0,math.floor(min(v[1] for v in polygon))),min(size,math.ceil(max(v[1] for v in polygon)))):
            y=row+.5;cuts=[]
            for a,b in zip(polygon,polygon[1:]+polygon[:1]):
                if (a[1]<=y<b[1]) or (b[1]<=y<a[1]):
                    cuts.append(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]))
            cuts.sort()
            for left,right in zip(cuts[::2],cuts[1::2]):
                for col in range(max(0,math.ceil(left-.5)),min(size,math.ceil(right-.5))):covered[row][col]=1
    pixels=[]
    for y in range(64):
        row=[]
        for x in range(64):
            # Supersampled silhouette with a narrow, soft penumbra.
            weight=total=0
            for dy in range(-1,3):
                for dx in range(-1,3):
                    xx=x*2+dx;yy=y*2+dy;w=2 if dx in (0,1) and dy in (0,1) else 1
                    total+=w
                    if 0<=xx<size and 0<=yy<size:weight+=covered[yy][xx]*w
            row.append((14,17,10,round(185*weight/total)))
        pixels.append(row)
    write_png(path,pixels)


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
        ("leaf_shade", "leaf_surface", 3, (.76, .91, .67)),
        ("leaf_old", "leaf_surface", 3, (.81, .96, .69)),
        ("leaf_old_shade", "leaf_surface", 3, (.64, .80, .51)),
        ("bud", "plant_bud", 1, (1, 1, 1)),
        ("bud_dark", "plant_bud", 1, (.52, .47, .65)),
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
                    if not lod:soil_shadow(mesh,root/f'textures/effect/plant_shadow_{stage}_{shape}_{load}.png')
                    data={"credit":"Original Stonedew reference-led art; tools/plant_art.py",
                          "loader":"neoforge:obj", "model":f"stonedew:models/block/plants/{name}.obj",
                          "automatic_culling":False,"shade_quads":True,"emissive_ambient":False,
                          "textures":{"particle":"stonedew:block/plant_leaf"}}
                    (directory/f"{name}.json").write_text(json.dumps(data,indent=2)+"\n")
                    report.append(dict(stage=stage,shape=shape,budLoad=load,buds=(5,9,13)[load] if stage==3 else 0,
                                       lod=lod,faces=len(mesh.faces),vertices=sum(len(f[1]) for f in mesh.faces)))
    return report
