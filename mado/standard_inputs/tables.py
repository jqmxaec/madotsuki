from typing import List

from PyQt5 import QtWidgets, QtGui, QtCore

from mado.input_base import InputBase


class TableInput(InputBase, QtWidgets.QTableView):
    model: QtGui.QStandardItemModel
    cell_edited = QtCore.pyqtSignal(tuple, str)

    def __init__(self, cell_edited: QtCore.pyqtSlot = None):
        super().__init__()

        self.model = QtGui.QStandardItemModel()
        self.setModel(self.model)

        self.model.itemChanged.connect(self.on_item_changed)

        if cell_edited is not None:
            self.cell_edited.connect(cell_edited)

    def set_value(self, value: List[List[str]]):
        for y, row in enumerate(value):
            for x, column in enumerate(row):
                if column is None:
                    continue

                self.model.setItem(y, x, QtGui.QStandardItem(column))

    def get_value(self) -> List[List[str]]:
        res = list()

        for row in range(self.model.rowCount()):
            row_data = list()
            for col in range(self.model.columnCount()):
                index = self.model.index(row, col)
                item = self.model.data(index)
                row_data.append(item)
            res.append(row_data)

        return res

    # здесь лучше не аннотировать pyqtSlot....
    def on_item_changed(self, item: QtGui.QStandardItem) -> None:
        self.cell_edited.emit((item.row(), item.column()), item.text())

    def reset_with_dimensions(self, rows: int, cols: int) -> None:
        self.model.clear()

        for _ in range(rows):
            self.model.appendRow([QtGui.QStandardItem() for _ in range(cols)])


class DelegatedTableInput(InputBase, QtWidgets.QTableView):
    model: QtGui.QStandardItemModel

    delegated_cells: dict[int, dict[int, InputBase]]

    def __init__(self):
        super().__init__()

        self.model = QtGui.QStandardItemModel()
        self.setModel(self.model)

        self.delegated_cells = dict()

    def set_value(self, value: List[List[any]]):
        for y, row in enumerate(value):
            for x, column in enumerate(row):
                if column is None:
                    continue

                delegated_cell = self.delegated_cells.get(y, dict()).get(x, None)
                if delegated_cell is not None:
                    delegated_cell.set_value(column)
                else:
                    self.model.setItem(y, x, QtGui.QStandardItem(column))

    def get_value(self) -> List[List[any]]:
        res = list()

        for row in range(self.model.rowCount()):
            row_data = list()
            for col in range(self.model.columnCount()):
                delegated_cell = self.delegated_cells.get(row, dict()).get(col, None)
                if delegated_cell is not None:
                    row_data.append(delegated_cell.get_value())
                else:
                    row_data.append(self.model.item(row, col).text())
            res.append(row_data)

        return res

    def set_custom_input(self, row: int, col: int, inp: InputBase | QtWidgets.QWidget) -> None:
        if self.delegated_cells.get(row) is None:
            self.delegated_cells[row] = dict()

        self.delegated_cells[row][col] = inp
        self.setIndexWidget(self.model.index(row, col), inp)

    def reset_with_dimensions(self, rows: int, cols: int) -> None:
        self.model.clear()

        for _ in range(rows):
            self.model.appendRow([QtGui.QStandardItem() for _ in range(cols)])
