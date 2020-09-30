import os
from pathlib import Path


DEFAULT_CONFIG = Path.cwd() / "shimekiri" / "default_config.json"
STYLES_LIB = Path.cwd() / "res" / "styles"
ICONS_LIB = Path.cwd() / "res" / "images" / "icons"


def get_icon(name):
    return (ICONS_LIB / name).__str__()
