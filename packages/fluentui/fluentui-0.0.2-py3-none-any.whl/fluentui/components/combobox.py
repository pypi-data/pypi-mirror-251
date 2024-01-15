from PySide6.QtCore import QSize
from PySide6.QtWidgets import QComboBox

from fluentui import AssetPath
from .widget import WidgetMix


class Combobox(WidgetMix, QComboBox):
    def __init__(self, max_visible=20, editable=False, **kwargs):
        super().__init__(**kwargs)
        self.setEditable(editable)
        self.setMaxVisibleItems(max_visible)

        self.setStyleSheet(
            "Combobox {\n"
            "    color: #242424;\n"
            "    border: 1 solid #d1d1d1;\n"
            "    border-radius: 4;\n"
            "    padding: 0 4 0 12\n"
            "}\n"
            ":hover { background: #f5f5f5; border-color: #c7c7c7 }\n"
            ":hover:on { background: #ebebeb; border-color: #bdbdbd }\n"
            ":hover:editable { color: #242424; background: #fff }\n"
            ":hover:editable:on { color: #242424; background: #fff }\n"
            ":disabled { color: #bdbdbd; background: #f0f0f0; border-color: #e0e0e0 }\n\n"

            ":on QAbstractItemView {\n"
            "    background: #fff;\n"
            "    outline: 0;\n"
            "    border: 1 solid #d1d1d1;\n"
            "    padding: 4 9\n"
            "}\n"
            ":item { height: 32px; color: #242424; }\n"
            ":item:hover { color: #242424; background: #f5f5f5 }\n"
            ":item:selected { color: #242424; background: #f5f5f5 }\n\n"

            "::drop-down { border: 0; width: 24px }\n"
            "::down-arrow {\n"
            f"   image: url({AssetPath}/images/down-30.png);\n"
            "    width: 12; right: 6\n"
            "}"
        )

    def sizeHint(self) -> QSize:
        size = super().sizeHint()
        size.setHeight(32)
        return size


class MenuCombobox(Combobox):
    def __init__(self, **kwargs):
        super().__init__(editable=False, **kwargs)
