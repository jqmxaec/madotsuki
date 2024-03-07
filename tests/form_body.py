import pickle
import sys
from typing import Tuple

from PyQt5 import QtWidgets, QtCore

from mado.form_body import FormBody
from mado.standard_inputs.tables import TableInput
from mado.standard_inputs.text import TextInput
from mado.widgets.tables import MReportTable

data = [
    ["foo", "sy"],
    ["baz", "le"],
    ["88", "zak", "a)"]
]


def make_form() -> FormBody:
    f = FormBody()

    report = TableInput()
    report.set_value(data)
    report.model.setHorizontalHeaderLabels(["п", "н", "х"])
    report.model.setVerticalHeaderLabels(["с", "к", "ладно"])

    @QtCore.pyqtSlot(str)
    def edited(_: str) -> None:
        print(pickle.dumps(report.get_value()))

    @QtCore.pyqtSlot(tuple, str)
    def cell_ed(coord: Tuple[int, int], text: str) -> None:
        print(coord, text)

    report.cell_edited.connect(cell_ed)

    f.add("name", TextInput(text_edited=edited), "Ваше имя")
    f.add("report", report, "Хорош")

    return f.draw()


class ApplicationWidget(QtWidgets.QWidget):
    layout: QtWidgets.QVBoxLayout

    def __init__(self) -> None:
        super().__init__()

        self.resize(self.screen().size() * 0.7)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(make_form())
        self.layout.addStretch()


if __name__ == "__main__":
    qt_app = QtWidgets.QApplication(sys.argv)

    app = ApplicationWidget()
    app.show()

    sys.exit(qt_app.exec())
