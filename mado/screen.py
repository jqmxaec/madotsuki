from PyQt5 import QtWidgets


class Screen:
    def reconfigure(self) -> None:
        pass


ScreenWidget = Screen | QtWidgets.QWidget
