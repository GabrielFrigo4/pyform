"""PyForm: ModernGL and GLFW graphics exploration engine."""

from typing import Any

__version__ = "0.1.0"
__all__ = ["__version__", "PyFormApp", "Window", "Renderer"]


def __getattr__(name: str) -> Any:
    if name == "PyFormApp":
        from pyform.app import PyFormApp
        return PyFormApp
    if name == "Renderer":
        from pyform.renderer import Renderer
        return Renderer
    if name == "Window":
        from pyform.window import Window
        return Window
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
