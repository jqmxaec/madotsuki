from __future__ import annotations

from abc import abstractmethod
from functools import singledispatchmethod
from typing import Dict, Callable, Type, TYPE_CHECKING

from PyQt5 import QtWidgets, QtCore

if TYPE_CHECKING:
    from mado.screen import ScreenWidget


class Window:
    @abstractmethod
    def register_screen(self, id_: str,
                        screen: Type[ScreenWidget] | Callable[[WindowWidget, ...], ScreenWidget]) -> None:
        pass

    @abstractmethod
    def change_screen(self, id_: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def push_screen(self, id_: str, *args, **kwargs) -> None:
        pass

    @QtCore.pyqtSlot()
    def pop_screen(self) -> None:
        pass

    @abstractmethod
    def push_anon_screen(self, screen: ScreenWidget) -> None:
        pass

    @abstractmethod
    def change_anon_screen(self, screen: ScreenWidget) -> None:
        pass


class ApplicationWindow(Window, QtWidgets.QMainWindow):
    screens: Dict[str, Type[ScreenWidget] | Callable[[WindowWidget, ...], ScreenWidget]]
    stack: QtWidgets.QStackedLayout

    def __init__(self) -> None:
        super().__init__()

        self.stack = QtWidgets.QStackedLayout()
        self.screens = dict()

        self.resize(self.screen().size() * 0.83)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        layout.addLayout(self.stack)

        app_widget = QtWidgets.QWidget()
        app_widget.setLayout(layout)

        self.setCentralWidget(app_widget)

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


WindowWidget = Window | QtWidgets.QWidget
