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
              material="leaf_blade", simple=False):
        """One textured finger with a real midrib fold and an arched centerline."""
        from botanical_leaf import profile
        data=profile();rx,ry=data['root'];scale=length/data['length']
        forward=(math.cos(angle)*math.cos(pitch),math.sin(pitch),math.sin(angle)*math.cos(pitch))
        side=(-math.sin(angle),0,math.cos(angle));normal=unit(cross(side,forward))
        side,normal=add(mul(side,math.cos(roll)),mul(normal,math.sin(roll))),add(mul(normal,math.cos(roll)),mul(side,-math.sin(roll)))
        def point(p):
            x=(p[0]-rx)*scale*1.38;t=(ry-p[1])/data['length']
            bend=length*(.07*math.sin(math.pi*t)-curl*t*t)-abs(x)*.18
            return add(base,add(mul(side,x),add(mul(forward,t*length),mul(normal,bend))))
        pieces=data['pieces']
        if simple:
            left,top,right,bottom=data['bounds'];wx,wy,ww,wh=data['window']
            polygon=[(left,bottom),(left,top),(right,top),(right,bottom)]
            pieces=[(polygon,[((x-wx)/ww,(y-wy)/wh) for x,y in polygon])]
        for polygon,uv in pieces:
            vertices=[point(p) for p in polygon]
            n=unit(cross(add(vertices[1],mul(vertices[0],-1)),add(vertices[2],mul(vertices[0],-1))))
            if sum(a*b for a,b in zip(n,normal))<0:
                vertices.reverse();uv=list(reversed(uv))
            # Stylized foliage normals turn both sides toward the canopy sky.
            # The underside still has its own lateral direction and paint tint;
            # it no longer becomes almost black under vanilla entity lighting.
            front=unit(add(mul(n,.65),(0,.45,0)))
            back=unit((-n[0]*.35,.80,-n[2]*.35))
            self.face(material,vertices,normals=[front]*len(vertices),uv=uv)
            self.face(material+'_back',list(reversed(vertices)),normals=[back]*len(vertices),uv=list(reversed(uv)))

    def fan(self, base, angle, length, pitch=.12, roll=0, curl=.06, variation=0, simple=False):
        """A recognizable FIVE-finger fan, lightly folded, eight faces total."""
        self.blade(base,angle,length,pitch,roll,curl,simple=simple)

    def leaflet(self, base, angle, length, pitch=.3, roll=0):
        # Small pointed sugar leaves are solid silhouettes, not full fan cards.
        forward=(math.cos(angle)*math.cos(pitch),math.sin(pitch),math.sin(angle)*math.cos(pitch))
        side=(-math.sin(angle),0,math.cos(angle))
        tip=add(base,mul(forward,length));middle=add(base,mul(forward,length*.45))
        vertices=[base,add(middle,mul(side,length*.16)),tip,add(middle,mul(side,-length*.16))]
        self.face('sugar_leaf',vertices)
        self.face('sugar_leaf_back',list(reversed(vertices)))

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
    """Stepped egg bracts with merged surfaces, small sugar leaves and raised pistils."""
    x,y,z=center
    if lod:
        lower=[(x+a*.22*size,y,z+b*.22*size) for a,b in ((-1,-1),(-1,1),(1,1),(1,-1))]
        middle=[(x+a*size,y+.95*size,z+b*size) for a,b in ((-1,-1),(-1,1),(1,1),(1,-1))]
        tip=(x+.08*size,y+2.8*size,z-.10*size)
        for i in range(4):
            j=(i+1)%4
            mesh.face('bud',[lower[i],lower[j],middle[j],middle[i]])
            mesh.face('bud_light',[middle[j],tip,middle[i]])
        return
    rng=random.Random(round(phase*1000)+441)
    cell=.38
    occupied=set()
    for layer,radius in enumerate((2.3,3.05,3.22,3.04,2.72,2.26,1.72,1.02)):
        for a in range(-3,4):
            for b in range(-3,4):
                if math.hypot(a,b)<radius+rng.uniform(-.18,.18):occupied.add((a,layer,b))
    shoulders=[]
    # Merge coplanar exposed voxel bracts into rectangles. The established egg
    # contour survives; internal / repeated coplanar faces do not reach the GPU.
    for axis in range(3):
        u,v=[a for a in range(3) if a!=axis]
        for sign in (-1,1):
            planes={}
            for point in occupied:
                neighbor=list(point);neighbor[axis]+=sign
                if tuple(neighbor) in occupied:continue
                planes.setdefault(point[axis],set()).add((point[u],point[v]))
                if axis==1 and sign>0:shoulders.append((point[0]*cell,(point[1]+1)*cell,point[2]*cell))
            for plane,mask in sorted(planes.items()):
                while mask:
                    a,b=min(mask);w=1
                    while (a+w,b) in mask:w+=1
                    h=1
                    while all((n,b+h) in mask for n in range(a,a+w)):h+=1
                    mask.difference_update((n,m) for n in range(a,a+w) for m in range(b,b+h))
                    vertices=[]
                    for du,dv in ((0,0),(1,0),(1,1),(0,1)):
                        p=[0,0,0];p[axis]=(plane+(.5*sign if axis!=1 else (1 if sign>0 else 0)))*cell
                        p[u]=(a-.5*(u!=1)+du*w)*cell
                        p[v]=(b-.5*(v!=1)+dv*h)*cell
                        vertices.append(add(center,mul(p,size)))
                    normal=[0,0,0];normal[axis]=sign
                    n=unit(cross(add(vertices[1],mul(vertices[0],-1)),add(vertices[2],mul(vertices[0],-1))))
                    if sum(n[i]*normal[i] for i in range(3))<0:vertices.reverse()
                    material='bud_light' if axis==1 and sign>0 else 'bud_dark' if axis==1 else 'bud'
                    mesh.face(material,vertices)
    outer=[p for p in shoulders if math.hypot(p[0],p[2])>.65]
    for i in range(4):
        angle=phase+i*2.39996
        p=max(outer,key=lambda p:p[0]*math.cos(angle)+p[2]*math.sin(angle)-abs(p[1]-(1+i*.35))*.7)
        start=add(center,mul(p,size));outward=(math.cos(angle),0,math.sin(angle));across=(-math.sin(angle),0,math.cos(angle))
        middle=add(start,add(mul(outward,.09*size),(0,.21*size,0)))
        end=add(middle,add(mul(outward,.14*size),(0,.08*size,0)))
        for first,last in ((start,middle),(middle,end)):
            side=mul(across,.028*size)
            vertices=[add(first,mul(side,-1)),add(last,mul(side,-.6)),add(last,mul(side,.6)),add(first,side)]
            mesh.face('hair',vertices);mesh.face('hair',list(reversed(vertices)))
        if i<3:
            sparkle=add(start,(0,.012*size,0));r=.06*size
            mesh.face('resin',[add(sparkle,(-r,0,0)),add(sparkle,(0,r,0)),add(sparkle,(r,0,0))])
    for i in range(3):
        angle=phase+i*2.4
        mesh.leaflet((x+math.cos(angle)*.6*size,y+(.5+i*.48)*size,z+math.sin(angle)*.6*size),angle,.9*size,.25)


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
            if lod:mesh.fan(tip,angle,length,pitch,simple=True)
            else:mesh.fan(tip,angle,length,pitch,roll=roll,variation=shape*31+i)
        return mesh
    scale=.86 if stage==2 else 1
    lean=((.55,.1),(-.55,.45),(.6,-.45),(-.4,-.5))[shape]
    height=(12.8,13.3,12.5,13.0)[shape]
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
        at*=1.30;reach*=1.35;top*=1.30
        root=main(at)
        mid=add(root,(math.cos(angle+bend)*reach*.62,(top-at)*.42,math.sin(angle+bend)*reach*.62))
        outer=add(root,(math.cos(angle)*reach,(top-at)*.78,math.sin(angle)*reach))
        tip=(outer[0]+math.cos(angle-bend)*.22,top,outer[2]+math.sin(angle-bend)*.22)
        if lod:mesh.tube(scaled(root),scaled(tip),.12*scale,sides=4)
        else:
            for a,b,r,R in ((root,mid,.135,.105),(mid,outer,.105,.07),(outer,tip,.07,.04)):
                mesh.tube(scaled(a),scaled(b),r*scale,sides=5,end_radius=R*scale)
        branches.append((root,mid,outer,tip,angle))
        # Three staggered fans on each branch: enough open space to read the
        # five fingers and each smaller flower from normal play distance.
        poses=((mid,angle-.48,6.2-(i%2)*.3,-.25-(i%3)*.08,(-.28,.40,.24,-.36)[i]),
               (outer,angle+.72,5.0+(i%2)*.2,-.36+(i%2)*.16,(.38,-.34,.32,-.28)[i]),
               (tip,angle-.55,4.1,.22+(i%2)*.15,(-.35,.28,-.30,.36)[i]))
        for k,(node,yaw,length,pitch,roll) in enumerate(poses):
            if lod and k==1:continue
            petiole=add(node,(math.cos(yaw)*.35,.10,math.sin(yaw)*.35))
            if not lod:mesh.tube(scaled(node),scaled(petiole),.045*scale,sides=4)
            if lod:mesh.fan(scaled(petiole),yaw,length*scale,pitch,roll=roll,simple=True)
            else:mesh.fan(scaled(petiole),yaw,length*scale,pitch,roll=roll,variation=shape*101+i*7+k)
    # Alternating internodes avoid symmetric shelves or a crown of flat cards.
    stem_leaves=((2.0,.4,6.3,-.30,.32),(3.9,3.0,6.0,-.24,-.35),
                 (6.1,4.9,5.3,-.20,.42),(8.3,1.8,4.7,-.08,-.35),
                 (9.5,5.7,4.5,-.28,-.36),(10.4,3.8,4.0,.16,.30),
                 (11.7,2.1,3.8,-.25,.32),(height-.2,.6,3.3,.30,-.28))
    for i,(y,angle,length,pitch,roll) in enumerate(stem_leaves):
        if lod and i not in (1,3,7):continue
        angle+=shape*.37
        root=main(min(y,height));petiole=add(root,(math.cos(angle)*.32,.12,math.sin(angle)*.32))
        if not lod:mesh.tube(scaled(root),scaled(petiole),.04*scale,sides=4)
        if lod:mesh.fan(scaled(petiole),angle,length*scale,pitch,roll=roll,simple=True)
        else:mesh.fan(scaled(petiole),angle,length*scale,pitch,roll=roll,variation=shape*101+i*13+37)
    if stage==3:
        sites=[(main(height-.28),.65,0)]
        for root,mid,outer,tip,angle in branches:sites.append((tip,.46+(.04 if tip[1]>9 else 0),angle))
        for i,(_,mid,outer,_,angle) in enumerate(branches):
            node=add(mid,mul(add(outer,mul(mid,-1)),.25))
            spur=add(node,(math.cos(angle+1)*.55,.30,math.sin(angle+1)*.55))
            sites.append((spur,.32+(i%2)*.03,angle+.35))
        for i,(root,mid,_,_,angle) in enumerate(branches):
            node=add(root,mul(add(mid,mul(root,-1)),.58))
            spur=add(node,(math.cos(angle-1)*.45,.30,math.sin(angle-1)*.45))
            sites.append((spur,.27+(i%2)*.03,angle-.4))
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
        ("bud_dark", "plant_bud", 1, (.72, .76, .65)),
        ("bud_light", "plant_bud", 4, (1, 1, 1)),
        ("hair", "plant_pistil", 2, (1, 1, 1)),
        ("resin", "plant_pistil", -1, (.82, .92, .78)),
    ]:
        materials += [f"newmtl {name}", "Kd " + " ".join(map(str, color)),
                      ("map_Kd stonedew:block/botanical/bud" if name.startswith("bud") else "map_Kd stonedew:block/botanical/stem" if name=="stem" else f"map_Kd stonedew:block/{texture}"), f"neoforge_TintIndex {tint}", ""]
    for name,color in (("leaf_blade",(1,1,1)),("leaf_blade_back",(.96,1,.94)),
                       ("sugar_leaf",(.55,.80,.28)),("sugar_leaf_back",(.39,.63,.20))):
        materials += [f'newmtl {name}','Kd '+' '.join(map(str,color)),
                      ('map_Kd stonedew:block/botanical/sugar' if name.startswith('sugar') else 'map_Kd stonedew:block/botanical/fan_v9'),'neoforge_TintIndex 3','']
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
