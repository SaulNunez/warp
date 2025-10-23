from enum import Enum, StrEnum
from wap.representation.markup import HtmlElement

class ImgAlignTypes(StrEnum):
    top = "top"
    middle = "middle"
    bottom = "bottom"

class MeasureType(Enum):
    PIXEL = 0
    PECENTAGE = 1

class Measurement:
    def __init__(self, representation: str):
        if representation.endswith("%"):
            self.type = MeasureType.PECENTAGE
            self.value = int(representation[:-1], base=10)
        else:
            self.type = MeasureType.PIXEL
            self.value = int(representation, base=10)


class Image(HtmlElement):
    def __init__(self, 
                 src: str, 
                 localsrc: str = "", 
                 alt: str = "", 
                 align = ImgAlignTypes.top, 
                 height = Measurement("0"), 
                 hspace = Measurement("0"), 
                 vspace = Measurement("0")):
        super().__init__()
        self.src = src
        self.alt = alt
        self.localsrc = localsrc
        self.align = align
        self.height = height
        self.hspace = hspace
        self.vspace = vspace

    def get_source(self) -> str:
        if self.localsrc:
            return self.localsrc
        else:
            return self.src
