from PySide6.QtWidgets import QBoxLayout, QWidget, QLayout

from .widget import Widget
from ..core.margins import Margins


class Spacing(int): ...


class Stretch(int): ...


class BoxLayout(QBoxLayout):
    def __init__(self, dir_: QBoxLayout.Direction, *,
                 margin='0',
                 spacing=0,
                 items: QLayout | Widget | list[Widget | Spacing | Stretch] = None,
                 parent: QWidget = None,
                 ):
        super().__init__(dir_, parent)
        self.setSpacing(spacing)

        if margin:
            self.setContentsMargins(Margins(margin))

        if items:
            for x in items if isinstance(items, list) else [items]:
                self.addWidget(x)

    def addWidget(self, item: QLayout | Stretch | Spacing | Widget) -> None:
        if isinstance(item, QLayout):
            return self.addLayout(item)
        if isinstance(item, Stretch):
            return self.addStretch(item)
        if isinstance(item, Spacing):
            return self.addSpacing(item)
        super().addWidget(item, alignment=item.grid.align)


class Row(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(QBoxLayout.Direction.LeftToRight, **kwargs)


class Column(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(QBoxLayout.Direction.TopToBottom, **kwargs)
