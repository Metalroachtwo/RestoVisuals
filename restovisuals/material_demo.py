"""Bounded original material demonstration using the existing windowless renderer."""
import hashlib
import json
import math
import statistics
import struct
import time
from pathlib import Path

from .d3d11_validation import D3D11Session, compile_validation_program, execute_texture
from .gpu_demo import PROFILES, _output_path, png_bytes
from .material_reference import shade, surface

VARIANTS = (("flat", (0, 0)), ("normal-detail", (1, 0)), ("normal-and-roughness", (1, 1)))


def probe_positions(width, height):
    if width <= 64 and height <= 48:
        return [(x,y) for y in range(height) for x in range(width)]
    return sorted({(round(i*(width-1)/10), round(j*(height-1)/8))
                   for i in range(11) for j in range(9)})


def verify_material(raw, width, height, parameters, *, normals=False, reference=None, cpu_tolerance=.0004):
    if len(raw) != width*height*16:
        raise ValueError("Material readback size mismatch")
    finite, alpha, max_normal_error = True, True, 0.0
    rough_min, rough_max = 1.0, 0.0
    for pixel in struct.iter_unpack('<4f', raw):
        if not all(math.isfinite(v) for v in pixel):
            finite = False
            break
        if normals:
            max_normal_error = max(max_normal_error, abs(math.sqrt(sum(v*v for v in pixel[:3]))-1))
            rough_min, rough_max = min(rough_min,pixel[3]), max(rough_max,pixel[3])
        else:
            alpha &= pixel[3] == 1.0
    error = 0.0
    positions = probe_positions(width,height)
    if finite:
        for x,y in positions:
            actual = struct.unpack_from('<4f',raw,(y*width+x)*16)
            uv = ((x+.5)/width,(y+.5)/height)
            expected = (reference(*uv,parameters,normals) if reference is not None else
                        surface(*uv,*parameters[:2]) if normals else shade(*uv,*parameters))
            error = max(error,max(abs(a-b) for a,b in zip(actual,expected)))
    passed = finite and alpha and error <= cpu_tolerance
    if normals:
        passed &= max_normal_error <= 0.000002 and rough_min >= .41999 and rough_max <= .86001
    return {'passed':bool(passed),'all_pixels_finite':finite,'all_pixels_alpha_one':alpha if not normals else None,
            'sampled_cpu_pixels':len(positions),'cpu_max_absolute_error':error,'cpu_absolute_tolerance':cpu_tolerance,
            'all_pixels_max_normal_length_error':max_normal_error if normals else None,
            'all_pixels_roughness_range':[rough_min,rough_max] if normals else None,
            'readback_sha256':hashlib.sha256(raw).hexdigest()}


def _sample_red(raw, width, height):
    return [struct.unpack_from('<f',raw,(y*width+x)*16)[0] for x,y in probe_positions(width,height)]


def _rms(values):
    return math.sqrt(sum(v*v for v in values)/len(values))


def demonstrate_material(adapter_index, source_path, output_dir, *, profile='both'):
    if profile not in (*PROFILES,'both'):
        raise ValueError('Unknown material profile')
    output = _output_path(output_dir)
    binaries, result = compile_validation_program(Path(source_path),pixel_entries=('PSMaterial','PSMaterialNormals'))
    output.mkdir(parents=True,exist_ok=False)
    result.update({'demonstration':'original_synthetic_material_v1','status':'running','cases':[],
                   'smoke_checks':[],'artifacts':{},'comparisons':[],
                   'geometry':{'vertices':3,'triangles':1,'tessellation':False,'displacement':False},
                   'input':'procedural XY height-gradient, fixed linear RGB albedo; no source textures',
                   'timing_scope':'3 batches of 5 draws, each after 2 warmup draws; no game FPS',
                   'memory_scope':'declared payload and sampled process-local DXGI usage, not physical allocation or peak'})
    session = None
    groups = []
    try:
        with D3D11Session(adapter_index) as session:
            result['adapter'] = session.adapter
            if session.adapter['vendor_id'] != 0x1002 or session.adapter['device_id'] != 0x731f:
                raise ValueError('This bounded experiment requires the explicitly selected RX 5700 XT')
            shaders = {entry:session.shader(12 if entry=='VSFullscreen' else 15,code) for entry,code in binaries.items()}

            def draw(width,height,parameters,*,normals=False,draws=1,warmup=0):
                started = time.perf_counter()
                raw, receipt = execute_texture(session,shaders,width,height,'rgba32f',
                    'PSMaterialNormals' if normals else 'PSMaterial',parameters,None,draws=draws,warmup=warmup)
                receipt['dispatch_sync_readback_wall_ms'] = (time.perf_counter()-started)*1000
                started = time.perf_counter()
                receipt.update(verify_material(raw,width,height,parameters,normals=normals))
                receipt['cpu_validation_wall_ms'] = (time.perf_counter()-started)*1000
                receipt['passed'] &= receipt['owned_com_references_before']==receipt['owned_com_references_after']
                if not receipt['passed']:
                    result['smoke_checks'].append(receipt)
                    raise ValueError('GPU material reference/normal/cleanup gate failed')
                return raw,receipt

            # All numerical/disable gates precede full-resolution work.
            for side in (-1,1):
                baseline = None
                for normal,roughness in ((0,0),(1,0),(1,1),(0,1),(0,0)):
                    raw,receipt = draw(64,48,(normal,roughness,side))
                    result['smoke_checks'].append(receipt)
                    if baseline is None:baseline=raw
                    if normal==roughness==0 and raw!=baseline:
                        raise ValueError('Disable is not byte-exact against baseline')
                _,receipt = draw(64,48,(1,1,side),normals=True)
                result['smoke_checks'].append(receipt)

            profiles = list(PROFILES.items()) if profile=='both' else [(profile,PROFILES[profile])]
            for name,(width,height) in profiles:
                details = {}
                for side in (-1,1):
                    light = 'left' if side<0 else 'right'
                    baseline, normal_raw = None, None
                    files = []
                    for label,(normal,roughness) in VARIANTS:
                        samples, reference = [], None
                        for _ in range(3):
                            raw,receipt = draw(width,height,(normal,roughness,side),draws=5,warmup=2)
                            if reference is not None and reference!=raw:
                                raise ValueError('Identical material draws are not deterministic')
                            reference = raw
                            samples.append(receipt)
                        durations = [r['gpu_duration_ms']/5 for r in samples if r['gpu_duration_ms'] is not None]
                        case = {'profile':name,'width':width,'height':height,'light':light,'variant':label,
                                'samples':samples,'gpu_ms_per_draw_median':statistics.median(durations) if len(durations)==3 else None}
                        if len(durations)!=3:
                            raise ValueError('Disjoint/invalid GPU timestamps: do not report a duration')
                        result['cases'].append(case)
                        if baseline is None:baseline=raw
                        if label=='normal-detail':normal_raw=raw
                        filename = f'{name}-{light}-{label}.png'
                        started = time.perf_counter()
                        image = png_bytes(raw,width,height,'rgba32f',linear=True)
                        output.joinpath(filename).write_bytes(image)
                        case['png_export_wall_ms'] = (time.perf_counter()-started)*1000
                        result['artifacts'][filename] = hashlib.sha256(image).hexdigest()
                        files.append((label,filename))
                    disabled,receipt = draw(width,height,(0,0,side))
                    receipt['disable_byte_exact'] = disabled==baseline
                    result['smoke_checks'].append(receipt)
                    if disabled!=baseline:raise ValueError('Full-resolution disable mismatch')
                    _,diagnostic = draw(width,height,(1,1,side),normals=True)
                    diagnostic.update({'profile':name,'light':light,'diagnostic':'normal and roughness'})
                    result['smoke_checks'].append(diagnostic)
                    flat_samples = _sample_red(baseline,width,height)
                    normal_samples = _sample_red(normal_raw,width,height)
                    full_samples = _sample_red(raw,width,height)
                    delta = [a-b for a,b in zip(normal_samples,flat_samples)]
                    rough_delta = [a-b for a,b in zip(full_samples,normal_samples)]
                    if _rms(delta)<.001 or _rms(rough_delta)<.00001:
                        raise ValueError('Material effects are not measurably distinct')
                    details[light] = delta
                    result['comparisons'].append({'profile':name,'light':light,'sampled_red_channel_pixels':len(delta),
                        'normal_detail_rms_from_flat':_rms(delta),'roughness_rms_from_normal_only':_rms(rough_delta)})
                    groups.append((f'{name}, light {light}',files))
                a,b = details['left'],details['right']
                am,bm = statistics.mean(a),statistics.mean(b)
                correlation = sum((x-am)*(y-bm) for x,y in zip(a,b))/math.sqrt(sum((x-am)**2 for x in a)*sum((y-bm)**2 for y in b))
                result['comparisons'].append({'profile':name,'opposite_light_detail_correlation':correlation})
        result['status'] = 'passed'
        sections = ''.join('<section><h2>'+label+'</h2><div>'+''.join(
            f'<figure><figcaption>{caption}</figcaption><img src="{filename}" alt="Synthetic {caption}"></figure>'
            for caption,filename in files)+'</div></section>' for label,files in groups)
        output.joinpath('index.html').write_text('<!doctype html><meta charset="utf-8"><title>Synthetic material GPU comparison</title>'
            '<style>body{background:#181b20;color:#eee;font:16px system-ui;margin:2rem}section>div{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}figure{margin:0}img{width:100%}</style>'
            '<h1>Original synthetic material demonstration</h1><p>Flat geometry; identical orthographic view, albedo and light within each row. '
            'Rows change light direction. Linear RGB readback encoded to sRGB previews. No game integration or gameplay FPS claim. '
            '<a href="report.json">Numerical, timestamp and memory receipts</a>.</p>'+sections,encoding='utf-8')
    except Exception as error:
        result.update({'status':'failed','failure_type':type(error).__name__,'failure':str(error)})
        raise
    finally:
        result['owned_context_released'] = session is not None and not session.owned
        output.joinpath('report.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    return result
