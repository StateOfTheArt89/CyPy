varying vec2 uv;
varying vec4 color;
void main()
{
    // Transforming The Vertex
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
 
    // Passing The Texture Coordinate Of Texture Unit 0 To The Fragment Shader
    uv = vec2(gl_MultiTexCoord0);
    color =  gl_Color;
}