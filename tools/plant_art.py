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

    def tube(self, start, end, radius=.13, material="stem", sides=5, end_radius=None):
        direction = unit(add(end, mul(start, -1)))
        side = unit(cross(direction, (0, 0, 1)))
        across = unit(cross(direction, side))
        rings = []
        for center, taper in ((start, 1), (end, .65 if end_radius is None else end_radius/radius)):
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

    def blade(self, base, angle, length, pitch=.15, roll=0, curl=.06,
              material="leaf_blade"):
        """One textured finger with a real midrib fold and an arched centerline."""
        from botanical_leaf import profile
        data=profile();rx,ry=data['root'];scale=length/data['length']
        forward=(math.cos(angle)*math.cos(pitch),math.sin(pitch),math.sin(angle)*math.cos(pitch))
        side=(-math.sin(angle),0,math.cos(angle));normal=unit(cross(side,forward))
        side,normal=add(mul(side,math.cos(roll)),mul(normal,math.sin(roll))),add(mul(normal,math.cos(roll)),mul(side,-math.sin(roll)))
        def point(p):
            x=(p[0]-rx)*scale*.83;t=(ry-p[1])/data['length']
            bend=length*(.07*math.sin(math.pi*t)-curl*t*t)-abs(x)*.18
            return add(base,add(mul(side,x),add(mul(forward,t*length),mul(normal,bend))))
        for polygon,uv in data['pieces']:
            vertices=[point(p) for p in polygon]
            n=unit(cross(add(vertices[1],mul(vertices[0],-1)),add(vertices[2],mul(vertices[0],-1))))
            if sum(a*b for a,b in zip(n,normal))<0:
                vertices.reverse();uv=list(reversed(uv))
            self.face(material,vertices,uv=uv)
            self.face(material+'_back',list(reversed(vertices)),uv=list(reversed(uv)))

    def fan(self, base, angle, length, pitch=.12, roll=0, curl=.06, variation=0):
        """Seven individually posed fingers, rather than one rigid leaf emblem."""
        rng=random.Random(3407+variation*397)
        for degrees,ratio in ((-76,.39),(-51,.66),(-25,.88),(0,1),(26,.87),(53,.64),(78,.37)):
            self.blade(base,angle+math.radians(degrees)+rng.uniform(-.035,.035),
                       length*ratio*rng.uniform(.95,1.05),pitch+rng.uniform(-.20,.32),
                       roll+rng.uniform(-.58,.58),curl+rng.uniform(-.045,.045))

    def leaflet(self, base, angle, length, pitch=.3, roll=0):
        self.blade(base,angle,length,pitch,roll,curl=.03,material='sugar_leaf')

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
        # Eight-face tapered flower silhouette, rather than a rectangular block.
        # The tiny open root is buried in its stem; detail stays below 100 faces.
        lower=[(x+a*.22*size,y,z+b*.22*size) for a,b in ((-1,-1),(-1,1),(1,1),(1,-1))]
        middle=[(x+a*size,y+.95*size,z+b*size) for a,b in ((-1,-1),(-1,1),(1,1),(1,-1))]
        tip=(x+.08*size,y+2.6*size,z-.10*size)
        for i in range(4):
            j=(i+1)%4
            mesh.face('bud',[lower[i],lower[j],middle[j],middle[i]])
            mesh.face('bud_light',[middle[j],tip,middle[i]])
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
            world=[(x+px*size,y+py*size,z+pz*size) for px,py,pz in vertices]
            puffed=direction[1]>=0 and (a*37+layer*17+b*23+direction[0]*11+direction[2]*7)%6==0
            if puffed:
                # A restrained raised bract crown and four sloping shoulders add
                # volume to the existing egg silhouette without changing its mass.
                center=tuple(sum(v[i] for v in world)/4 for i in range(3))
                raised=[add(center,add(mul(add(v,mul(center,-1)),.74),mul(normals[0],.055*size))) for v in world]
                mesh.face(material,raised,normals,uv)
                for j in range(4):mesh.face('bud',[world[j],world[(j+1)%4],raised[(j+1)%4],raised[j]])
            else:mesh.face(material,world,normals,uv)
            if direction[1]>0:shoulders.append((a*cell,(layer+1)*cell+(.055 if puffed else 0),b*cell))
    # Paired, curved pistils grow from exposed bract shoulders. Crossed fine
    # ribbons read as short hairs instead of the previous five square post caps.
    shoulders.sort(key=lambda p:(p[1],p[0],p[2]))
    outer=[p for p in shoulders if math.hypot(p[0],p[2])>.65]
    for i in range(8):
        heading=phase+i*2.39996;level=.8+(i%3)*.65
        px,py,pz=max(outer,key=lambda p:p[0]*math.cos(heading)+p[2]*math.sin(heading)-abs(p[1]-level)*.75)
        for strand in range(2):
            angle=phase+i*2.39+strand*.8
            start=(x+(px+(strand-.5)*.055)*size,y+py*size,z+pz*size)
            points=[add(start,(math.cos(angle)*distance*size,up*size,math.sin(angle)*distance*size))
                    for distance,up in ((0,0),(.10,.18),(.26,.30),(.34,.24))]
            for j,(first,last) in enumerate(zip(points,points[1:])):
                width=(.032-j*.008)*size
                for across in ((width,0,0),(0,0,width)):
                    vertices=[add(first,mul(across,-1)),add(last,mul(across,-.55)),add(last,mul(across,.55)),add(first,across)]
                    mesh.face('hair',vertices)
                    mesh.face('hair',list(reversed(vertices)))
    # Small sugar leaves break up the lower and middle flower silhouette; the
    # established voxel-egg bract volume stays intact underneath these details.
    for i in range(4):
        angle=phase+i*2.4
        level=(.55,1.25,1.8,2.25)[i]*size
        base=(x+math.cos(angle)*.65*size,y+level,z+math.sin(angle)*.65*size)
        mesh.leaflet(base,angle,(1.35 if i<2 else .95)*size,.35+i*.06,roll=(i-1.5)*.2)
    # A few non-emissive resin points catch normal light; no sparkling aura.
    for i in range(7):
        px,py,pz=shoulders[round((len(shoulders)-1)*(i+.6)/8)]
        center=(x+px*size,y+py*size+.008*size,z+pz*size);r=.045*size
        corners=[add(center,offset) for offset in ((-r,0,0),(0,0,r),(r,0,0),(0,0,-r))]
        tip=add(center,(0,r,0))
        for j in range(4):mesh.face('resin',[corners[j],tip,corners[(j+1)%4]])


# Four deliberately asymmetric branch gestures. Tuples are attachment height,
# heading, reach, tip height, bend. No repeated radial tiers or crown rosette.
BRANCH_LAYOUTS=(
    ((1.1,2.95,2.8,5.4,.18),(1.9,.48,2.5,6.7,-.20),(3.3,-1.22,2.0,7.8,.16),(2.3,-2.18,2.7,6.1,-.18)),
    ((1.5,-2.72,2.5,6.2,-.17),(1.0,.25,2.9,5.5,.18),(3.1,1.87,2.0,7.9,-.20),(2.0,-.94,2.6,6.5,.14)),
    ((1.0,2.44,2.9,5.3,.18),(2.8,-.13,2.2,7.7,-.20),(2.0,-1.65,2.7,6.4,.16),(1.6,.95,2.6,5.9,-.15)),
    ((1.7,-2.93,2.5,6.2,.18),(1.0,.80,2.9,5.3,-.17),(3.0,-.78,2.0,7.8,.14),(2.4,2.03,2.3,6.7,-.16)),
)


def plant(stage, shape, load=1, lod=False):
    mesh=Mesh()
    if stage==0:
        mesh.tube((0,0,0),(.13,1.9,-.08),.10,sides=4)
        for i in range(2):mesh.cotyledon((.13,1.9,-.08),i*math.pi+shape*.3)
        return mesh
    if stage==1:
        joints=((0,0,0),(.1,1.7,-.1),(-.15,3.2,.15),(.2,4.7,.12))
        for i,(a,b) in enumerate(zip(joints,joints[1:])):mesh.tube(a,b,.14-i*.025,sides=4,end_radius=.115-i*.025)
        for i,(y,angle,length,pitch,roll) in enumerate(((1.5,.4,3.2,.12,.14),(2.4,3.4,3.0,.22,-.18),(3.9,-1.35,2.4,.40,.16))):
            root=(0,y,0);tip=add(root,(math.cos(angle)*.9,.3,math.sin(angle)*.9))
            if not lod:mesh.tube(root,tip,.055,sides=4)
            if lod:mesh.card(tip,angle,length,length*1.1,pitch,material='leaf_lod',simple=True)
            else:mesh.fan(tip,angle,length,pitch,roll=roll,variation=shape*31+i)
        return mesh
    scale=.86 if stage==2 else 1
    lean=((.55,.1),(-.55,.45),(.6,-.45),(-.4,-.5))[shape]
    height=(9.5,9.9,9.2,9.6)[shape]
    anchors=[(0,0,0)]+[(lean[0]*(y/height)+.18*math.sin(y*.8+shape),y,
                         lean[1]*(y/height)+.16*math.sin(y*.61)) for y in (2.8,6.1,height)]
    def main(y):
        for a,b in zip(anchors,anchors[1:]):
            if y<=b[1]:return add(a,mul(add(b,mul(a,-1)),(y-a[1])/(b[1]-a[1])))
        return anchors[-1]
    def scaled(p):return mul(p,scale)
    joints=anchors
    for i,(a,b) in enumerate(zip(joints,joints[1:])):
        mesh.tube(scaled(a),scaled(b),(.20-i*.045)*scale,sides=4,end_radius=(.155-i*.045)*scale)
    branches=[]
    for i,(at,angle,reach,top,bend) in enumerate(BRANCH_LAYOUTS[shape]):
        root=main(at)
        mid=add(root,(math.cos(angle+bend)*reach*.62,(top-at)*.42,math.sin(angle+bend)*reach*.62))
        outer=add(root,(math.cos(angle)*reach,(top-at)*.78,math.sin(angle)*reach))
        tip=(outer[0]+math.cos(angle-bend)*.22,top,outer[2]+math.sin(angle-bend)*.22)
        if lod:mesh.tube(scaled(root),scaled(tip),.12*scale,sides=4)
        else:
            for a,b,r,R in ((root,mid,.135,.105),(mid,outer,.105,.07),(outer,tip,.07,.04)):
                mesh.tube(scaled(a),scaled(b),r*scale,sides=5,end_radius=R*scale)
        branches.append((root,mid,outer,tip,angle))
        # Three overlapping leaves per short branch. Different attachment
        # heights and finger bends keep the canopy continuous without shelves.
        poses=((mid,angle-.36,5.2-(i%2)*.2,.09+(i%3)*.06,(-.14,.18,.24,-.18)[i]),
               (outer,angle+.42,4.2+(i%2)*.2,.16+(i%2)*.07,(.16,-.20,.10,.18)[i]),
               (tip,angle-.65,3.3,.25+(i%2)*.10,(-.13,.12,-.18,.15)[i]))
        for k,(node,yaw,length,pitch,roll) in enumerate(poses):
            if lod and k:continue
            petiole=add(node,(math.cos(yaw)*.35,.10,math.sin(yaw)*.35))
            if not lod:mesh.tube(scaled(node),scaled(petiole),.045*scale,sides=4)
            if lod:mesh.card(scaled(petiole),yaw,length*scale,length*1.1*scale,pitch,material='leaf_lod',simple=True)
            else:mesh.fan(scaled(petiole),yaw,length*scale,pitch,roll=roll,variation=shape*101+i*7+k)
    # Alternating small internodes fill the middle and hide most of the stem.
    # Leaf sizes taper gradually; no node carries a symmetric radial ring.
    stem_leaves=((1.6,.4,5.1,.09,.10),(2.5,2.9,4.9,.15,-.10),
                 (3.4,4.9,4.6,.20,.20),(4.3,1.8,4.4,.18,-.14),
                 (5.2,3.8,4.1,.24,.14),(6.25,.5,3.8,.32,-.12),
                 (7.35,2.8,3.3,.38,.17),(8.4,4.7,3.1,.43,-.10),
                 (height-.15,.85,2.9,.48,.12),(height-.35,3.65,2.7,.30,-.12))
    for i,(y,angle,length,pitch,roll) in enumerate(stem_leaves):
        if lod and i not in (1,4,7):continue
        angle+=shape*.37
        root=main(min(y,height));petiole=add(root,(math.cos(angle)*.32,.12,math.sin(angle)*.32))
        if not lod:mesh.tube(scaled(root),scaled(petiole),.04*scale,sides=4)
        if lod:mesh.card(scaled(petiole),angle,length*scale,length*1.1*scale,pitch,material='leaf_lod',simple=True)
        else:mesh.fan(scaled(petiole),angle,length*scale,pitch,roll=roll,variation=shape*101+i*13+37)
    if stage==3:
        sites=[(main(height-.28),.78,0)]
        for root,mid,outer,tip,angle in branches:sites.append((tip,.60+(.06 if tip[1]>6 else 0),angle))
        for i,(_,mid,outer,_,angle) in enumerate(branches):
            node=add(mid,mul(add(outer,mul(mid,-1)),.25))
            spur=add(node,(math.cos(angle+1)*.55,.30,math.sin(angle+1)*.55))
            sites.append((spur,.49+(i%2)*.04,angle+.35))
        for i,(root,mid,_,_,angle) in enumerate(branches):
            node=add(root,mul(add(mid,mul(root,-1)),.58))
            spur=add(node,(math.cos(angle-1)*.45,.30,math.sin(angle-1)*.45))
            sites.append((spur,.39+(i%2)*.04,angle-.4))
        count=(5,9,13)[load]
        for i,(center,size,angle) in enumerate(sites[:count]):
            if lod and i>=(3,5,7)[load]:continue
            if not lod and i>=5:
                branch=branches[(i-5)%4]
                origin=branch[1] if i<9 else add(branch[0],mul(add(branch[1],mul(branch[0],-1)),.58))
                mesh.tube(origin,center,.055,sides=4)
            first=len(mesh.faces);flower(mesh,center,size,shape+i*.7,lod)
            # Preserve the bract volume; tilt side flowers with their branch.
            if i and not lod:
                x,y,z=center;tilt=.13+(i%3)*.06
                def rotate(v,normal=False):
                    dx,dy,dz=v if normal else (v[0]-x,v[1]-y,v[2]-z)
                    radial=dx*math.cos(angle)+dz*math.sin(angle)
                    along=-radial*math.sin(tilt)+dy*math.cos(tilt)
                    out=radial*math.cos(tilt)+dy*math.sin(tilt)-radial
                    result=(dx+out*math.cos(angle),along,dz+out*math.sin(angle))
                    return result if normal else (x+result[0],y+result[1],z+result[2])
                for face in range(first,len(mesh.faces)):
                    mat,vertices,normals,uv=mesh.faces[face]
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
        ("leaf", "plant_leaf", 3, (1, 1, 1)),
        ("leaf_shade", "plant_leaf", 3, (.76, .91, .67)),
        ("bud", "plant_bud", 1, (1, 1, 1)),
        ("bud_dark", "plant_bud", 1, (.52, .47, .65)),
        ("bud_light", "plant_bud", 4, (1, 1, 1)),
        ("hair", "plant_pistil", 2, (1, 1, 1)),
        ("resin", "plant_pistil", -1, (.82, .92, .78)),
    ]:
        materials += [f"newmtl {name}", "Kd " + " ".join(map(str, color)),
                      f"map_Kd stonedew:block/{texture}", f"neoforge_TintIndex {tint}", ""]
    for name,color in (("leaf_blade",(1,1,1)),("leaf_blade_back",(.88,.95,.82)),
                       ("sugar_leaf",(1,1,1)),("sugar_leaf_back",(.88,.95,.82))):
        materials += [f'newmtl {name}','Kd '+' '.join(map(str,color)),
                      'map_Kd stonedew:block/botanical/leaflet_v8','neoforge_TintIndex 3','']
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
