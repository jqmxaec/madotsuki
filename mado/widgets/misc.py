from __future__ import annotations

from PyQt5 import QtWidgets, QtGui, QtCore

from mado.application_window import WindowWidget


def make_font(family: str = None, size: int = None, bold: bool = False, italic: bool = False,
              underline: bool = False) -> QtGui.QFont:
    w = QtGui.QFont()

    if family is not None:
        w.setFamily(family)
    if size is not None:
        w.setPointSize(size)

    w.setBold(bold)
    w.setItalic(italic)
    w.setUnderline(underline)

    return w


def make_label(text: str = "", font: QtGui.QFont = None) -> QtWidgets.QLabel:
    w = QtWidgets.QLabel()

    w.setText(text)
    if font is not None:
        w.setFont(font)

    return w


def make_button(label: str = "", font: QtGui.QFont = None, flat: bool = False,
                icon: QtGui.QIcon = None, icon_size: int = 20) -> QtWidgets.QPushButton:
    w = QtWidgets.QPushButton()

    w.setText(label)
    if font is not None:
        w.setFont(font)
    if icon is not None:
        w.setIcon(icon)
        w.setIconSize(QtCore.QSize(icon_size, icon_size))

    w.setFlat(flat)

    return w


def make_icon_button(flat: bool = False, icon: QtGui.QIcon = None,
                     icon_size: int = 20) -> QtWidgets.QPushButton:
    w = QtWidgets.QPushButton()

    if icon is not None:
        w.setIcon(icon)
        w.setIconSize(QtCore.QSize(icon_size, icon_size))

    w.setFlat(flat)

    return w


def make_back_button(window: WindowWidget) -> QtWidgets.QPushButton:
    w = make_button("Назад", flat=True, icon=QtGui.QIcon(":/icons/go_back"), icon_size=20,
                    font=make_font(size=14))
    w.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
    w.clicked.connect(window.pop_screen)

    return w
