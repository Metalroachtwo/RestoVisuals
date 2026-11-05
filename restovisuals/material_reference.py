"""Original double-precision mathematical oracle for the synthetic XY plane."""
import math


def _lattice(x, y, seed):
    value = (x * 37 + y * 101 + x * y * 17 + seed * 13) % 251
    return ((value * value * 29 + value * 53 + seed * 19) % 251) / 250.0


def noise_gradient(x, y, seed, *, period=None):
    ix, iy = math.floor(x), math.floor(y)
    fx, fy = x - ix, y - iy
    bx, by = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    def corner(x,y):
        return _lattice(x%period,y%period,seed) if period is not None else _lattice(x,y,seed)
    a, b = corner(ix,iy),corner(ix+1,iy)
    c, d = corner(ix,iy+1),corner(ix+1,iy+1)
    return ((1-by)*((1-bx)*a+bx*b)+by*((1-bx)*c+bx*d),
            ((1-by)*(b-a)+by*(d-c))*6*fx*(1-fx),
            ((1-bx)*(c-a)+bx*(d-b))*6*fy*(1-fy))


def height(u, v):
    return (sum(weight/frequency*noise_gradient(u*frequency,v*frequency,seed)[0]
                for weight,frequency,seed in ((.12,10,1),(.10,32,2),(.055,90,3)))
            + .07/(2*math.pi*18)*math.sin(2*math.pi*(18*u+1.5*v)))


def surface(u, v, normal_amount=1, roughness_amount=1):
    gx = gy = 0.0
    for weight, frequency, seed in ((.12,10,1),(.10,32,2),(.055,90,3)):
        _, dx, dy = noise_gradient(u*frequency,v*frequency,seed)
        gx += weight*dx
        gy += weight*dy
    groove = .07*math.cos(2*math.pi*(18*u+1.5*v))
    gx, gy = normal_amount*(gx+groove), normal_amount*(gy+groove*1.5/18)
    length = math.sqrt(1+gx*gx+gy*gy)
    roughness = .64 + roughness_amount*.44*(noise_gradient(u*7,v*7,4)[0]-.5)
    return (-gx/length,-gy/length,1/length,roughness)


def shade(u, v, normal_amount=1, roughness_amount=1, light_side=1):
    return shade_surface(surface(u,v,normal_amount,roughness_amount),light_side)


def shade_surface(material, light_side=1, view=(0,0,1)):
    """The same lighting oracle for analytic and sampled surface data."""
    *normal, roughness = material
    length = math.sqrt(.85**2+.25**2+.65**2)
    light = (.85*light_side/length,.25/length,.65/length)
    half = tuple(a+b for a,b in zip(light,view))
    half_length = math.sqrt(sum(x*x for x in half))
    half = tuple(x/half_length for x in half)
    nl = max(0,sum(a*b for a,b in zip(normal,light)))
    nv = max(0,sum(a*b for a,b in zip(normal,view))); nh = max(0,sum(a*b for a,b in zip(normal,half)))
    a2 = roughness**4
    distribution = a2/(math.pi*(nh*nh*(a2-1)+1)**2)
    def masking(cosine):
        return 2*cosine/max(cosine+math.sqrt(a2+(1-a2)*cosine*cosine),1e-6)
    fresnel = .04+.96*(1-sum(a*b for a,b in zip(view,half)))**5
    specular = distribution*masking(nl)*masking(nv)*fresnel/max(4*nl*nv,1e-6)
    return tuple(.12*a+1.8*nl*((1-fresnel)*a/math.pi+specular) for a in (.13,.135,.14))+(1.0,)
