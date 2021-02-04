# byte is a tool convert bytes to MB or GB etc.

import typer
from typing import Optional

__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        typer.echo(f"Bytes {__version__}")
        raise typer.Exit()


def emphasize(s: str):
    return typer.style(s, fg=typer.colors.GREEN, bold=True)


def main(
    capacity: int,
    MB: bool = typer.Option(False, "--mb", "-m", help="convert MB to each other"),
    GB: bool = typer.Option(False, "--gb", "-g", help="convert GB to each other"),
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    """
    Bytes is a tools to convert bytes and MB and GB each other.
    """
    if MB:
        b = capacity * 1024
        mb = capacity
        gb = capacity / 1024
    elif GB:
        b = capacity * 1024 * 1024
        mb = capacity * 1024
        gb = capacity
    else:
        b = capacity
        mb = capacity / 1024
        gb = capacity / 1024 / 1024

    bytes = emphasize("bytes: ")
    MB = emphasize("MB: ")
    GB = emphasize("GB: ")
    typer.echo(f"{bytes}{b}, {MB}{mb:.2f}, {GB}{gb:.2f}")


if __name__ == "__main__":
    typer.run(main)
