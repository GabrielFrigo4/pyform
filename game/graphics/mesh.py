import moderngl
import numpy as np


class Mesh:
    """Estrutura base para buffers de vértice (VBO) e arrays de vértice (VAO)."""

    def __init__(
        self,
        ctx: moderngl.Context,
        program: moderngl.Program,
        vertices: np.ndarray,
    ) -> None:
        self.ctx = ctx
        self.program = program
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


class TriangleMesh(Mesh):
    """Encapsula a geometria do triângulo com dados intercalados de posição e cor."""

    def __init__(self, ctx: moderngl.Context, program: moderngl.Program) -> None:
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
        super().__init__(ctx, program, vertices)


class QuadMesh(Mesh):
    """Encapsula um quad de tela cheia para shaders analíticos e computação gráfica."""

    def __init__(self, ctx: moderngl.Context, program: moderngl.Program) -> None:
        vertices = np.array(
            [
                -1.0,
                -1.0,
                0.0,
                1.0,
                0.0,
                0.0,
                1.0,
                -1.0,
                0.0,
                0.0,
                1.0,
                0.0,
                -1.0,
                1.0,
                0.0,
                0.0,
                0.0,
                1.0,
                -1.0,
                1.0,
                0.0,
                0.0,
                0.0,
                1.0,
                1.0,
                -1.0,
                0.0,
                0.0,
                1.0,
                0.0,
                1.0,
                1.0,
                0.0,
                1.0,
                1.0,
                1.0,
            ],
            dtype="f4",
        )
        super().__init__(ctx, program, vertices)
