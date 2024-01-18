from PySide6.QtCore import QSize
from PySide6.QtWidgets import QComboBox
from ifn import for_each

from fluentui import AssetPath
from .widget import WidgetMix
from ..theme import Theme


class Combobox(WidgetMix, QComboBox):
    def __init__(self, max_visible=20,
                 editable=False,
                 items: list[str | dict | tuple] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        icon = f"{'dark' if Theme.is_dark() else 'light'}_chevron_down.png"
        self.setStyleSheet(
            ":item { height: 32px; }\n"
            "::drop-down { border: 0; width: 24px }\n"
            "::down-arrow {\n"
            f"   image: url({AssetPath}/images/{icon});\n"
            "    width: 12; right: 6\n"
            "}"
        )

        self.setEditable(editable)
        self.setMaxVisibleItems(max_visible)

        if items:
            if isinstance(items[0], str):
                self.addItems(items)
            else:
                for_each(items, lambda x, y: self.addItem(x, y))

    def sizeHint(self) -> QSize:
        size = super().sizeHint()
        size.setHeight(32)
        return size


class MenuCombobox(Combobox):
    def __init__(self, **kwargs):
        super().__init__(editable=False, **kwargs)
