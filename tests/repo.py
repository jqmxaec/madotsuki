import sys

from PyQt5 import QtWidgets

from example import tables
from mado.application_window import ApplicationWindow, WindowWidget
from mado.db import setup_database_connection
from mado.form_body import FormBody
from mado.report import Report
from mado.standard_inputs.selectables import RelationInput

from example.entity_configs.rooms import RoomsEntityConfig

from mado.utils import set_app_name

import mado.resources.resources


def make_rooms_report(window: WindowWidget) -> QtWidgets.QWidget:
    f = FormBody()

    f.add("room", RelationInput(RoomsEntityConfig()), "Комната")

    rep = Report(window, f)

    return rep


if __name__ == "__main__":
    set_app_name("bsdenjoyer_v1")
    setup_database_connection(tables.meta)

    qt_app = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.register_screen("rooms_report", make_rooms_report)
    app.change_screen("rooms_report")

    app.show()

    sys.exit(qt_app.exec())
