import shutil
from typing import Annotated
from pathlib import Path

import typer

from .constants import LIB_DIR, REQUIREMENTS, PLUGIN_MANIFEST
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
Requirements = Annotated[Path, typer.Option(help='Path to requirements.txt file.', file_okay=True, dir_okay=False)]

@app.command()
def zipapp(source: Source, clean: Clean = False, requirements: Requirements = Path(REQUIREMENTS)):
    """
    Package Plugin as zipapp.
    """
    if not Path(source).joinpath(PLUGIN_MANIFEST).exists():
        typer.echo(f'Plugin manifest not found in {source}.')
        raise typer.Exit(code=1)
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
