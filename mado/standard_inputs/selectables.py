from enum import Enum
from typing import Tuple, List, Dict, Type

from PyQt5 import QtWidgets, QtCore, QtGui

from mado.entity.config import EntityConfig
from mado.input_base import InputBase
from mado.widgets.misc import make_label, make_button
from mado.widgets.modal import Modal
from mado.widgets.tables import MRecordTable


class ComboInput(InputBase, QtWidgets.QComboBox):
    variant_selected = QtCore.pyqtSignal(object)

    def __init__(self, variants: List[Tuple[any, str]], no_initial_selection: bool = False,
                 variant_selected: QtCore.pyqtSlot = None) -> None:
        super().__init__()

        for user_data, text in variants:
            self.addItem(text, user_data)

        if no_initial_selection:
            self.setCurrentIndex(-1)

        self.currentIndexChanged.connect(lambda *args, **kwargs: self.variant_selected.emit(self.get_value()))

        if variant_selected is not None:
            self.variant_selected.connect(variant_selected)

    def get_value(self) -> any:
        return self.currentData()

    def set_value(self, value: any) -> None:
        self.setCurrentIndex(self.findData(value))


class EnumInput(ComboInput):
    enum: Type[Enum]

    def __init__(self, enum: Type[Enum], no_initial_selection: bool = False,
                 variant_selected: QtCore.pyqtSlot = None) -> None:
        self.enum = enum
        to_list = [(x.name, x.value) for x in self.enum]

        super().__init__(to_list, no_initial_selection=no_initial_selection, variant_selected=variant_selected)

    def get_value(self) -> any:
        key = self.currentData()
        if key is None:
            return None
        return self.enum[key]

    def set_value(self, value: any) -> None:
        self.setCurrentIndex(self.findData(value.name))


class RelationChooserScreen(QtWidgets.QWidget):
    config: EntityConfig

    record_selected = QtCore.pyqtSignal(int, str)
    record_label_edited = QtCore.pyqtSignal(int, str)

    layout: QtWidgets.QVBoxLayout
    control_box: QtWidgets.QHBoxLayout

    table: MRecordTable
    confirm_button: QtWidgets.QPushButton
    create_button: QtWidgets.QPushButton
    manage_button: QtWidgets.QPushButton

    def __init__(self, config: EntityConfig) -> None:
        super().__init__()

        self.config = config

        self.confirm_button = make_button("Выбрать", icon=QtGui.QIcon(":/icons/select_record"))
        self.manage_button = make_button("Открыть запись")
        self.manage_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.manage_button.setEnabled(False)
        self.create_button = make_button("Создать", icon=QtGui.QIcon(":/icons/new_record"))
        self.create_button.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.confirm_button.setEnabled(False)
        self.control_box = QtWidgets.QHBoxLayout()
        self.control_box.addWidget(self.create_button)
        self.control_box.addWidget(self.manage_button)
        self.control_box.addStretch()
        self.control_box.addWidget(self.confirm_button)

        self.table = MRecordTable()
        self.table.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.control_box)

        self.setLayout(self.layout)

        self.table.row_double_clicked.connect(self.on_submit)
        self.confirm_button.clicked.connect(self.on_submit)
        self.table.row_selected.connect(self.on_table_row_selected)
        self.table.model.modelReset.connect(self.on_table_model_reset)

        self.create_button.clicked.connect(self.on_create_button_clicked)
        self.manage_button.clicked.connect(self.on_manage_button_clicked)

        self.table.model.setHorizontalHeaderLabels([self.config.table_labels[self.config.table_columns.index("name")]])
        self.fill_table()

    @QtCore.pyqtSlot()
    def on_table_row_selected(self) -> None:
        self.confirm_button.setEnabled(True)
        self.manage_button.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_table_model_reset(self) -> None:
        self.confirm_button.setEnabled(False)
        self.manage_button.setEnabled(False)

    def fill_table(self) -> None:
        self.table.set_data(
            [([x.name], (x.id, x.name)) for x in
             self.config.repository.fetch_all()]
        )
        self.table.normalize()

    @QtCore.pyqtSlot()
    def on_submit(self) -> None:
        row = self.table.get_selected_row()
        if row is None:
            return
        self.record_selected.emit(*row)

    @QtCore.pyqtSlot()
    def on_create_button_clicked(self) -> None:
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

    @QtCore.pyqtSlot()
    def on_manage_button_clicked(self) -> None:
        modal = Modal(self)

        row = self.table.get_selected_row()
        if row is None:
            return

        id_ = row[0]

        manager = self.config.manager(modal, self.config, id_)

        @QtCore.pyqtSlot(dict)
        def record_edited(data: Dict[str, any]) -> None:
            self.fill_table()

            self.record_label_edited.emit(id_, data["name"])

        manager.record_edited.connect(record_edited)

        modal.change_anon_screen(manager)
        modal.exec()


class RelationInput(InputBase, QtWidgets.QWidget):
    layout: QtWidgets.QHBoxLayout
    record_label: QtWidgets.QLabel
    choose_button: QtWidgets.QPushButton

    chosen_id: int

    config: EntityConfig

    def __init__(self, config: EntityConfig) -> None:
        super().__init__()

        self.chosen_id = -1
        self.config = config
        self.title = f"{self.config.entity_label}: выбор связанной записи"

        self.record_label = make_label("<не выбрано>")
        self.record_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        self.choose_button = make_button("Выбрать")
        self.choose_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.record_label)
        self.layout.addWidget(self.choose_button)

        self.setLayout(self.layout)

        self.choose_button.clicked.connect(self.on_choose_button_clicked)

    @QtCore.pyqtSlot()
    def on_choose_button_clicked(self) -> None:
        modal = Modal(self)

        chooser = RelationChooserScreen(self.config)

        @QtCore.pyqtSlot(tuple)
        def choose_submitted(id_: int, label: str) -> None:
            self.chosen_id = id_
            self.record_label.setText(label)

            modal.accept()

        @QtCore.pyqtSlot(int, str)
        def record_label_edited(id_: int, label: str) -> None:
            if id_ == self.chosen_id:
                self.record_label.setText(label)

        chooser.record_selected.connect(choose_submitted)
        chooser.record_label_edited.connect(record_label_edited)

        size = self.window().screen().size()
        modal.resize(int(size.width() * 0.3), int(size.height() * 0.5))

        modal.change_anon_screen(chooser)
        modal.exec()

    def get_value(self) -> int:
        return self.chosen_id

    def set_value(self, value: int) -> None:
        self.chosen_id = value

        self.record_label.setText(self.config.repository.fetch_one(self.chosen_id).name)

    def set_readonly(self) -> None:
        self.choose_button.hide()
