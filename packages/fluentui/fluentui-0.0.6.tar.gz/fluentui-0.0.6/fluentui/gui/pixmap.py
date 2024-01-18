from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class Pixmap(QPixmap):
    def __init__(self,
                 size: tuple[int, int] = None,
                 filename='', format_: str = None, flags=Qt.ImageConversionFlag.AutoColor,
                 xpm: list[str] = None,
                 pixmap: QPixmap = None,
                 variant: Any = None,
                 ):
        """
        QPixmap()
        QPixmap(size)
        QPixmap(fileName, format: str = None, flags=Qt.AutoColor)
        QPixmap(xpm: list[str])
        QPixmap(a0: QPixmap)
        QPixmap(variant: Any)
        """
        if size is not None:
            super().__init__(size)
        elif filename:
            super().__init__(filename, format_, flags)
        elif xpm:
            super().__init__(xpm)
        elif pixmap is not None:
            super().__init__(pixmap)
        elif variant is not None:
            super().__init__(variant)
