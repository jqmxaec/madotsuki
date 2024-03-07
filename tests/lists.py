import sys

from PyQt5 import QtWidgets, QtCore

from mado.application_window import ApplicationWindow, WindowWidget
from mado.form_body import FormBody
from mado.standard_inputs.lists import ListInput
from mado.standard_inputs.text import TextInput
from mado.widgets.misc import make_button

import mado.resources.resources


def make_main_screen(window: WindowWidget) -> QtWidgets.QWidget:
    f = FormBody()

    lst = ListInput(TextInput)
    lst.set_value(["foo", "bar"])

    f.add("list", lst)

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
    qt_app = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.register_screen("main_screen", make_main_screen)
    app.change_screen("main_screen")

    app.show()

    sys.exit(qt_app.exec())
