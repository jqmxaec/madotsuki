from __future__ import annotations

from enum import Enum
from typing import Dict, OrderedDict

from PyQt5 import QtWidgets, QtCore

from mado.input_base import InputBase
from mado.utils import make_warning
from mado.capabilities import ReadonlyCapable


class FormBody(QtWidgets.QWidget):
    _readonly: bool
    _drawn: bool

    widgets: OrderedDict[str, InputBase | QtWidgets.QWidget]
    _labels: Dict[str, str]

    def __init__(self):
        super().__init__()

        self.widgets = OrderedDict[str, InputBase | QtWidgets.QWidget]()
        self._labels = dict()
        self._readonly = False
        self._drawn = False

        self.layout = QtWidgets.QFormLayout()
        self.setLayout(self.layout)

    def add(self, id_: str, w: QtWidgets.QWidget, label: str = None) -> FormBody:
        if label is not None:
            self._labels[id_] = label

        self.widgets[id_] = w

        return self

    def draw(self) -> FormBody:
        if self._drawn:
            raise Exception("already drawn")
        self._drawn = True

        if self._readonly:
            self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        for k, v in self.widgets.items():
            if self._readonly:
                if isinstance(v, ReadonlyCapable):
                    v.set_readonly()

                v.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

            if self._labels.get(k, None):
                self.layout.addRow(self._labels[k], v)
            else:
                self.layout.addRow(v)

        return self

    def set_value(self, value: Dict[str, any]) -> FormBody:
        for k, v in value.items():
            if self.widgets.get(k, None) is not None:
                self.widgets[k].set_value(v)

        return self

    def get_value(self) -> Dict[str, any]:
        res = dict()

        for k, v in self.widgets.items():
            if isinstance(v, InputBase):
                res[k] = v.get_value()

        return res

    def warn(self, msg: str) -> None:
        make_warning(self, msg).exec()

    def set_readonly(self) -> FormBody:
        self._readonly = True

        return self


class FormType(Enum):
    VIEW = 1
    MANAGE = 2
    CREATE = 3
