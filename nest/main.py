# byte is a tool convert bytes to MB or GB etc.

import typer
from typing import Optional
from .translate import trans
import sys
import subprocess
import os

__version__ = "0.1.0"

app = typer.Typer()


@app.command(name="t")
def trans_cli(
    query: str,
    source: str = typer.Option("auto", "--source", "-s", help="source language"),
    target: str = typer.Option("auto", "--target", "-t", help="target launguage"),
    engine: str = typer.Option("baidu", "--engine", "-e", help="translate engine"),
):
    """command t is a translation tool."""
    typer.echo("\033[1;31m---------------------\033[0m")
    result = trans(query, src=source, to=target, engine=engine)
    typer.echo(result)
    typer.echo("\033[1;31m---------------------\033[0m")
    typer.echo("翻译结果来自: %s" % engine)


def version_callback(value: bool):
    if value:
        typer.echo(f"Bytes {__version__}")
        raise typer.Exit()


def emphasize(s: str):
    return typer.style(s, fg=typer.colors.GREEN, bold=True)


@app.command(name="b")
def bytes_cli(
    capacity: int,
    MB: bool = typer.Option(False, "--mb", "-m", help="convert MB to each other"),
    GB: bool = typer.Option(False, "--gb", "-g", help="convert GB to each other"),
    version: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    """
    command b is a bytes convert tool.
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


@app.command("w")
def weather_cli(location: str):
    """
    command w is a weather query tool.
    """
    if location != "":
        location = "/" + location

    if sys.platform == "win32":
        # use powershell to exec
        s = subprocess.Popen(
            [
                "powershell.exe",
                'Invoke-RestMethod "wttr.in{}?lang=zh&format=3"'.format(location),
            ],
            stdout=sys.stdout,
        )
        s.communicate()
    else:
        os.system('curl "wttr.in{}?lang=zh&format=3"'.format(location))


if __name__ == "__main__":
    app()
