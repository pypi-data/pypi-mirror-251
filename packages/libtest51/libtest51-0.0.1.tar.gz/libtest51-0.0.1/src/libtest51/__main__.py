"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Libtest51."""


if __name__ == "__main__":
    main(prog_name="libtest51")  # pragma: no cover
