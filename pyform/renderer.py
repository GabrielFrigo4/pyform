import array
from typing import Any
import moderngl

from pyform.shaders import FRAGMENT_SHADER, VERTEX_SHADER


class Renderer:
    def __init__(self) -> None:
        self.ctx: moderngl.Context = moderngl.create_context()
        self.prog = self.ctx.program(
            vertex_shader=VERTEX_SHADER,
            fragment_shader=FRAGMENT_SHADER,
        )

        vertices = array.array(
            "f",
            [
                -1.0, -1.0, 1.0, 0.4, 0.4,
                 1.0, -1.0, 0.4, 1.0, 0.4,
                -1.0,  1.0, 0.4, 0.4, 1.0,
                -1.0,  1.0, 0.4, 0.4, 1.0,
                 1.0, -1.0, 0.4, 1.0, 0.4,
                 1.0,  1.0, 1.0, 1.0, 0.4,
            ],
        )

        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.vertex_array(
            self.prog,
            [(self.vbo, "2f 3f", "in_position", "in_color")],
        )

    def resize(self, width: int, height: int) -> None:
        self.ctx.viewport = (0, 0, width, height)

    def render(self, time_sec: float, width: int, height: int) -> None:
        self.ctx.clear(0.06, 0.07, 0.09, 1.0)

        if "u_time" in self.prog:
            self.prog["u_time"].value = float(time_sec)

        if "u_resolution" in self.prog:
            self.prog["u_resolution"].value = (float(width), float(height))

        self.vao.render(moderngl.TRIANGLES)

    def destroy(self) -> None:
        self.vbo.release()
        self.vao.release()
        self.prog.release()
        self.ctx.release()
