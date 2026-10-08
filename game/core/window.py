import configparser
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import glfw
import moderngl
from PIL import Image

DEFAULT_ICON_PATH = Path(__file__).resolve().parents[1] / "assets" / "icons" / "icon.png"
MSAA_SAMPLES = 4


def _configure_cursor_environment() -> None:
    """Configura variáveis XCURSOR no ambiente para consistência entre desktops Wayland/X11."""
    base_paths = [
        str(Path.home() / ".local" / "share" / "icons"),
        str(Path.home() / ".icons"),
        "/usr/local/share/icons",
        "/usr/share/icons",
    ]
    if not os.environ.get("XCURSOR_PATH"):
        valid_paths = [p for p in base_paths if Path(p).is_dir()]
        if valid_paths:
            os.environ["XCURSOR_PATH"] = ":".join(valid_paths)

    if "XCURSOR_THEME" in os.environ and "XCURSOR_SIZE" in os.environ:
        return

    detected_theme: str | None = None
    detected_size: str | None = None

    default_theme_file = Path.home() / ".icons" / "default" / "index.theme"
    if default_theme_file.is_file():
        try:
            parser = configparser.ConfigParser()
            parser.read(default_theme_file)
            if parser.has_option("Icon Theme", "Inherits"):
                val = parser.get("Icon Theme", "Inherits").strip()
                if val:
                    detected_theme = val
        except Exception:
            pass

    config_candidates = (
        (Path.home() / ".config" / "kcminputrc", "Mouse", "cursorTheme", "cursorSize"),
        (
            Path.home() / ".config" / "kdedefaults" / "kcminputrc",
            "Mouse",
            "cursorTheme",
            "cursorSize",
        ),
        (
            Path.home() / ".config" / "gtk-4.0" / "settings.ini",
            "Settings",
            "gtk-cursor-theme-name",
            "gtk-cursor-theme-size",
        ),
        (
            Path.home() / ".config" / "gtk-3.0" / "settings.ini",
            "Settings",
            "gtk-cursor-theme-name",
            "gtk-cursor-theme-size",
        ),
    )

    for cfg_path, section, theme_key, size_key in config_candidates:
        if not cfg_path.is_file():
            continue
        try:
            parser = configparser.ConfigParser()
            parser.read(cfg_path)
            if not detected_theme and parser.has_option(section, theme_key):
                val = parser.get(section, theme_key).strip()
                if val:
                    detected_theme = val
            if not detected_size and parser.has_option(section, size_key):
                val = str(parser.getint(section, size_key))
                if val:
                    detected_size = val
            if detected_theme and detected_size:
                break
        except Exception:
            continue

    if (not detected_theme or not detected_size) and shutil.which("gsettings"):
        try:
            if not detected_theme:
                res = subprocess.run(
                    ["gsettings", "get", "org.gnome.desktop.interface", "cursor-theme"],
                    capture_output=True,
                    text=True,
                    timeout=0.2,
                )
                if res.returncode == 0:
                    val = res.stdout.strip().strip("'\"")
                    if val:
                        detected_theme = val
            if not detected_size:
                res = subprocess.run(
                    ["gsettings", "get", "org.gnome.desktop.interface", "cursor-size"],
                    capture_output=True,
                    text=True,
                    timeout=0.2,
                )
                if res.returncode == 0:
                    val = res.stdout.strip().strip("'\"")
                    if val and val.isdigit():
                        detected_size = val
        except Exception:
            pass

    if not detected_theme:
        desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").upper()
        if "KDE" in desktop:
            detected_theme = "breeze_cursors"
        elif any(d in desktop for d in ("GNOME", "UBUNTU")):
            detected_theme = "Adwaita"
        else:
            detected_theme = "default"

    if not detected_size:
        detected_size = "24"

    os.environ.setdefault("XCURSOR_THEME", detected_theme)
    os.environ.setdefault("XCURSOR_SIZE", detected_size)


class Window:
    """Gerencia a janela GLFW, o contexto ModernGL e o tratamento de eventos de tela."""

    def __init__(
        self,
        width: int,
        height: int,
        title: str,
        icon_path: Path | str | None = None,
        app_id: str = "moderngl",
    ) -> None:
        self.width = width
        self.height = height
        self.title = title
        self.app_id = app_id
        self.icon_path = Path(icon_path) if icon_path else DEFAULT_ICON_PATH

        self._init_glfw()
        self.handle = self._create_window()
        self.ctx = self._create_context()
        self._setup_callbacks()
        self._apply_window_icon()

    def _init_glfw(self) -> None:
        _configure_cursor_environment()
        glfw.set_error_callback(self._on_error)
        if not glfw.init():
            raise RuntimeError("Falha crítica ao inicializar o GLFW.")

    def _create_window(self) -> Any:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, True)
        glfw.window_hint(glfw.SAMPLES, MSAA_SAMPLES)

        if sys.platform == "darwin":
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

        if hasattr(glfw, "WAYLAND_APP_ID"):
            glfw.window_hint_string(glfw.WAYLAND_APP_ID, self.app_id)
        if hasattr(glfw, "X11_CLASS_NAME"):
            glfw.window_hint_string(glfw.X11_CLASS_NAME, self.app_id)

        handle = glfw.create_window(self.width, self.height, self.title, None, None)
        if not handle:
            glfw.terminate()
            raise RuntimeError("Falha ao instanciar janela GLFW.")

        glfw.make_context_current(handle)
        glfw.swap_interval(1)
        return handle

    def _create_context(self) -> moderngl.Context:
        ctx = moderngl.create_context()
        glfw.set_window_user_pointer(self.handle, self)
        fb_width, fb_height = glfw.get_framebuffer_size(self.handle)
        ctx.viewport = (0, 0, fb_width, fb_height)
        return ctx

    def _apply_window_icon(self) -> None:
        """Carrega e define o ícone da janela respeitando particularidades do compositor."""
        if not self.icon_path.exists():
            return

        is_wayland = (
            glfw.get_platform() == getattr(glfw, "PLATFORM_WAYLAND", -1)
            if hasattr(glfw, "get_platform")
            else bool(os.environ.get("WAYLAND_DISPLAY"))
        )

        if is_wayland:
            return

        try:
            icon_image = Image.open(self.icon_path).convert("RGBA")
            glfw.set_window_icon(self.handle, 1, [icon_image])
        except Exception as exc:
            print(f"[GLFW AVISO] Falha ao carregar ícone da janela: {exc}", file=sys.stderr)

    def _setup_callbacks(self) -> None:
        glfw.set_framebuffer_size_callback(self.handle, self._on_resize)
        glfw.set_key_callback(self.handle, self._on_key)

    @staticmethod
    def _on_error(error_code: int, description: str) -> None:
        print(f"[GLFW ERRO {error_code}] {description}", file=sys.stderr)

    @staticmethod
    def _on_resize(window: Any, width: int, height: int) -> None:
        win: Window = glfw.get_window_user_pointer(window)
        if win and win.ctx and width > 0 and height > 0:
            win.width = width
            win.height = height
            win.ctx.viewport = (0, 0, width, height)

    @staticmethod
    def _on_key(window: Any, key: int, scancode: int, action: int, mods: int) -> None:
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    @property
    def should_close(self) -> bool:
        return bool(glfw.window_should_close(self.handle))

    @property
    def framebuffer_size(self) -> tuple[int, int]:
        """Retorna as dimensões atuais em pixels do framebuffer."""
        return tuple(glfw.get_framebuffer_size(self.handle))

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
