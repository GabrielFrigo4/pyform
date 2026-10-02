import argparse
import sys


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="PyForm: ModernGL and GLFW graphics exploration engine.",
    )
    parser.add_argument("--width", type=int, default=960, help="Largura da janela em pixels")
    parser.add_argument("--height", type=int, default=540, help="Altura da janela em pixels")
    parser.add_argument(
        "--title",
        type=str,
        default="PyForm Graphics Engine",
        help="Título da janela gráfica",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()
    try:
        from pyform.app import PyFormApp

        app = PyFormApp(
            width=args.width,
            height=args.height,
            title=args.title,
        )
        app.run()
    except ImportError as error:
        print(f"Dependência gráfica ausente: {error}", file=sys.stderr)
        print("Instale o ambiente com: 'make install' ou 'uv sync'.", file=sys.stderr)
        sys.exit(1)
    except Exception as error:
        print(f"Erro fatal: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
