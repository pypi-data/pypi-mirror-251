from PySide6.QtCore import QRectF, QSize
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtWidgets import QPushButton, QSizePolicy, QAbstractButton

from .widget import WidgetMix


class AbstractButtonMix(WidgetMix):
    def __init__(self: QAbstractButton,
                 text: str = '', *,
                 tool_tip: str = '',
                 icon: QIcon | str = None,
                 icon_size: int | tuple[int, int] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.__icon = QIcon()

        self.setText(text)
        self.setToolTip(tool_tip)
        if icon is not None: self.setIcon(icon)
        if icon_size is not None: self.setIconSize(icon_size)

    def setIcon(self, icon: QIcon | str):
        icon = QIcon(icon) if isinstance(icon, str) else icon
        super().setIcon(icon)

    def setIconSize(self, size: int | tuple[int, int]):
        size = size if isinstance(size, tuple) else (size, size)
        super().setIconSize(QSize(*size))

    def setProperty(self, name: str, value) -> bool:
        if name != 'icon':
            return super().setProperty(name, value)
        self.setIcon(value)
        return True


class AbstractButton(AbstractButtonMix, QAbstractButton):
    ...


class Button(AbstractButtonMix, QPushButton):
    def __init__(self, text='', **kwargs):
        super().__init__(text, **kwargs)
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
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)

    def setIcon(self, icon: QIcon | str):
        self.__icon = QIcon(icon) if isinstance(icon, str) else icon
        self.setProperty('hasIcon', not self.__icon.isNull())
        self.update()

    def icon(self):
        return self.__icon

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
