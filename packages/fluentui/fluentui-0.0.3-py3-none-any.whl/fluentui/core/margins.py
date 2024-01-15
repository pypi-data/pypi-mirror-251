from typing import Self

from PySide6.QtCore import QMargins


class Margins(QMargins):
    def __init__(self, *margin: int | str | QMargins):
        """
        Margin(QMargins)\n
        Margin("top[, right[, bottom[, left]]]")\n
        Margin(top: int, right: int, bottom: int, left: int)
        """
        if margin and isinstance(margin[0], str):
            match len(m := [int(x) for x in margin[0].split(' ')]):
                case 1:
                    margin = (m[0], m[0], m[0], m[0])
                case 2:
                    margin = (m[1], m[0], m[1], m[0])
                case 3:
                    margin = (m[1], m[0], m[1], m[2])
                case _:
                    margin = (m[3], m[0], m[1], m[2])
        super().__init__(*margin)

    def merge(self, top: int = None,
              right: int = None,
              bottom: int = None,
              left: int = None) -> Self:
        if top is not None: self.setTop(top)
        if right is not None: self.setRight(right)
        if bottom is not None: self.setBottom(bottom)
        if left is not None: self.setLeft(left)
        return self

    def __str__(self) -> str:
        top = f"top: {self.top()}"
        right = f"right: {self.right()}"
        bottom = f"bottom: {self.bottom()}"
        left = f"left: {self.left()}"
        return f'Margins{{{top}, {right}, {bottom}, {left}}}'
