from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QSizePolicy

from .widget import WidgetMix


class Label(WidgetMix, QLabel):
    def __init__(self, text='',
                 text_align: Qt.AlignmentFlag = None,
                 **kwargs
                 ):
        super().__init__(text, **kwargs)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        if text_align: self.setAlignment(text_align)
