from PyQt5 import QtWidgets

from mado.application_window import WindowWidget
from mado.form_body import FormBody
from mado.widgets.misc import make_back_button, make_label, make_font, make_button
from mado.widgets.tables import MReportTable


class Report(QtWidgets.QWidget):
    back_button: QtWidgets.QPushButton
    header_label: QtWidgets.QLabel

    top_box: QtWidgets.QHBoxLayout
    req_box: QtWidgets.QVBoxLayout
    layout: QtWidgets.QVBoxLayout

    table: MReportTable
    form_body: FormBody

    make_button_box: QtWidgets.QHBoxLayout
    make_button: QtWidgets.QPushButton

    def __init__(self, window: WindowWidget, form: FormBody) -> None:
        super().__init__()

        self.form_body = form
        self.form_body.draw()

        self.make_ui(window)

        self.header_label.setText("Отчёт такой-то")

    def make_ui(self, window: WindowWidget) -> None:
        self.back_button = make_back_button(window)
        self.header_label = make_label(font=make_font(size=14))
        self.top_box = QtWidgets.QHBoxLayout()
        self.top_box.addWidget(self.back_button)
        self.top_box.addWidget(self.header_label)
        self.top_box.addStretch()

        self.make_button = make_button("Составить отчёт")
        self.make_button_box = QtWidgets.QHBoxLayout()
        self.make_button_box.addStretch()
        self.make_button_box.addWidget(self.make_button)

        self.table = MReportTable()
        self.req_box = QtWidgets.QVBoxLayout()
        self.req_box.addWidget(self.form_body)
        self.req_box.addLayout(self.make_button_box)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.top_box)
        self.layout.addLayout(self.req_box)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
