from enum import Enum
from typing import List, Tuple, Type

from PyQt5 import QtWidgets, QtCore, QtGui

from mado.input_base import InputBase


# TODO test
class RadioInput(InputBase, QtWidgets.QWidget):
    radio_selected = QtCore.pyqtSignal(object)
    selected_data: any

    buttons_group: QtWidgets.QButtonGroup
    layout: QtWidgets.QHBoxLayout

    @QtCore.pyqtSlot()
    def on_button_toggled(self) -> None:
        button: QtWidgets.QRadioButton = self.sender()

        if button.isChecked():
            self.selected_data = button.property("user_data")

            self.radio_selected.emit(self.selected_data)

    def __init__(self, variants: List[Tuple[any, str]], radio_selected: QtCore.pyqtSlot = None,
                 horizontal: bool = True) -> None:
        super().__init__()

        self.buttons_group = QtWidgets.QButtonGroup()
        self.layout = QtWidgets.QHBoxLayout() if horizontal else QtWidgets.QVBoxLayout()
        self.selected_data = None

        for user_data, text in variants:
            button = QtWidgets.QRadioButton()
            button.setText(text)
            button.setProperty("user_data", user_data)

            button.toggled.connect(self.on_button_toggled)

            self.buttons_group.addButton(button)
            self.layout.addWidget(button)
        self.layout.addStretch()

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        if radio_selected is not None:
            self.radio_selected.connect(radio_selected)

    def get_value(self) -> any:
        return self.selected_data

    def set_value(self, value: any) -> None:
        for x in self.buttons_group.buttons():
            x: QtWidgets.QRadioButton

            if x.property("user_data") == value:
                x.setChecked(True)


# TODO test
class EnumRadioInput(RadioInput):
    enum: Type[Enum]

    def __init__(self, enum: Type[Enum], radio_selected: QtCore.pyqtSlot = None,
                 horizontal: bool = True) -> None:
        self.enum = enum
        to_list = [(x.name, x.value) for x in self.enum]

        super().__init__(to_list, radio_selected, horizontal)

    def get_value(self) -> any:
        key = self.selected_data
        if key is None:
            return None
        
        return self.enum[self.selected_data]

    def set_value(self, value: any) -> None:
        for x in self.buttons_group.buttons():
            x: QtWidgets.QRadioButton

            if x.property("user_data") == value.name:
                x.setChecked(True)


class BoolInput(InputBase, QtWidgets.QCheckBox):
    mark_changed = QtCore.pyqtSignal(bool)

    def __init__(self, label: str = None, mark_changed: QtCore.pyqtSlot = None):
        super().__init__()

        if label:
            self.setText(label)

        if mark_changed:
            self.mark_changed.connect(mark_changed)

        self.stateChanged.connect(lambda state: self.mark_changed.emit(state == QtCore.Qt.CheckState.Checked))

        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)

    def get_value(self) -> bool:
        return self.checkState() == QtCore.Qt.CheckState.Checked

    def set_value(self, value: bool) -> None:
        if value:
            self.toggle()
