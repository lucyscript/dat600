"""CLI entrypoint for generating the Org solution."""

from .report import render_org


def main() -> None:
    print(render_org())


if __name__ == "__main__":
    main()
