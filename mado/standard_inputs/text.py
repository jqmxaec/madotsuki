from __future__ import annotations

from typing import Tuple

from PyQt5 import QtWidgets, QtCore, QtGui

from mado.input_base import InputBase
from mado.widgets.misc import make_icon_button


class TextInput(InputBase, QtWidgets.QLineEdit):
    def __init__(self, placeholder: str = None, text_edited: QtCore.pyqtSlot = None) -> None:
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)

        if placeholder is not None:
            self.setPlaceholderText(placeholder)
        if text_edited is not None:
            self.textEdited.connect(text_edited)

    def set_value(self, value: any) -> None:
        self.setText(str(value))

    def get_value(self) -> str:
        return self.text()


class PasswordInput(InputBase, QtWidgets.QWidget):
    text_input: TextInput
    reveal_button: QtWidgets.QPushButton
    layout: QtWidgets.QHBoxLayout
    password_revealed: bool

    def __init__(self, placeholder: str = None, text_edited: QtCore.pyqtSlot = None) -> None:
        super().__init__()

        self.password_revealed = False

        self.text_input = TextInput(placeholder, text_edited)
        self.reveal_button = make_icon_button(icon=QtGui.QIcon(":/icons/view_record"))
        self.reveal_button.clicked.connect(self.on_reveal_button_clicked)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.reveal_button)

        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.text_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def set_value(self, value: str) -> None:
        self.text_input.set_value(value)

    def get_value(self) -> str:
        return self.text_input.get_value()

    @QtCore.pyqtSlot()
    def on_reveal_button_clicked(self) -> None:
        self.password_revealed = not self.password_revealed

        if self.password_revealed:
            self.text_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.text_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)


class MultilineTextInput(InputBase, QtWidgets.QTextEdit):
    def __init__(self, placeholder: str = None, text_edited: QtCore.pyqtSlot = None) -> None:
        super().__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)

        if placeholder is not None:
            self.setPlaceholderText(placeholder)
        if text_edited is not None:
            self.textChanged.connect(text_edited)

    def set_value(self, value: any) -> None:
        self.setText(str(value))

    def get_value(self) -> str:
        return self.toPlainText()


class NumberInput(InputBase, QtWidgets.QSpinBox):
    def __init__(self, number_edited: QtCore.pyqtSlot = None, values_range: Tuple[int, int] = (0, 99),
                 default_value: int = None):
        super().__init__()

        self.setRange(*values_range)

        if default_value is None:
            default_value = values_range[0]
        self.setValue(default_value)

        if number_edited:
            self.valueChanged.connect(number_edited)

    def set_value(self, value: int) -> None:
        self.setValue(value)

    def get_value(self) -> int:
        return self.value()
