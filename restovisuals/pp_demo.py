"""Offline PP evidence using the existing windowless D3D11 dispatch and PNG writer."""
import argparse
import ctypes
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import struct
from .photographic import ROOT, Settings, presets, process, shader_source, filter_ini
from .shader_compile import compile_bytecode
from .d3d11_validation import D3D11Session, execute_texture
from .gpu_demo import png_bytes

def fixture(width=512, height=128):
    colors = []
    patches = [(1,.08,.03),(.04,.4,1),(.05,.6,.08),(.7,.4,.25),(.18,.18,.18),(.9,.85,.65)]
    for y in range(height):
        band = y * 4 // height
        for x in range(width):
            t = x / (width-1)
            if band == 0: rgb = (4*t,)*3
            elif band == 1: rgb = (.08*t,)*3
            elif band == 2: rgb = tuple(v * (0.1+2.9*t) for v in patches[min(5,x*6//width)])
            else: rgb = (.12+.18*t, .23+.22*t, .45+.35*t)
            colors.append((*rgb, .375))
    return colors

def demonstrate(output, adapter=0):
    output = Path(output).resolve()
    if not output.is_relative_to(ROOT) or output.exists():
        raise ValueError('Require a new owned workspace output folder')
    output.mkdir(parents=True)
    width,height=512,128
    inputs = fixture(width,height)
    packed=b''.join(struct.pack('<4f',*v) for v in inputs)
    uploaded=list(struct.iter_unpack('<4f',packed))
    output.joinpath('input.png').write_bytes(png_bytes(packed,width,height,'rgba32f',linear=True))
    vertex=compile_bytecode((ROOT/'shaders/RV_FullscreenValidation.hlsl').read_bytes(),'VSFullscreen','vs_5_0')[0]
    report={'scope':'original_synthetic_offline_d3d11','native_csp_pure_validated':False,
            'dimensions':[width,height],'input_encoding':'linear Rec.709; explicit sRGB PNG encoding',
            'source_scene':'original grey/HDR/shadow/color/sky chart; not a game capture',
            'source_sha256':hashlib.sha256((ROOT/'shaders/RV_Photographic.hlsl').read_bytes()).hexdigest(),
            'cases':[],'installation_diff':[]}
    bank={'neutral':Settings(),**presets()}
    with D3D11Session(adapter) as session:
        native_vertex=session.shader(12,vertex)
        for name,settings in bank.items():
            source=shader_source(settings)
            ps,compilation=compile_bytecode(source,'PSLinear')
            _,srgb_compilation=compile_bytecode(source,'PSSrgb')
            shaders={'VSFullscreen':native_vertex,'PSLinear':session.shader(15,ps)}
            if not all(isinstance(p,ctypes.c_void_p) and p.value for p in shaders.values()):
                raise ValueError('Owned native shader objects required; bytecode is not a shader handle')
            mark=len(session.owned)
            raw,execution=execute_texture(session,shaders,width,height,'rgba32f','PSLinear',(0,0,1),packed)
            assert len(session.owned)==mark, 'Dispatch resource cleanup failed'
            actual=list(struct.iter_unpack('<4f',raw))
            expected=[process(v,settings) for v in uploaded]
            error=max(abs(a-b) for aa,bb in zip(actual,expected) for a,b in zip(aa,bb))
            if error>0.00003 or not all(math.isfinite(v) for p in actual for v in p):
                raise ValueError('GPU/CPU photographic validation failed')
            alpha_exact=all(a[3]==b[3] for a,b in zip(actual,uploaded))
            assert alpha_exact
            if name=='neutral':assert raw==packed
            clipped=sum(max(v[:3])>=1 for v in actual)
            # Keep process memory samples and raw device timestamps private.
            public_execution={k:v for k,v in execution.items() if not k.startswith('memory_')
                and k not in ('gpu_timestamp_start','gpu_timestamp_end','gpu_timestamp_frequency_hz')}
            report['cases'].append({'preset':name,'processing_settings':asdict(settings),
                'parameters_specialized_at_compile_time':True,
                'max_absolute_cpu_gpu_error':error,
                'alpha_exact':alpha_exact,'identity_bytes_equal':raw==packed,
                'display_clipped_pixels':clipped,'compiled_entries':[compilation,srgb_compilation],
                'dispatch_receipt':public_execution,'owned_dispatch_resources_released':True})
            output.joinpath(name+'.png').write_bytes(png_bytes(raw,width,height,'rgba32f',linear=True))
    assert not session.owned, 'Device resources remain owned'
    report['all_device_resources_released']=True
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    labels={'balanced':'Balanced Photorealism — Default','warm':'Warm Photorealism','cool':'Cool / High Contrast'}
    rows=''.join('<h2>'+label+'</h2><img src="input.png" alt="Unprocessed original chart"><img src="'+name+'.png" alt="Offline GPU processed chart">' for name,label in labels.items())
    (output/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>RestoVisuals offline PP comparison</title>'
        '<style>body{background:#17191c;color:#eee;font:16px system-ui;margin:24px}img{width:48%;image-rendering:auto;margin-right:1%}</style>'
        '<h1>Original synthetic offline PP comparison</h1><p>Left: unprocessed. Right: original GPU shader. '
        'Rows: HDR ramp, shadows, colors, sky. Not Assetto Corsa/Pure output; no game-performance claim.</p>'+rows)
    config_dir=output/'filters';config_dir.mkdir()
    for name,settings in presets().items():
        filename={'balanced':'RestoVisuals.ini','warm':'RestoVisuals_Warm.ini','cool':'RestoVisuals_Cool.ini'}[name]
        (config_dir/filename).write_text(filter_ini(settings),encoding='utf-8',newline='\n')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    parser.add_argument('--adapter',type=int,default=0)
    args=parser.parse_args()
    result=demonstrate(args.output,args.adapter)
    print(json.dumps({'cases':[{k:v for k,v in c.items() if k not in ('compiled_entries','dispatch_receipt')} for c in result['cases']],
                      'all_device_resources_released':result['all_device_resources_released']},indent=2))
