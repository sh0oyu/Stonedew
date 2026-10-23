"""Complete reference-sheet art catalog. Future tiers are visual previews, not gameplay.
Shared construction/materials with the working P1 equipment; original authored geometry.
"""
import json
import math
from equipment_art import Prop, pot, bed, lamp, DISPLAY, emission_pass


def cloth_pot():
    m=Prop()
    m.bevel((2.5,.25,2.5),(13.5,1.2,13.5),.26,'fabric','iron')
    m.bevel((2.2,1.1,2.2),(13.8,10.3,13.8),.38,'fabric','iron')
    m.rim(9.7,6.25,5.25,1,'fabric')
    m.block((2.8,9.6,2.8),(13.2,10,13.2),'soil')
    for x in (2.35,13.65):
        for z in (3,12.5):m.beam((x,1,z),(x,10.3,z),.22,'iron_light')
    # Open reinforced carry loops on opposing sides.
    for x in (2,14):
        for a,b in [((x,10,4),(x,12.8,4)),((x,12.8,4),(x,12.8,12)),((x,12.8,12),(x,10,12))]:m.beam(a,b,.60,'fabric')
        for z in (4,12):m.bevel((x-.4,8.6,z-.5),(x+.4,10.4,z+.5),.1,'iron')
    return m


def automated_pot():
    m=Prop()
    m.bevel((.7,.25,.7),(15.3,2.2,15.3),.25,'iron','iron_light')
    m.bevel((1.0,1.8,1),(15,12,15),.32,'iron','iron_light')
    m.rim(11.6,7.9,6.1,1.7,'iron_light')
    m.block((1.95,11.8,1.95),(14.05,12.4,14.05),'soil_wet')
    for x in (.15,13.9):
        for z in (.15,13.9):
            m.bevel((x,0,z),(x+1.95,13.9,z+1.95),.16,'iron_light','rivet_dark')
            for y in (1.2,12.6):m.bevel((x-.12,y-.7,z-.12),(x+2.07,y+.7,z+2.07),.18,'iron_light')
    m.bevel((6.2,3,.65),(9.8,8.3,1),.18,'iron_light')
    m.bevel((6.7,3.5,.5),(9.3,7.8,.72),.09,'iron')
    for y in (4,5.1,6.2):m.block((7.3,y,.43),(8.7,y+.7,.53),'cyan_emission')
    m.beam((8,12.4,12),(8,18.5,12),1,'iron_light')
    m.beam((4,18.5,12),(12,18.5,12),.9,'iron_light')
    for x in (4,12):m.bevel((x-.6,17.9,11.4),(x+.6,19.1,12.6),.1,'iron','iron_light');m.block((x-.25,18.2,11.35),(x+.25,18.8,11.43),'cyan_emission')
    # Reference-only dashed irrigation arcs. These are static art, not an active machine.
    for side in (-1,1):
        for i in range(1,9):
            t=i/9;x=8+side*(4+2*t);z=12-8*t;y=18.5+1.25*math.sin(math.pi*t)-6.1*t*t
            half=.11 if i%2 else .15
            m.block((x-half,y-half,z-half),(x+half,y+half,z+half),'cyan_emission')
    return m


def panel(tier=3):
    m=Prop();width=18 if tier==3 else 23;depth=14 if tier==3 else 18
    x0=8-width/2;x1=8+width/2;z0=8-depth/2;z1=8+depth/2
    for z in (z0,z1-1.4):m.bevel((x0,4.8,z),(x1,6.6,z+1.4),.18,'iron','iron_light')
    for x in (x0,x1-1.4):m.bevel((x,4.8,z0+1.4),(x+1.4,6.6,z1-1.4),.18,'iron','iron_light')
    count=4 if tier==3 else 6
    for i in range(count):
        x=x0+2+(width-4)*i/(count-1)
        m.bevel((x-.65,4.35,z0+1.2),(x+.65,5.7,z1-1.2),.13,'iron_light')
        m.bevel((x-.46,4.15,z0+1.7),(x+.46,4.6,z1-1.7),.08,'emission')
        m.block((x-.22,4.12,z0+1.9),(x+.22,4.2,z1-1.9),'white_emission')
    for x in (x0+.7,x1-.7):
        for z in (z0,z1-1):
            m.bevel((x-.7,4.5,z-.25),(x+.7,7.4,z+1.25),.15,'iron_light')
            m.block((x-.24,5.35,z-.28),(x+.24,6.5,z-.20),'emission')
    for x in (x0+width*.25,x0+width*.75):
        m.bevel((x-1.7,6.5,6.7),(x+1.7,8.9,9.3),.17,'iron','iron_light')
        m.block((x-.8,7.2,6.65),(x+.8,8.1,6.73),'emission')
    for x in (x0+.7,x1-.7):
        if tier==3:
            for i in range(5):m.link(x,6.8+i*1.25,8,i%2==1)
        else:
            for z in (z0+.7,z1-.7):m.beam((x,6.7,z),(x,12.3,8),.4,'iron')
    return m


def pendant():
    m=Prop()
    m.bevel((4.3,2.2,4.3),(11.7,3.3,11.7),.20,'iron','iron_light')
    m.bevel((5,3.3,5),(11,6.5,11),.4,'glass')
    m.bevel((5.6,2.9,5.6),(10.4,6.8,10.4),.26,'emission')
    m.bevel((6.5,1.2,6.5),(9.5,3.1,9.5),.24,'white_emission')
    for x in (4.5,10.7):
        for z in (4.5,10.7):m.beam((x,3,z),(x,8,z),.65,'iron')
    m.bevel((4,6.8,4),(12,8.4,12),.25,'iron','iron_light')
    for z in (3.85,11.95):m.block((7,7.1,z),(9,8,z+.2),'emission')
    for i in range(5):m.link(8,8.3+i*1.25,8,i%2==1)
    m.bevel((5.5,14.2,5.5),(10.5,15.2,10.5),.15,'iron','iron_light')
    return m


def append(m, other, offset=(0,0,0), scale=1):
    # Prop faces are already centered; compensate before passing through Prop.face.
    for material,vertices,normals,uv in other.faces:
        m.face(material,[((v[0]+8)*scale+offset[0],v[1]*scale+offset[1],(v[2]+8)*scale+offset[2]) for v in vertices],normals,uv)


def tent(tier):
    m=Prop();w=(18,24,29,34)[tier-1];d=(18,20,23,26)[tier-1];h=(36,37,40,43)[tier-1]
    # Outer fabric envelope, real panel seams and pale reflective inner lining.
    m.bevel((0,0,0),(w,1.5,d),.2,'fabric','iron_light')
    m.bevel((0,h-2.1,0),(w,h,d),.28,'fabric','iron_light')
    for x in (0,w-1):
        m.bevel((x,1.5,.7),(x+1,h-2.1,d-.5),.16,'fabric')
        inside=x+1.015 if x==0 else x-.025
        m.block((inside,2.0,1.9),(inside+.05,h-2.5,d-1.7),'lining')
    m.bevel((1,1.5,d-1),(w-1,h-2.1,d),.18,'fabric')
    m.block((1.8,2,d-1.06),(w-1.8,h-2.6,d-.98),'lining')
    # Heavy front valance and corner couplers define the open mouth.
    m.bevel((.5,h-6.4,-.2),(w-.5,h-1.2,1.5),.20,'fabric','iron_light')
    for x in (.9,w-1.9):
        for z in (.8,d-1.8):
            m.bevel((x,1,z),(x+1,h-1,z+1),.15,'iron','iron_light')
            for y in (1.1,h*.52,h-3.4):
                m.bevel((x-.6,y,z-.6),(x+1.6,y+1.7,z+1.6),.14,'iron_light','rivet_dark')
                if z<2:m.bolt(x+.5,y+.85,z-.67)
    m.bevel((.5,.6,-.2),(w-.5,2.1,1.3),.18,'iron','iron_light')
    # Gathered fabric side flaps with folds, cinched straps and rolled upper corners.
    for side in (0,1):
        x=2.1 if side==0 else w-3.3
        for a,b,th in [((x,2,1.3),(x+.4,h*.48,1.0),1.5),((x+.4,h*.48,1),(x+.7,h-7,1.0),2.0)]:m.beam(a,b,th,'fabric')
        for delta in (-.42,.45):m.beam((x+delta,3,.7),(x+.3+delta,h*.48,.4),.23,'iron')
        m.bevel((x-.8,h*.48-.3,-.1),(x+1.9,h*.48+.9,1.5),.12,'iron_light')
        m.bevel((x-.1,h*.48-.02,-.17),(x+.8,h*.48+.6,-.03),.08,'iron')
        m.bevel((x-.5,h-7.3,.0),(x+2,h-4.8,2.8),.55,'fabric','iron')
    # Actual lamp geometry in the preview, matching the corresponding reference tier.
    fixture=pendant() if tier==1 else lamp(True) if tier==2 else panel(tier)
    append(m,fixture,((w-16)/2,h-20,(d-16)/2))
    # Reflective panel quilting has shallow, irregular seams, not busy white noise.
    for x in range(4,int(w)-2,6):m.beam((x,3,d-1.13),(x+.35,h-7,d-1.13),.12,'lining_seam')
    if tier==2:
        m.bevel((w-.15,h-12,d*.46),(w+.35,h-7,d*.46+5),.14,'iron_light')
        m.block((w+.34,h-11.4,d*.46+.6),(w+.43,h-7.6,d*.46+4.4),'fabric')
        for z in (d*.46+1.2,d*.46+2.5,d*.46+3.8):m.beam((w+.46,h-11.1,z),(w+.46,h-7.9,z),.19,'iron')
    if tier>=3:
        # External fan housing with inset grille, blades, a ribbed elbow and service cable.
        m.bevel((w-1,h-12,d*.55),(w+2.8,h-4,d*.55+7),.4,'iron','iron_light')
        m.bevel((w+2.75,h-10.8,d*.55+1.0),(w+3.2,h-5.2,d*.55+6.0),.18,'iron_light')
        m.block((w+3.18,h-10.2,d*.55+1.6),(w+3.25,h-5.8,d*.55+5.4),'fabric')
        for z in (d*.55+2.1,d*.55+3.5,d*.55+4.9):m.beam((w+3.3,h-10.1,z),(w+3.3,h-5.9,z),.20,'iron_light')
        for y in (h-9.4,h-7.8,h-6.4):m.beam((w+3.32,y,d*.55+1.65),(w+3.32,y,d*.55+5.35),.2,'iron_light')
        for i in range(6):m.bevel((w-3+i*.68,h-4.9,d*.70),(w-2.05+i*.68,h+.9,d*.70+4.0),.27,'iron','iron_light')
        m.beam((w+2,h-11,d*.55+5.5),(w+2,3,d*.55+5.5),.40,'iron')
    if tier==4:
        m.bevel((w-.1,13,5),(w+2.5,24,9.5),.23,'iron','iron_light')
        for y in (15,18,21):m.block((w+2.49,y,6.2),(w+2.59,y+1.6,8.3),'cyan_emission')
        for y in (9,27):m.bevel((w-.2,y,6.1),(w+.8,y+.8,8.4),.13,'iron_light')
    return m


def generate(root):
    directory=root/'models/block/catalog';directory.mkdir(parents=True,exist_ok=True)
    meshes={'pot_fabric':cloth_pot(),'pot_automated':automated_pot(),'uv_pendant':pendant(),'uv_panel_4':panel(3),'uv_panel_6':panel(4)}
    meshes.update({f'tent_{tier}':tent(tier) for tier in range(1,5)})
    meshes['uv_twin']=lamp(True)
    # Share exactly the same authored material library and maps as the working equipment.
    material=(root/'models/block/equipment/equipment.mtl').read_text()
    for name,texture,color,emissive in [('fabric','fabric',(1,1,1),False),('lining','lining',(1,1,1),False),('lining_seam','lining',(.77,.77,.81),False),('cyan_emission','glow_cyan',(1,1,1),True),('white_emission','glow_core',(1,1,1),True)]:
        material+=f'\nnewmtl {name}\nKd '+' '.join(map(str,color))+f'\nmap_Kd stonedew:block/{texture}\nKa '+('1 1 1' if emissive else '0 0 0')+'\n'
    (directory/'catalog.mtl').write_text(material)
    overrides=[];report=[]
    for code,(name,mesh) in enumerate(meshes.items(),100):
        mesh.write(directory/f'{name}.obj','catalog.mtl')
        target=root/f'models/item/art/{name}.json';target.parent.mkdir(parents=True,exist_ok=True)
        binding={'credit':'Original Stonedew reference catalog. Art preview; no future gameplay implied.','loader':'neoforge:obj','model':f'stonedew:models/block/catalog/{name}.obj','automatic_culling':False,'shade_quads':True,'emissive_ambient':True,'textures':{'particle':'stonedew:block/iron'}}
        binding=emission_pass(mesh,directory,name,'catalog.mtl',binding)
        target.write_text(json.dumps(binding,indent=2)+'\n')
        overrides.append({'predicate':{'custom_model_data':code},'model':f'stonedew:item/art/{name}'})
        report.append({'model':name,'customModelData':code,'faces':len(mesh.faces),'status':'Art preview; not functional automation'})
    cell=root/'models/item/glow_cell.json';data=json.loads(cell.read_text());data['overrides']=overrides;cell.write_text(json.dumps(data,indent=2)+'\n')
    return report
