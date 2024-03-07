from __future__ import annotations
import sys
import os
from typing import Tuple, Callable, TYPE_CHECKING

from PyQt5 import QtWidgets

if TYPE_CHECKING:
    from mado.application_window import ApplicationWindow

app_name = ""
app: ApplicationWindow = None


def set_app(a: ApplicationWindow) -> None:
    global app

    app = a


def get_app() -> ApplicationWindow:
    return app


def set_app_name(name: str) -> None:
    global app_name

    app_name = name


def absolute_bundled_path(path: str) -> str:
    prefix = "."

    if getattr(sys, "frozen", False):
        prefix = sys._MEIPASS

    return os.path.join(prefix, path)


def absolute_appdata_path(path: str) -> str:
    prefix = "."

    if getattr(sys, "frozen", False):
        prefix = os.getenv("APPDATA")

    prefix = os.path.join(prefix, app_name)

    if not os.path.exists(prefix):
        os.makedirs(prefix)

    return os.path.join(prefix, path)


def make_warning(parent: any, msg: str, title: str = None) -> QtWidgets.QMessageBox:
    box = QtWidgets.QMessageBox(parent)

    box.setText(msg)
    box.setIcon(QtWidgets.QMessageBox.Icon.Warning)

    if title is not None:
        box.setWindowTitle(title)

    return box


def make_info(parent: any, msg: str, title: str = None) -> QtWidgets.QMessageBox:
    box = QtWidgets.QMessageBox(parent)

    box.setText(msg)
    box.setIcon(QtWidgets.QMessageBox.Icon.Information)

    if title is not None:
        box.setWindowTitle(title)

    return box
