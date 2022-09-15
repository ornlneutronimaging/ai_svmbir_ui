from ._version import get_versions
from qtpy.uic import loadUi
import os

__version__ = get_versions()['version']
del get_versions

__all__ = ['load_ui']

root = os.path.dirname(os.path.realpath(__file__))
refresh_image = os.path.join(root, "static/refresh.png")
more_infos = os.path.join(root, "static/more_infos.png")

UI_TITLE = "Ai Svmbir UI"


def load_ui(ui_filename, baseinstance):
    return loadUi(ui_filename, baseinstance=baseinstance)
