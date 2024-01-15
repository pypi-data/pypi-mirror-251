from typing import Any

from PySide6.QtGui import QIcon, QPixmap, QIconEngine


class Icon(QIcon):
    def __init__(self, *icon: str | QPixmap | QIconEngine | QIcon | Any):
        super().__init__(*icon)
