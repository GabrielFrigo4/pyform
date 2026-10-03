import moderngl
import numpy as np


class TriangleMesh:
    """Encapsula a geometria do triângulo com dados intercalados de posição e cor."""

    def __init__(self, ctx: moderngl.Context, program: moderngl.Program) -> None:
        self.ctx = ctx
        self.program = program

        vertices = np.array(
            [
                0.0,
                0.5,
                0.0,
                1.0,
                0.0,
                0.0,
                -0.5,
                -0.5,
                0.0,
                0.0,
                1.0,
                0.0,
                0.5,
                -0.5,
                0.0,
                0.0,
                0.0,
                1.0,
            ],
            dtype="f4",
        )

        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, "3f 3f", "in_position", "in_color")],
        )

    def render(self) -> None:
        """Submete a geometria ao pipeline para rasterização."""
        self.vao.render(moderngl.TRIANGLES)

    def release(self) -> None:
        """Libera os buffers alocados na memória de vídeo."""
        if self.vbo:
            self.vbo.release()
        if self.vao:
            self.vao.release()
