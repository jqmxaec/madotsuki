from __future__ import annotations

from PyQt5 import QtWidgets, QtCore

from mado.input_base import InputBase

from datetime import date, datetime, time


class DateInput(InputBase, QtWidgets.QDateEdit):
    def __init__(self, date_changed: QtCore.pyqtSlot = None) -> None:
        super().__init__()

        self.setCalendarPopup(True)
        self.setDate(QtCore.QDate.currentDate())

        if date_changed is not None:
            self.dateChanged.connect(lambda x: date_changed(x.toPyDate()))

    def get_value(self) -> date:
        return self.date().toPyDate()

    def set_value(self, value: date) -> None:
        self.setDate(QtCore.QDate(value.year, value.month, value.day))

    def set_readonly(self) -> None:
        self.setButtonSymbols(QtWidgets.QDateEdit.ButtonSymbols.NoButtons)
        self.setCalendarPopup(False)


class DateTimeInput(InputBase, QtWidgets.QDateTimeEdit):
    def __init__(self, datetime_changed: QtCore.pyqtSlot = None) -> None:
        super().__init__()

        self.setCalendarPopup(True)
        self.setDateTime(QtCore.QDateTime.currentDateTime())

        if datetime_changed is not None:
            self.dateTimeChanged.connect(lambda x: datetime_changed(x.toPyDateTime()))

    def get_value(self) -> datetime:
        return self.dateTime().toPyDateTime()

    def set_value(self, value: datetime) -> None:
        self.setDateTime(QtCore.QDateTime(value.year, value.month, value.day, value.hour, value.minute))

    def set_readonly(self) -> None:
        self.setCalendarPopup(False)


class TimeInput(InputBase, QtWidgets.QTimeEdit):
    def __init__(self, time_changed: QtCore.pyqtSlot = None) -> None:
        super().__init__()

        self.setTime(QtCore.QTime.currentTime())

        if time_changed is not None:
            self.timeChanged.connect(lambda x: time_changed(x.toPyTime()))

    def get_value(self) -> time:
        return self.time().toPyTime()

    def set_value(self, value: time) -> None:
        self.setTime(QtCore.QTime(value.hour, value.minute))
