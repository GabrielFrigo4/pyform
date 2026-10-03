import glfw

from game.code.core.window import Window
from game.code.graphics.diagnostics import log_hardware_info


class Engine:
    """Coordena o loop principal da aplicação e o subsistema de renderização."""

    def __init__(self, width: int = 960, height: int = 540, title: str = "PyForm Engine") -> None:
        self.window = Window(width=width, height=height, title=title)
        log_hardware_info(self.window.ctx)

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

                # Limpeza de buffer com cor de fundo padrão
                self.window.ctx.clear(0.10, 0.12, 0.15, 1.0)

                self.window.swap_buffers()
                self.window.poll_events()
        finally:
            self.window.destroy()
