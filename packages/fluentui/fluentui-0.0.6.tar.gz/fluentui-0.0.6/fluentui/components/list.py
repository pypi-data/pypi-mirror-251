from PySide6.QtWidgets import QListView

from .item_view import ItemViewMix


class ListView(ItemViewMix, QListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
