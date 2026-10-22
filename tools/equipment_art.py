"""Reference-led grow equipment: tapered ceramics, reinforced timber, bolted UV steel.
Original authored geometry. References in CODEX_REFERENCE_NEW are preserved unchanged.
"""
import json
import math
from plant_art import Mesh, unit, cross, add, mul

DISPLAY = {
    'gui': {'rotation': [25, 225, 0], 'translation': [0, 1, 0], 'scale': [.8]*3},
    'ground': {'translation': [0, 3, 0], 'scale': [.5]*3},
    'fixed': {'rotation': [0, 180, 0], 'scale': [.8]*3},
    'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 1.5, 0], 'scale': [.7]*3},
    'firstperson_lefthand': {'rotation': [0, -45, 0], 'translation': [0, 1.5, 0], 'scale': [.7]*3},
    'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [.5]*3}}

class Prop(Mesh):
    def face(self, material, vertices, normals=None, uv=None):
        # Geometry below is authored in the familiar absolute 0..16 block coordinates.
        if uv is None:
            normal = unit(cross(add(vertices[1], mul(vertices[0], -1)), add(vertices[2], mul(vertices[0], -1))))
            axis = max(range(3), key=lambda a: abs(normal[a]))
            # Consistent 32 texels per block, including narrow rails, bolts and angled walls.
            axes = (0,2) if axis == 1 else (2,1) if axis == 0 else (0,1)
            uv = [(v[axes[0]]/16, 1-v[axes[1]]/16) for v in vertices]
        super().face(material, [(x-8,y,z-8) for x,y,z in vertices], normals, uv)

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
        self.block((8-outside,y,8-outside),(8+outside,y+thick,8-inside),mat)
        self.block((8-outside,y,8+inside),(8+outside,y+thick,8+outside),mat)
        self.block((8-outside,y,8-inside),(8-inside,y+thick,8+inside),mat)
        self.block((8+inside,y,8-inside),(8+outside,y+thick,8+inside),mat)

    def bolt(self,x,y,z,axis='z'):
        if axis=='z': self.block((x-.20,y-.20,z-.1),(x+.20,y+.20,z+.1),'rivet')
        else: self.block((x-.1,y-.20,z-.20),(x+.1,y+.20,z+.20),'rivet')

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
    m.block((1,.6,1),(15,1.2,15),'wood_dark')
    m.block((1.3,5.7,1.3),(14.7,6.25,14.7),'soil_wet' if wet else 'soil')
    # Three individual rails on all four faces, with inset dark seams.
    for y in (1.1,2.8,4.5):
        for lo,hi in [((.4,y,.4),(15.6,y+1.55,1.4)),((.4,y,14.6),(15.6,y+1.55,15.6)),((.4,y,1.4),(1.4,y+1.55,14.6)),((14.6,y,1.4),(15.6,y+1.55,14.6))]: m.block(lo,hi,'wood')
    for x in (.1,14.4):
        for z in (.1,14.4):
            m.block((x,0,z),(x+1.5,7.2,z+1.5),'iron')
            m.block((x-.15,.15,z-.15),(x+1.65,.9,z+1.65),'iron_light')
            m.block((x-.2,6.3,z-.2),(x+1.7,7.4,z+1.7),'iron_light')
            for y in (1.4,5.8):
                m.bolt(x+.75,y,z-.11 if z<8 else z+1.61)
                m.bolt(x-.11 if x<8 else x+1.61,y,z+.75,'x')
    return m


def lamp(lit):
    m=Prop()
    # UV2 reference: inset twin tubes, raised driver, reinforced end housings.
    m.block((1,5,4.7),(15,6.6,11.3),'iron')
    m.block((1,4.5,4.4),(15,5.25,5.15),'iron_light')
    m.block((1,4.5,10.85),(15,5.25,11.6),'iron_light')
    for x in (1,13.5):
        m.block((x,4,4.1),(x+1.5,7.2,11.9),'iron')
        m.block((x+.15,4.15,4),(x+1.35,7.05,4.25),'iron_light')
        m.block((x+.15,4.15,11.75),(x+1.35,7.05,12),'iron_light')
        for z in (4,12):
            for y in (4.6,6.6):m.bolt(x+.75,y,z)
    for z in (6,8.8):
        m.block((2.5,4.35,z),(13.5,4.8,z+1.25),'glass')
        m.block((2.9,4.1,z+.2),(13.1,4.4,z+1.05),'emission' if lit else 'glass')
        for x in (2.5,12.9):m.block((x,4.05,z-.1),(x+.6,4.9,z+1.35),'iron_light')
    m.block((5.8,6.6,6.5),(10.2,8.1,9.5),'iron')
    m.block((6.9,6.95,6.35),(9.1,7.6,6.5),'emission' if lit else 'glass')
    for x in (3,13):
        for i in range(7):m.link(x,7+i*1.25,8,i%2==1)
    # Finned ballast on top reads even with the fixture viewed from above.
    for x in (6.1,6.8,7.5,8.2,8.9,9.6): m.block((x,8.1,6.8),(x+.25,8.35,9.2),'iron_light')
    return m


def cell():
    m=Prop()
    m.taper(2,3,2.25,3,'iron')
    m.taper(3,4,3,2.6,'iron_light')
    m.taper(4,6,2.0,2.25,'emission')
    m.taper(6,10.8,2.25,1.8,'emission')
    m.taper(10.8,12,1.8,2.6,'iron_light')
    m.block((5.4,12,5.4),(10.6,13.3,10.6),'iron')
    for x in (5.15,10.2):
        for z in (5.15,10.2):m.block((x,3.7,z),(x+.65,12,z+.65),'iron')
    for y in (5.2,8.5):m.block((5.7,y,5.65),(10.3,y+.35,5.85),'glass')
    m.block((7,13.3,7),(9,14.1,9),'rivet')
    return m


def watering_can():
    m=Prop()
    # Chamfered reservoir and real open arched carry handle, segmented rising spout.
    m.taper(1.5,2.3,2.6,3.15,'iron_light',cx=8,cz=8.5)
    m.taper(2.3,8.4,3.15,2.95,'teal',cx=8,cz=8.5)
    m.taper(8.4,9.2,2.95,2.45,'teal',cx=8,cz=8.5)
    m.block((6.5,9.1,7),(9.5,9.5,10),'iron')
    m.block((7,9.45,7.5),(9,9.55,9.5),'soil_wet')
    for a,b in [((6,6,11.5),(6,11,13)),((6,11,13),(10,11,13)),((10,11,13),(10,6,11.5))]:m.beam(a,b,.8,'iron_light')
    for a,b,w in [((5.2,3.9,8.5),(2.5,6.6,8.5),1.25),((2.5,6.6,8.5),(1,9.1,8.5),1.05)]:m.beam(a,b,w,'teal')
    m.block((.1,8.7,6.9),(1.45,9.5,10.1),'iron_light')
    for z in (7.3,8.2,9.1):m.block((.05,9.1,z),(.18,9.35,z+.3),'iron')
    for y in (3.1,7.5):
        m.block((4.8,y,7.5),(5,y+.25,9.5),'iron_light')
    m.block((7,4.3,5.29),(9,6.2,5.42),'iron_light')
    m.block((7.5,4.8,5.2),(8.5,5.8,5.35),'teal')
    return m


def packet():
    m=Prop()
    m.block((4,1.5,7.4),(12,13,8.6),'paper')
    m.block((4.25,12.7,7.1),(11.75,13.4,8.85),'paper_dark')
    m.block((4.35,2,7.15),(11.65,2.55,7.4),'iron')
    m.block((4.35,10.8,7.15),(11.65,11.35,7.4),'iron')
    # Actual colored flower emblem and green leaf rays, rather than a rectangle badge.
    for a,b in [((8,4.3,7.03),(8,9.5,7.03)),((8,6,7.03),(5.8,8.4,7.03)),((8,6,7.03),(10.2,8.4,7.03)),((8,5.3,7.03),(5.8,6.6,7.03)),((8,5.3,7.03),(10.2,6.6,7.03))]:m.beam(a,b,.38,'leaf')
    m.block((7.35,8,6.8),(8.65,9.45,7.1),'seed_bud')
    m.block((7.6,9.45,6.85),(8.4,10.05,7.1),'seed_bud')
    return m


def ledger():
    m=Prop()
    # A bound field ledger in a low timber stand, replacing the anonymous cube terminal.
    m.block((1.5,0,3),(14.5,1.2,13),'iron')
    for x in (2,12):m.block((x,1,4),(x+2,4.5,12),'wood_dark')
    m.taper(3.7,4.3,6.2,6.5,'wood',cz=8)
    m.block((2,4.25,3),(14,4.7,13),'iron')
    m.block((2.5,4.7,3.4),(7.8,5.35,12.6),'paper')
    m.block((8.2,4.7,3.4),(13.5,5.35,12.6),'paper')
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


def generate(root):
    directory=root/'models/block/equipment';directory.mkdir(parents=True,exist_ok=True)
    mtl=[]
    specs=[('wood','wood',(1,1,1)),('wood_dark','wood',(.58,.56,.60)),('ceramic','ceramic',(1,1,1)),('ceramic_light','ceramic_rim',(1,1,1)),('ceramic_dark','ceramic_inner',(1,1,1)),('iron','iron',(1,1,1)),('iron_light','iron_light',(1,1,1)),('rivet','copper',(1,1,1)),('teal','teal',(1,1,1)),('glass','glass',(.6,.55,.68)),('soil','soil',(1,1,1)),('soil_wet','soil_wet',(1,1,1)),('paper','paper',(1,1,1)),('paper_dark','paper',(.65,.61,.61)),('ink','iron',(.6,.6,.6)),('leaf','plant_leaf',(1,1,1)),('seed_bud','plant_bud',(1,1,1)),('emission','glow',(1,1,1))]
    for name,texture,color in specs:
        mtl += [f'newmtl {name}','Kd '+' '.join(map(str,color)),f'map_Kd stonedew:block/{texture}', 'Ka 1 1 1' if name=='emission' else 'Ka 0 0 0']
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
        path.write_text(json.dumps(data,indent=2)+'\n')
        report.append(dict(model=name,faces=len(mesh.faces)))
    return report
