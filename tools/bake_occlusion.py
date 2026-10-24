"""Bake bounded ambient occlusion into NeoForge OBJ vertex colors with Blender BVH.

Run through Blender, invoked by generate_game_assets.py. No image manipulation.
The authored meshes remain ordinary Minecraft assets: no Blender/runtime dependency.
"""
from pathlib import Path
import math
import sys
import hashlib
import tempfile
import shutil
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def bake(path):
    payload=path.read_bytes()
    if b'\nvc ' in payload:return
    key=hashlib.sha256(Path(__file__).read_bytes()+payload).hexdigest()
    cache_path=Path(tempfile.gettempdir())/'stonedew-ao-cache'/f'{key}.obj'
    if cache_path.exists() and not path.stem.endswith('_body'):
        shutil.copyfile(cache_path,path)
        return
    lines=payload.decode().splitlines();verts=[];normals=[];faces=[];material=''
    for line in lines:
        p=line.split()
        if not p:continue
        if p[0]=='v':verts.append(tuple(map(float,p[1:4])))
        elif p[0]=='vn':normals.append(tuple(map(float,p[1:4])))
        elif p[0]=='usemtl':material=p[1]
        elif p[0]=='f':faces.append((material,[list(map(int,v.split('/'))) for v in p[1:]]))
    if path.stem.endswith('_body'):
        # Keep whole-prop occlusion / lit-preview reflections when separating draw passes.
        whole=path.with_name(path.stem.removesuffix('_body')+'.obj')
        bake(whole)
        full_v=[];full_n=[];full_c=[];lookup={}
        for line in whole.read_text().splitlines():
            p=line.split()
            if not p:continue
            if p[0]=='v':full_v.append(tuple(map(float,p[1:4])))
            elif p[0]=='vn':full_n.append(tuple(map(float,p[1:4])))
            elif p[0]=='vc':full_c.append(tuple(map(float,p[1:5])))
            elif p[0]=='f':
                for ref in p[1:]:
                    v,_,n,c=map(int,ref.split('/'))
                    lookup[(full_v[v-1],full_n[n-1])]=full_c[c-1]
        colors=[];indices={};rewritten=[]
        for material,face in faces:
            for v in face:
                color=lookup[(verts[v[0]-1],normals[v[2]-1])]
                if color not in indices:colors.append(color);indices[color]=len(colors)
                v.append(indices[color])
            rewritten.append('f '+' '.join('/'.join(map(str,v)) for v in face))
        out=[];i=0
        for line in lines:
            if line.startswith('f '):out.append(rewritten[i]);i+=1
            else:out.append(line)
        insert=next(i for i,l in enumerate(out) if l.startswith('f '))
        out[insert:insert]=['vc '+' '.join(f'{v:.5f}' for v in color) for color in colors]
        path.write_text('\n'.join(out)+'\n')
        cache_path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,cache_path)
        return
    tree=BVHTree.FromPolygons(verts,[[v[0]-1 for v in face] for material,face in faces
                                   if material not in ('emission_halo','emission_aura')],all_triangles=False)
    light_points=[]
    if path.parent.name=='catalog':
        for mat,face in faces:
            if mat in ('emission','emission_core','white_emission') and normals[face[0][2]-1][1]<-.5:
                c=sum((Vector(verts[v[0]-1]) for v in face),Vector())/len(face)
                c.y-=.003
                if all((c-p).length>.08 for p in light_points):light_points.append(c)
    samples=[]
    for i in range(16):
        r=math.sqrt((i+.5)/16);a=i*2.399963229728653
        samples.append((r*math.cos(a),r*math.sin(a),math.sqrt(1-r*r)))
    cache={};shadow_cache={};colors=[];color_indices={}
    plant=path.parent.name=='plants'
    key_light=Vector((-.45,.82,-.35)).normalized()
    for material,face in faces:
        # Emissive lenses and light cores must not receive baked shadows.
        emission=material.startswith('emission') or material in ('cyan_emission','white_emission')
        foliage=material.startswith(('leaf','sugar_leaf'))
        floral=material.startswith('bud')
        center=sum((Vector(verts[v[0]-1]) for v in face),Vector())/len(face)
        for v in face:
            p=Vector(verts[v[0]-1]);n=Vector(normals[v[2]-1]);key=(1 if foliage else 2 if floral else 0,)+tuple(round(t,5) for t in (*p,*n))
            if emission or material=='hair':ao=1
            elif key in cache:ao=cache[key]
            else:
                # Tiny inward barycentric offset keeps coplanar edges stable.
                origin=p.lerp(center,.035)+n*.0015
                tangent=n.cross(Vector((0,0,1) if abs(n.z)<.9 else (0,1,0))).normalized()
                bitangent=n.cross(tangent);visibility=0
                for x,y,z in samples:
                    direction=tangent*x+bitangent*y+n*z
                    location,_,_,distance=tree.ray_cast(origin,direction,.33)
                    visibility+=1 if location is None else min(1,(distance/.33)**.60)
                ao=(.88+.12*visibility/len(samples)) if foliage else (.78+.22*visibility/len(samples)) if floral else (.53+.47*visibility/len(samples))
                cache[key]=ao
            if plant and not emission and material!='hair':
                # Cast foliage/flower shadows are separate from ambient occlusion.
                # This authored key fills the deep spaces between overlapping fans;
                # runtime entity lighting is still applied once to surface normals.
                if key not in shadow_cache:
                    origin=p.lerp(center,.02)+n*.0015
                    hits=0
                    for offset in ((0,0,0),(.045,0,-.02),(-.025,0,.04)):
                        direction=(key_light+Vector(offset)).normalized()
                        hit,_,_,_=tree.ray_cast(origin,direction,1.5)
                        hits+=hit is None
                    shadow_cache[key]=hits/3
                shade=shadow_cache[key]
                ao*= (.88+.12*shade) if foliage else (.84+.16*shade) if floral else (.76+.24*shade)
            # Static lit reference previews also bake occlusion-aware violet reflections.
            # Working P1 plants still get their actual fuel-dependent UV light at runtime.
            uv=0
            if light_points and not emission:
                origin=p+n*.002
                for light in light_points:
                    delta=light-origin;distance=delta.length
                    if distance<.005:continue
                    direction=delta/distance;cosine=max(0,n.dot(direction))
                    if cosine<=0:continue
                    hit,_,_,_=tree.ray_cast(origin,direction,max(0,distance-.004))
                    if hit is None:uv+=cosine/(.35+distance*distance)
                uv=min(1,uv/max(1,len(light_points))*2.4)
            color=tuple(round(max(0,min(1,c))*63)/63 for c in (ao+.05*uv,ao*(1-.48*uv),ao+.45*uv))+(1,)
            if color not in color_indices:
                colors.append(color);color_indices[color]=len(colors)
            v.append(color_indices[color])
    out=[];i=0
    for line in lines:
        if line.startswith('f '):
            _,face=faces[i];i+=1
            out.append('f '+' '.join('/'.join(map(str,v)) for v in face))
        else:out.append(line)
    insert=next(i for i,l in enumerate(out) if l.startswith('f '))
    out[insert:insert]=['vc '+' '.join(f'{v:.5f}' for v in color) for color in colors]
    path.write_text('\n'.join(out)+'\n')
    cache_path.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(path,cache_path)


root=Path(sys.argv[sys.argv.index('--')+1])
paths=sorted(p for p in root.rglob('*.obj') if not p.stem.endswith('_lod'))
for i,path in enumerate(paths):
    bake(path)
    if i%8==0:print(f'AO {i+1}/{len(paths)}: {path.name}',flush=True)
print(f'Baked vertex ambient occlusion for {len(paths)} meshes.',flush=True)
