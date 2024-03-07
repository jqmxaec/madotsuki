from typing import Type, Callable, List

from mado.input_base import InputBase
from PyQt5 import QtWidgets, QtCore, QtGui

from mado.widgets.misc import make_button


class ListBody(QtWidgets.QListWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setSelectionMode(QtWidgets.QListWidget.SelectionMode.SingleSelection)

    def get_value(self) -> List[any]:
        res = list()

        for i in range(self.count()):
            list_item_widget = self.itemWidget(self.item(i))
            inp = list_item_widget.layout().itemAt(0).widget()

            res.append(inp.get_value())

        return res

    def add_entry(self, inp: InputBase | QtWidgets.QWidget) -> InputBase:
        item = QtWidgets.QListWidgetItem()

        w = QtWidgets.QWidget()
        w.setLayout(QtWidgets.QVBoxLayout())
        w.layout().setContentsMargins(10, 20, 10, 20)
        w.layout().addWidget(inp)

        item.setSizeHint(w.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, w)

        return inp


class ListInput(InputBase, QtWidgets.QWidget):
    list_body: ListBody

    control_box: QtWidgets.QHBoxLayout
    layout: QtWidgets.QVBoxLayout

    add_button: QtWidgets.QPushButton
    delete_button: QtWidgets.QPushButton

    input_delegate: Type[InputBase] | Callable[[], InputBase]

    def __init__(self, input_delegate: Type[InputBase] | Callable[[], InputBase],
                 list_body: ListBody = None) -> None:
        super().__init__()

        if list_body is None:
            list_body = ListBody()

        self.list_body = list_body
        self.input_delegate = input_delegate

        self.add_button = make_button("Добавить", icon=QtGui.QIcon(":/icons/new_record"))
        self.delete_button = make_button("Удалить", icon=QtGui.QIcon(":/icons/delete_record"))
        self.delete_button.setEnabled(False)
        self.control_box = QtWidgets.QHBoxLayout()
        self.control_box.addWidget(self.add_button)
        self.control_box.addStretch()
        self.control_box.addWidget(self.delete_button)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.control_box)
        self.layout.addWidget(self.list_body)

        self.setLayout(self.layout)

        self.list_body.itemClicked.connect(lambda: self.delete_button.setEnabled(True))
        self.list_body.model().modelReset.connect(lambda: self.delete_button.setEnabled(False))

        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)

    def get_value(self) -> List[any]:
        return self.list_body.get_value()

    def set_value(self, value: List[any]) -> None:
        self.list_body.clear()

        for x in value:
            inp = self.list_body.add_entry(self.input_delegate())

            inp.set_value(x)

    @QtCore.pyqtSlot()
    def on_add_button_clicked(self) -> None:
        self.list_body.add_entry(self.input_delegate())

    @QtCore.pyqtSlot()
    def on_delete_button_clicked(self) -> None:
        row = self.list_body.currentRow()

        if row != -1:
            self.list_body.takeItem(row)
