from PySide6.QtGui import QFont, QFontDatabase


class FontMix:
    def __init__(self, *,
                 src: list[str] = None,
                 point_size=0,
                 pixel_size=0,
                 weight=QFont.Weight.Normal,
                 bold=False,
                 families='Segoe UI, Microsoft YaHei UI'
                 ):
        self.src = src
        self.bold = bold
        self.point_size = point_size
        self.pixel_size = pixel_size
        self.weight = weight
        self.families = [x.strip(' ') for x in families.split(',')]

    def merge_to(self, font: QFont) -> QFont:
        for x in self.src or []:
            _id = QFontDatabase.addApplicationFont(x)
            QFontDatabase.applicationFontFamilies(_id)

        font.setBold(self.bold)
        font.setFamilies(self.families)

        if self.point_size: font.setPointSize(self.point_size)
        if self.pixel_size: font.setPixelSize(self.pixel_size)
        if self.weight: font.setWeight(self.weight)

        return font
