// Original synthetic material experiment; never installed into a game.
// Plane XY, world +Z normal, orthographic view +Z; linear RGB, alpha 1.
cbuffer MaterialParameters : register(b0)
{
    float normalAmount;       // [0,1], zero restores the flat normal
    float roughnessAmount;    // [0,1], zero restores uniform roughness
    float lightSide;          // exactly -1 or +1
    float reserved;
};
struct PixelInput { float4 position : SV_Position; float2 uv : TEXCOORD0; };
static const float PI = 3.141592653589793;

float lattice(uint2 cell, uint seed)
{
    uint v = (cell.x * 37u + cell.y * 101u + cell.x * cell.y * 17u + seed * 13u) % 251u;
    return ((v * v * 29u + v * 53u + seed * 19u) % 251u) / 250.0;
}

// Value and analytic derivatives of a C1-continuous interpolated height field.
float3 noiseGradient(float2 p, uint seed)
{
    uint2 cell = uint2(floor(p));
    float2 f = frac(p), blend = f * f * (3.0 - 2.0 * f);
    float2 derivative = 6.0 * f * (1.0 - f);
    float a = lattice(cell, seed), b = lattice(cell + uint2(1,0), seed);
    float c = lattice(cell + uint2(0,1), seed), d = lattice(cell + uint2(1,1), seed);
    return float3(lerp(lerp(a,b,blend.x),lerp(c,d,blend.x),blend.y),
        lerp(b-a,d-c,blend.y) * derivative.x,
        lerp(c-a,d-b,blend.x) * derivative.y);
}

float4 surface(float2 uv)
{
    float2 gradient = 0;
    [branch] if (normalAmount != 0)
    {
        gradient = 0.12 * noiseGradient(uv*10,1).yz
                 + 0.10 * noiseGradient(uv*32,2).yz
                 + 0.055 * noiseGradient(uv*90,3).yz;
        float groove = 0.07 * cos(2.0 * PI * dot(uv,float2(18,1.5)));
        gradient += groove * float2(1,1.5/18.0);
    }
    float roughness = 0.64;
    [branch] if (roughnessAmount != 0)
        roughness += roughnessAmount * 0.44 * (noiseGradient(uv*7,4).x - 0.5);
    return float4(normalize(float3(-normalAmount*gradient,1)),roughness);
}

float4 PSMaterialNormals(PixelInput input) : SV_Target
{
    return surface(input.uv); // diagnostic XYZ unit normal, A roughness
}

float4 PSMaterial(PixelInput input) : SV_Target
{
    float4 material = surface(input.uv);
    float3 n = material.xyz, l = normalize(float3(0.85*lightSide,0.25,0.65));
    float3 v = float3(0,0,1), h = normalize(l+v);
    float nl = saturate(dot(n,l)), nv = saturate(dot(n,v));
    float nh = saturate(dot(n,h)), vh = saturate(dot(v,h));
    float alpha = material.w * material.w, a2 = alpha * alpha;
    float denominator = nh*nh*(a2-1.0)+1.0;
    float distribution = a2 / (PI*denominator*denominator);
    // Separable Smith GGX masking; guarded cosines, single-scattering model.
    float gl = 2.0*nl / max(nl+sqrt(a2+(1.0-a2)*nl*nl),1e-6);
    float gv = 2.0*nv / max(nv+sqrt(a2+(1.0-a2)*nv*nv),1e-6);
    float fresnel = 0.04 + 0.96*pow(1.0-vh,5.0);
    float specular = distribution*gl*gv*fresnel / max(4.0*nl*nv,1e-6);
    float3 albedo = float3(0.13,0.135,0.14);
    float3 diffuse = (1.0-fresnel)*albedo/PI;
    return float4(0.12*albedo + 1.8*nl*(diffuse+specular),1);
}
