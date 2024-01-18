from enum import Enum, Flag
from typing import Callable

from PySide6.QtCore import QAbstractItemModel, QModelIndex
from PySide6.QtWidgets import QAbstractItemView, QAbstractItemDelegate, QTableView

from .scroll_area import ScrollAreaMix


class ItemViewMix(ScrollAreaMix):
    class EditTrigger(Flag):
        No = 0
        CurrentChanged = 1
        DoubleClicked = 2
        Clicked = 4
        EditKey = 8
        AnyKey = 16
        All = 30

    class ScrollMode(Enum):
        PerItem = 0
        PerPixel = 1

    class SelectionBehavior(Enum):
        Items = 0
        Rows = 1
        Columns = 2

    class SelectionMode(Enum):
        No = 0
        Single = 1
        Multi = 2
        Extended = 3
        Contiguous = 4

    def __init__(self: QAbstractItemView,
                 model: QAbstractItemModel = None,
                 auto_scroll=False,
                 edit_triggers=EditTrigger.No,
                 delegate: QAbstractItemDelegate = None,
                 on_cell_clicked: Callable[[QModelIndex], None] = None,
                 on_double_clicked: Callable[[QModelIndex], None] = None,
                 **kwargs
                 ):
        super().__init__(**kwargs)

        self.setAutoScroll(auto_scroll)
        self.setEditTriggers(edit_triggers)
        self.setHorizontalScrollMode(self.ScrollMode.PerPixel)
        self.setVerticalScrollMode(self.ScrollMode.PerPixel)
        self.setSelectionBehavior(self.SelectionBehavior.Rows)
        self.setSelectionMode(self.SelectionMode.Single)

        if delegate:
            if not delegate.parent():
                delegate.setParent(self)
            self.setItemDelegate(delegate)

        if model: self.setModel(model)
        if on_double_clicked: self.doubleClicked.connect(on_double_clicked)
        if on_cell_clicked: self.clicked.connect(on_cell_clicked)

    def setModel(self, model: QAbstractItemModel) -> None:
        super().setModel(model)
        model.rowsRemoved.connect(self.rowsRemoved)

    def currentChanged(self, current: QModelIndex, previous: QModelIndex) -> None:
        super().currentChanged(current, previous)
        if current.row() != previous.row():
            self.currentRowChanged(current, previous)

    def currentRowChanged(self, current: QModelIndex, previous: QModelIndex) -> None:
        ...

    def rowsRemoved(self, parent: QModelIndex, first: int, last: int) -> None:
        if not (index := self.currentIndex()).isValid():
            return
        if isinstance(self, QTableView):
            self.selectRow(index.row())

    def rowsAboutToBeRemoved(self, parent: QModelIndex, first: int, last: int) -> None:
        ...

    def setCurrentIndex(self, index: QModelIndex, clicked=False) -> None:
        super().setCurrentIndex(index)
        if clicked:
            self.clicked.emit(index)

    def openPersistentEditor(self, index: QModelIndex, col=-1) -> None:
        """ openPersistentEditor(index=currentIndex(), col: int = None) """
        index = index or self.currentIndex()
        index = index if col == -1 else index.siblingAtColumn(col)
        if not self.isPersistentEditorOpen(index):
            super().openPersistentEditor(index)

    def setEditTriggers(self, triggers: EditTrigger) -> None:
        super().setEditTriggers(QAbstractItemView.EditTrigger(triggers.value))

    def setHorizontalScrollMode(self, mode: ScrollMode) -> None:
        super().setHorizontalScrollMode(QAbstractItemView.ScrollMode(mode.value))

    def setVerticalScrollMode(self, mode: ScrollMode) -> None:
        super().setVerticalScrollMode(QAbstractItemView.ScrollMode(mode.value))

    def setSelectionBehavior(self, behavior: SelectionBehavior) -> None:
        super().setSelectionBehavior(QAbstractItemView.SelectionBehavior(behavior.value))

    def setSelectionMode(self, mode: SelectionMode) -> None:
        super().setSelectionMode(QAbstractItemView.SelectionMode(mode.value))
