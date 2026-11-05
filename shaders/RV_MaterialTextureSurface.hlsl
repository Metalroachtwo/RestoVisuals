// Original compact fixture surface; replaces only surface() in the original
// procedural source IN MEMORY. The BRDF, parameters and entries are unchanged.
Texture2D<float4> normalRoughness : register(t0);
SamplerState materialSampler : register(s0);
float4 surface(float2 uv)
{
    float4 material = float4(0,0,1,0.64);
    [branch] if (normalAmount != 0 || roughnessAmount != 0)
    {
        float4 sampleValue = normalRoughness.Sample(materialSampler,uv / RV_DOMAIN);
        float3 normal = normalize(float3(normalAmount * sampleValue.xy / max(sampleValue.z,0.001),1));
        material = float4(normal,0.64+roughnessAmount*(sampleValue.w-0.64));
    }
    return material;
}
