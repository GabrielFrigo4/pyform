import os
import re
import unittest

from game import __version__
from game.core.window import DEFAULT_ICON_PATH, _configure_cursor_environment
from game.graphics.shader import load_shader_source
from game.scenes.base import Scene
from game.scenes.sandbox import SandboxScene
from main import parse_args

VERTEX_SHADER = load_shader_source("default.vert")
FRAGMENT_SHADER = load_shader_source("default.frag")


def extract_glsl_interface(glsl_source: str) -> dict[str, dict[str, str]]:
    """Remove comentários e extrai declarações de 'in', 'out' e 'uniform'

    retornando um dicionário no formato: {qualificador: {nome_variavel: tipo}}
    """
    clean_code = re.sub(r"//.*", "", glsl_source)
    clean_code = re.sub(r"/\*.*?\*/", "", clean_code, flags=re.DOTALL)

    pattern = re.compile(
        r"(?:layout\s*\([^)]*\)\s*)?"
        r"\b(in|out|uniform)\b\s+"
        r"([a-zA-Z_][a-zA-Z0-9_]*)\s+"
        r"([a-zA-Z_][a-zA-Z0-9_]*)\s*;"
    )

    interface: dict[str, dict[str, str]] = {
        "in": {},
        "out": {},
        "uniform": {},
    }
    for qualifier, var_type, name in pattern.findall(clean_code):
        interface[qualifier][name] = var_type

    return interface


class TestShaderPipelineContract(unittest.TestCase):
    """Valida as regras fundamentais do pipeline gráfico sem acoplar a nomes fixos."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.v_interface = extract_glsl_interface(VERTEX_SHADER)
        cls.f_interface = extract_glsl_interface(FRAGMENT_SHADER)

    def test_glsl_version_headers(self) -> None:
        """Garante que a diretiva #version 420 core está no topo de ambos."""
        for name, src in [
            ("Vertex", VERTEX_SHADER),
            ("Fragment", FRAGMENT_SHADER),
        ]:
            lines = [line.strip() for line in src.strip().splitlines() if line.strip()]
            self.assertTrue(
                lines[0].startswith("#version 420 core"),
                f"{name} shader deve iniciar com '#version 420 core'. Encontrado: {lines[0]}",
            )

    def test_entrypoints_exist(self) -> None:
        """Ambos os shaders precisam conter a função main."""
        self.assertRegex(VERTEX_SHADER, r"\bvoid\s+main\s*\(\s*\)")
        self.assertRegex(FRAGMENT_SHADER, r"\bvoid\s+main\s*\(\s*\)")

    def test_vertex_writes_gl_position(self) -> None:
        """Vertex shader precisa definir as coordenadas de clip space."""
        self.assertIn("gl_Position", VERTEX_SHADER)

    def test_fragment_declares_render_target_output(self) -> None:
        """No OpenGL 4.2 Core, o fragment shader deve declarar ao menos um 'out vec4'."""
        f_outs = self.f_interface["out"]
        self.assertGreater(
            len(f_outs),
            0,
            "Fragment shader não declara nenhum 'out' para o framebuffer.",
        )
        self.assertTrue(
            any(t in ("vec4", "dvec4", "uvec4", "ivec4") for t in f_outs.values()),
            "Nenhum render target de 4 componentes encontrado nos 'out' do fragment.",
        )

    def test_pipeline_varying_interface_matching(self) -> None:
        """Toda saída (out) do Vertex que chega no Fragment (in) deve coincidir em tipo e nome."""
        v_outs = self.v_interface["out"]
        f_ins = self.f_interface["in"]

        for var_name, var_type in v_outs.items():
            if var_name in f_ins:
                self.assertEqual(
                    var_type,
                    f_ins[var_name],
                    (
                        f"Tipo incompatível no canal '{var_name}': "
                        f"Vertex emite '{var_type}', mas Fragment espera '{f_ins[var_name]}'."
                    ),
                )

        for var_name in f_ins:
            self.assertIn(
                var_name,
                v_outs,
                (
                    f"Fragment shader exige a entrada '{var_name}', "
                    "mas ela não é emitida pelo Vertex shader."
                ),
            )


class TestSceneArchitecture(unittest.TestCase):
    """Valida o contrato e a estrutura do subsistema de cenas."""

    def test_sandbox_scene_satisfies_protocol(self) -> None:
        """Verifica se SandboxScene satisfaz em runtime o protocolo Scene."""
        self.assertTrue(issubclass(SandboxScene, Scene))
        self.assertTrue(hasattr(SandboxScene, "update"))
        self.assertTrue(hasattr(SandboxScene, "render"))
        self.assertTrue(hasattr(SandboxScene, "release"))


class TestGraphicsArchitecture(unittest.TestCase):
    """Valida a integridade do subsistema de malhas e utilitários gráficos."""

    def test_mesh_classes_hierarchy(self) -> None:
        """Verifica se TriangleMesh e QuadMesh herdam corretamente de Mesh."""
        from game.graphics import Mesh, QuadMesh, TriangleMesh

        self.assertTrue(issubclass(TriangleMesh, Mesh))
        self.assertTrue(issubclass(QuadMesh, Mesh))

    def test_diagnostics_callable(self) -> None:
        """Verifica se a função de log de hardware é executável."""
        from game.graphics import log_hardware_info

        self.assertTrue(callable(log_hardware_info))


class TestEngineSanity(unittest.TestCase):
    """Testes estruturais de CLI e metadados."""

    def test_version_format(self) -> None:
        self.assertRegex(__version__, r"^\d+\.\d+\.\d+(\.[a-zA-Z0-9]+)?$")

    def test_argument_defaults(self) -> None:
        args = parse_args([])
        self.assertEqual(args.width, 960)
        self.assertEqual(args.height, 540)
        self.assertEqual(args.title, "PyForm Graphics Engine")

    def test_argument_custom_values(self) -> None:
        args = parse_args(["--width", "1280", "--height", "720", "--title", "Dev Sandbox"])
        self.assertEqual(args.width, 1280)
        self.assertEqual(args.height, 720)
        self.assertEqual(args.title, "Dev Sandbox")

    def test_default_icon_exists(self) -> None:
        self.assertTrue(
            DEFAULT_ICON_PATH.exists(),
            f"Ícone padrão não encontrado: {DEFAULT_ICON_PATH}",
        )


class TestWindowEnvironment(unittest.TestCase):
    """Valida o isolamento e configuração defensiva do ambiente gráfico."""

    def test_configure_cursor_environment_sets_defaults(self) -> None:
        orig_theme = os.environ.get("XCURSOR_THEME")
        orig_size = os.environ.get("XCURSOR_SIZE")

        try:
            if "XCURSOR_THEME" in os.environ:
                del os.environ["XCURSOR_THEME"]
            if "XCURSOR_SIZE" in os.environ:
                del os.environ["XCURSOR_SIZE"]

            _configure_cursor_environment()

            self.assertIn("XCURSOR_THEME", os.environ)
            self.assertIn("XCURSOR_SIZE", os.environ)
            self.assertTrue(bool(os.environ["XCURSOR_THEME"]))
            self.assertTrue(os.environ["XCURSOR_SIZE"].isdigit())
        finally:
            if orig_theme is not None:
                os.environ["XCURSOR_THEME"] = orig_theme
            elif "XCURSOR_THEME" in os.environ:
                del os.environ["XCURSOR_THEME"]

            if orig_size is not None:
                os.environ["XCURSOR_SIZE"] = orig_size
            elif "XCURSOR_SIZE" in os.environ:
                del os.environ["XCURSOR_SIZE"]


if __name__ == "__main__":
    unittest.main()
