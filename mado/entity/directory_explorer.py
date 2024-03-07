from __future__ import annotations

from PyQt5 import QtCore, QtGui

from mado.application_window import WindowWidget
from mado.entity.config import EntityConfig
from mado.entity.entity_explorer import EntityExplorer
from mado.entity.explorer_mixins import WithCreateOperation, WithDeleteOperation, WithManageOperation, WithViewOperation
from mado.widgets.misc import make_button


class ReadonlyDirectoryExplorer(EntityExplorer, WithViewOperation):
    def __init__(self, window: WindowWidget, config: EntityConfig) -> None:
        super().__init__(window, config)

        self.view_button.clicked.connect(self.open_view_screen)
        self.table.row_double_clicked.connect(self.open_view_screen)

    def make_ui(self, window: WindowWidget) -> None:
        super().make_ui(window)

        self.view_button = make_button("Просмотреть", icon=QtGui.QIcon(":/icons/view_record"))
        self.view_button.setEnabled(False)

        self.control_box.addStretch()
        self.control_box.addWidget(self.view_button)

    @QtCore.pyqtSlot()
    def on_table_row_selected(self) -> None:
        self.view_button.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_table_model_reset(self) -> None:
        self.view_button.setEnabled(False)


class DirectoryExplorer(EntityExplorer, WithCreateOperation, WithDeleteOperation, WithManageOperation):
    def __init__(self, window: WindowWidget, config: EntityConfig):
        super().__init__(window, config)

        self.table.row_double_clicked.connect(self.open_manage_screen)

        self.manage_button.clicked.connect(self.open_manage_screen)
        self.create_button.clicked.connect(self.open_create_screen)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)

    def make_ui(self, window: WindowWidget) -> None:
        super().make_ui(window)

        self.manage_button = make_button("Открыть запись")
        # icon=QtGui.QIcon(":/icons/manage_record")
        # self.manage_button.setIconSize(QtCore.QSize(30, 20))
        self.manage_button.setEnabled(False)

        self.delete_button = make_button("Удалить", icon=QtGui.QIcon(":/icons/delete_record"))
        self.delete_button.setEnabled(False)

        self.create_button = make_button("Создать", icon=QtGui.QIcon(":/icons/new_record"))

        self.control_box.addWidget(self.create_button)
        self.control_box.addWidget(self.delete_button)
        self.control_box.addStretch()
        self.control_box.addWidget(self.manage_button)

    @QtCore.pyqtSlot()
    def on_table_row_selected(self) -> None:
        self.manage_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_table_model_reset(self) -> None:
        self.manage_button.setEnabled(False)
        self.delete_button.setEnabled(False)
