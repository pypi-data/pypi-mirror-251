from typing import Any, Callable

from PySide6.QtCore import QSize
from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QLineEdit

from .label import Label
from .layout import Row, Column
from .widget import WidgetMix, Widget


class LineEdit(WidgetMix, QLineEdit):
    def __init__(self, text: Any = '', *,
                 placeholder='',
                 read_only=False,
                 text_changed: Callable[[str], ...] = None,
                 validator: QValidator = None,
                 **kwargs
                 ):
        super().__init__(f'{text}', **kwargs)

        self.setStyleSheet(
            "LineEdit {\n"
            "    color: #242424;\n"
            "    border: 1 solid #d1d1d1;\n"
            "    border-bottom: 1 solid #616161;\n"
            "    border-radius: 4;\n"
            "}\n"
            ":focus {\n"
            "    border: 1 solid #b3b3b3;\n"
            "    border-bottom: 1 solid #0f6cbd;\n"
            "}\n"
            ":disabled {\n"
            "    color: #bdbdbd;\n"
            "    border: 1 solid #e0e0e0\n"
            "}"
        )

        self.setReadOnly(read_only)
        self.setTextMargins(10, 0, 10, 0)
        self.setPlaceholderText(placeholder)

        if validator is not None:
            self.setValidator(validator)

        if text_changed:
            self.textChanged.connect(text_changed)

    def setText(self, text: Any, block_signals=False):
        if block_signals: self.blockSignals(True)
        super().setText(f'{text}')
        if block_signals: self.blockSignals(False)

    def willDisplay(self) -> None:
        self.setCursorPosition(0)

    def sizeHint(self) -> QSize:
        size = super().sizeHint()
        size.setHeight(32)
        return size


class InlineEdit(Widget):
    def __init__(self, label='', text='', *, spacing=0, **kwargs):
        self.label = Label(label, margins=f'0 {spacing} 0 0')
        self.input = LineEdit(text, fill_width=True, fill_height=True)
        super().__init__(**kwargs, body=Row(items=[self.label, self.input]))


class InputEdit(Widget):
    def __init__(self, label='', text='', **kwargs):
        self.label = Label(label)
        self.input = LineEdit(text, fill_width=True, fill_height=True)
        super().__init__(
            **kwargs,
            body=Column(spacing=2, items=[self.label, self.input])
        )
