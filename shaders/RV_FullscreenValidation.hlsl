// Original windowless validation vertex shader; never installed into CSP.
struct VertexOutput
{
    float4 position : SV_Position;
    float2 uv : TEXCOORD0;
};

VertexOutput VSFullscreen(uint vertexID : SV_VertexID)
{
    VertexOutput result;
    result.uv = float2((vertexID << 1) & 2, vertexID & 2);
    result.position = float4(result.uv * float2(2.0, -2.0) + float2(-1.0, 1.0), 0.0, 1.0);
    return result;
}
