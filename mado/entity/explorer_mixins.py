from __future__ import annotations

from typing import Dict

from PyQt5 import QtWidgets, QtCore
from sqlalchemy import exc

from mado.entity.entity_explorer import EntityExplorer
from mado.utils import make_warning
from mado.widgets.modal import Modal


class WithCreateOperation:
    create_button: QtWidgets.QPushButton

    @QtCore.pyqtSlot()
    def open_create_screen(self: EntityExplorer) -> None:
        modal = Modal(self)

        creator = self.config.creator(modal, self.config)

        created_id = -1
        created_data = dict()

        @QtCore.pyqtSlot(int, dict)
        def on_record_created(id_: int, data: Dict[str, any]) -> None:
            nonlocal created_id, created_data

            created_id = id_
            created_data = data

            self.fill_table()

        @QtCore.pyqtSlot()
        def on_record_creation_finalized() -> None:
            manager = self.config.manager(modal, self.config, created_id, created_data)

            manager.record_edited.connect(lambda *args, **kwargs: self.fill_table())

            modal.push_anon_screen(manager)

        creator.record_created.connect(on_record_created)
        creator.record_creation_finalized.connect(on_record_creation_finalized)

        modal.change_anon_screen(creator)
        modal.exec()


class WithManageOperation:
    manage_button: QtWidgets.QPushButton

    @QtCore.pyqtSlot()
    def open_manage_screen(self: EntityExplorer):
        modal = Modal(self)

        row = self.table.get_selected_row()
        if row is None:
            return

        manager = self.config.manager(modal, self.config, row)
        manager.record_edited.connect(lambda *args, **kwargs: self.fill_table())

        modal.change_anon_screen(manager)
        modal.exec()


class WithDeleteOperation:
    delete_button: QtWidgets.QPushButton

    @QtCore.pyqtSlot()
    def on_delete_button_clicked(self) -> None:
        id_ = self.table.get_selected_row()
        if id_ is None:
            return

        dialog = QtWidgets.QMessageBox()
        dialog.setIcon(QtWidgets.QMessageBox.Icon.Question)
        dialog.setWindowTitle(f"{self.config.entity_label}: удаление записи")
        dialog.setText("Вы действительно хотите удалить запись?")
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.No | QtWidgets.QMessageBox.StandardButton.Yes)
        dialog.button(QtWidgets.QMessageBox.StandardButton.Yes).setText("Да")
        dialog.button(QtWidgets.QMessageBox.StandardButton.No).setText("Нет")

        reply = dialog.exec()
        if reply == QtWidgets.QMessageBox.StandardButton.No:
            return

        try:
            self.config.repository.delete(id_)
        except exc.IntegrityError as e:
            make_warning(self, self.config.process_delete_error(str(e.orig)), "Ошибка").exec()

        self.fill_table()


class WithViewOperation:
    view_button: QtWidgets.QPushButton

    @QtCore.pyqtSlot()
    def open_view_screen(self) -> None:
        modal = Modal(self)

        row = self.table.get_selected_row()
        if row is None:
            return

        viewer = self.config.viewer(modal, self.config, lambda *args, **kwargs: modal.accept(), row)

        modal.change_anon_screen(viewer)
        modal.exec()
