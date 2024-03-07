import sys
from enum import Enum

from PyQt5 import QtWidgets, QtCore

from example import tables
from mado.application_window import ApplicationWindow, WindowWidget
from mado.db import setup_database_connection
from mado.form_body import FormBody
from mado.standard_inputs.selectables import EnumInput
from mado.standard_inputs.tables import TableInput, DelegatedTableInput
from mado.utils import set_app_name
from mado.widgets.misc import make_button


class WeekTimes(Enum):
    one = "1 раз в неделю"
    two = "2 раза в неделю"
    three = "3 раза в неделю"


def make_main_screen(window: WindowWidget) -> QtWidgets.QWidget:
    f = FormBody()

    table = DelegatedTableInput()
    table.reset_with_dimensions(4, 2)

    for x in range(4):
        table.set_custom_input(x, 1, EnumInput(enum=WeekTimes))

    # table.setIndexWidget(table.model.index(0, 1), )

    f.add("table", table)

    @QtCore.pyqtSlot()
    def btn_clicked():
        print(f.get_value())

    b = make_button("ок")
    b.clicked.connect(btn_clicked)

    w = QtWidgets.QWidget()
    w.setLayout(QtWidgets.QVBoxLayout())
    w.layout().addWidget(f.draw())
    w.layout().addStretch()
    w.layout().addWidget(b)

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
