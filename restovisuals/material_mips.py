"""Original periodic surface, mean-vector mips and controlled pinhole geometry."""
from array import array
import math
import struct

from .material_reference import noise_gradient


def periodic_height(u,v):
    return (sum(w/f*noise_gradient(u*f,v*f,s,period=f)[0]
                for w,f,s in ((.12,10,1),(.10,32,2),(.055,90,3)))
            + .07/(2*math.pi*18)*math.sin(2*math.pi*(18*u+2*v)))


def periodic_surface(u,v,normal_amount=1,roughness_amount=1):
    u,v=u%1,v%1
    gx=gy=0.0
    for w,f,s in ((.12,10,1),(.10,32,2),(.055,90,3)):
        _,dx,dy=noise_gradient(u*f,v*f,s,period=f);gx+=w*dx;gy+=w*dy
    groove=.07*math.cos(2*math.pi*(18*u+2*v));gx=normal_amount*(gx+groove);gy=normal_amount*(gy+groove*2/18)
    length=math.sqrt(1+gx*gx+gy*gy)
    return (-gx/length,-gy/length,1/length,.64+roughness_amount*.44*(noise_gradient(u*7,v*7,4,period=7)[0]-.5))


def build_mips(size):
    if type(size) is not int or size not in (256,512):raise ValueError('Bounded 256/512 fixture required')
    values=array('d')
    for y in range(size):
        for x in range(size):
            n=periodic_surface((x+.5)/size,(y+.5)/size);values.extend((*n[:3],n[3]**4))
    levels=[];stats=[];width=size
    while True:
        packed=b''.join(struct.pack('<4e',*values[i:i+4]) for i in range(0,len(values),4))
        levels.append(packed)
        lengths=[sum(values[i+j]**2 for j in range(3)) for i in range(0,len(values),4)]
        stats.append({'width':width,'payload_bytes':len(packed),'mean_vector_length_range':[math.sqrt(min(lengths)),math.sqrt(max(lengths))],
                      'mean_direction_variance':sum(max(0,1-v) for v in lengths)/len(lengths)})
        if width==1:break
        next_width=width//2;coarse=array('d')
        for y in range(next_width):
            for x in range(next_width):
                indices=[((2*y+dy)*width+2*x+dx)*4 for dy in (0,1) for dx in (0,1)]
                coarse.extend(sum(values[i+c] for i in indices)/4 for c in range(4))
        values=coarse;width=next_width
    return tuple(levels),stats


def sample_moment(level,size,u,v,*,linear=True):
    if not linear:
        return struct.unpack_from('<4e',level,((math.floor(v*size)%size)*size+math.floor(u*size)%size)*8)
    x,y=u*size-.5,v*size-.5;ix,iy=math.floor(x),math.floor(y);fx,fy=x-ix,y-iy
    def fetch(dx,dy):return struct.unpack_from('<4e',level,(((iy+dy)%size)*size+(ix+dx)%size)*8)
    a,b,c,d=fetch(0,0),fetch(1,0),fetch(0,1),fetch(1,1)
    return tuple((1-fy)*((1-fx)*a[i]+fx*b[i])+fy*((1-fx)*c[i]+fx*d[i]) for i in range(4))


def decode_moment(moment,normal_amount=1,roughness_amount=1,compensation=0):
    x,y,z,a=moment
    gx,gy=normal_amount*x/max(z,.001),normal_amount*y/max(z,.001)
    length=math.sqrt(1+gx*gx+gy*gy)
    r=.64+roughness_amount*(max(a,1e-8)**.25-.64)
    variance=max(0,1-x*x-y*y-z*z)
    r=min(.98,(r**4+compensation*normal_amount**2*variance)**.25)
    return (gx/length,gy/length,1/length,r)


def camera_parameters(angle,distance,phase=0):
    if not 0<=angle<=80 or not 1<=distance<=12 or abs(phase)>2:raise ValueError('Fixture outside bounds')
    return tuple(struct.unpack('<f',struct.pack('<f',v))[0] for v in (math.sin(math.radians(angle)),math.cos(math.radians(angle)),distance,phase))


def plane_coordinates(u,v,fixture):
    sine,cosine,distance,phase=fixture
    sx=(2*u-1)*(16/9)*math.tan(math.radians(9));sy=(1-2*v)*math.tan(math.radians(9))
    ray=(sx,sine+sy*cosine,-cosine+sy*sine)
    t=-distance*cosine/ray[2]
    p=(t*ray[0],-distance*sine+t*ray[1])
    length=math.sqrt(sum(x*x for x in ray))
    return (p[0]+phase,p[1]),tuple(-x/length for x in ray)
