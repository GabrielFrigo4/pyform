import moderngl

from game.graphics.mesh import TriangleMesh
from game.graphics.shader import ShaderProgram


class SandboxScene:
    """Cena demonstrativa de introdução à rasterização e shaders com ModernGL."""

    def __init__(self, ctx: moderngl.Context) -> None:
        self.ctx = ctx
        self.shader = ShaderProgram(self.ctx)
        self.mesh = TriangleMesh(self.ctx, self.shader.program)
        self.elapsed_time = 0.0

    def update(self, delta_time: float) -> None:
        self.elapsed_time += delta_time
        self.shader.set_uniform("u_time", self.elapsed_time)

    def render(self) -> None:
        self.mesh.render()

    def release(self) -> None:
        self.mesh.release()
        self.shader.release()
