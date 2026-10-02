import sys
from typing import Any, Callable, Optional
import glfw


class Window:
    def __init__(
        self,
        width: int = 960,
        height: int = 540,
        title: str = "PyForm Graphics Engine",
        resize_callback: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.title = title
        self._resize_callback = resize_callback

        def _error_handler(code: int, description: str) -> None:
            print(f"GLFW [{code}]: {description}", file=sys.stderr)

        glfw.set_error_callback(_error_handler)

        if not glfw.init():
            raise RuntimeError("Falha ao inicializar GLFW.")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

        self._handle = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self._handle:
            glfw.terminate()
            raise RuntimeError("Falha ao criar janela GLFW.")

        glfw.make_context_current(self._handle)
        glfw.swap_interval(1)

        glfw.set_framebuffer_size_callback(self._handle, self._on_resize)

    def _on_resize(self, window: Any, width: int, height: int) -> None:
        self.width = width
        self.height = height
        if self._resize_callback:
            self._resize_callback(width, height)

    @property
    def handle(self) -> Any:
        return self._handle

    @property
    def should_close(self) -> bool:
        return bool(glfw.window_should_close(self._handle))

    def poll_events(self) -> None:
        glfw.poll_events()
        if glfw.get_key(self._handle, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self._handle, True)

    def swap_buffers(self) -> None:
        glfw.swap_buffers(self._handle)

    def get_time(self) -> float:
        return float(glfw.get_time())

    def destroy(self) -> None:
        if self._handle:
            glfw.destroy_window(self._handle)
            self._handle = None
        glfw.terminate()
