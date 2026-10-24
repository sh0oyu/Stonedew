"""Bind the unchanged original material painting through Minecraft's atlas loader.

The engine's native unstitch source selects 256px material swatches. No resampling,
postprocessing or Python image editing is performed. The complete source PNG is
packaged unchanged outside textures/block so it cannot lower block-atlas mip levels.
"""
from pathlib import Path
import json
import shutil
import struct

SOURCE=Path(__file__).resolve().parents[1]/'docs/art/sources/materials-v9.png'
TILES=('ceramic','ceramic_rim','wood','wood_edge',
       'iron','iron_light','fabric','lining',
       'teal','copper','soil','soil_wet',
       'paper','glass','cyan','recess')
ALIASES={'ceramic_inner':'ceramic','glow':'glass','fabric':'fabric'}


def sprite(name):
    name=ALIASES.get(name,name)
    return f'stonedew:block/painted/{name}' if name in TILES else f'stonedew:block/{name}'


def generate(root):
    target=root/'textures/art/materials_v9.png'
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(SOURCE,target)
    width,height=struct.unpack('>II',SOURCE.read_bytes()[16:24])
    regions=[]
    for i,name in enumerate(TILES):
        # Inset native UV windows avoid the neighboring material and preserve
        # power-of-two sprite dimensions without changing the source painting.
        x=round((i%4+.5)*width/4)-128
        y=round((i//4+.5)*height/4)-128
        regions.append(dict(sprite=f'stonedew:block/painted/{name}',x=x,y=y,width=256,height=256))
    atlas=dict(sources=[dict(type='minecraft:unstitch',resource='stonedew:art/materials_v9',
                            divisor_x=width,divisor_y=height,regions=regions)])
    source=SOURCE.with_name('dewstone-v9.png')
    shutil.copyfile(source,root/'textures/art/dewstone_v9.png')
    dw,dh=struct.unpack('>II',source.read_bytes()[16:24])
    atlas['sources'].append(dict(type='minecraft:unstitch',resource='stonedew:art/dewstone_v9',
                                divisor_x=dw,divisor_y=dh,regions=[dict(sprite='stonedew:block/painted/dewstone',x=(dw-512)//2,y=(dh-512)//2,width=512,height=512)]))
    path=root/'atlases/blocks.json';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(atlas,indent=2)+'\n')
