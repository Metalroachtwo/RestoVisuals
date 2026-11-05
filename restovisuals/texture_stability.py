"""Bounded geometric/filtering experiments through the existing D3D11 executor."""
import hashlib
import json
import math
import statistics
import struct
import sys
import time
from pathlib import Path

from .d3d11_validation import D3D11Session,compile_validation_program,execute_texture
from .gpu_demo import PROFILES,_output_path,png_bytes
from .material_demo import probe_positions
from .material_mips import build_mips,camera_parameters,decode_moment,periodic_surface,plane_coordinates,sample_moment
from .material_reference import shade_surface,surface
from .material_optimization import compare_readbacks

ROOT=Path(__file__).resolve().parents[1]
VIEWS={'front-near':(0,2),'front-far':(0,8),'moderate':(55,4),'grazing-near':(78,2),'grazing-far':(78,8)}


def stability_source(backend,ssaa=1,explicit_lod=-1):
    if backend not in ('original','periodic','texture') or ssaa not in (1,4,8) or explicit_lod not in (-1,0,3,8,9):
        raise ValueError('Unsupported bounded stability program')
    original=(ROOT/'shaders/RV_MaterialRealism.hlsl').read_text(encoding='utf-8')
    prefix=original[:original.index('float4 PSMaterialNormals(')].replace('float reserved;','float reserved;\n    float4 fixture;')
    tail=original[original.index('float4 PSMaterial(PixelInput input)'):]
    body=tail[tail.index('{')+1:tail.rindex('}')]
    body=body.replace('    float4 material = surface(input.uv);\n','',1)
    body=body.replace('float3 v = float3(0,0,1), h = normalize(l+v);','float3 h = normalize(l+v);',1)
    shared='float4 rvShade(float4 material,float3 v)\n{'+body+'}\n'
    library=(ROOT/'shaders/RV_TextureStability.hlsl').read_text(encoding='utf-8').replace('// RV_SHARED_BRDF',shared)
    return f'#define RV_BACKEND {("original","periodic","texture").index(backend)}\n#define RV_SSAA {ssaa}\n#define RV_EXPLICIT_LOD {int(explicit_lod>=0)}\n#define RV_LOD {max(0,explicit_lod)}\n'+prefix+library


def write_programs(output):
    programs={};metadata={}
    choices=[('original',1,-1),('periodic',1,-1),('periodic',4,-1),('periodic',8,-1),
             ('texture',1,-1),('texture',1,0),('texture',1,3),('texture',1,8),('texture',1,9)]
    for backend,ssaa,lod in choices:
        key=f'{backend}-{ssaa}-{lod}';source=stability_source(backend,ssaa,lod)
        path=output/f'{key}.hlsl';path.write_text(source,encoding='utf-8')
        programs[key],metadata[key]=compile_validation_program(path,pixel_entries=('PSMaterial','PSMaterialNormals','PSFixtureCoordinates'))
    return programs,metadata


def verify_frame(raw,width,height,*,normal=False):
    if len(raw)!=width*height*16:raise ValueError('Bad fixture readback shape')
    maximum=0.0;lo=1.0;hi=0.0;clipped=0
    for p in struct.iter_unpack('<4f',raw):
        if not all(math.isfinite(x) for x in p):raise ValueError('Nonfinite fixture output')
        if normal:
            maximum=max(maximum,abs(math.sqrt(sum(x*x for x in p[:3]))-1));lo=min(lo,p[3]);hi=max(hi,p[3])
        elif p[3]!=1:raise ValueError('Fixture color alpha changed')
        else:clipped+=any(x>1 or x<0 for x in p[:3])
    if normal and (maximum>2e-6 or lo<.419 or hi>.981):raise ValueError('Decoded normal/roughness contract failed')
    return {'all_pixels_finite':True,'all_pixels_alpha_one':not normal,
            'normal_length_max_error':maximum if normal else None,'roughness_range':[lo,hi] if normal else None,
            'preview_clipped_pixels':clipped if not normal else None,'readback_sha256':hashlib.sha256(raw).hexdigest()}


def image_metrics(raw,reference,width,height):
    if len(raw)!=len(reference) or len(raw)!=width*height*16:raise ValueError('Quality image shape mismatch')
    squared=maximum=0.0;bands={'top':[],'bottom':[]}
    # Row-centered luminance variance measures detail separately from broad view-angle shading.
    for y in range(height):
        a=memoryview(raw)[y*width*16:(y+1)*width*16];b=memoryview(reference)[y*width*16:(y+1)*width*16]
        sums=[0.0,0.0];squares=[0.0,0.0]
        for p,q in zip(struct.iter_unpack('<4f',a),struct.iter_unpack('<4f',b)):
            for x,z in zip(p[:3],q[:3]):
                error=abs(x-z);squared+=error*error;maximum=max(maximum,error)
            for i,v in enumerate((p,q)):
                luminance=.2126*v[0]+.7152*v[1]+.0722*v[2];sums[i]+=luminance;squares[i]+=luminance*luminance
        key='top' if y<height//4 else 'bottom' if y>=3*height//4 else None
        if key:bands[key].append(tuple(max(0,squares[i]/width-(sums[i]/width)**2) for i in (0,1)))
    ratios={key:math.sqrt(sum(v[0] for v in rows)/max(sum(v[1] for v in rows),1e-20)) for key,rows in bands.items()}
    return {'rgb_rmse_vs_4x4':math.sqrt(squared/(width*height*3)),'rgb_max_error_vs_4x4':maximum,
            'row_centered_detail_std_ratio_vs_4x4':ratios}


class StabilityDevice:
    """Experiment orchestration only; all allocation/draw/readback stays in D3D11Session."""
    def __init__(self,session,binaries,maps):
        self.session=session;self.maps=maps;self.shaders={}
        vertex=None
        for key,program in binaries.items():
            shaders={}
            for entry,code in program.items():
                if entry=='VSFullscreen':
                    if vertex is None:vertex=session.shader(12,code)
                    shaders[entry]=vertex
                else:shaders[entry]=session.shader(15,code)
            self.shaders[key]=shaders

    def draw(self,key,fixture,width,height,*,size=512,filter_name='trilinear',mips=True,compensation=0,
             entry='PSMaterial',parameters=(1,1,1),repeat=1):
        texture=key.startswith('texture');levels=self.maps[size][0]
        options={'fixture_parameters':fixture,'roughness_compensation':compensation}
        if texture:options.update(material_texture_size=size,material_mips=levels if mips else None,
                                  material_filter=filter_name,material_wrap=True)
        frames=[];samples=[]
        for _ in range(repeat):
            started=time.perf_counter()
            raw,r=execute_texture(self.session,self.shaders[key],width,height,'rgba32f',entry,parameters,
                                  levels[0] if texture else None,draws=5,warmup=2,**options)
            r['dispatch_sync_readback_wall_ms']=(time.perf_counter()-started)*1000
            if r['gpu_duration_ms'] is None or r['owned_com_references_before']!=r['owned_com_references_after']:
                raise ValueError('Invalid timing or owned-reference restoration')
            if entry!='PSFixtureCoordinates':r.update(verify_frame(raw,width,height,normal=entry=='PSMaterialNormals'))
            elif not all(math.isfinite(v) for p in struct.iter_unpack('<4f',raw) for v in p):
                raise ValueError('Nonfinite geometric coordinates or LOD')
            if frames and frames[0]!=raw:raise ValueError('Repeated stable inputs changed output')
            frames=[raw];samples.append(r)
        return frames[0],{'samples':samples,'gpu_ms_per_draw_median':statistics.median(r['gpu_duration_ms']/5 for r in samples)}


def numerical_smoke(device):
    receipts=[]
    for view in ('front-near','moderate','grazing-far'):
        fixture=camera_parameters(*VIEWS[view])
        coords,cr=device.draw('periodic-1--1',fixture,64,36,entry='PSFixtureCoordinates')
        max_position=max_view=0.0
        for x,y in probe_positions(64,36):
            uv,v=plane_coordinates((x+.5)/64,(y+.5)/36,fixture)
            actual=struct.unpack_from('<4f',coords,(y*64+x)*16)
            max_position=max(max_position,max(abs(actual[i]-uv[i])/max(1,abs(uv[i])) for i in (0,1)))
            max_view=max(max_view,abs(actual[2]-v[2]))
        if max_position>3e-5 or max_view>2e-6:raise ValueError('Pinhole plane geometry oracle failed')
        receipts.append({'view':view,'geometry_relative_error':max_position,'view_z_error':max_view,'receipt':cr})
        for backend in ('original','periodic'):
            raw,r=device.draw(f'{backend}-1--1',fixture,64,36)
            max_error=0.0
            for x,y in probe_positions(64,36):
                uv=struct.unpack_from('<4f',coords,(y*64+x)*16)[:2]
                # Use measured UV after independently verifying the geometric projection.
                sine,cosine,distance,_=fixture;p=(uv[0],uv[1],0)
                v=(-p[0],-distance*sine-p[1],distance*cosine);length=math.sqrt(sum(a*a for a in v));v=tuple(a/length for a in v)
                material=surface(uv[0]%1,uv[1]%1) if backend=='original' else periodic_surface(*uv)
                expected=shade_surface(material,view=v);actual=struct.unpack_from('<4f',raw,(y*64+x)*16)
                max_error=max(max_error,max(abs(a-b) for a,b in zip(actual,expected)))
            if max_error>.001:raise ValueError('Oblique procedural color oracle failed')
            receipts.append({'view':view,'backend':backend,'cpu_max_absolute_error':max_error,'receipt':r})
    for size in (256,512):
        levels=device.maps[size][0]
        fixture=camera_parameters(55,4)
        coords,_=device.draw('periodic-1--1',fixture,64,36,entry='PSFixtureCoordinates')
        for lod in (0,3,len(levels)-1):
            for comp in (0,1):
                key=f'texture-1-{lod}';raw,r=device.draw(key,fixture,64,36,size=size,compensation=comp,entry='PSMaterialNormals')
                error=0.0
                for x,y in probe_positions(64,36):
                    uv=struct.unpack_from('<4f',coords,(y*64+x)*16)[:2]
                    expected=decode_moment(sample_moment(levels[lod],size>>lod,*uv),compensation=comp)
                    actual=struct.unpack_from('<4f',raw,(y*64+x)*16)
                    error=max(error,max(abs(a-b) for a,b in zip(actual,expected)))
                if error>.002:raise ValueError('Explicit mip/vector-variance oracle failed')
                receipts.append({'size':size,'explicit_mip':lod,'compensation':comp,'cpu_max_absolute_error':error,'receipt':r})
        # Independent implicit-LOD oracle: this catches an accidentally forced base mip.
        fixture=camera_parameters(78,8)
        coordinates,cr=device.draw('texture-1--1',fixture,64,36,size=size,entry='PSFixtureCoordinates')
        raw,r=device.draw('texture-1--1',fixture,64,36,size=size,entry='PSMaterialNormals')
        error=0.0
        for x,y in probe_positions(64,36):
            u,v,_,lod=struct.unpack_from('<4f',coordinates,(y*64+x)*16)
            lod=max(0,min(len(levels)-1,lod));low=math.floor(lod);high=min(len(levels)-1,low+1);blend=lod-low
            a=sample_moment(levels[low],size>>low,u,v);b=sample_moment(levels[high],size>>high,u,v)
            expected=decode_moment(tuple(x*(1-blend)+y*blend for x,y in zip(a,b)))
            actual=struct.unpack_from('<4f',raw,(y*64+x)*16)
            error=max(error,max(abs(a-b) for a,b in zip(actual,expected)))
        if error>.002:raise ValueError('Implicit trilinear mip selection oracle failed')
        receipts.append({'size':size,'implicit_lod_cpu_max_error':error,'receipt':r,'coordinate_receipt':cr})
    fixture=camera_parameters(78,8)
    flat,_=device.draw('periodic-1--1',fixture,64,36,parameters=(0,0,1))
    for size in (256,512):
        off,r=device.draw('texture-1--1',fixture,64,36,size=size,parameters=(0,0,1),compensation=1)
        if off!=flat:raise ValueError('Oblique disabled baseline is not exact')
        receipts.append({'size':size,'disable_byte_exact':True,'receipt':r})
    return receipts


def run_stability_smoke(adapter_index,output_dir):
    output=_output_path(output_dir);output.mkdir(parents=True)
    result={'status':'running','cases':[],'compilation':{},'maps':{}}
    session=None
    try:
        maps={}
        for size in (256,512):
            started=time.perf_counter();maps[size]=build_mips(size)
            result['maps'][size]={'generation_wall_ms':(time.perf_counter()-started)*1000,'payload_bytes':sum(map(len,maps[size][0])),'levels':maps[size][1]}
        binaries,result['compilation']=write_programs(output)
        with D3D11Session(adapter_index) as session:
            result['adapter']=session.adapter
            if session.adapter['vendor_id']!=0x1002 or session.adapter['device_id']!=0x731f:raise ValueError('Explicit RX 5700 XT required')
            device=StabilityDevice(session,binaries,maps);result['cases']=numerical_smoke(device)
        result['status']='passed'
    except Exception as error:result.update(status='failed',failure=str(error));raise
    finally:
        result['owned_context_released']=session is None or not session.owned
        output.joinpath('report.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return result


def matrix_cases(view,stage,candidate,compensation):
    cases=[{'key':'periodic-1--1','label':'periodic-raw'}, {'key':'periodic-4--1','label':'reference-4x4'}]
    if stage=='screen' and view in ('front-far','grazing-far'):
        cases.append({'key':'original-1--1','label':'original-repeat'})
    if stage=='confirm':cases.append({'key':'periodic-1--1','label':'flat','parameters':(0,0,1)})
    for size in (256,512):
        cases.append({'key':'texture-1--1','label':f'{size}-trilinear-c0','size':size,'filter_name':'trilinear'})
        if stage=='screen':
            if view in ('front-near','grazing-far'):
                cases.extend({'key':'texture-1--1','label':f'{size}-{name}-c0','size':size,
                              'filter_name':'trilinear' if name=='base' else name,'mips':name!='base'}
                             for name in ('base','point','bilinear'))
            if view in ('moderate','grazing-near','grazing-far'):
                cases.append({'key':'texture-1--1','label':f'{size}-aniso4-c0','size':size,'filter_name':'aniso4'})
            if view in ('moderate','grazing-far'):
                cases.append({'key':'texture-1--1','label':f'{size}-trilinear-c1','size':size,'compensation':1})
            if view=='grazing-far':
                cases.extend({'key':'texture-1--1','label':f'{size}-{name}-c0','size':size,'filter_name':name}
                             for name in ('aniso2','aniso8','aniso16'))
                cases.append({'key':'texture-1--1','label':f'{size}-aniso8-c1','size':size,'filter_name':'aniso8','compensation':1})
        elif view in ('moderate','grazing-near','grazing-far') and (candidate!='trilinear' or compensation!=0):
            cases.append({'key':'texture-1--1','label':f'{size}-{candidate}-c{compensation}','size':size,
                          'filter_name':candidate,'compensation':compensation})
    return cases


def _viewer(output,result):
    sections=[]
    for view in dict.fromkeys(c.get('view') for c in result['cases']):
        cases=[c for c in result['cases'] if c.get('view')==view and c.get('image')]
        if not cases:continue
        pictures=''.join(f'<figure><figcaption>{c["label"]}: {c["gpu_ms_per_draw_median"]:.4f} ms</figcaption><img src="{c["image"]}" alt="Synthetic {c["label"]}"></figure>' for c in cases)
        sections.append(f'<section><h2>{view}</h2><div>{pictures}</div></section>')
    output.joinpath('index.html').write_text('<!doctype html><meta charset="utf-8"><title>Synthetic texture stability</title>'
        '<style>body{font:16px system-ui;background:#181b20;color:#eee;margin:2rem}section>div{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}figure{margin:0}img{width:100%}</style>'
        '<h1>Original synthetic texture filtering experiment</h1><p>Controlled pinhole camera, infinite flat plane, fixed light and albedo. '
        'Matrix views use 0, 55 and 78 degrees from the geometric normal; temporal probes use the recorded grazing camera. '
        'The original repeating field is intentionally nonperiodic. Periodic raw and finite 4x4 supersampling are separate references. '
        'No post-processing seam blur, game integration or FPS claim. RGB8 sRGB previews from linear GPU readback. '
        '<a href="report.json">Quality, raw timestamps, memory and limitations</a>.</p>'+''.join(sections),encoding='utf-8')


def run_stability_matrix(adapter_index,output_dir,*,stage='screen',candidate='aniso4',compensation=0):
    if stage not in ('screen','confirm') or candidate not in ('trilinear','aniso2','aniso4','aniso8','aniso16') or compensation not in (0,1):
        raise ValueError('Unknown bounded filtering matrix')
    profile='720p' if stage=='screen' else '1080p';width,height=PROFILES[profile]
    output=_output_path(output_dir);output.mkdir(parents=True)
    result={'status':'running','stage':stage,'profile':profile,'candidate':candidate,'compensation':compensation,
            'cases':[],'artifacts':{},'maps':{},'numerical_gates':[],'sampling_limitations':
            '4x4 reference is finite supersampling, not exact pixel integration; GPU LOD is a diagnostic, not tap-count proof'}
    session=None
    def save():output.joinpath('report.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    try:
        maps={}
        for size in (256,512):
            started=time.perf_counter();maps[size]=build_mips(size)
            result['maps'][size]={'generation_wall_ms':(time.perf_counter()-started)*1000,
                                 'payload_bytes':sum(map(len,maps[size][0])),'levels':maps[size][1]}
            for i,packed in enumerate(maps[size][0]):
                filename=f'map-{size}-mip-{i}.rgba16f';output.joinpath(filename).write_bytes(packed)
                result['artifacts'][filename]=hashlib.sha256(packed).hexdigest()
        binaries,result['compilation']=write_programs(output)
        with D3D11Session(adapter_index) as session:
            result['adapter']=session.adapter
            if session.adapter['vendor_id']!=0x1002 or session.adapter['device_id']!=0x731f:raise ValueError('Explicit RX 5700 XT required')
            device=StabilityDevice(session,binaries,maps)
            result['numerical_gates']=numerical_smoke(device);save()
            for view,(angle,distance) in VIEWS.items():
                fixture=camera_parameters(angle,distance)
                reference,ref_receipt=device.draw('periodic-4--1',fixture,width,height)
                for configuration in matrix_cases(view,stage,candidate,compensation):
                    options={k:v for k,v in configuration.items() if k not in ('label','key')}
                    key=configuration['key'];label=configuration['label']
                    if label=='reference-4x4':raw,receipt=reference,ref_receipt
                    else:
                        try:raw,receipt=device.draw(key,fixture,width,height,repeat=3,**options)
                        except ValueError as error:
                            if 'CreateSamplerState' in str(error):
                                result['cases'].append({'view':view,'label':label,'status':'unavailable','reason':str(error)});save();continue
                            raise
                    filename=f'{view}-{label}.png';started=time.perf_counter()
                    image=png_bytes(raw,width,height,'rgba32f',linear=True);output.joinpath(filename).write_bytes(image)
                    record={'view':view,'angle_degrees':angle,'distance':distance,'label':label,'image':filename,
                            'png_export_wall_ms':(time.perf_counter()-started)*1000,'configuration':configuration,**receipt}
                    started=time.perf_counter();record['quality']=image_metrics(raw,reference,width,height)
                    record['cpu_quality_wall_ms']=(time.perf_counter()-started)*1000
                    record['quality_scope']='field-periodization difference; exclude from filter ranking' if label=='original-repeat' else 'versus finite periodic 4x4 reference'
                    if label!='reference-4x4' and label!='flat':
                        normal,nr=device.draw(key,fixture,width,height,entry='PSMaterialNormals',**options)
                        record['normal_diagnostic']=nr
                    if key.startswith('texture'):
                        coordinates,cr=device.draw(key,fixture,width,height,entry='PSFixtureCoordinates',**options)
                        lods=[p[3] for p in struct.iter_unpack('<4f',coordinates)]
                        record['gpu_lod_range']=[min(lods),max(lods)];record['coordinate_receipt']=cr
                        off,offr=device.draw(key,fixture,width,height,parameters=(0,0,1),
                                            **{k:v for k,v in options.items() if k!='parameters'})
                        flat,_=device.draw('periodic-1--1',fixture,width,height,parameters=(0,0,1))
                        if off!=flat:raise ValueError('Full-resolution oblique disable changed baseline')
                        record['disabled_byte_exact']=True;record['disabled_receipt']=offr
                    result['cases'].append(record);result['artifacts'][filename]=hashlib.sha256(image).hexdigest();save()
                    print(json.dumps({'completed':f'{profile}/{view}/{label}','gpu_ms':record['gpu_ms_per_draw_median'],
                                      'rmse':record['quality']['rgb_rmse_vs_4x4']}),file=sys.stderr,flush=True)
        result['status']='passed';_viewer(output,result)
    except Exception as error:result.update(status='failed',failure=str(error));raise
    finally:result['owned_context_released']=session is None or not session.owned;save()
    return result


def change_residual(current,previous,reference_current,reference_previous):
    if not (len(current)==len(previous)==len(reference_current)==len(reference_previous)) or not current or len(current)%16:
        raise ValueError('Synthetic change comparison shape mismatch')
    total=0.0;maximum=0.0;count=0
    for a,b,c,d in zip(*(struct.iter_unpack('<4f',v) for v in (current,previous,reference_current,reference_previous))):
        for i in range(3):
            residual=(a[i]-b[i])-(c[i]-d[i])
            if not math.isfinite(residual):raise ValueError('Nonfinite synthetic change')
            total+=residual*residual;maximum=max(maximum,abs(residual));count+=1
    return {'reference_change_residual_rgb_rms':math.sqrt(total/count),'reference_change_residual_rgb_max':maximum,
            'scope':'deterministic input change minus finite reference change; not optical flow or in-game temporal validation'}


def cpu_pixel_integral(x,y,width,height,fixture,samples):
    total=[0.0]*4
    for sy in range(samples):
        for sx in range(samples):
            uv,view=plane_coordinates((x+(sx+.5)/samples)/width,(y+(sy+.5)/samples)/height,fixture)
            color=shade_surface(periodic_surface(*uv),view=view)
            for i in range(4):total[i]+=color[i]
    return tuple(v/(samples*samples) for v in total)


def run_stability_temporal(adapter_index,output_dir,*,candidate='aniso4',compensation=0,size=512):
    if candidate not in ('aniso2','aniso4','aniso8','aniso16') or compensation not in (0,1) or size not in (256,512):
        raise ValueError('Unknown bounded synthetic change probe')
    width,height=PROFILES['720p'];output=_output_path(output_dir);output.mkdir(parents=True)
    result={'status':'running','stage':'temporal','profile':'720p','size':size,'candidate':candidate,
            'compensation':compensation,'cases':[],'changes':[],'artifacts':{},'maps':{},
            'scope':'three deterministic UV phases and three camera distances; no game motion/history'}
    session=None
    def save():output.joinpath('report.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    try:
        maps={n:build_mips(n) for n in (256,512)}
        result['maps']={n:{'payload_bytes':sum(map(len,v[0])),'levels':v[1]} for n,v in maps.items()}
        binaries,result['compilation']=write_programs(output)
        with D3D11Session(adapter_index) as session:
            result['adapter']=session.adapter
            if session.adapter['vendor_id']!=0x1002 or session.adapter['device_id']!=0x731f:raise ValueError('Explicit RX 5700 XT required')
            device=StabilityDevice(session,binaries,maps)
            sequences={'uv-shift':[camera_parameters(78,8,k*.25/size) for k in range(3)],
                       'camera-distance':[camera_parameters(78,d) for d in (7.8,8,8.2)]}
            baseline_reference=None
            for name,fixtures in sequences.items():
                previous={};previous_reference=None
                for i,fixture in enumerate(fixtures):
                    reference,rr=device.draw('periodic-4--1',fixture,width,height)
                    if name=='uv-shift' and i==0:baseline_reference=reference
                    frames={'reference-4x4':reference};receipts={'reference-4x4':rr}
                    for filter_name in dict.fromkeys(('point','bilinear','trilinear',candidate)):
                        raw,r=device.draw('texture-1--1',fixture,width,height,size=size,filter_name=filter_name,
                                          compensation=compensation,repeat=3)
                        frames[filter_name]=raw;receipts[filter_name]=r
                        if previous_reference is not None:
                            change=change_residual(raw,previous[filter_name],reference,previous_reference)
                            change.update(sequence=name,frame=i,filter=filter_name);result['changes'].append(change)
                    for label,raw in frames.items():
                        filename=f'{name}-{i}-{label}.png';image=png_bytes(raw,width,height,'rgba32f',linear=True)
                        output.joinpath(filename).write_bytes(image);result['artifacts'][filename]=hashlib.sha256(image).hexdigest()
                        result['cases'].append({'view':name,'label':f'frame-{i}-{label}','frame':i,'filter':label,'fixture':fixture,
                                                'image':filename,'quality':image_metrics(raw,reference,width,height),**receipts[label]})
                    previous=frames;previous_reference=reference;save()
                    print(json.dumps({'sequence':name,'frame':i,'complete':True}),file=sys.stderr,flush=True)
            fixture=camera_parameters(78,8)
            finer,fr=device.draw('periodic-8--1',fixture,width,height)
            image=png_bytes(finer,width,height,'rgba32f',linear=True);output.joinpath('grazing-reference-8x8.png').write_bytes(image)
            result['artifacts']['grazing-reference-8x8.png']=hashlib.sha256(image).hexdigest()
            result['reference_convergence']={'comparison':compare_readbacks(baseline_reference,finer),'reference_8x8_receipt':fr,'cpu_spots':[]}
            for xf,yf in ((.2,.03),(.5,.03),(.8,.03),(.5,.3),(.5,.7)):
                x,y=int(width*xf),int(height*yf)
                values={str(n):cpu_pixel_integral(x,y,width,height,fixture,n) for n in (4,8,16,32)}
                gpu4=struct.unpack_from('<4f',baseline_reference,(y*width+x)*16)
                gpu8=struct.unpack_from('<4f',finer,(y*width+x)*16)
                result['reference_convergence']['cpu_spots'].append({'pixel':[x,y],'integrals':values,
                    'cpu_gpu_4_max_error':max(abs(a-b) for a,b in zip(gpu4,values['4'])),
                    'cpu_gpu_8_max_error':max(abs(a-b) for a,b in zip(gpu8,values['8']))})
            a,ar=device.draw('texture-1--1',camera_parameters(55,4),width,height,size=size,filter_name=candidate,compensation=compensation)
            b,br=device.draw('texture-1--1',camera_parameters(55,4,1),width,height,size=size,filter_name=candidate,compensation=compensation)
            result['integer_wrap_translation']={**compare_readbacks(a,b),'receipts':[ar,br],
                'meaning':'same periodic field shifted one tile; finite coordinate/filter precision may prevent exact bytes'}
        result['status']='passed';_viewer(output,result)
    except Exception as error:result.update(status='failed',failure=str(error));raise
    finally:result['owned_context_released']=session is None or not session.owned;save()
    return result
