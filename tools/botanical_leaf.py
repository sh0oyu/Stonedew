"""Bind an unchanged leaflet painting and read alpha to author compact geometry.

Pillow/NumPy only READ the source. The engine's native atlas selects a power-of-two
window; no reference/source image is cropped, resized, edited or rewritten.
"""
from functools import lru_cache
from pathlib import Path
import json
import math
import shutil

SOURCE=Path(__file__).resolve().parents[1]/'docs/art/sources/cannabis-leaflet-v8.png'
SPRITE='stonedew:block/botanical/leaflet_v8'


@lru_cache(maxsize=1)
def profile():
    from PIL import Image
    import numpy as np
    with Image.open(SOURCE) as image:
        if image.mode!='RGBA':raise ValueError('Leaflet painting must retain its original alpha')
        rgba=np.asarray(image);height,width=rgba.shape[:2];alpha=rgba[:,:,3]
        ys,xs=np.nonzero(alpha>=128)
        left,right=int(xs.min()),int(xs.max());top,bottom=int(ys.min()),int(ys.max())
        root_x=float(xs[ys>=bottom-7].mean());root_y=float(bottom)
        length=bottom-top
        window_w=2**math.ceil(math.log2(right-left+9))
        window_h=2**math.ceil(math.log2(bottom-top+9))
        if window_w>width or window_h>height:
            raise ValueError('Original leaflet needs more transparent canvas padding for native atlas windows')
        window_x=max(0,min(width-window_w,(left+right-window_w)//2))
        window_y=max(0,min(height-window_h,(top+bottom-window_h)//2))
        pieces=[]
        for i in range(6):
            y0=top+length*i/6;y1=top+length*(i+1)/6
            band=alpha[math.floor(y0):math.ceil(y1)+1]
            _,opaque=np.nonzero(band>=80)
            x0=max(window_x,int(opaque.min())-3);x1=min(window_x+window_w,int(opaque.max())+3)
            for start,end in ((x0,root_x),(root_x,x1)):
                polygon=[(start,y1),(start,y0),(end,y0),(end,y1)]
                uv=[((x-window_x)/window_w,(y-window_y)/window_h) for x,y in polygon]
                pieces.append((polygon,uv))
    return dict(width=width,height=height,root=(root_x,root_y),length=length,pieces=pieces,
                window=(window_x,window_y,window_w,window_h),bounds=(left,top,right,bottom))


def generate(root):
    data=profile();target=root/'textures/art/cannabis_leaflet_v8.png'
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(SOURCE,target)
    x,y,w,h=data['window'];region=dict(sprite=SPRITE,x=x,y=y,width=w,height=h)
    path=root/'atlases/blocks.json';atlas=json.loads(path.read_text())
    atlas['sources'].append(dict(type='minecraft:unstitch',resource='stonedew:art/cannabis_leaflet_v8',
                                divisor_x=data['width'],divisor_y=data['height'],regions=[region]))
    path.write_text(json.dumps(atlas,indent=2)+'\n')
