from __future__ import annotations

from PyQt5 import QtWidgets, QtCore

from mado.application_window import WindowWidget
from mado.entity.config import EntityConfig
from mado.screen import Screen
from mado.widgets.misc import make_font, make_label, make_back_button
from mado.widgets.tables import MRecordTable, fixed_hover_effects


class EntityExplorer(Screen, QtWidgets.QWidget):
    table: MRecordTable
    config: EntityConfig

    top_box: QtWidgets.QHBoxLayout
    control_box: QtWidgets.QHBoxLayout
    table_box: QtWidgets.QVBoxLayout
    layout: QtWidgets.QVBoxLayout

    back_button: QtWidgets.QPushButton
    name_label: QtWidgets.QLabel

    def __init__(self, window: WindowWidget, config: EntityConfig):
        super().__init__()

        self.config = config
        window.setWindowTitle(f"{self.config.entity_label}: обзор записей")

        self.make_ui(window)

        self.table.row_selected.connect(self.on_table_row_selected)
        self.table.model.modelReset.connect(self.on_table_model_reset)

        self.fill_table()

    def make_ui(self, window: WindowWidget) -> None:
        self.table = MRecordTable()
        self.table.model.setHorizontalHeaderLabels(self.config.table_labels)
        # self.table.setStyleSheet(fixed_hover_effects)

        self.name_label = make_label(self.config.entity_label, font=make_font(size=14))

        self.back_button = make_back_button(window)
        self.back_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.top_box = QtWidgets.QHBoxLayout()
        self.top_box.addWidget(self.back_button)
        self.top_box.addSpacing(5)
        self.top_box.addWidget(self.name_label)
        self.top_box.addStretch()

        self.control_box = QtWidgets.QHBoxLayout()

        self.table_box = QtWidgets.QVBoxLayout()
        self.table_box.addWidget(self.table)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addLayout(self.top_box)
        self.layout.addSpacing(10)
        self.layout.addLayout(self.control_box)
        self.layout.addLayout(self.table_box)

    def fill_table(self):
        self.table.set_data(
            [([x[y] for y in self.config.table_columns], x.id) for x in self.config.repository.fetch_all()])
        self.table.normalize()

    @QtCore.pyqtSlot()
    def on_table_row_selected(self) -> None:
        pass

    @QtCore.pyqtSlot()
    def on_table_model_reset(self) -> None:
        pass
