// Original RestoVisuals feasibility shader. Not installed or bound to CSP.
// Host must validate stage encoding, resource format and Pure ownership.
// Defaults for an identity pass: exposureEV=0, shoulderStrength=0, saturation=1.

Texture2D<float4> sourceColor : register(t0);
SamplerState sourceSampler : register(s0);

cbuffer ColorParameters : register(b0)
{
    float exposureEV;         // [-4, 4]
    float shoulderStrength;   // [0, 1]
    float saturation;         // [0, 1.5]
    float reserved;
};

struct PixelInput
{
    float4 position : SV_Position;
    float2 uv : TEXCOORD0;
};

float3 processLinear(float3 color)
{
    float3 exposed = max(color, 0.0) * exp2(clamp(exposureEV, -4.0, 4.0));
    float luminance = dot(exposed, float3(0.2126, 0.7152, 0.0722));
    float3 compressed = exposed / (1.0 + saturate(shoulderStrength) * luminance);
    float grey = dot(compressed, float3(0.2126, 0.7152, 0.0722));
    return clamp(lerp(grey.xxx, compressed, clamp(saturation, 0.0, 1.5)), 0.0, 65504.0);
}

float3 decodeSrgb(float3 value)
{
    value = saturate(value);
    return float3(
        value.r <= 0.04045 ? value.r / 12.92 : pow((value.r + 0.055) / 1.055, 2.4),
        value.g <= 0.04045 ? value.g / 12.92 : pow((value.g + 0.055) / 1.055, 2.4),
        value.b <= 0.04045 ? value.b / 12.92 : pow((value.b + 0.055) / 1.055, 2.4));
}

float3 encodeSrgb(float3 value)
{
    value = saturate(value);
    return float3(
        value.r <= 0.0031308 ? 12.92 * value.r : 1.055 * pow(value.r, 1.0 / 2.4) - 0.055,
        value.g <= 0.0031308 ? 12.92 * value.g : 1.055 * pow(value.g, 1.0 / 2.4) - 0.055,
        value.b <= 0.0031308 ? 12.92 * value.b : 1.055 * pow(value.b, 1.0 / 2.4) - 0.055);
}

float4 PSLinear(PixelInput input) : SV_Target
{
    float4 sampleColor = sourceColor.Sample(sourceSampler, input.uv);
    return float4(processLinear(sampleColor.rgb), sampleColor.a);
}

float4 PSSrgb(PixelInput input) : SV_Target
{
    float4 sampleColor = sourceColor.Sample(sourceSampler, input.uv);
    return float4(encodeSrgb(processLinear(decodeSrgb(sampleColor.rgb))), sampleColor.a);
}
