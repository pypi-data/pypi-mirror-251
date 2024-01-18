import sys
from pathlib import Path
from typing import Callable, Any

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget

from fluentui import AssetPath, Theme
from ..gui import FontMix


class App(QApplication):
    def __init__(self, argv: list[str] = None, *,
                 theme='light',
                 font=FontMix(),
                 show: Callable[..., QWidget] = None):
        super().__init__(argv or sys.argv)

        Theme._theme = theme
        self.setStyleSheet(Path(f'{AssetPath}/{theme}.qss').read_text())

        if font is not None:
            self.setFont(font)

        self.__top_widget: QWidget = None
        if show_fn := show:
            self.__top_widget = show_fn()

    def exec(self) -> Any:
        if self.__top_widget:
            self.__top_widget.show()
        return sys.exit(super().exec())

    def setFont(self, font: QFont | FontMix):
        if isinstance(font, FontMix):
            super().setFont(font.merge_to(self.font()))
            return
        super().setFont(font)
