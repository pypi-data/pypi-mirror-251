import shutil
from typing import Annotated
from pathlib import Path

import typer

from .constants import LIB_DIR
from .zipapp import (
    build,
    dist,
    lib,
)
from .package import package as pkg
from .manifest import create_manifest


app = typer.Typer(no_args_is_help=True)


Source = Annotated[Path, typer.Argument(help='Path to Plugin source directory.', file_okay=False)]
Clean = Annotated[bool, typer.Option(help='Build using clean cache.')]


@app.command()
def zipapp(source: Source, clean: Clean = False):
    """
    Package Plugin as zipapp.
    """
    if clean:
        shutil.rmtree(LIB_DIR)
    lib.lib()
    build.build(source_path=source)
    dist.dist(source_dir=source)


Dir = Annotated[Path, typer.Argument(help='Path to directory to package.', file_okay=False)]


@app.command()
def package(dir: Dir):
    """
    Package directory.
    """
    pkg(dir)


@app.command()
def init_manifest(path: Path = Path.cwd()):
    """
    Initialize Plugin manifest.
    """
    create_manifest(str(path))
