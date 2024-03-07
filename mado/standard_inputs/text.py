from __future__ import annotations

from PyQt5 import QtWidgets, QtCore

from mado.input_base import InputBase


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


class PasswordInput(TextInput):
    def __init__(self, placeholder: str = None, text_edited: QtCore.pyqtSlot = None) -> None:
        super().__init__(placeholder, text_edited)

        self.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)


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
