from pathlib import Path
from zipfile import ZipFile

from .manifest import PluginManifest
from .constants import DIST_DIR
from .utils import convert_name


def package(dir: Path = Path(DIST_DIR)):
    """
    Packages plugin into a zip file for releases.
    """
    manifest = PluginManifest.from_path(dir)
    slugified_name = convert_name(manifest.Name)
    target_path = Path(slugified_name).with_suffix('.zip')
    with ZipFile(target_path, 'w') as zip_file:
        for file in Path(dir).iterdir():
            zip_file.write(file, arcname=file.name)
