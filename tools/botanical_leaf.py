"""Read the original leaf's alpha contour to author foliage geometry.

The image is never edited, resized or rewritten. Native 256px atlas windows cover
the complete painting, including its petiole and all seven leaflet tips. Pillow
and NumPy are used only to READ alpha for the original mesh topology.
"""
from functools import lru_cache
from pathlib import Path
import json
import math
import shutil

SOURCE=Path(__file__).resolve().parents[1]/'docs/art/sources/cannabis-fan-v7.png'
TILE=256


def area(polygon):
    return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(polygon,polygon[1:]+polygon[:1]))/2


def clip(polygon, axis, bound, greater):
    result=[]
    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
        da=a[axis]-bound;db=b[axis]-bound
        inside_a=da>=-1e-8 if greater else da<=1e-8
        inside_b=db>=-1e-8 if greater else db<=1e-8
        if inside_a:result.append(a)
        if inside_a!=inside_b:
            t=da/(da-db);result.append(tuple(x+(y-x)*t for x,y in zip(a,b)))
    clean=[]
    for p in result:
        if not clean or math.dist(p,clean[-1])>1e-7:clean.append(p)
    if len(clean)>1 and math.dist(clean[0],clean[-1])<1e-7:clean.pop()
    return clean


@lru_cache(maxsize=1)
def profile():
    from PIL import Image
    import numpy as np
    with Image.open(SOURCE) as source:
        if source.mode!='RGBA':raise ValueError('Botanical leaf source must retain original RGBA alpha')
        rgba=np.asarray(source)
        height,width=rgba.shape[:2]
        alpha=rgba[:,:,3]
        ys,xs=np.nonzero(alpha>=128)
        root_y=float(ys.max())
        bottom=xs[ys>=root_y-8]
        root_x=float(bottom.mean())
        length=root_y-float(ys.min())
        size=48
        mask=set()
        for y in range(size):
            for x in range(size):
                region=alpha[y*height//size:(y+1)*height//size,x*width//size:(x+1)*width//size]
                if region.max()>=96:mask.add((x,y))
    # Conservative mesh margin lets the texture preserve every fine serration.
    mask={(x+dx,y+dy) for x,y in mask for dx,dy in ((0,0),(-1,0),(1,0),(0,-1),(0,1))
          if 0<=x+dx<size and 0<=y+dy<size}
    unseen=set(mask);components=[]
    while unseen:
        start=min(unseen);unseen.remove(start);component={start};queue=[start]
        while queue:
            x,y=queue.pop()
            for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if p in unseen:unseen.remove(p);component.add(p);queue.append(p)
        components.append(component)
    mask=max(components,key=len)
    # Merge neighboring opaque coverage into short rectangles. Native cutout
    # retains the painted serrations, while coarse geometry avoids a huge mesh.
    rectangles=[];active={}
    for y in range(size):
        spans=[];x=0
        while x<size:
            if (x,y) not in mask:x+=1;continue
            start=x
            while x<size and (x,y) in mask:x+=1
            spans.append((start,x))
        for span in list(active):
            if span not in spans:
                first,last=active.pop(span);rectangles.append((*span,first,last))
        for span in spans:active[span]=(active[span][0],y+1) if span in active else (y,y+1)
    rectangles += [(*span,first,last) for span,(first,last) in active.items()]
    pieces=[]
    cols=math.ceil(width/TILE);rows=math.ceil(height/TILE)
    for x0,x1,y0,y1 in rectangles:
        rectangle=[(x0*width/size,y0*height/size),(x1*width/size,y0*height/size),
                   (x1*width/size,y1*height/size),(x0*width/size,y1*height/size)]
        for row in range(rows):
            for col in range(cols):
                part=rectangle
                for axis,bound,greater in ((0,col*TILE,True),(0,min(width,(col+1)*TILE),False),
                                           (1,row*TILE,True),(1,min(height,(row+1)*TILE),False)):
                    part=clip(part,axis,bound,greater)
                    if len(part)<3:break
                if len(part)<3 or abs(area(part))<1e-5:continue
                window_x=min(col*TILE,width-TILE);window_y=min(row*TILE,height-TILE)
                uv=[((x-window_x)/TILE,(y-window_y)/TILE) for x,y in part]
                pieces.append((col,row,part,uv))
    return dict(width=width,height=height,root=(root_x,root_y),length=length,
                pieces=pieces,cols=cols,rows=rows)


def generate(root):
    data=profile()
    target=root/'textures/art/cannabis_fan_v7.png';target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(SOURCE,target)
    regions=[]
    for row in range(data['rows']):
        for col in range(data['cols']):
            regions.append(dict(sprite=f'stonedew:block/botanical/leaf_{col}_{row}',
                                x=min(col*TILE,data['width']-TILE),y=min(row*TILE,data['height']-TILE),
                                width=TILE,height=TILE))
    path=root/'atlases/blocks.json';atlas=json.loads(path.read_text())
    atlas['sources'].append(dict(type='minecraft:unstitch',resource='stonedew:art/cannabis_fan_v7',
                                divisor_x=data['width'],divisor_y=data['height'],regions=regions))
    path.write_text(json.dumps(atlas,indent=2)+'\n')
