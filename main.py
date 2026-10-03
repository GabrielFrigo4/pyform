import argparse

from game.code.core.engine import Engine


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
    engine = Engine(width=args.width, height=args.height, title=args.title)
    engine.run()


if __name__ == "__main__":
    main()
