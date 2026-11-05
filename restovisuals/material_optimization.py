"""One bounded compact material bake/comparison; reuses the D3D11 renderer."""
import hashlib
import json
import math
import statistics
import struct
import time
from pathlib import Path

from .d3d11_validation import D3D11Session, compile_validation_program, execute_texture
from .gpu_demo import PROFILES, _output_path, png_bytes
from .material_demo import probe_positions, verify_material
from .material_reference import shade, shade_surface, surface

ROOT = Path(__file__).resolve().parents[1]


def bake_material(size=256, domain=1):
    if type(size) is not int or size not in (256,512) or type(domain) is not int or domain not in (1,2):
        raise ValueError('Only two bounded fixture sizes and domain probes are supported')
    return b''.join(struct.pack('<4e',*surface((x+.5)/size*domain,(y+.5)/size*domain))
                    for y in range(size) for x in range(size))


def sample_material(packed,size,u,v,parameters):
    """Half-float texels, linear clamp sampling, slope strength and renormalization."""
    x,y=u*size-.5,v*size-.5
    ix,iy=math.floor(x),math.floor(y);fx,fy=x-ix,y-iy
    def texel(dx,dy):
        return struct.unpack_from('<4e',packed,(max(0,min(size-1,iy+dy))*size+max(0,min(size-1,ix+dx)))*8)
    a,b,c,d=texel(0,0),texel(1,0),texel(0,1),texel(1,1)
    p=[(1-fy)*((1-fx)*a[i]+fx*b[i])+fy*((1-fx)*c[i]+fx*d[i]) for i in range(4)]
    n,r,_=parameters
    gx,gy=n*p[0]/max(p[2],.001),n*p[1]/max(p[2],.001)
    length=math.sqrt(1+gx*gx+gy*gy)
    return (gx/length,gy/length,1/length,.64+r*(p[3]-.64))


def shader_sources(domain=1):
    original=(ROOT/'shaders/RV_MaterialRealism.hlsl').read_text(encoding='utf-8')
    fragment=(ROOT/'shaders/RV_MaterialTextureSurface.hlsl').read_text(encoding='utf-8')
    start=original.index('float4 surface(float2 uv)')
    end=original.index('\nfloat4 PSMaterialNormals(',start)
    sampled=original[:start]+fragment+original[end:]
    # A single optional material-frequency probe, applied equally to both paths.
    def coordinate(source):
        return source.replace('surface(input.uv)',f'surface(input.uv * {domain}.0)')
    return coordinate(original),f'#define RV_DOMAIN {domain}.0\n'+coordinate(sampled)


def compare_readbacks(procedural,sampled):
    if len(procedural)!=len(sampled) or not procedural or len(sampled)%16:
        raise ValueError('Comparison buffer shape mismatch')
    squared=maximum=0.0;count=0
    for a,b in zip(struct.iter_unpack('<4f',procedural),struct.iter_unpack('<4f',sampled)):
        for x,y in zip(a[:3],b[:3]):
            if not math.isfinite(x) or not math.isfinite(y):raise ValueError('Nonfinite comparison')
            error=abs(x-y);squared+=error*error;maximum=max(maximum,error);count+=1
    return {'all_pixel_rgb_rmse':math.sqrt(squared/count),'all_pixel_rgb_max_error':maximum}


def optimize_material(adapter_index,output_dir,*,texture_size=256,profile='both',domain=1):
    if profile not in (*PROFILES,'both'):raise ValueError('Unknown comparison profile')
    output=_output_path(output_dir)
    started=time.perf_counter();packed=bake_material(texture_size,domain)
    bake_ms=(time.perf_counter()-started)*1000
    output.mkdir(parents=True,exist_ok=False)
    output.joinpath('fixture.rgba16f').write_bytes(packed)
    sources=shader_sources(domain)
    binaries={};compilation={}
    result={'status':'running','texture_size':texture_size,'domain':domain,'format':'RGBA16F normal XYZ + roughness',
            'texture_payload_bytes':len(packed),'texture_sha256':hashlib.sha256(packed).hexdigest(),
            'bake_cpu_wall_ms':bake_ms,'compilation':compilation,'cases':[],'diagnostics':[],
            'quality':[],'artifacts':{},'geometry_vertices':3,'window_created':False,'gameplay_validated':False,
            'quality_targets_proposed':{'rgb_rmse_max':.002,'normal_angle_p95_degrees_max':3},
            'timing':'median of 3 interleaved 5-draw batches; 2 warmups each; allocations/upload/readback excluded'}
    session=None;rows=[]
    try:
        for label,source in zip(('procedural','texture'),sources):
            path=output/f'{label}.hlsl';path.write_text(source,encoding='utf-8')
            binaries[label],compilation[label]=compile_validation_program(path,pixel_entries=('PSMaterial','PSMaterialNormals'))
        with D3D11Session(adapter_index) as session:
            result['adapter']=session.adapter
            if session.adapter['vendor_id']!=0x1002 or session.adapter['device_id']!=0x731f:
                raise ValueError('Explicit RX 5700 XT required for this comparison')
            shaders={label:{name:session.shader(12 if name=='VSFullscreen' else 15,code)
                            for name,code in programs.items()} for label,programs in binaries.items()}
            def reference(label,u,v,params,normals):
                if label=='texture':
                    material=sample_material(packed,texture_size,u,v,params)
                    return material if normals else shade_surface(material,params[2])
                return surface(u*domain,v*domain,*params[:2]) if normals else shade(u*domain,v*domain,*params)
            def draw(label,width,height,params,normals=False):
                raw,receipt=execute_texture(session,shaders[label],width,height,'rgba32f',
                    'PSMaterialNormals' if normals else 'PSMaterial',params,packed if label=='texture' else None,
                    draws=5,warmup=2,material_texture_size=texture_size if label=='texture' else None)
                started=time.perf_counter()
                receipt.update(verify_material(raw,width,height,params,normals=normals,
                    reference=lambda u,v,p,n:reference(label,u,v,p,n),cpu_tolerance=.002 if normals else .0004))
                receipt['cpu_validation_wall_ms']=(time.perf_counter()-started)*1000
                receipt['backend']=label
                if (not receipt['passed'] or receipt['gpu_duration_ms'] is None
                        or receipt['owned_com_references_before']!=receipt['owned_com_references_after']):
                    result['diagnostics'].append(receipt);raise ValueError('Texture comparison correctness/timing/cleanup gate failed')
                return raw,receipt
            # Small checks include fractional strength and independent switches.
            for label in ('procedural','texture'):
                for params in ((0,0,1),(1,0,1),(0,1,-1),(.5,.5,1),(1,1,-1)):
                    for normal_pass in (False,True):
                        _,receipt=draw(label,32,24,params,normal_pass);result['diagnostics'].append(receipt)
            profiles=list(PROFILES.items()) if profile=='both' else [(profile,PROFILES[profile])]
            for name,(width,height) in profiles:
                for side in (-1,1):
                    raw_images={};receipts={label:[] for label in ('flat','procedural','texture')}
                    for repeat in range(3):
                        for label in (('flat','procedural','texture') if repeat%2==0 else ('texture','procedural','flat')):
                            raw,receipt=draw('procedural' if label=='flat' else label,width,height,
                                             (0,0,side) if label=='flat' else (1,1,side))
                            if label in raw_images and raw_images[label]!=raw:raise ValueError('Nondeterministic comparison')
                            raw_images[label]=raw;receipts[label].append(receipt)
                    light='left' if side<0 else 'right'
                    for label in receipts:
                        filename=f'{name}-{light}-{label}.png';started=time.perf_counter()
                        image=png_bytes(raw_images[label],width,height,'rgba32f',linear=True)
                        output.joinpath(filename).write_bytes(image);result['artifacts'][filename]=hashlib.sha256(image).hexdigest()
                        result['cases'].append({'profile':name,'light':light,'backend':label,'samples':receipts[label],
                            'gpu_ms_per_draw_median':statistics.median(r['gpu_duration_ms']/5 for r in receipts[label]),
                            'png_export_wall_ms':(time.perf_counter()-started)*1000})
                    disabled,receipt=draw('texture',width,height,(0,0,side))
                    receipt['disable_exact_against_procedural_flat']=disabled==raw_images['flat']
                    result['diagnostics'].append(receipt)
                    if disabled!=raw_images['flat']:raise ValueError('Disabled texture path differs from flat baseline')
                    q=compare_readbacks(raw_images['procedural'],raw_images['texture'])
                    q.update({'profile':name,'light':light});result['quality'].append(q)
                    rows.append((f'{name}, {light} light',[f'{name}-{light}-{b}.png' for b in ('flat','procedural','texture')]))
                diagnostics={}
                for label in ('procedural','texture'):
                    raw,receipt=draw(label,width,height,(1,1,1),True)
                    result['diagnostics'].append(receipt);diagnostics[label]=raw
                angles=[]
                for x,y in probe_positions(width,height):
                    a=struct.unpack_from('<4f',diagnostics['procedural'],(y*width+x)*16)
                    b=struct.unpack_from('<4f',diagnostics['texture'],(y*width+x)*16)
                    cosine=sum(x*y for x,y in zip(a[:3],b[:3]))/math.sqrt(sum(x*x for x in a[:3])*sum(x*x for x in b[:3]))
                    angles.append(math.degrees(math.acos(max(-1,min(1,cosine)))))
                result['quality'].append({'profile':name,'normal_angle_samples':len(angles),
                    'normal_angle_p95_degrees':sorted(angles)[math.ceil(.95*len(angles))-1],'normal_angle_max_degrees':max(angles)})
        result['status']='passed'
        html=''.join('<section><h2>'+label+'</h2><div>'+''.join(f'<figure><figcaption>{caption}</figcaption><img src="{file}"></figure>'
            for caption,file in zip(('Flat','Preserved procedural model','Compact sampled model'),files))+'</div></section>' for label,files in rows)
        output.joinpath('index.html').write_text('<!doctype html><meta charset="utf-8"><title>Original material optimization comparison</title>'
            '<style>body{font:16px system-ui;background:#181b20;color:#eee;margin:2rem}section>div{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}figure{margin:0}img{width:100%}</style>'
            '<h1>Synthetic material: procedural versus texture</h1><p>Identical geometry, light, albedo, material strength and output format within each row. '
            f'Texture {texture_size} square, RGBA16F; material domain {domain}. No game integration or FPS claim. '
            '<a href="report.json">Raw timings, numerical and resource receipts</a>.</p>'+html,encoding='utf-8')
    except Exception as error:
        result.update({'status':'failed','failure_type':type(error).__name__,'failure':str(error)});raise
    finally:
        result['native_device_created']=session is not None
        result['owned_context_released']=session is None or not session.owned
        output.joinpath('report.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return result
