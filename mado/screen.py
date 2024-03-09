from typing import Union

from PyQt5 import QtWidgets


class Screen:
    def reconfigure(self) -> None:
        pass


ScreenWidget = Union[Screen, QtWidgets.QWidget]
