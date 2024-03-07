from __future__ import annotations
from typing import Dict, Type, Callable, TYPE_CHECKING

from PyQt5 import QtWidgets, QtCore

from mado.application_window import Window

if TYPE_CHECKING:
    from mado.application_window import WindowWidget
    from mado.screen import ScreenWidget


class Modal(Window, QtWidgets.QDialog):
    screens: Dict[str, Type[ScreenWidget] | Callable[[WindowWidget, ...], ScreenWidget]]
    stack: QtWidgets.QStackedLayout

    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)

        self.stack = QtWidgets.QStackedLayout()
        self.screens = dict()

        size = self.screen().size()
        self.resize(int(size.width() * 0.55), int(size.height() * 0.7))

        self.stack = QtWidgets.QStackedLayout()

        self.setLayout(self.stack)

    def register_screen(self, id_: str,
                        screen: Type[ScreenWidget] | Callable[[WindowWidget, ...], ScreenWidget]) -> None:
        self.screens[id_] = screen

    def change_anon_screen(self, screen: ScreenWidget) -> None:
        self.push_anon_screen(screen)

        while self.stack.count() > 1:
            widget = self.stack.takeAt(0).widget()
            if widget:
                widget.deleteLater()

    def push_anon_screen(self, screen: ScreenWidget) -> None:
        self.stack.addWidget(screen)

        self.stack.setCurrentIndex(self.stack.count() - 1)

    def change_screen(self, id_: str, *args, **kwargs) -> None:
        self.change_anon_screen(self.screens[id_](self, *args, **kwargs))

    def push_screen(self, id_: str, *args, **kwargs) -> None:
        self.push_anon_screen(self.screens[id_](self, *args, **kwargs))

    @QtCore.pyqtSlot()
    def pop_screen(self) -> None:
        widget = self.stack.widget(self.stack.count() - 1)
        self.stack.removeWidget(widget)
        widget.deleteLater()

        screen: ScreenWidget = self.stack.widget(self.stack.count() - 1)
        screen.reconfigure()
