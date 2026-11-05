"""Offline checks of original OBJ/MTL/data; no DCC or exporter invocation."""
import hashlib
import json
import math
from pathlib import Path
import struct
import unittest
import zlib

from restovisuals.material_assets import parse_dds

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'examples/phase0l-fixture-source'


def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def length(v): return math.sqrt(dot(v, v))
def unit(v): return tuple(x/length(v) for x in v)


class FixtureSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads((SOURCE/'source-contract.json').read_bytes())
        cls.manifest = json.loads((SOURCE/'manifest.json').read_bytes())
        cls.tokens = [line.split() for line in (SOURCE/'pad.obj').read_text().splitlines()
                      if line.strip() and not line.startswith('#')]
        cls.vertices = [tuple(map(float, v[1:])) for v in cls.tokens if v[0]=='v']
        cls.uvs = [tuple(map(float, v[1:])) for v in cls.tokens if v[0]=='vt']
        cls.normals = [tuple(map(float, v[1:])) for v in cls.tokens if v[0]=='vn']
        cls.faces = [[tuple(int(x)-1 for x in corner.split('/')) for corner in row[1:]]
                     for row in cls.tokens if row[0]=='f']

    def test_one_original_named_object_and_material_with_valid_indices(self):
        self.assertEqual([row[1] for row in self.tokens if row[0]=='o'], [self.contract['mesh']])
        self.assertEqual([row[1] for row in self.tokens if row[0]=='usemtl'], [self.contract['material']])
        self.assertEqual((len(self.vertices),len(self.uvs),len(self.normals),len(self.faces)), (4,4,1,1))
        self.assertEqual(len(self.faces[0]),4)
        for vertex,uv,normal in self.faces[0]:
            self.assertIn(vertex,range(4)); self.assertIn(uv,range(4)); self.assertEqual(normal,0)
        self.assertEqual(len({corner[0] for corner in self.faces[0]}),4)
        self.assertTrue(all(row[0] in ('mtllib','o','v','vt','vn','usemtl','s','f') for row in self.tokens))

    def test_positions_uvs_and_intended_bounds_match_source_contract(self):
        self.assertEqual(self.vertices,[tuple(v) for v in self.contract['positions']])
        self.assertEqual(self.uvs,[tuple(v) for v in self.contract['uv1']])
        self.assertTrue(all(math.isfinite(x) for v in self.vertices+self.uvs for x in v))
        self.assertEqual([min(v[i] for v in self.vertices) for i in range(3)],[-6,0,-6])
        self.assertEqual([max(v[i] for v in self.vertices) for i in range(3)],[6,0,6])
        self.assertEqual(self.contract['intended_metres_per_source_unit'],1)

    def test_quad_is_planar_front_facing_and_has_expected_area(self):
        normal=self.normals[0]; self.assertAlmostEqual(length(normal),1)
        self.assertEqual(normal,tuple(self.contract['normal']))
        for vertex in self.vertices:self.assertAlmostEqual(dot(sub(vertex,self.vertices[0]),normal),0)
        area=0.0
        for indices in ((0,1,2),(0,2,3)):
            a,b,c=(self.vertices[i] for i in indices); vector=cross(sub(b,a),sub(c,a))
            self.assertGreater(dot(vector,normal),0); area+=length(vector)/2
        self.assertAlmostEqual(area,144)

    def test_uv_derivatives_establish_known_tangent_basis_and_two_metre_repeat(self):
        a,b,c=self.vertices[:3]; ua,ub,uc=self.uvs[:3]
        e1,e2=sub(b,a),sub(c,a); d1,d2=sub(ub,ua),sub(uc,ua)
        determinant=d1[0]*d2[1]-d1[1]*d2[0]; self.assertGreater(determinant,0)
        tangent=tuple((d2[1]*e1[i]-d1[1]*e2[i])/determinant for i in range(3))
        bitangent=tuple((-d2[0]*e1[i]+d1[0]*e2[i])/determinant for i in range(3))
        self.assertEqual(unit(tangent),tuple(self.contract['tangent']))
        self.assertEqual(unit(bitangent),tuple(self.contract['bitangent']))
        self.assertAlmostEqual(length(tangent),2); self.assertAlmostEqual(length(bitangent),2)
        self.assertAlmostEqual(dot(unit(tangent),unit(bitangent)),0)
        self.assertEqual(unit(cross(tangent,bitangent)),self.normals[0])
        self.assertIn('OBJ stores no explicit tangents',self.contract['tangent_storage'])

    def test_preview_material_has_relative_texture_and_no_native_shader_claim(self):
        rows=[line.split() for line in (SOURCE/'pad.mtl').read_text().splitlines() if line.strip() and not line.startswith('#')]
        self.assertEqual([row[1] for row in rows if row[0]=='newmtl'],[self.contract['material']])
        texture=next(row[1] for row in rows if row[0]=='map_Kd')
        self.assertEqual(texture,'textures/neutral_diffuse.png'); self.assertTrue((SOURCE/texture).is_file())
        self.assertEqual(next(row[1:] for row in rows if row[0]=='Ks'),['0','0','0'])
        self.assertFalse(any('SHADER' in row[0] for row in rows))

    def test_flat_dds_is_an_unchanged_original_candidate(self):
        data=(SOURCE/'textures/flat.dds').read_bytes()
        self.assertEqual(data,(ROOT/'examples/phase0k-normal-probe/textures/flat.dds').read_bytes())
        self.assertEqual(hashlib.sha256(data).hexdigest(),'ce82d560691c9fcd58ca30ba22f725e48b293048547e0f4c1a77f1ac360393d1')
        levels=parse_dds(data); self.assertEqual(len(levels),9)
        self.assertEqual(levels[-1],bytes((128,128,255,255)))

    def test_diffuse_png_is_original_constant_rgb8_with_valid_chunks(self):
        raw=(SOURCE/'textures/neutral_diffuse.png').read_bytes()
        self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
        offset=8; compressed=b''; tags=[]
        while offset<len(raw):
            size=struct.unpack_from('>I',raw,offset)[0]; tag=raw[offset+4:offset+8]; data=raw[offset+8:offset+8+size]
            expected=struct.unpack_from('>I',raw,offset+8+size)[0]
            self.assertEqual(zlib.crc32(tag+data)&0xffffffff,expected)
            tags.append(tag)
            if tag==b'IHDR':self.assertEqual(struct.unpack('>IIBBBBB',data),(32,32,8,2,0,0,0))
            if tag==b'sRGB':self.assertEqual(data,b'\0')
            if tag==b'IDAT':compressed+=data
            offset+=size+12
        self.assertEqual(tags,[b'IHDR',b'sRGB',b'IDAT',b'IEND']); self.assertEqual(offset,len(raw))
        self.assertEqual(zlib.decompress(compressed),(b'\0'+bytes((128,128,128))*32)*32)

    def test_camera_pose_proposals_are_nondegenerate_and_do_not_claim_native_markers(self):
        plan=self.contract['future_scene_requirements'];target=plan['camera_target']
        angles=[]
        for camera in plan['cameras']:
            view=sub(target,camera['position']);up=camera['up']
            self.assertGreater(length(view),0);self.assertGreater(length(cross(view,up)),1e-6)
            angles.append(math.degrees(math.acos(unit(sub(camera['position'],target))[1])))
        self.assertAlmostEqual(angles[0],0); self.assertTrue(45<angles[1]<65); self.assertTrue(75<angles[2]<82)
        self.assertFalse(plan['spawn']['native_marker_and_collision_verified'])
        self.assertFalse(plan['track_container_prepared'])

    def test_native_and_export_gates_are_false_and_no_exported_file_is_fabricated(self):
        for key in ('native_ready','fbx_export_succeeded','kn5_export_succeeded','dcc_import_validated'):
            self.assertIs(self.contract[key],False)
        proposal=self.contract['material_proposal']
        self.assertFalse(proposal['native_shader_contract_verified'])
        self.assertEqual(proposal['shader_candidate'],'ksPerPixelNM')
        self.assertEqual(set(proposal['expected_required_slots']),{'txDiffuse','txNormal'})
        self.assertEqual(proposal['expected_properties']['ksSpecular'],0)
        self.assertFalse(any(p.suffix.lower() in ('.fbx','.kn5','.blend') for p in SOURCE.rglob('*')))

    def test_source_manifest_exactly_matches_all_payloads(self):
        files={p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file() and p.name!='manifest.json'}
        self.assertEqual(files,set(self.manifest['files'])); self.assertEqual(len(files),6)
        for name,receipt in self.manifest['files'].items():
            path=Path(name);self.assertFalse(path.is_absolute());self.assertNotIn('..',path.parts)
            raw=(SOURCE/path).read_bytes()
            self.assertEqual(receipt,{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
        for key in ('native_ready','fbx_export_succeeded','kn5_export_succeeded'):self.assertIs(self.manifest[key],False)
