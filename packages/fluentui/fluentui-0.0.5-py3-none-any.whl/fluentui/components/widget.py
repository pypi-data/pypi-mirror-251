import sys
from typing import Callable, Self, Iterator, Optional

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QMouseEvent, QShowEvent, QFont, QCloseEvent, QKeyEvent
from PySide6.QtWidgets import QSizePolicy, QWidget, QLayout
from attrs import define
from ifn.seq import append

from ..core.margins import Margins
from ..gui import FontMix


@define
class GridPos:
    row: int = -1  # 在 grid 中的行
    column: int = 0  # 在 grid 中的列
    row_span: int = 1  # 在 grid 中的行跨度
    column_span: int = 1  # 在 grid 中的列跨度
    align: Qt.AlignmentFlag = Qt.AlignmentFlag(0)  # 在布局中的对齐方式


class WidgetMix:
    on_clicked = Signal(QMouseEvent)
    on_closed = Signal()

    def __init__(self: QWidget | Self, *args,
                 parent: 'WidgetMix' = None,
                 font: FontMix | QFont = None,
                 win_title='',
                 window_modality: Qt.WindowModality = None,
                 win_flags: Qt.WindowType = None,

                 size: tuple[int, int] = None,  # 大小
                 fixed_size: tuple[int, int] = None,  # 固定大小
                 width: int = None,  # 固定宽
                 height: int = None,  # 固定高
                 min_width: int = None,  # 最小宽
                 min_height: int = None,  # 最小高
                 max_width: int = None,  # 最大宽
                 max_height: int = None,  # 最大高

                 hor_stretch=0,  # 水平伸缩系数
                 ver_stretch=0,  # 垂直伸缩系数
                 fill_width=False,  # 填充宽度
                 fill_height=False,  # 填充高度
                 ignore_width=False,  # 忽略 sizeHint()，视图尽可能获得更多宽度
                 ignore_height=False,  # 忽略 sizeHint()，视图尽可能获得更多高度

                 grid=GridPos(),  # 布局属性
                 body: QLayout = None,

                 enabled=True,
                 hidden=False,
                 margins='0',
                 focus_policy: Qt.FocusPolicy = None,
                 attributes: list[Qt.WidgetAttribute] = None,

                 on_clicked: Callable[[QMouseEvent], None] = None,
                 on_destroyed: Callable = None,
                 **kwargs
                 ):
        self.__pressed = False
        self.__displayed = False
        self.grid = grid
        super().__init__(*args, parent=parent, **kwargs)

        # 事件
        if on_clicked: self.on_clicked.connect(on_clicked)
        if on_destroyed: self.destroyed.connect(on_destroyed)

        # 外观
        if isinstance(font, FontMix):
            self.setFont(font.merge_to(self.font()))
        elif isinstance(font, QFont):
            self.setFont(font)

        # 大小策略
        if fill_width or fill_height or ignore_width or ignore_height or hor_stretch > 0 or ver_stretch > 0:
            if (policy := self.sizePolicy()) and fill_width:
                policy.setHorizontalStretch(sys.maxunicode)
                policy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
            if fill_height:
                policy.setVerticalStretch(sys.maxunicode)
                policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
            if ignore_width: policy.setHorizontalPolicy(QSizePolicy.Policy.Ignored)
            if ignore_height: policy.setVerticalPolicy(QSizePolicy.Policy.Ignored)
            if hor_stretch: policy.setHorizontalStretch(hor_stretch)
            if ver_stretch: policy.setVerticalStretch(ver_stretch)
            self.setSizePolicy(policy)

        # 设置大小
        if min_width is not None or min_height is not None:
            self.setMinimumSize(min_width or self.minimumWidth(), min_height or self.minimumHeight())
        if max_width is not None or max_height is not None:
            self.setMaximumSize(max_width or self.maximumWidth(), max_height or self.maximumHeight())

        if size is not None:
            self.resize(*size)
        elif fixed_size is not None:
            self.setFixedSize(*fixed_size)
        elif isinstance(width, int) and isinstance(height, int):
            self.setFixedSize(width, height)
        elif isinstance(width, int):
            self.setFixedWidth(width)
        elif isinstance(height, int):
            self.setFixedHeight(height)

        # 属性
        self.setEnabled(enabled)
        self.setWindowTitle(win_title)
        self.setContentsMargins(Margins(margins))

        for x in append(attributes, [
            Qt.WidgetAttribute.WA_StyledBackground,
            Qt.WidgetAttribute.WA_DeleteOnClose
        ]):
            self.setAttribute(x)

        if win_flags is not None: self.setWindowFlags(win_flags)
        if focus_policy is not None: self.setFocusPolicy(focus_policy)
        if window_modality is not None: self.setWindowModality(window_modality)
        if hidden: self.setHidden(hidden)
        if body: self.setLayout(body)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        self.__pressed = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        super().mouseReleaseEvent(e)
        if self.__pressed:
            self.__pressed = False
            self.on_clicked.emit(e)

    def showEvent(self: QWidget | Self, e: QShowEvent) -> None:
        if not self.__displayed: self.willDisplay()
        super().showEvent(e)
        if not self.__displayed: self.displayed()
        self.__displayed = True

    def keyPressEvent(self: QWidget, e: QKeyEvent) -> None:
        super().keyPressEvent(e)
        if e.key() == Qt.Key.Key_Escape:
            if (Qt.WindowType.Dialog in self.windowFlags()
                    or self.windowModality() != Qt.WindowModality.NonModal):
                self.close()

    def closeEvent(self, e: QCloseEvent) -> None:
        super().closeEvent(e)
        self.on_closed.emit()

    def willDisplay(self) -> None:
        ...

    def displayed(self) -> None:
        ...

    def __iter__(self: QWidget) -> Iterator['WidgetMix']:
        return iter(self.children())

    def __getitem__(self: QWidget, index: int) -> Optional['WidgetMix']:
        return self.children()[index]


class Widget(WidgetMix, QWidget):
    ...
