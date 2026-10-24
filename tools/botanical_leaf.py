"""Bind an unchanged five-finger painting and read alpha to author compact geometry.

Pillow/NumPy only READ the source. The engine's native atlas selects a power-of-two
window; no reference/source image is cropped, resized, edited or rewritten.
"""
from functools import lru_cache
from pathlib import Path
import json
import math
import shutil

SOURCE=Path(__file__).resolve().parents[1]/'docs/art/sources/cannabis-fan-v9.png'
SPRITE='stonedew:block/botanical/fan_v9'


@lru_cache(maxsize=1)
def profile():
    from PIL import Image
    import numpy as np
    with Image.open(SOURCE) as image:
        if image.mode!='RGBA':raise ValueError('Fan painting must retain its original alpha')
        rgba=np.asarray(image);height,width=rgba.shape[:2];alpha=rgba[:,:,3]
        ys,xs=np.nonzero(alpha>=128)
        left,right=int(xs.min()),int(xs.max());top,bottom=int(ys.min()),int(ys.max())
        root_x=float(xs[ys>=bottom-7].mean());root_y=float(bottom)
        length=bottom-top
        window_w=2**math.ceil(math.log2(right-left+9))
        window_h=2**math.ceil(math.log2(bottom-top+9))
        if window_w>width or window_h>height:
            raise ValueError('Original fan needs more transparent canvas padding for native atlas windows')
        window_x=max(0,min(width-window_w,(left+right-window_w)//2))
        window_y=max(0,min(height-window_h,(top+bottom-window_h)//2))
        pieces=[]
        # Four folded patches cover a WHOLE five-finger painting. Transparent
        # gaps carry the serration; no per-tooth or per-finger geometry.
        for i in range(2):
            y0=top+length*i/2;y1=top+length*(i+1)/2
            for x0,x1 in ((left-2,root_x),(root_x,right+2)):
                polygon=[(x0,y1),(x0,y0),(x1,y0),(x1,y1)]
                uv=[((x-window_x)/window_w,(y-window_y)/window_h) for x,y in polygon]
                pieces.append((polygon,uv))
    return dict(width=width,height=height,root=(root_x,root_y),length=length,pieces=pieces,
                window=(window_x,window_y,window_w,window_h),bounds=(left,top,right,bottom))


def generate(root):
    data=profile();target=root/'textures/art/cannabis_fan_v9.png'
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(SOURCE,target)
    x,y,w,h=data['window'];region=dict(sprite=SPRITE,x=x,y=y,width=w,height=h)
    path=root/'atlases/blocks.json';atlas=json.loads(path.read_text())
    atlas['sources'].append(dict(type='minecraft:unstitch',resource='stonedew:art/cannabis_fan_v9',
                                divisor_x=data['width'],divisor_y=data['height'],regions=[region]))
    source=SOURCE.with_name('botanical-materials-v9.png')
    shutil.copyfile(source,root/'textures/art/botanical_materials_v9.png')
    import struct
    width,height=struct.unpack('>II',source.read_bytes()[16:24])
    regions=[]
    for i,name in enumerate(('bud','stem','leaf','sugar')):
        regions.append(dict(sprite='stonedew:block/botanical/'+name,
                            x=round((i%2+.5)*width/2)-128,
                            y=round((i//2+.5)*height/2)-128,width=256,height=256))
    atlas['sources'].append(dict(type='minecraft:unstitch',resource='stonedew:art/botanical_materials_v9',
                                divisor_x=width,divisor_y=height,regions=regions))
    path.write_text(json.dumps(atlas,indent=2)+'\n')
