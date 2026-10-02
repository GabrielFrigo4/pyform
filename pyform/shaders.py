VERTEX_SHADER = """#version 330 core
in vec2 in_position;
in vec3 in_color;

out vec3 v_color;
out vec2 v_uv;

uniform float u_time;
uniform vec2 u_resolution;

void main() {
    float aspect = u_resolution.x / max(u_resolution.y, 1.0);
    vec2 pos = in_position;
    pos.x /= aspect;

    v_color = in_color;
    v_uv = in_position;
    gl_Position = vec4(pos, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """#version 330 core
in vec3 v_color;
in vec2 v_uv;

out vec4 frag_color;

uniform float u_time;
uniform vec2 u_resolution;

void main() {
    vec2 st = v_uv;
    float dist = length(st);

    float angle = atan(st.y, st.x);
    float petals = 6.0;
    float radius = 0.55 + 0.15 * cos(angle * petals + u_time * 2.0);

    float edge = smoothstep(radius, radius - 0.015, dist);

    vec3 col_a = vec3(0.12, 0.58, 0.95);
    vec3 col_b = vec3(0.95, 0.28, 0.55);
    vec3 gradient = mix(col_a, col_b, 0.5 + 0.5 * sin(angle * 3.0 + u_time));

    vec3 bg_color = vec3(0.06, 0.07, 0.09);
    vec3 final_rgb = mix(bg_color, gradient * v_color, edge);

    frag_color = vec4(final_rgb, 1.0);
}
"""
