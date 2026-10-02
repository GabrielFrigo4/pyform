from typing import Optional
from pyform.renderer import Renderer
from pyform.window import Window


class PyFormApp:
    def __init__(
        self,
        width: int = 960,
        height: int = 540,
        title: str = "PyForm Graphics Engine",
    ) -> None:
        self.window = Window(
            width=width,
            height=height,
            title=title,
            resize_callback=self._on_resize,
        )
        self.renderer = Renderer()
        self.renderer.resize(self.window.width, self.window.height)

    def _on_resize(self, width: int, height: int) -> None:
        self.renderer.resize(width, height)

    def run(self) -> None:
        try:
            while not self.window.should_close:
                self.window.poll_events()
                current_time = self.window.get_time()
                self.renderer.render(current_time, self.window.width, self.window.height)
                self.window.swap_buffers()
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        self.renderer.destroy()
        self.window.destroy()
