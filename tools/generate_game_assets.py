#!/usr/bin/env python3
"""Generate original game art, bake vertex AO, then install only a successful result.
Blender and tools/requirements-art.txt are authoring dependencies. Ordinary Gradle
builds use the checked-in assets.
"""
from pathlib import Path
import hashlib
import json
import shutil
import struct
import subprocess
import tempfile

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/'src/main/resources/assets/stonedew'


def generate():
    from stylized_textures import generate as textures
    from equipment_art import generate as equipment
    from plant_art import generate as plants
    from reference_catalog import generate as catalog, generate_placements
    blender=shutil.which('blender')
    if not blender:
        raise SystemExit('Asset authoring requires Blender 4.x for vertex ambient occlusion. Normal Gradle builds use the checked-in baked assets.')
    with tempfile.TemporaryDirectory(prefix='stonedew-art-') as temporary:
        staged=Path(temporary)
        (staged/'models/item').mkdir(parents=True)
        textures(staged)
        shutil.copyfile(REPO/'docs/art/sources/journal-v9.png', staged/'textures/art/journal_v9.png')
        equipment_stats=equipment(staged)
        catalog_stats=catalog(staged)
        generate_placements(staged)
        stats=plants(staged)
        subprocess.run([blender,'--python-exit-code','1','--background','--factory-startup','--python',str(REPO/'tools/bake_occlusion.py'),'--',str(staged/'models')],check=True)
        for path in sorted(staged.rglob('*')):
            if not path.is_file():continue
            relative=path.relative_to(staged)
            target=(ROOT.parent/'minecraft'/relative if relative==Path('atlases/blocks.json')
                    else ROOT/relative)
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(path,target)
        # Retire only obsolete files in the generated plant mesh directory.
        for path in (ROOT/'models/block/plants').iterdir():
            if path.suffix in ('.obj','.json') and not (staged/path.relative_to(ROOT)).exists():path.unlink()
        # The rejected full-fan painting remains preserved in docs, outside runtime art.
        for name in ('cannabis_fan_v7.png','cannabis_leaflet_v8.png','materials_v6.png'):
            (ROOT/'textures/art'/name).unlink(missing_ok=True)
    reports=REPO/'docs/art';reports.mkdir(parents=True,exist_ok=True)
    for name,data in (('mesh-budget',stats),('equipment-budget',equipment_stats),('catalog-budget',catalog_stats)):
        (reports/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
    sources=[]
    for path in sorted((ROOT/'textures').rglob('*.png')):
        if path.parent.name=='item':continue
        raw=path.read_bytes()
        painted=path.name in ('materials_v9.png','cannabis_fan_v9.png','journal_v9.png','botanical_materials_v9.png','dewstone_v9.png')
        painting='docs/art/sources/'+{'materials_v9.png':'materials-v9.png','cannabis_fan_v9.png':'cannabis-fan-v9.png','journal_v9.png':'journal-v9.png','botanical_materials_v9.png':'botanical-materials-v9.png','dewstone_v9.png':'dewstone-v9.png'}.get(path.name,'')
        sources.append(dict(path=str(path.relative_to(REPO)),dimensions=list(struct.unpack('>II',raw[16:24])),
                            sha256=hashlib.sha256(raw).hexdigest(),source=painting if painted else 'tools/plant_art.py' if path.name.startswith('plant_shadow_') else 'tools/stylized_textures.py',
                            creation='Original reference-guided material painting, unchanged source; native UV swatches' if painted else 'Original authored silhouettes, palettes and material marks; deterministic generation'))
    (reports/'authored-sources.json').write_text(json.dumps(sources,indent=2)+'\n')
    print('Generated original materials, working equipment, complete reference catalog and 64 plant meshes.')
    print('Maximum plant faces (near / distant):',max(x['faces'] for x in stats if not x['lod']),
          '/',max(x['faces'] for x in stats if x['lod']))


if __name__=='__main__':generate()
