varying vec2 uv; 
varying vec4 color;
uniform sampler2D tex;
uniform sampler2D glow;

void main()
{
    // Sampling The Texture And Passing It To The Frame Buffer
    vec4 fragColor = texture2D(tex, uv)* 0.5 + texture2D(glow,uv)*0.5;
    gl_FragColor  = vec4(fragColor.r * color.r,fragColor.g * color.g,fragColor.b * color.b, 1.0);
}