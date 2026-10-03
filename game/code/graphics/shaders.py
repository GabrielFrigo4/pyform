VERTEX_SHADER = """
#version 420 core

in vec3 in_position;

void main() {
    gl_Position = vec4(in_position, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 420 core

out vec4 frag_color;

void main() {
    frag_color = vec4(1.0, 1.0, 1.0, 1.0);
}
"""
