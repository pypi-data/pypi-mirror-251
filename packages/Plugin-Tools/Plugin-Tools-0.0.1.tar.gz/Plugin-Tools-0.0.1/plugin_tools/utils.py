from .manifest import PluginManifest


def convert_name(name: str) -> str:
    """
    Converts plugin name to format Flow Launcher uses
    """
    return name.replace('_', '-').replace(" ", "-")


def plugin_install_dir(manifest: PluginManifest) -> str:
    """
    Returns the install directory for the plugin
    """
    return f'{convert_name(manifest.Name)}-{manifest.Version}'
