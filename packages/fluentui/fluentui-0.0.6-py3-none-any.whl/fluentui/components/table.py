from PySide6.QtWidgets import QTableView

from .item_view import ItemViewMix


class TableView(ItemViewMix, QTableView):
    def __init__(self, default_row_height=0,
                 max_col_width: int = None,
                 word_wrap=True,
                 show_grid=True,
                 hor_header_visible=True,
                 ver_header_visible=True,
                 **kwargs
                 ):
        super().__init__(**kwargs)
        hor_header = self.horizontalHeader()
        ver_header = self.verticalHeader()

        hor_header.setVisible(hor_header_visible)
        ver_header.setVisible(ver_header_visible)
        ver_header.setDefaultSectionSize(default_row_height)

        self.setShowGrid(show_grid)
        self.setWordWrap(word_wrap)
        if max_col_width is not None: hor_header.setMaximumSectionSize(max_col_width)
