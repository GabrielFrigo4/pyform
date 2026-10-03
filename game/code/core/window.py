import sys

import glfw
import moderngl


class Window:
    """Gerencia a janela GLFW, o contexto ModernGL e o tratamento de eventos de tela."""

    def __init__(self, width: int, height: int, title: str) -> None:
        self.width = width
        self.height = height
        self.title = title

        self._init_glfw()
        self.handle = self._create_window()
        self.ctx = self._create_context()
        self._setup_callbacks()

    def _init_glfw(self) -> None:
        glfw.set_error_callback(self._on_error)
        if not glfw.init():
            sys.exit("Falha crítica ao inicializar o GLFW.")

    def _create_window(self):
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, True)

        if sys.platform == "darwin":
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

        handle = glfw.create_window(self.width, self.height, self.title, None, None)
        if not handle:
            glfw.terminate()
            sys.exit("Falha ao instanciar janela GLFW.")

        glfw.make_context_current(handle)
        glfw.swap_interval(1)
        return handle

    def _create_context(self) -> moderngl.Context:
        ctx = moderngl.create_context()
        glfw.set_window_user_pointer(self.handle, self)
        fb_w, fb_h = glfw.get_framebuffer_size(self.handle)
        ctx.viewport = (0, 0, fb_w, fb_h)
        return ctx

    def _setup_callbacks(self) -> None:
        glfw.set_framebuffer_size_callback(self.handle, self._on_resize)
        glfw.set_key_callback(self.handle, self._on_key)

    @staticmethod
    def _on_error(error_code: int, description: str) -> None:
        print(f"[GLFW ERRO {error_code}] {description}", file=sys.stderr)

    @staticmethod
    def _on_resize(window, width: int, height: int) -> None:
        win: Window = glfw.get_window_user_pointer(window)
        if win and win.ctx and width > 0 and height > 0:
            win.width = width
            win.height = height
            win.ctx.viewport = (0, 0, width, height)

    @staticmethod
    def _on_key(window, key: int, scancode: int, action: int, mods: int) -> None:
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    @property
    def should_close(self) -> bool:
        return bool(glfw.window_should_close(self.handle))

    def swap_buffers(self) -> None:
        glfw.swap_buffers(self.handle)

    def poll_events(self) -> None:
        glfw.poll_events()

    def destroy(self) -> None:
        if self.ctx:
            self.ctx.release()
        if self.handle:
            glfw.destroy_window(self.handle)
        glfw.terminate()
