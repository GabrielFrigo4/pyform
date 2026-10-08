from pathlib import Path
from typing import Any

import moderngl

PACKAGE_DIR = Path(__file__).resolve().parents[1]
SHADERS_DIR = PACKAGE_DIR / "assets" / "shaders"


def load_shader_source(file_path: Path | str) -> str:
    """Lê o código fonte GLSL de um arquivo no disco com codificação UTF-8."""
    path = Path(file_path)
    if not path.is_absolute():
        path = SHADERS_DIR / path

    if not path.exists():
        raise FileNotFoundError(f"Shader não encontrado no caminho: {path}")

    return path.read_text(encoding="utf-8")


class ShaderProgram:
    """Gerencia a compilação, ciclo de vida e uniforms de um programa de shader OpenGL."""

    def __init__(
        self,
        ctx: moderngl.Context,
        vert_path: Path | str = "default.vert",
        frag_path: Path | str = "default.frag",
    ) -> None:
        self.ctx = ctx
        self.vert_source = load_shader_source(vert_path)
        self.frag_source = load_shader_source(frag_path)

        try:
            self.program = self.ctx.program(
                vertex_shader=self.vert_source,
                fragment_shader=self.frag_source,
            )
        except moderngl.Error as exc:
            raise RuntimeError(f"Falha na compilação do Shader Program:\n{exc}") from exc

    def set_uniform(self, name: str, value: Any) -> None:
        """Atualiza o valor de uma variável uniforme no shader se ela estiver ativa."""
        if name in self.program:
            self.program[name].value = value

    def release(self) -> None:
        """Libera os recursos alocados na GPU."""
        if self.program:
            self.program.release()
