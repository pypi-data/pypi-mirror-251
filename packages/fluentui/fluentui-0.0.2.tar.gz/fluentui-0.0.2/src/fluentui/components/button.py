from PySide6.QtCore import QRectF
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtWidgets import QPushButton, QSizePolicy

from .widget import WidgetMix


class Button(WidgetMix, QPushButton):
    def __init__(self, text='', *, icon: QIcon | str = '', **kwargs):
        super().__init__(text, **kwargs)
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

        self.setStyleSheet(
            "[hasIcon=true] { padding: 5 12 5 30 }\n"
            ":disabled { color: #bdbdbd; background: #f0f0f0; border-color: #e0e0e0 }\n\n"

            "Button {\n"
            "    color: #242424;\n"
            "    background: #fff;\n"
            "    border: 1px solid #d1d1d1;\n"
            "    border-radius: 4px;\n"
            "    padding: 5 12\n"
            "}\n"
            ".Button:hover { background: #f5f5f5; border-color: #c7c7c7 }\n"
            ".Button:pressed { background: #e0e0e0; border-color: #b3b3b3 }\n"

            "SubtleButton {\n"
            "    padding: 5 12;\n"
            "    color: #242424;\n"
            "    border: 1 solid transparent;\n"
            "    border-radius: 4px\n"
            "}\n"
            ".SubtleButton:hover { background: #f5f5f5 }\n"
            ".SubtleButton:pressed { background: #e0e0e0 }\n"
        )

        self.__icon: QIcon = None
        self.setIcon(icon)

    def setIcon(self, icon: QIcon | str):
        self.__icon = QIcon(icon) if isinstance(icon, str) else icon or QIcon()
        self.setProperty('hasIcon', not self.__icon.isNull())
        self.update()

    def icon(self):
        return self.__icon

    def setProperty(self, name: str, value) -> bool:
        if name != 'icon':
            return super().setProperty(name, value)
        self.setIcon(value)
        return True

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.__icon.isNull():
            return

        p = QPainter(self)
        p.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        w, h = self.iconSize().width(), self.iconSize().height()
        rect = QRectF(12, (self.height() - h) / 2, w, h)

        mode = QIcon.Mode.Normal if self.isEnabled() else QIcon.Mode.Disabled
        self.__icon.paint(p, rect.toRect(), mode=mode)


class SubtleButton(Button):
    ...
