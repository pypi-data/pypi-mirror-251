from PySide6.QtCore import QDate, QDateTime, QTime, QSize
from PySide6.QtWidgets import QDateTimeEdit

from .widget import WidgetMix


class DateTimeEdit(WidgetMix, QDateTimeEdit):
    def __init__(self, t: QDate | QDateTime | str = '', *,
                 calendar_popup=False,
                 display_format='',
                 **kwargs
                 ):
        if isinstance(t, str):
            t = QDateTime.fromString(t)
        elif isinstance(t, QDate):
            t = QDateTime(t, QTime())
        super().__init__(t or QDateTime(), **kwargs)
        if display_format:
            self.setDisplayFormat(display_format)
        self.setCalendarPopup(calendar_popup)

    def setDate(self, date: QDate | str) -> None:
        date = QDate.fromString(date) if isinstance(date, str) else date
        super().setDate(date)

    def sizeHint(self) -> QSize:
        size = super().sizeHint()
        size.setHeight(32)
        return size


class DateEdit(DateTimeEdit):
    def __init__(self, date: QDate | QDateTime | str = '', **kwargs):
        super().__init__(date, display_format='yyyy-MM-dd', **kwargs)
