#!/usr/bin/env python3
"""Regenerate original Stonedew geometry, authored pixel art and integrity manifests."""
from pathlib import Path
import hashlib
import json
import struct

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/'src/main/resources/assets/stonedew'


def generate():
    from stylized_textures import generate as textures
    from equipment_art import generate as equipment
    from plant_art import generate as plants
    textures(ROOT)
    equipment_stats=equipment(ROOT)
    stats=plants(ROOT)
    reports=REPO/'docs/art'
    reports.mkdir(parents=True,exist_ok=True)
    for name,data in (('mesh-budget',stats),('equipment-budget',equipment_stats)):
        (reports/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
    sources=[]
    for path in sorted((ROOT/'textures').rglob('*.png')):
        if path.parent.name=='item':continue # unchanged legacy particle identity
        raw=path.read_bytes()
        sources.append(dict(path=str(path.relative_to(REPO)),dimensions=list(struct.unpack('>II',raw[16:24])),
                            sha256=hashlib.sha256(raw).hexdigest(),source='tools/stylized_textures.py',
                            creation='Original authored silhouettes, palettes and material marks; deterministic generation'))
    (reports/'authored-sources.json').write_text(json.dumps(sources,indent=2)+'\n')
    print('Generated original pixel materials, rebuilt equipment and 64 shaded plant meshes.')
    print('Maximum plant faces (near / distant):',max(x['faces'] for x in stats if not x['lod']),
          '/',max(x['faces'] for x in stats if x['lod']))


if __name__=='__main__':generate()
