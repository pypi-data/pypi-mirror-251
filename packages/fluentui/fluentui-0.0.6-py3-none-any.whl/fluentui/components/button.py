from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QAbstractButton

from .widget import WidgetMix


class AbstractButtonMix(WidgetMix):
    def __init__(self: QAbstractButton,
                 text: str = '', *,
                 tool_tip: str = '',
                 icon: QIcon | str = None,
                 icon_size: int | tuple[int, int] = 16,
                 **kwargs
                 ):
        self._icon = QIcon()
        super().__init__(**kwargs)

        self.setText(text)
        self.setToolTip(tool_tip)
        self.setIconSize(icon_size)
        if icon: self.setIcon(icon)

    def setIcon(self, icon: QIcon | str):
        icon = QIcon(icon) if isinstance(icon, str) else icon
        super().setIcon(icon)

    def setIconSize(self, size: int | tuple[int, int]):
        size = size if isinstance(size, tuple) else (size, size)
        super().setIconSize(QSize(*size))


class AbstractButton(AbstractButtonMix, QAbstractButton):
    ...


class Button(AbstractButtonMix, QPushButton):
    ...


class SubtleButton(Button):
    ...
