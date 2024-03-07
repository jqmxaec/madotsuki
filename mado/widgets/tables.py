from __future__ import annotations

from typing import List, Tuple, Optional

from PyQt5 import QtWidgets, QtGui, QtCore

fixed_hover_effects = """
QTableView::item:hover {
    background-color: transparent;
    margin: 0;
    padding: 0;
}

QTableView::item:selected {
    background-color: palette(hightlight);
    color: palette(highlightedText);
};"""


def make_item_with_data(value: str, item_data: any) -> QtGui.QStandardItem:
    item = QtGui.QStandardItem(str(value))
    item.setData(item_data)

    return item


class MReportTable(QtWidgets.QTableView):
    model: QtGui.QStandardItemModel

    def __init__(self):
        super().__init__()

        self.model = QtGui.QStandardItemModel()
        self.setModel(self.model)

        self.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QTableView.SelectionMode.NoSelection)

    def set_data(self, data: List[List[object]]) -> None:
        self.model.clear()

        for row in data:
            self.model.appendRow([QtGui.QStandardItem(str(col)) for col in row])


class MSelectableTable(QtWidgets.QTableView):
    model: QtGui.QStandardItemModel

    def __init__(self) -> None:
        super().__init__()

        self.model = QtGui.QStandardItemModel()
        self.setModel(self.model)

    def _selected_indexes_to_cells(self, indexes: List[QtCore.QModelIndex]) -> List[Tuple[Tuple[int, int], any]]:
        cells = [((x.row(), x.column()), self.model.itemFromIndex(x).data())
                 for x in indexes]

        return cells

    def get_selected_cells(self) -> List[Tuple[Tuple[int, int], any]]:
        selection_model = self.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        return self._selected_indexes_to_cells(selected_indexes)


class MRecordTable(MSelectableTable):
    row_double_clicked = QtCore.pyqtSignal(object)
    row_selected = QtCore.pyqtSignal(tuple)

    def __init__(self) -> None:
        super().__init__()

        self.setEditTriggers(QtWidgets.QTableView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.verticalHeader().setDefaultSectionSize(45)

        self.model.setHorizontalHeaderLabels(["Наименование"])

        self.doubleClicked.connect(
            lambda index: self.row_double_clicked.emit(self.model.itemFromIndex(index).data()))
        self.selectionModel().selectionChanged.connect(
            lambda selection: self.row_selected.emit(self._selected_indexes_to_cells(selection.indexes())[0]))

    def normalize(self):
        if self.model.columnCount() > 0:
            self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

    def set_data(self, data: List[Tuple[List[any], any]]):
        horizontal_labels = [self.model.horizontalHeaderItem(x).text() for x in range(self.model.columnCount())]

        self.model.clear()
        self.model.setHorizontalHeaderLabels(horizontal_labels)

        for x in data:
            rows, payload = x

            self.model.appendRow([make_item_with_data(x, payload) for x in rows])

    def get_selected_row(self) -> Optional[any]:
        cells = self.get_selected_cells()

        return cells[0][1] if len(cells) > 0 else None
