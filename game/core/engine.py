import glfw

from game.graphics.diagnostics import log_hardware_info
from game.scenes.base import Scene
from game.scenes.sandbox import SandboxScene

from .window import Window


class Engine:
    """Coordena o loop principal da aplicação e o subsistema de renderização."""

    def __init__(
        self,
        width: int = 960,
        height: int = 540,
        title: str = "PyForm Engine",
        scene: Scene | None = None,
        app_id: str = "moderngl",
    ) -> None:
        self.window = Window(width=width, height=height, title=title, app_id=app_id)
        log_hardware_info(self.window.ctx)

        self.scene: Scene = scene or SandboxScene(self.window.ctx)
        self._last_time = glfw.get_time()
        self.delta_time = 0.0

    def _update_delta_time(self) -> None:
        current_time = glfw.get_time()
        self.delta_time = current_time - self._last_time
        self._last_time = current_time

    def run(self) -> None:
        """Executa o loop contínuo de renderização."""
        try:
            while not self.window.should_close:
                self._update_delta_time()

                self.window.ctx.clear(0.08, 0.09, 0.12, 1.0)

                self.scene.update(self.delta_time)
                self.scene.render()

                self.window.swap_buffers()
                self.window.poll_events()
        finally:
            self.scene.release()
            self.window.destroy()
