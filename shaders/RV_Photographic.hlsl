// Original offline photographic core. Host supplies explicit linear Rec.709 or sRGB.
// Controls are specialized from validated Settings; no CSP texture/source assumption.
Texture2D<float4> sourceColor : register(t0);
SamplerState sourceSampler : register(s0);
struct PixelInput {float4 position:SV_Position; float2 uv:TEXCOORD0;};
float3 decode(float3 v) {
    v=saturate(v);
    return float3(v.r<=.04045?v.r/12.92:pow((v.r+.055)/1.055,2.4),
                  v.g<=.04045?v.g/12.92:pow((v.g+.055)/1.055,2.4),
                  v.b<=.04045?v.b/12.92:pow((v.b+.055)/1.055,2.4));
}
float3 encode(float3 v) {
    v=saturate(v);
    return float3(v.r<=.0031308?12.92*v.r:1.055*pow(v.r,1.0/2.4)-.055,
                  v.g<=.0031308?12.92*v.g:1.055*pow(v.g,1.0/2.4)-.055,
                  v.b<=.0031308?12.92*v.b:1.055*pow(v.b,1.0/2.4)-.055);
}
float3 photographic(float3 original) {
    const float3 weights=float3(.2126,.7152,.0722);
    const float3 gains=float3(RV_WR,RV_WG,RV_WB);
    float3 rgb=original*gains/dot(gains,weights)*exp2(RV_EV);
    float y=dot(rgb,weights);
    if(y>0) {
        float tone=.18*pow(abs(y)/.18,RV_CONTRAST);
        tone*=1+RV_SHADOW/(1+tone/.18);
        rgb*=tone/y;
        float grey=dot(rgb,weights);
        rgb=max(0,grey+RV_SATURATION*(rgb-grey));
        float peak=max(rgb.r,max(rgb.g,rgb.b));
        if(peak>.72) {
            float mapped=.72+(peak-.72)/(1+RV_HIGHLIGHT*(peak-.72)/.28);
            rgb*=mapped/peak;
        }
    }else rgb=0;
    return clamp(original+RV_INTENSITY*(rgb-original),0,65504);
}
float4 PSLinear(PixelInput input):SV_Target {
    float4 c=sourceColor.Sample(sourceSampler,input.uv);
#if RV_NEUTRAL
    return c;
#else
    return float4(photographic(c.rgb),c.a);
#endif
}
float4 PSSrgb(PixelInput input):SV_Target {
    float4 c=sourceColor.Sample(sourceSampler,input.uv);
#if RV_NEUTRAL
    return c;
#else
    return float4(encode(photographic(decode(c.rgb))),c.a);
#endif
}
