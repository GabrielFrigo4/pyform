import unittest

from game import __version__
from game.code.graphics.shaders import FRAGMENT_SHADER, VERTEX_SHADER
from main import parse_args


class TestPyForm(unittest.TestCase):
    def test_version_present(self) -> None:
        self.assertTrue(isinstance(__version__, str))
        self.assertTrue(len(__version__) > 0)

    def test_shaders_defined(self) -> None:
        self.assertIn("#version 330 core", VERTEX_SHADER)
        self.assertIn("#version 330 core", FRAGMENT_SHADER)
        self.assertIn("in_position", VERTEX_SHADER)
        self.assertIn("frag_color", FRAGMENT_SHADER)

    def test_argument_defaults(self) -> None:
        args = parse_args([])
        self.assertEqual(args.width, 960)
        self.assertEqual(args.height, 540)
        self.assertEqual(args.title, "PyForm Graphics Engine")


if __name__ == "__main__":
    unittest.main()
