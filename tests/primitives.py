import datetime
import pprint
import sys
from enum import Enum
from typing import Tuple

from PyQt5 import QtWidgets, QtCore

from example import tables
from example.entity_configs.events import EventsEntityConfig
from mado.application_window import ApplicationWindow, WindowWidget
from mado.db import setup_database_connection
from mado.form_body import FormBody
from mado.standard_inputs.controls import RadioInput, EnumRadioInput, BoolInput
from mado.standard_inputs.dates import DateInput, DateTimeInput, TimeInput
from mado.standard_inputs.lists import ListInput
from mado.standard_inputs.selectables import ComboInput, EnumInput, RelationInput
from mado.standard_inputs.tables import TableInput, DelegatedTableInput
from mado.standard_inputs.text import TextInput, PasswordInput, MultilineTextInput
from mado.utils import set_app_name
from mado.widgets.misc import make_button

import mado.resources.resources

class EnumRadioTest(Enum):
    quick = "Вариант один"
    brown = "Вариант два"
    fox = "Вариант три"


radio_input_test = [(3, "Вариант первый"), (9, "Вариант второй"), (5, "Вариант третий")]
combo_input_test = [(4, "Вариант первый"), (12, "Вариант второй"), (7, "Вариант третий"), (2, "Вариант четвертый")]


class EnumTest(Enum):
    openbsd = "Вариант один"
    freebsd = "Вариант два"
    netbsd = "Вариант три"
    plan9 = "Вариант четыре"


def make_main_screen(window: WindowWidget) -> QtWidgets.QWidget:
    window.setWindowTitle("primitives test")

    f = FormBody()

    @QtCore.pyqtSlot(str)
    def on_text_input(text: str) -> None:
        print("Text edited, text:", text)

    @QtCore.pyqtSlot(str)
    def on_password_input(text: str) -> None:
        print("PasswordInput, text:", text)

    @QtCore.pyqtSlot()
    def on_multiline_text_input() -> None:
        print("MultilineTextInput edited")

    @QtCore.pyqtSlot(object)
    def on_date_input(date_: datetime.date) -> None:
        print("Date edited, date", date_)

    @QtCore.pyqtSlot(object)
    def on_datetime_input(datetime_: datetime.datetime) -> None:
        print("DateTime edited, datetime:", datetime_)

    @QtCore.pyqtSlot(object)
    def on_time_input(time_: datetime.time) -> None:
        print("Time edited, time:", time_)

    @QtCore.pyqtSlot(object)
    def on_radio_input(choice: int) -> None:
        print("Radio edited, choice:", choice)

    @QtCore.pyqtSlot(object)
    def on_enum_radio_input(choice: EnumRadioTest) -> None:
        print("EnumRadio edited, choice:", choice)

    @QtCore.pyqtSlot(object)
    def on_bool_input(choice: bool) -> None:
        print("Bool edited, choice:", choice)

    @QtCore.pyqtSlot(object)
    def on_combo_input(choice: any) -> None:
        print("Combo edited, choice:", choice)

    @QtCore.pyqtSlot(object)
    def on_enum_input(choice: any) -> None:
        print("Enum edited, choice:", choice)

    @QtCore.pyqtSlot(tuple, str)
    def on_table_input(pos: Tuple[int, int], text: str) -> None:
        print("Table edited, pos: ", pos, ", text: ", text, sep="")

    f.add("text_input", TextInput(text_edited=on_text_input), "TextInput")
    f.add("password_input", PasswordInput(text_edited=on_password_input), "PasswordInput")
    f.add("multiline_input", MultilineTextInput(text_edited=on_multiline_text_input), "MultilineTextInput")
    f.add("date_input", DateInput(date_changed=on_date_input), "DateInput")
    f.add("datetime_input", DateTimeInput(datetime_changed=on_datetime_input), "DateTimeInput")
    f.add("time_input", TimeInput(time_changed=on_time_input), "TimeInput")
    f.add("radio_input", RadioInput(variants=radio_input_test, radio_selected=on_radio_input), "RadioInput")
    f.add("enum_radio_input", EnumRadioInput(enum=EnumRadioTest, radio_selected=on_enum_radio_input), "EnumRadioInput")
    f.add("bool_input", BoolInput(label="Lorem ipsum", mark_changed=on_bool_input), "BoolInput")
    f.add("combo_input", ComboInput(variants=combo_input_test, variant_selected=on_combo_input), "ComboInput")
    f.add("enum_input", EnumInput(enum=EnumTest, variant_selected=on_enum_input, no_initial_selection=True))

    f.add("relation_input", RelationInput(EventsEntityConfig()), "RelationInput")
    f.add("table_input", TableInput(cell_edited=on_table_input))
    f.add("delegated_table_input", DelegatedTableInput())
    f.add("list_input", ListInput(lambda: RelationInput(EventsEntityConfig())))

    table_input: TableInput = f.widgets["table_input"]
    table_input.reset_with_dimensions(5, 6)

    delegated_table_input: DelegatedTableInput = f.widgets["delegated_table_input"]
    delegated_table_input.reset_with_dimensions(4, 5)
    delegated_table_input.set_custom_input(0, 2, BoolInput(label="The quick"))
    delegated_table_input.set_custom_input(1, 3, ComboInput(variants=combo_input_test))
    delegated_table_input.set_custom_input(3, 4, DateTimeInput())

    submit_button = make_button("Ок")

    @QtCore.pyqtSlot()
    def on_submit_button() -> None:
        print("=== FormBody value ===")

        pprint.pprint(f.get_value(), sort_dicts=False)

    submit_button.clicked.connect(on_submit_button)

    w = QtWidgets.QWidget()
    w.setLayout(QtWidgets.QVBoxLayout())
    w.layout().addWidget(f.draw())
    w.layout().addStretch()
    w.layout().addWidget(submit_button)

    return w


if __name__ == "__main__":
    set_app_name("bsdenjoyer_v1")
    setup_database_connection(tables.meta)

    qt_app = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.register_screen("main_screen", make_main_screen)
    app.change_screen("main_screen")

    app.show()

    sys.exit(qt_app.exec())
