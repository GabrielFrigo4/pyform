import argparse
import sys

import glfw
import moderngl


def on_error(error_code: int, description: str) -> None:
    """Captura e exibe falhas internas do GLFW."""
    print(f"[GLFW ERRO {error_code}] {description}", file=sys.stderr)


def on_framebuffer_resize(window, width: int, height: int) -> None:
    """Atualiza a viewport do ModernGL quando a janela for redimensionada."""
    ctx: moderngl.Context = glfw.get_window_user_pointer(window)
    if ctx and width > 0 and height > 0:
        ctx.viewport = (0, 0, width, height)


def on_key(window, key: int, scancode: int, action: int, mods: int) -> None:
    """Fecha a aplicação ao pressionar ESC."""
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PyForm Engine")
    parser.add_argument("--width", type=int, default=960, help="Largura da janela")
    parser.add_argument("--height", type=int, default=540, help="Altura da janela")
    parser.add_argument(
        "--title",
        type=str,
        default="PyForm Graphics Engine",
        help="Título da janela",
    )
    return parser.parse_args(args)


def main() -> None:
    args = parse_args()

    glfw.set_error_callback(on_error)

    if not glfw.init():
        sys.exit("Falha crítica ao inicializar o GLFW.")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, True)

    if sys.platform == "darwin":
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

    window = glfw.create_window(args.width, args.height, args.title, None, None)
    if not window:
        glfw.terminate()
        sys.exit("Falha ao instanciar janela GLFW.")

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    ctx = moderngl.create_context()
    glfw.set_window_user_pointer(window, ctx)

    fb_width, fb_height = glfw.get_framebuffer_size(window)
    ctx.viewport = (0, 0, fb_width, fb_height)

    glfw.set_framebuffer_size_callback(window, on_framebuffer_resize)
    glfw.set_key_callback(window, on_key)

    has_compute = "GL_ARB_compute_shader" in ctx.extensions
    has_spirv = "GL_ARB_gl_spirv" in ctx.extensions

    print("=" * 64)
    print(f" Renderer  : {ctx.info['GL_RENDERER']}")
    print(f" Versão GL : {ctx.info['GL_VERSION']}")
    print(f" Compute   : {'Disponível (ARB)' if has_compute else 'Não suportado'}")
    print(f" SPIR-V    : {'Disponível (ARB)' if has_spirv else 'Não suportado'}")
    print("=" * 64)

    while not glfw.window_should_close(window):
        ctx.clear(0.10, 0.12, 0.15, 1.0)
        glfw.swap_buffers(window)
        glfw.poll_events()

    ctx.release()
    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
