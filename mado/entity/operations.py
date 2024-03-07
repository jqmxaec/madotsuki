from __future__ import annotations

from abc import abstractmethod
from typing import Callable, TYPE_CHECKING

from PyQt5 import QtWidgets, QtCore, QtGui
from sqlalchemy import exc

from mado.application_window import Window, WindowWidget
from mado.form_body import FormBody, FormType
from mado.screen import Screen
from mado.utils import make_warning, make_info
from mado.widgets.misc import make_button

if TYPE_CHECKING:
    from mado.entity.config import EntityConfig


class RecordCreator(Screen):
    record_created: QtCore.pyqtSignal
    record_creation_finalized: QtCore.pyqtSignal

    config: EntityConfig

    @abstractmethod
    def __init__(self, window: WindowWidget, config: EntityConfig) -> None:
        super().__init__()


class RecordManager(Screen):
    record_edited: QtCore.pyqtSignal
    record_edition_finalized: QtCore.pyqtSignal

    config: EntityConfig

    @abstractmethod
    def __init__(self, window: WindowWidget, config: EntityConfig, id_: int,
                 initial_data: dict = None) -> None:
        super().__init__()


class RecordViewer(Screen):
    close_viewer: callable
    config: EntityConfig

    @abstractmethod
    def __init__(self, window: WindowWidget, config: EntityConfig, close_viewer: callable, id_: int,
                 initial_data: dict = None) -> None:
        super().__init__()


class BasicRecordCreator(RecordCreator, QtWidgets.QWidget):
    record_created = QtCore.pyqtSignal(int, dict)
    record_creation_finalized = QtCore.pyqtSignal()

    control_box: QtWidgets.QHBoxLayout
    form_box: QtWidgets.QVBoxLayout
    create_button: QtWidgets.QPushButton
    layout: QtWidgets.QVBoxLayout

    form_body: FormBody

    def __init__(self, window: WindowWidget, config: EntityConfig) -> None:
        super().__init__(window, config)

        self.config = config
        self.form_body = self.config.make_form(FormType.CREATE)

        self.make_ui()

        self.create_button.clicked.connect(self.on_create_button_clicked)

        window.setWindowTitle(f"{self.config.entity_label}: создание записи")

    def make_ui(self) -> None:
        self.control_box = QtWidgets.QHBoxLayout()
        self.control_box.setContentsMargins(10, 5, 5, 5)
        self.form_box = QtWidgets.QVBoxLayout()

        self.create_button = make_button("Создать", icon=QtGui.QIcon(":/icons/new_record"))
        self.create_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.control_box.addWidget(self.create_button)
        self.control_box.addStretch()

        self.form_box.addWidget(self.form_body.draw())
        self.form_box.addStretch()

        self.layout.addLayout(self.control_box)
        self.layout.addLayout(self.form_box)

    @QtCore.pyqtSlot()
    def on_create_button_clicked(self):
        value = self.config.to_database(self.form_body.get_value())

        err = self.config.validate_record(value)
        if err is not None:
            make_warning(self, err, "Ошибка").exec()

            return

        try:
            id_ = self.config.repository.insert(value)
            self.record_created.emit(id_, value)

            make_info(self, "Запись создана", "Успешно").exec()
            self.record_creation_finalized.emit()
        except exc.IntegrityError as e:
            make_warning(self, self.config.process_commit_error(str(e.orig)), "Ошибка").exec()


class BasicRecordManager(RecordManager, QtWidgets.QWidget):
    record_edited = QtCore.pyqtSignal(dict)
    record_edition_finalized = QtCore.pyqtSignal()

    control_box: QtWidgets.QHBoxLayout
    form_box: QtWidgets.QVBoxLayout
    edit_button: QtWidgets.QPushButton
    layout: QtWidgets.QVBoxLayout

    form_body: FormBody
    record_id: int

    def __init__(self, window: WindowWidget, config: EntityConfig, id_: int,
                 initial_data: dict = None) -> None:
        super().__init__(window, config, id_, initial_data)

        self.config = config
        self.record_id = id_
        self.form_body = self.config.make_form(FormType.MANAGE)

        if initial_data is None:
            initial_data = self.config.from_database(self.config.repository.fetch_one(id_))
        self.form_body.set_value(initial_data)

        self.make_ui()

        self.edit_button.clicked.connect(self.on_save_button_clicked)

        window.setWindowTitle(f"{self.config.entity_label}: управление записью")

    def make_ui(self) -> None:
        self.control_box = QtWidgets.QHBoxLayout()
        self.control_box.setContentsMargins(10, 5, 5, 5)
        self.form_box = QtWidgets.QVBoxLayout()
        self.edit_button = make_button("Сохранить", icon=QtGui.QIcon(":/icons/save_record"))
        self.edit_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.control_box.addWidget(self.edit_button)
        self.control_box.addStretch()

        self.form_box.addWidget(self.form_body.draw())
        self.form_box.addStretch()

        self.layout.addLayout(self.control_box)
        self.layout.addLayout(self.form_box)

    @QtCore.pyqtSlot()
    def on_save_button_clicked(self) -> None:
        value = self.config.to_database(self.form_body.get_value())

        err = self.config.validate_record(value)
        if err is not None:
            make_warning(self, err, "Ошибка").exec()

            return

        try:
            self.config.repository.update(self.record_id, value)
            self.record_edited.emit(value)

            make_info(self, "Запись изменена", "Успешно").exec()
            self.record_edition_finalized.emit()
        except exc.IntegrityError as e:
            make_warning(self, self.config.process_commit_error(str(e.orig)), "Ошибка").exec()


class BasicRecordViewer(RecordViewer, QtWidgets.QWidget):
    control_box: QtWidgets.QHBoxLayout
    form_box: QtWidgets.QVBoxLayout
    close_button: QtWidgets.QPushButton
    layout: QtWidgets.QVBoxLayout

    form_body: FormBody

    def __init__(self, window: WindowWidget, config: EntityConfig, close_viewer: callable, id_: int,
                 initial_data: dict = None) -> None:
        super().__init__(window, config, close_viewer, id_, initial_data)

        self.config = config
        self.close_viewer = close_viewer
        self.form_body = self.config.make_form(FormType.VIEW)

        if initial_data is None:
            initial_data = self.config.from_database(self.config.repository.fetch_one(id_))
        self.form_body.set_value(initial_data)

        self.make_ui()

        self.close_button.clicked.connect(close_viewer)

        self.setWindowTitle(f"{self.config.entity_label}: просмотр записи")

    def make_ui(self) -> None:
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.control_box = QtWidgets.QHBoxLayout()
        self.control_box.setContentsMargins(10, 5, 5, 5)
        self.form_box = QtWidgets.QVBoxLayout()
        self.close_button = make_button("Закрыть", icon=QtGui.QIcon(":/icons/close_record_view_screen"))
        self.close_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

        self.control_box.addWidget(self.close_button)
        self.control_box.addStretch()

        self.form_box.addWidget(self.form_body.draw())
        self.form_box.addStretch()

        self.layout.addLayout(self.control_box)
        self.layout.addLayout(self.form_box)
