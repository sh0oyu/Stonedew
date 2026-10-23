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
    """Painted material ramps: grain, kiln mottling, faceted metal, soil clods.

    These are authored texel functions, not edits or samples of the reference PNGs.
    Broad forms come first; small marks are restricted to wear and material features.
    """
    colors=list(map(rgba,palette));rng=random.Random('stonedew-v5-'+name)
    pixels=[]
    def ramp(t):
        t=max(0,min(1,t));t=round(t*9)/9
        a,b=(colors[0],colors[1]) if t<.5 else (colors[1],colors[2])
        f=t*2 if t<.5 else (t-.5)*2
        return tuple(round(a[i]*(1-f)+b[i]*f) for i in range(3))+(255,)
    macro=[[rng.uniform(-.16,.16) for _ in range(8)] for _ in range(8)]
    for y in range(size):
        row=[]
        for x in range(size):
            t=.48+macro[y//4][x//4]
            if name.startswith('wood'):
                grain=math.sin(y*1.6+math.sin(x*.22)*.65)+.35*math.sin(y*3.9+x*.14)
                t=.50+.13*grain+macro[y//4][x//4]*.65
                # Painted carved grain, with a light lip next to the dark cut.
                if (y+round(math.sin(x*.19)*1.3))%11==0:t-=.28
                if (y+round(math.sin(x*.19)*1.3))%11==1:t+=.14
            elif name in ('iron','iron_light','copper','teal','fabric','lining'):
                t=.43+.11*math.sin(x*.25+y*.1)+.08*math.sin(y*.61)+macro[y//4][x//4]*.5
                if name=='fabric':t-=.11 if x%7==0 else 0
                if name=='lining':t+=.10*math.cos((x+y)*.43)
            elif name.startswith('ceramic'):
                t=.46+.15*math.sin(x*.19)+macro[y//4][x//4]*.65
                if y in (3,14,26):t+=.09
            elif name in ('plant_bud','bud'):
                t=.68+.11*math.sin(x*.32+y*.23)+macro[y//4][x//4]*.22
            elif name=='leaf_surface':
                # Midrib-to-edge luminosity and restrained broad painted patches.
                t=.87+.05*math.sin(y*.22)
                if x<2:t=.48
                elif x>29:t=.94
                elif (y+round(x*.4))%10==0:t-=.13
                if 6<x<20 and y in (9,10,21,22):t+=.07
            elif name in ('plant_stem','stem'):
                t=.45+.17*math.sin(x*.9)+macro[y//4][x//4]*.3
            elif name in ('soil','soil_wet'):
                # Offset chunks: lit clay/perlite flecks and deeply shaded crevices.
                xx=(x+(y//5%2)*3)%32
                t=.23+macro[y//4][x//4]
                if xx%7 in (1,2,3,4) and y%5 in (1,2,3):t=.60+macro[y//4][x//4]
                if xx%7==2 and y%5==1:t=.94
            elif name=='glow_core':
                t=.90 if y%10 in (0,9) else 1
            elif name=='glow':
                t=.40 if y%10 in (0,9) else .85 if y%10 in (1,8) else 1
            row.append(ramp(t))
        pixels.append(row)
    # A few designed scuffs. Avoid filling every face with equally loud noise.
    if name in ('iron','iron_light','copper','teal'):
        for x,y,w in ((3,5,7),(20,25,5),(12,17,3)):
            for xx in range(x,x+w):pixels[y][xx]=ramp(.78)
            for xx in range(x+1,x+w):pixels[y+1][xx]=ramp(.35)
    if name=='dewstone':
        for cx,cy in ((6,8),(23,22),(13,27),(27,5)):
            for dy in range(-2,3):
                for dx in range(-2,3):
                    if abs(dx)+abs(dy)>3:continue
                    pixels[(cy+dy)%size][(cx+dx)%size]=rgba('493258' if abs(dx)+abs(dy)==3 else '76508D' if dy>0 else 'AC7AC1')
            pixels[cy-1][cx]=rgba('E2B9F5')
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


def seed_packet():
    """Original sealed seed envelope illustration, drawn at final 64px resolution."""
    pixels=[[rgba('D5BE8E' if (x//8+y//8)%3 else 'DCC79D') for x in range(64)] for y in range(64)]
    def rect(x,y,w,h,c):
        for yy in range(y,y+h):
            for xx in range(x,x+w):pixels[yy][xx]=rgba(c)
    rect(3,3,58,1,'9D8058');rect(3,60,58,1,'9D8058')
    rect(3,4,1,56,'B69A6E');rect(60,4,1,56,'B69A6E')
    font={'S':['01111','10000','10000','01110','00001','00001','11110'],
          'T':['11111','00100','00100','00100','00100','00100','00100'],
          'O':['01110','10001','10001','10001','10001','10001','01110'],
          'N':['10001','11001','11001','10101','10011','10011','10001'],
          'E':['11111','10000','10000','11110','10000','10000','11111'],
          'D':['11110','10001','10001','10001','10001','10001','11110'],
          'W':['10001','10001','10001','10101','10101','11011','10001']}
    for i,char in enumerate('STONEDEW'):
        for y,row in enumerate(font[char]):
            for x,on in enumerate(row):
                if on=='1':pixels[y+7][x+8+i*6]=rgba('4C4C38')
    rect(8,17,48,1,'837047');rect(8,49,48,1,'837047')
    root=(32,43)
    for degree,length in ((-65,18),(-32,25),(0,28),(32,25),(65,18)):
        a=math.radians(degree);dx,dy=math.sin(a),-math.cos(a)
        for y in range(20,48):
            for x in range(9,56):
                along=(x-root[0])*dx+(y-root[1])*dy
                side=(x-root[0])*(-dy)+(y-root[1])*dx;t=along/length
                if 0<t<1 and abs(side)<2.7*math.sin(math.pi*t)*(1 if int(along)%3 else .72):
                    pixels[y][x]=rgba('43803E' if side<0 else '315E36')
    rect(31,42,2,5,'527040')
    # Seed tally and a quiet green certification seal.
    for x in (13,20,27):rect(x,54,3,2,'725B3A');rect(x+1,53,2,1,'947745')
    rect(43,53,8,5,'586C43');rect(45,54,4,3,'C5C193')
    return pixels


PALETTES={
 'glow_core':('BE6EF5','EAC0FF','FFF4FF'),
 'glow_cyan':('147590','3EE5F6','E5FFFF'),
 'leaf_surface':('B8B8B8','E7E7E7','FFFFFF'),
 'fabric':('25212C','3D3545','594C5E'),
 'lining':('794E94','AE7DC8','D4A5E9'),
 'wood':('633218','A15B29','CC8744'),
 'wood_edge':('694427','8D5A30','AB7541'),
 'ceramic':('A44B30','B95B36','CA6B40'),
 'ceramic_rim':('B85834','D07447','E28B57'),
 'ceramic_inner':('713A28','93472C','AB5832'),
 'teal':('24313E','455569','748296'),
 'copper':('877D8A','A69AA9','C2B7C5'),
 'iron':('302A36','4E4457','706077'),
 'iron_light':('514458','79657D','A38BA5'),
 'soil':('352217','51301E','6C4228'),
 'soil_wet':('291D17','3B261A','50311D'),
 'paper':('C7B58C','DDCDA5','E9DCBA'),
 'glow':('763AB3','B35EF0','EDB0FF'),
 'glass':('695780','947CAB','B8A2C8'),
 'dewstone':('29252E','39313F','4A4051'),
 'plant_bud':('B5B5B5','E4E4E4','FFFFFF'),
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
    write_png(root/'textures/block/seed_packet.png',seed_packet())
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
    beam=[]
    for y in range(64):
        t=y/63
        beam.append([(163,81,255,round(max(0,1-abs(x-31.5)/31.5)**1.7*(1-t)**1.2*38)) for x in range(64)])
    write_png(root/'textures/effect/uv_beam.png',beam)
