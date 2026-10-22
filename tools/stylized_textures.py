"""Original pixel art authored as silhouettes, ramps and material marks.
No source-image sampling, generated-image processing, or reference crops. Pixel scale and
palette are chosen to match the owner's reference sheets; lighting is supplied by rendering.
"""
from pathlib import Path
import math
import random
import struct
import zlib


def write_png(path, pixels):
    height, width = len(pixels), len(pixels[0])
    def chunk(kind, payload):
        return struct.pack('>I', len(payload)) + kind + payload + struct.pack('>I', zlib.crc32(kind+payload))
    raw=b''.join(b'\0'+bytes(c for pixel in row for c in pixel) for row in pixels)
    data=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,6,0,0,0))
    data+=chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)


def rgba(color): return tuple(int(color[i:i+2],16) for i in (0,2,4))+(255,)


def material(name, palette, size=32):
    colors=list(map(rgba,palette))
    rng=random.Random('stonedew-authored-'+name)
    pixels=[[colors[1] for _ in range(size)] for _ in range(size)]
    # Broad, sparse, aligned patches. No per-pixel speckle or high-frequency white highlights.
    for _ in range(44 if name in ('soil','soil_wet') else 128 if name.startswith('ceramic') else 36):
        x,y=rng.randrange(size),rng.randrange(size)
        w,h=rng.randint(2,5),rng.randint(1,3)
        color=colors[rng.choice((0,1,1,2))]
        for yy in range(y,min(size,y+h)):
            for xx in range(x,min(size,x+w)):pixels[yy][xx]=color
    if name in ('wood','wood_edge'):
        for y in (0,15,31):
            for x in range(size):pixels[y][x]=colors[0]
        for x,y,length in ((3,6,11),(17,11,8),(1,24,9),(15,20,13)):
            for xx in range(x,x+length):pixels[y][xx]=colors[2]
        for x,y,length in ((6,9,8),(21,27,9),(2,18,6)):
            for xx in range(x,x+length):pixels[y][xx]=colors[0]
    if name in ('iron','iron_light','copper'):
        # Long restrained reflected strips, rather than a tile of mottled noise.
        for x in range(4,27):pixels[5][x]=colors[2]
    if name=='glow':
        for y in range(size):
            for x in range(size):pixels[y][x]=colors[2 if y%10 in (3,4,5) else 1 if y%10<8 else 0]
    if name=='dewstone':
        for x,y in ((7,8),(8,8),(9,9),(22,24),(23,24)):pixels[y][x]=rgba('9955BE')
    return pixels


def leaf_fan(neutral=False):
    """A 64px, broad seven-finger silhouette, with two quiet tones per finger.
    The straight shared root and explicit serrations are authored at final texel scale.
    """
    size=64
    pixels=[[(0,0,0,0) for _ in range(size)] for _ in range(size)]
    root=(31.5,56)
    for degrees,length,width in ((-80,20,3.5),(-56,31,4.4),(-29,42,5.2),(0,49,6.2),(29,42,5.2),(56,31,4.4),(80,20,3.5)):
        angle=math.radians(degrees)
        dx,dy=math.sin(angle),-math.cos(angle)
        for y in range(size):
            for x in range(size):
                relx,rely=x-root[0],y-root[1]
                along=relx*dx+rely*dy
                across=relx*(-dy)+rely*dx
                t=along/length
                if t<0 or t>1:continue
                # A filled lance with small, regular teeth. Keep broad finger mass readable.
                belly=math.sin(math.pi*t)**.68
                tooth=1.0 if int(along/2)%2 else .78
                half=width*belly*tooth
                if abs(across)>half:continue
                color='5AB933' if across<-.3 else '419B29'
                if t>.84:color='77CA43' if across<0 else '59B831'
                if abs(across)<.45 and .10<t<.85:color='3A8B26'
                if neutral:
                    color = 'F5F5F5' if across<-.3 else 'C4C4C4'
                    if t>.84:color='FFFFFF' if across<0 else 'E3E3E3'
                    if abs(across)<.45 and .10<t<.85:color='AEAEAE'
                pixels[y][x]=rgba(color)
    for y in range(53,62):
        for x in (31,32):pixels[y][x]=rgba('BFBFBF' if neutral else '438B2A')
    return pixels


PALETTES={
 'wood':('764322','A86732','BC8144'),
 'wood_edge':('694427','8D5A30','AB7541'),
 'ceramic':('A44B30','B95B36','CA6B40'),
 'ceramic_rim':('B85834','D07447','E28B57'),
 'ceramic_inner':('713A28','93472C','AB5832'),
 'teal':('345C56','467970','5B8B7F'),
 'copper':('877D8A','A69AA9','C2B7C5'),
 'iron':('443D4B','584E60','695D70'),
 'iron_light':('615567','786A7D','8D7D92'),
 'soil':('352217','51301E','6C4228'),
 'soil_wet':('291D17','3B261A','50311D'),
 'paper':('C7B58C','DDCDA5','E9DCBA'),
 'glow':('763AB3','B35EF0','EDB0FF'),
 'glass':('695780','947CAB','B8A2C8'),
 'dewstone':('29252E','39313F','4A4051'),
 'plant_bud':('DFDFDF','F4F4F4','FFFFFF'),
 'plant_leaf':('358627','4AA32D','65BA38'),
 'plant_stem':('305221','3F6926','527C2C'),
 'plant_pistil':('DFD9C8','F2EBDB','FFFFFF'),
 'leaf':('358627','4AA32D','65BA38'),
 'bud':('DFDFDF','F4F4F4','FFFFFF'),
 'hair':('DFD9C8','F2EBDB','FFFFFF'),
 'stem':('305221','3F6926','527C2C'),
}


def generate(root):
    tiles={name:material(name,palette) for name,palette in PALETTES.items()}
    for name,pixels in tiles.items():write_png(root/f'textures/block/{name}.png',pixels)
    write_png(root/'textures/block/leaf_fan.png',leaf_fan(True))
    write_png(root/'textures/block/leaf_emblem.png',leaf_fan())
    # UI shares the very same authored material ramps, rather than the old imagegen atlas.
    order=('wood','wood_edge','ceramic','teal','copper','iron','soil','soil_wet','paper','glow','glass','dewstone','plant_bud','plant_leaf','plant_stem','plant_pistil')
    sheet=[[(0,0,0,255) for _ in range(128)] for _ in range(128)]
    for i,name in enumerate(order):
        for y,row in enumerate(tiles[name]):
            for x,pixel in enumerate(row):sheet[i//4*32+y][i%4*32+x]=pixel
    write_png(root/'textures/gui/materials.png',sheet)
    shadow=[]
    for y in range(32):
        row=[]
        for x in range(32):
            radius=math.hypot((x-15.5)/15.5,(y-15.5)/15.5)
            row.append((24,19,27,round(max(0,1-radius)**1.8*160)))
        shadow.append(row)
    write_png(root/'textures/effect/contact_shadow.png',shadow)
    halo=[]
    for y in range(64):
        row=[]
        for x in range(64):
            radius=math.hypot((x-31.5)/31.5,(y-31.5)/31.5)
            row.append((190,103,255,round(max(0,1-radius)**2*155)))
        halo.append(row)
    write_png(root/'textures/effect/lamp_halo.png',halo)

