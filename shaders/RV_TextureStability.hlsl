// Original controlled infinite-plane fixture. Appended to owned procedural
// functions; shared BRDF is inserted without changing its equations.
Texture2D<float4> normalMoments : register(t0);
SamplerState stabilitySampler : register(s0);

void rvPlane(float2 screen, out float2 uv, out float3 view)
{
    float sine=fixture.x, cosine=fixture.y, distance=fixture.z;
    float2 film=(screen*float2(2,-2)+float2(-1,1))*float2(16.0/9.0,1)*0.1583844403245363;
    float3 ray=float3(film.x,sine+film.y*cosine,-cosine+film.y*sine);
    float t=-distance*cosine/ray.z;
    uv=float2(t*ray.x,-distance*sine+t*ray.y)+float2(fixture.w,0);
    view=normalize(-ray);
}

float3 rvPeriodicNoise(float2 uv,uint cells,uint seed)
{
    float2 p=frac(uv)*cells;
    uint2 cell=uint2(floor(p));float2 f=frac(p), b=f*f*(3-2*f), d=6*f*(1-f);
    float a0=lattice(cell%cells,seed),a1=lattice((cell+uint2(1,0))%cells,seed);
    float a2=lattice((cell+uint2(0,1))%cells,seed),a3=lattice((cell+uint2(1,1))%cells,seed);
    return float3(lerp(lerp(a0,a1,b.x),lerp(a2,a3,b.x),b.y),
        lerp(a1-a0,a3-a2,b.y)*d.x,lerp(a2-a0,a3-a1,b.x)*d.y);
}

float4 rvPeriodicSurface(float2 uv)
{
    float2 gradient=0;
    [branch] if(normalAmount!=0)
    {
        gradient=.12*rvPeriodicNoise(uv,10u,1u).yz+.10*rvPeriodicNoise(uv,32u,2u).yz+.055*rvPeriodicNoise(uv,90u,3u).yz;
        float groove=.07*cos(2*PI*dot(frac(uv),float2(18,2)));
        gradient+=groove*float2(1,2.0/18.0);
    }
    float r=.64+roughnessAmount*.44*(rvPeriodicNoise(uv,7u,4u).x-.5);
    return float4(normalize(float3(-normalAmount*gradient,1)),r);
}

float4 rvSurface(float2 uv)
{
#if RV_BACKEND == 0
    return surface(frac(uv));
#elif RV_BACKEND == 1
    return rvPeriodicSurface(uv);
#else
    float4 result=float4(0,0,1,.64);
    [branch] if(normalAmount!=0 || roughnessAmount!=0)
    {
#if RV_EXPLICIT_LOD
        float4 m=normalMoments.SampleLevel(stabilitySampler,uv,RV_LOD);
#else
        float4 m=normalMoments.Sample(stabilitySampler,uv);
#endif
        float3 n=normalize(float3(normalAmount*m.xy/max(m.z,.001),1));
        float r=lerp(.64,pow(max(m.w,1e-8),.25),roughnessAmount);
        float variance=max(0,1-dot(m.xyz,m.xyz));
        r=min(.98,pow(max(r*r*r*r+reserved*normalAmount*normalAmount*variance,1e-8),.25));
        result=float4(n,r);
    }
    return result;
#endif
}

// RV_SHARED_BRDF

float4 rvEvaluate(float2 screen)
{
    float2 uv;float3 view;rvPlane(screen,uv,view);
    return rvShade(rvSurface(uv),view);
}

float4 PSMaterial(PixelInput input) : SV_Target
{
#if RV_SSAA > 1
    float2 dx=ddx(input.uv),dy=ddy(input.uv);float4 total=0;
    [unroll] for(int y=0;y<RV_SSAA;y++)
        [unroll] for(int x=0;x<RV_SSAA;x++)
            total+=rvEvaluate(input.uv+dx*((x+.5)/RV_SSAA-.5)+dy*((y+.5)/RV_SSAA-.5));
    return total/(RV_SSAA*RV_SSAA);
#else
    return rvEvaluate(input.uv);
#endif
}

float4 PSMaterialNormals(PixelInput input) : SV_Target
{
    float2 uv;float3 view;rvPlane(input.uv,uv,view);
    return rvSurface(uv);
}

float4 PSFixtureCoordinates(PixelInput input) : SV_Target
{
    float2 uv;float3 view;rvPlane(input.uv,uv,view);
    float lod=0;
#if RV_BACKEND == 2
    lod=normalMoments.CalculateLevelOfDetail(stabilitySampler,uv);
#endif
    return float4(uv,view.z,lod);
}
