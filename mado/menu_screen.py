from __future__ import annotations

from PyQt5 import QtWidgets, QtCore

from mado.application_window import WindowWidget
from mado.screen import Screen
from mado.widgets.misc import make_label, make_font, make_back_button, make_button


class MenuScreen(Screen, QtWidgets.QWidget):
    top_box: QtWidgets.QHBoxLayout
    layout: QtWidgets.QVBoxLayout
    header_label: QtWidgets.QLabel
    back_button: QtWidgets.QPushButton
    sections: QtWidgets.QGridLayout

    window_title: str
    window_instance: WindowWidget

    def __init__(self, window: WindowWidget, header: str = "", window_title: str = "",
                 need_back_button: bool = True) -> None:
        super().__init__()

        self.i = 0
        self.window_title = window_title
        self.window_instance = window

        self.window_instance.setWindowTitle(self.window_title)

        self.make_ui(self.window_instance, need_back_button)

        self.header_label.setText(header)

    def make_ui(self, window: WindowWidget, need_back_button: bool) -> None:
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.header_label = make_label(font=make_font(size=14))
        self.top_box = QtWidgets.QHBoxLayout()

        if need_back_button:
            self.back_button = make_back_button(window)
            self.top_box.addWidget(self.back_button)

        self.top_box.addSpacing(5)
        self.top_box.addWidget(self.header_label)
        self.top_box.addStretch()

        self.sections = QtWidgets.QGridLayout()
        self.sections.setContentsMargins(20, 20, 20, 20)
        self.sections.setSpacing(25)

        self.layout.addLayout(self.top_box)
        self.layout.addLayout(self.sections)
        self.layout.addStretch()

    def add_section(self, section: MenuScreenSection):
        self.sections.addWidget(section, self.i // 2, self.i % 2)
        self.i += 1

    def reconfigure(self) -> None:
        self.window_instance.setWindowTitle(self.window_title)


class MenuScreenSection(QtWidgets.QWidget):
    header_label: QtWidgets.QLabel
    layout: QtWidgets.QVBoxLayout
    buttons: QtWidgets.QVBoxLayout

    def __init__(self, header: str = "") -> None:
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.header_label = make_label(header, font=make_font(size=16, bold=True))
        self.header_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.buttons = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.header_label)
        self.layout.addSpacing(7)
        self.layout.addLayout(self.buttons)
        self.layout.addStretch()

    def add_button(self, text: str = "", button_clicked: QtCore.pyqtSlot = None) -> None:
        button = make_button(text, font=make_font(underline=True), flat=True)
        button.setStyleSheet('color: "darkblue";')
        button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        if button_clicked is not None:
            button.clicked.connect(button_clicked)

        self.buttons.addWidget(button)

    def add_existing_button(self, button: QtWidgets.QPushButton) -> None:
        self.buttons.addWidget(button)
