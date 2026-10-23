"""Reference-led grow equipment: tapered ceramics, reinforced timber, bolted UV steel.
Original authored geometry. References in CODEX_REFERENCE_NEW are preserved unchanged.
"""
import json
import math
from plant_art import Mesh, unit, cross, add, mul
from material_atlas import sprite

DISPLAY = {
    'gui': {'rotation': [25, 225, 0], 'translation': [0, 1, 0], 'scale': [.8]*3},
    'ground': {'translation': [0, 3, 0], 'scale': [.5]*3},
    'fixed': {'rotation': [0, 180, 0], 'scale': [.8]*3},
    'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 1.5, 0], 'scale': [.7]*3},
    'firstperson_lefthand': {'rotation': [0, -45, 0], 'translation': [0, 1.5, 0], 'scale': [.7]*3},
    'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [.5]*3}}

def fixture_bloom(mesh, vertices, radial=False):
    # Additive eyes blending ignores alpha: radiance falls to BLACK at the border.
    material='emission_aura' if radial else 'emission_halo'
    uv=[(0,0),(0,1),(1,1),(1,0)]
    mesh.face(material,vertices,uv=uv)
    mesh.face(material,list(reversed(vertices)),uv=list(reversed(uv)))


class Prop(Mesh):
    def face(self, material, vertices, normals=None, uv=None):
        # Minecraft sprites sit in an atlas: UVs outside [0,1] sample OTHER sprites.
        # Clip projected polygons into 16-unit material tiles before assigning local UVs.
        if uv is not None:
            super().face(material,[(x-8,y,z-8) for x,y,z in vertices],normals,uv)
            return
        normal=unit(cross(add(vertices[1],mul(vertices[0],-1)),add(vertices[2],mul(vertices[0],-1))))
        axis=max(range(3),key=lambda a:abs(normal[a]))
        axes=(0,2) if axis==1 else (2,1) if axis==0 else (0,1)
        polygon=[(*v,v[axes[0]]/16,1-v[axes[1]]/16) for v in vertices]
        def clip(poly,component,bound,greater):
            result=[]
            for start,end in zip(poly,poly[1:]+poly[:1]):
                a=start[component]-bound;b=end[component]-bound
                ina=a>=-1e-9 if greater else a<=1e-9
                inb=b>=-1e-9 if greater else b<=1e-9
                if ina:result.append(start)
                if ina!=inb:
                    t=a/(a-b)
                    result.append(tuple(x+(y-x)*t for x,y in zip(start,end)))
            clean=[]
            for point in result:
                if not clean or any(abs(a-b)>1e-8 for a,b in zip(point,clean[-1])):clean.append(point)
            if len(clean)>1 and all(abs(a-b)<1e-8 for a,b in zip(clean[0],clean[-1])):clean.pop()
            return clean
        for tu in range(math.floor(min(p[3] for p in polygon)+1e-8),math.ceil(max(p[3] for p in polygon)-1e-8)):
            for tv in range(math.floor(min(p[4] for p in polygon)+1e-8),math.ceil(max(p[4] for p in polygon)-1e-8)):
                part=polygon
                for component,bound,greater in ((3,tu,True),(3,tu+1,False),(4,tv,True),(4,tv+1,False)):
                    part=clip(part,component,bound,greater)
                    if len(part)<3:break
                if len(part)<3:continue
                parts=[part] if len(part)<=4 else [[part[0],part[i],part[i+1]] for i in range(1,len(part)-1)]
                for face in parts:
                    positions=[(x-8,y,z-8) for x,y,z,_,_ in face]
                    uvs=[(max(0,min(1,u-tu)),max(0,min(1,v-tv))) for _,_,_,u,v in face]
                    super().face(material,positions,[normal]*len(face),uvs)

    def beam(self, a, b, width, material='iron'):
        # Rectangular slanted member, e.g. carry handle / hose / suspension brace.
        dx,dy,dz=(b[i]-a[i] for i in range(3))
        length=math.sqrt(dx*dx+dy*dy+dz*dz)
        axis=(dx/length,dy/length,dz/length)
        helper=(0,0,1) if abs(axis[2])<.9 else (1,0,0)
        from plant_art import cross,unit,mul,add
        side=mul(unit(cross(axis,helper)),width/2)
        across=mul(unit(cross(axis,side)),width/2)
        rings=[[add(center,add(mul(side,s),mul(across,t))) for s,t in ((-1,-1),(1,-1),(1,1),(-1,1))] for center in (a,b)]
        self.face(material,list(reversed(rings[0])))
        self.face(material,rings[1])
        for i in range(4):
            j=(i+1)%4
            self.face(material,[rings[0][i],rings[0][j],rings[1][j],rings[1][i]])

    def taper(self, y0, y1, bottom, top, material, cx=8,cz=8, cap=True):
        rings=[[(cx-w,y,cz-w),(cx+w,y,cz-w),(cx+w,y,cz+w),(cx-w,y,cz+w)] for y,w in ((y0,bottom),(y1,top))]
        for i in range(4):
            j=(i+1)%4
            self.face(material,[rings[0][j],rings[0][i],rings[1][i],rings[1][j]])
        if cap:
            self.face(material,rings[0])
            self.face(material,list(reversed(rings[1])))

    def rim(self, y, outside, inside, thick, mat):
        self.bevel((8-outside,y,8-outside),(8+outside,y+thick,8-inside),.10,mat)
        self.bevel((8-outside,y,8+inside),(8+outside,y+thick,8+outside),.10,mat)
        self.bevel((8-outside,y,8-inside),(8-inside,y+thick,8+inside),.10,mat)
        self.bevel((8+inside,y,8-inside),(8+outside,y+thick,8+inside),.10,mat)

    def bolt(self,x,y,z,axis='z'):
        if axis=='z':
            self.bevel((x-.31,y-.31,z-.12),(x+.31,y+.31,z+.12),.07,'rivet')
            self.block((x-.06,y-.15,z-.135),(x+.06,y+.15,z+.135),'iron')
        else:
            self.bevel((x-.12,y-.31,z-.31),(x+.12,y+.31,z+.31),.07,'rivet')
            self.block((x-.135,y-.15,z-.06),(x+.135,y+.15,z+.06),'iron')

    def link(self,x,y,z,turn=False):
        # Real open alternating chain links, not a string of solid cubes.
        if not turn:
            for a,b in [((x-.42,y,z-.12),(x-.18,y+1.1,z+.12)),((x+.18,y,z-.12),(x+.42,y+1.1,z+.12)),((x-.18,y,z-.12),(x+.18,y+.24,z+.12)),((x-.18,y+.86,z-.12),(x+.18,y+1.1,z+.12))]: self.block(a,b,'iron')
        else:
            for a,b in [((x-.12,y,z-.42),(x+.12,y+1.1,z-.18)),((x-.12,y,z+.18),(x+.12,y+1.1,z+.42)),((x-.12,y,z-.18),(x+.12,y+.24,z+.18)),((x-.12,y+.86,z-.18),(x+.12,y+1.1,z+.18))]: self.block(a,b,'iron')


def pot(wet):
    m=Prop()
    # Sloping vessel narrows toward the foot; an actual recessed soil opening.
    m.taper(.3,1,3.35,3.7,'ceramic')
    m.taper(1,7.1,3.7,4.85,'ceramic',cap=False)
    m.taper(6.8,7.4,4.85,5.3,'ceramic',cap=False)
    m.taper(6.4,6.85,4.8,5.05,'ceramic_dark',cap=False)
    m.rim(7.4,5.3,4.25,1.1,'ceramic_light')
    m.taper(7.5,8.5,4.25,4.25,'ceramic_dark',cap=False)
    m.block((3.75,6.9,3.75),(12.25,7.5,12.25),'soil_wet' if wet else 'soil')
    # Shallow kiln chips, restrained molded seams and two darker drain notches.
    for x in (5.2,10.5): m.block((x,.8,4.25),(x+.45,1.25,4.45),'ceramic_dark')
    return m


def bed(wet):
    m=Prop()
    m.bevel((.6,.65,.6),(15.4,2.1,15.4),.16,'wood_dark','wood')
    m.block((1.4,12.8,1.4),(14.6,13.6,14.6),'soil_wet' if wet else 'soil')
    # Full-height chest silhouette, broad inset planks and substantial steel corner posts.
    for y in (2.15,5.65,9.15):
        for lo,hi in [((.4,y,.4),(15.6,y+3.35,1.45)),((.4,y,14.55),(15.6,y+3.35,15.6)),((.4,y,1.45),(1.45,y+3.35,14.55)),((14.55,y,1.45),(15.6,y+3.35,14.55))]:
            m.bevel(lo,hi,.13,'wood','wood_light')
    for lo,hi in [((.4,12.65,.4),(15.6,14.1,1.5)),((.4,12.65,14.5),(15.6,14.1,15.6)),((.4,12.65,1.5),(1.5,14.1,14.5)),((14.5,12.65,1.5),(15.6,14.1,14.5))]:m.bevel(lo,hi,.12,'wood','wood_light')
    for x in (.0,14.15):
        for z in (.0,14.15):
            m.bevel((x,.0,z),(x+1.85,14.4,z+1.85),.14,'iron','iron_light')
            m.bevel((x-.12,.1,z-.12),(x+1.97,1.2,z+1.97),.18,'iron','iron_light')
            m.bevel((x-.15,13.0,z-.15),(x+2,14.7,z+2),.16,'iron_light','rivet_dark')
            for y in (2.25,13.6):
                m.bolt(x+.925,y,z-.19 if z<8 else z+2.04)
                m.bolt(x-.19 if x<8 else x+2.04,y,z+.925,'x')
    return m


def lamp(lit, preview=False):
    m=Prop();glow='emission' if lit else 'glass'
    # Open twin-bar chassis. Light tubes are genuinely recessed below the metal frame.
    for z in (4.2,10.65):m.bevel((.8,5,z),(15.2,6.5,z+1.15),.14,'iron','iron_light')
    for x in (.8,13.7):
        m.bevel((x,4.4,3.9),(x+1.5,7.35,12.1),.18,'iron','iron_light')
        for z in (3.72,11.95):
            m.bevel((x-.12,4.45,z),(x+1.62,7.3,z+.32),.09,'iron_light','rivet_dark')
            m.block((x+.30,5.15,z-.025),(x+1.2,6.55,z+.345),'glass')
            m.block((x+.48,5.4,z-.04),(x+1.02,6.30,z+.36),glow)
    for z in (6,8.7):
        m.bevel((2.35,4.4,z-.15),(13.65,5.35,z+1.45),.11,'iron_light')
        m.bevel((2.75,4.15,z+.05),(13.25,4.7,z+1.25),.10,'glass')
        m.bevel((3.05,4.05,z+.25),(12.95,4.35,z+1.05),.07,glow)
        m.block((3.2,4.015,z+.49),(12.8,4.06,z+.81),'emission_core' if lit else 'glass')
        if preview and lit:fixture_bloom(m,[(1.5,3.99,z-1.3),(1.5,3.99,z+2.6),(14.5,3.99,z+2.6),(14.5,3.99,z-1.3)])
        for x in (2.45,12.95):m.bevel((x,4.05,z-.15),(x+.60,5.1,z+1.45),.09,'iron','iron_light')
    m.bevel((5.6,6.1,6.45),(10.4,8.2,9.55),.18,'iron','iron_light')
    m.bevel((6.5,6.7,6.25),(9.5,7.8,6.5),.08,'iron_light')
    m.block((7,6.97,6.20),(9,7.55,6.26),glow)
    for x in (6.0,6.8,7.6,8.4,9.2):m.block((x,8.18,6.85),(x+.3,8.42,9.15),'iron_light')
    for x in (2.8,13.2):
        m.bevel((x-.65,6.5,7.35),(x+.65,7.2,8.65),.12,'iron_light')
        for i in range(7):m.link(x,7+i*1.25,8,i%2==1)
    # Small externally visible cable and connector, not a floating ballast box.
    m.beam((10.2,7.3,8),(11.5,7.3,8),.28,'iron')
    m.beam((11.5,7.3,8),(11.5,6.2,10.8),.28,'iron')
    return m


def cell():
    m=Prop()
    m.taper(2,3,2.25,3,'iron')
    m.taper(3,4,3,2.6,'iron_light')
    m.taper(4,6,2.0,2.25,'emission')
    m.taper(6,10.8,2.25,1.8,'emission')
    m.taper(10.8,12,1.8,2.6,'iron_light')
    m.bevel((5.4,12,5.4),(10.6,13.3,10.6),.24,'iron','iron_light')
    for x in (5.15,10.2):
        for z in (5.15,10.2):m.block((x,3.7,z),(x+.65,12,z+.65),'iron')
    for y in (5.2,8.5):m.block((5.7,y,5.65),(10.3,y+.35,5.85),'glass')
    m.block((7,13.3,7),(9,14.1,9),'rivet')
    return m


def watering_can():
    m=Prop()
    # Blue-gray cast vessel, chamfered corners, raised rolled seams and open metal handle.
    m.bevel((6.2,1.3,4.9),(14.2,2.15,12.1),.23,'iron','iron_light')
    m.bevel((6.4,2.05,5.1),(14.0,8.6,11.9),.75,'teal','can_edge')
    m.bevel((6.3,8.15,5),(14.1,8.85,12),.25,'can_edge','rivet_dark')
    m.bevel((6.8,8.75,5.5),(13.6,9.15,11.5),.35,'teal','can_edge')
    m.bevel((8.4,9.1,7),(11.6,9.5,10.2),.24,'iron_light')
    m.block((8.8,9.48,7.4),(11.2,9.51,9.8),'soil_wet')
    # The carry handle is an open arch above the reservoir, with riveted mountings.
    for a,b in [((8,7.8,11.7),(8,12.5,12.8)),((8,12.5,12.8),(12,12.5,12.8)),((12,12.5,12.8),(12,7.8,11.7))]:m.beam(a,b,.72,'can_edge')
    for x in (8,12):m.bevel((x-.52,7.15,11.55),(x+.52,8.4,12.0),.10,'iron_light')
    # Tapered three-piece neck and a flared chamfered rose with nine inset holes.
    for a,b,w in [((6.6,3.4,8.4),(4.0,6.1,8.4),1.50),((4.0,6.1,8.4),(1.45,9.5,8.4),1.10)]:m.beam(a,b,w,'teal')
    first=len(m.faces)
    m.bevel((.35,9.25,6.8),(2.55,10.15,10),.22,'can_edge','iron_light')
    for x in (.85,1.45,2.05):
        for z in (7.3,8.4,9.5):m.block((x-.11,10.14,z-.11),(x+.11,10.19,z+.11),'iron')
    # The flared rose follows the sloping neck instead of sitting flat like a lid.
    c=math.cos(.55);s=math.sin(.55);cx=1.45-8;cy=9.7
    for f in range(first,len(m.faces)):
        mat,vertices,normals,uv=m.faces[f]
        def tilt(v,normal=False):
            x,y,z=v if normal else (v[0]-cx,v[1]-cy,v[2])
            return (x*c-y*s,y*c+x*s,z) if normal else (cx+x*c-y*s,cy+y*c+x*s,z)
        m.faces[f]=(mat,[tilt(v) for v in vertices],[tilt(v,True) for v in normals],uv)
    # Front pressed panel with an actual recessed border and pale corner fasteners.
    m.bevel((7.85,3.35,5.02),(12.55,6.8,5.24),.11,'can_edge')
    m.bevel((8.25,3.75,4.94),(12.15,6.4,5.05),.08,'teal')
    for x in (7.15,13.25):m.bolt(x,7.6,5.04)
    return m


def packet():
    m=Prop()
    m.bevel((4,1.5,7.4),(12,13,8.6),.12,'paper','paper_dark')
    m.bevel((4.05,12.7,7.2),(11.95,13.4,8.8),.12,'paper_dark','paper')
    m.face('packet_front',[(4.12,1.65,7.28),(4.12,12.9,7.28),(11.88,12.9,7.28),(11.88,1.65,7.28)],uv=[(1,1),(1,0),(0,0),(0,1)])
    # Embossed cultivar seal keeps the genome's actual pigment on the packet.
    m.bevel((9.3,3.4,7.05),(10.8,4.8,7.3),.10,'seed_bud')
    m.face('paper_dark',[(4.2,11.6,8.62),(11.8,11.6,8.62),(8,9.3,8.67)])
    return m


def ledger():
    m=Prop()
    # A bound field ledger in a low timber stand, replacing the anonymous cube terminal.
    m.bevel((1.5,0,3),(14.5,1.2,13),.18,'iron','iron_light')
    for x in (2,12):m.block((x,1,4),(x+2,4.5,12),'wood_dark')
    m.taper(3.7,4.3,6.2,6.5,'wood',cz=8)
    m.bevel((2,4.25,3),(14,4.7,13),.12,'iron','iron_light')
    m.bevel((2.5,4.7,3.4),(7.8,5.35,12.6),.10,'paper','paper_dark')
    m.bevel((8.2,4.7,3.4),(13.5,5.35,12.6),.10,'paper','paper_dark')
    for x in (2.52,13.42):
        for y in (4.84,5.02,5.20):m.block((x,y,3.65),(x+.06,y+.04,12.35),'paper_dark')
    m.block((7.8,4.65,3.3),(8.2,5.05,12.7),'paper_dark')
    for x in (3.1,8.8):
        for i in range(5):m.block((x,5.35,5+i*1.1),(x+3.8-(i%3)*.5,5.39,5.15+i*1.1),'ink')
    m.block((10.8,5.37,10),(11.5,5.42,13.6),'teal')
    for x in (2.1,13.0):
        for z in (3.1,12.1):m.block((x,4.62,z),(x+.8,4.82,z+.8),'iron_light')
    m.beam((12.8,5.5,4.8),(10.4,5.5,9),.25,'wood_dark')
    m.block((1.8,1.9,2.9),(4.4,3.1,3.15),'iron_light')
    m.block((2.5,2.1,2.8),(3.7,2.8,3),'emission')
    return m



def emission_pass(mesh, directory, name, library, binding):
    """Native composite separates luminous surfaces from item diffuse lighting."""
    glow=Mesh();glow.faces=[face for face in mesh.faces if 'emission' in face[0]]
    if not glow.faces:return binding
    glow.write(directory/f'{name}_emission.obj',library)
    body=Mesh();body.faces=[face for face in mesh.faces if 'emission' not in face[0]]
    body.write(directory/f'{name}_body.obj',library)
    base={key:value for key,value in binding.items() if key in ('loader','model','automatic_culling','shade_quads','emissive_ambient','textures')}
    base['render_type']='minecraft:cutout'
    base['model']=binding['model'].removesuffix('.obj')+'_body.obj'
    light=dict(base,model=binding['model'].removesuffix('.obj')+'_emission.obj',render_type='stonedew:emissive')
    result={key:value for key,value in binding.items() if key not in base}
    result['textures']=binding['textures']
    result.update(loader='neoforge:composite',children={'body':base,'light':light},item_render_order=['body','light'])
    return result

def generate(root):
    directory=root/'models/block/equipment';directory.mkdir(parents=True,exist_ok=True)
    mtl=[]
    specs=[('packet_front','seed_packet',(1,1,1)),('wood','wood',(1,1,1)),('wood_dark','wood',(.58,.56,.60)),('wood_light','wood',(1.13,1.10,1.02)),('rivet_dark','iron_light',(.86,.83,.89)),('can_edge','teal',(1.25,1.20,1.16)),('ceramic','ceramic',(1,1,1)),('ceramic_light','ceramic_rim',(1,1,1)),('ceramic_dark','ceramic_inner',(1,1,1)),('iron','iron',(1,1,1)),('iron_light','iron_light',(1,1,1)),('rivet','copper',(1,1,1)),('teal','teal',(1,1,1)),('glass','glass',(.6,.55,.68)),('soil','soil',(1,1,1)),('soil_wet','soil_wet',(1,1,1)),('paper','paper',(1,1,1)),('paper_dark','paper',(.65,.61,.61)),('ink','iron',(.6,.6,.6)),('leaf','plant_leaf',(1,1,1)),('seed_bud','plant_bud',(1,1,1)),('emission','glow',(1,1,1)),('emission_core','glow_core',(1,1,1))]
    specs += [('emission_halo','fixture_halo',(1,1,1)),('emission_aura','fixture_aura',(1,1,1))]
    for name,texture,color in specs:
        if name=='emission':color=(.75,.35,1)
        mtl += [f'newmtl {name}','Kd '+' '.join(map(str,color)),f'map_Kd {sprite(texture)}', 'Ka 1 1 1' if name.startswith('emission') else 'Ka 0 0 0']
        if name=='seed_bud': mtl.append('neoforge_TintIndex 0')
        mtl.append('')
    (directory/'equipment.mtl').write_text('\n'.join(mtl))
    meshes={}
    for wet in (False,True):
        suffix='_wet' if wet else ''
        meshes['clay_pot'+suffix]=(pot(wet),False,'ceramic')
        meshes['planter_bed'+suffix]=(bed(wet),False,'wood')
    for lit in (False,True):meshes['bulb_lamp'+('_lit' if lit else '')]=(lamp(lit),False,'iron')
    meshes.update(glow_cell=(cell(),True,'glow'),watering_can=(watering_can(),True,'teal'),wild_seed=(packet(),True,'paper'),ledger=(ledger(),False,'wood'))
    report=[]
    for name,(mesh,item,particle) in meshes.items():
        mesh.write(directory/f'{name}.obj','equipment.mtl')
        display=json.loads(json.dumps(DISPLAY))
        if name=='watering_can':
            for hand,angle in (('righthand',-45),('lefthand',45)):
                display['firstperson_'+hand]={'rotation':[0,angle,0],'translation':[-1,4,0],'scale':[.55]*3}
        data={'credit':'Original Stonedew reference-led equipment; tools/equipment_art.py','loader':'neoforge:obj',
              'model':f'stonedew:models/block/equipment/{name}.obj','automatic_culling':False,
              'shade_quads':True,'emissive_ambient':True,'textures':{'particle':f'stonedew:block/{particle}'},'display':display}
        path=root/('models/item' if item else 'models/block')/f'{name}.json'
        data=emission_pass(mesh,directory,name,'equipment.mtl',data)
        path.write_text(json.dumps(data,indent=2)+'\n')
        report.append(dict(model=name,faces=len(mesh.faces)))
    return report
