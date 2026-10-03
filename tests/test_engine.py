import re
import unittest

from game import __version__
from game.code.graphics.shader import load_shader_source
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


if __name__ == "__main__":
    unittest.main()
