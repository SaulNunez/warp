from enum import StrEnum
from typing import List, Union
from wap.representation.markup import Card, HtmlElement

class TextContent(HtmlElement):
    def __init__(self, content):
        super().__init__()
        self.content = content

class TextHtmlSubElement(TextContent):
    pass

class StrongTextHtmlElement(TextHtmlSubElement):
    pass

class BoldTextHtmlElement(TextHtmlSubElement):
    pass

class BigTextHtmlElement(TextHtmlSubElement):
    pass

class SmallTextHtmlElement(TextHtmlSubElement):
    pass

class ItalicTextElement(TextHtmlSubElement):
    pass

class UnderlineTextElement(TextHtmlSubElement):
    pass

class AHtmlElement(TextHtmlSubElement):
    def __init__(self, content: str, href: str):
        super().__init__(content)
        self.href = href

class BreakHtmlElement(TextHtmlSubElement):
    pass

class PreformattedText(TextContent):
    pass

class AlignTypes(StrEnum):
    left = "left",
    right = "right"
    center = "center"

class ModeTypes(StrEnum):
    wrap = "wrap"
    no_wrap = "no-wrap"

class ParagraphHtmlElement(HtmlElement):
    def __init__(self, children: List[Union[str, TextContent]] = [], align=AlignTypes.left, mode=ModeTypes.no_wrap, parent: Card = None):
        super().__init__(parent)
        self.align = align
        self.mode = mode
        self.children = children
    
    def align_from_str(self, input: str):
        self.align = getattr(AlignTypes, input, AlignTypes.left)

    def mode_from_str(self, input: str):
        self.mode = getattr(ModeTypes, input, ModeTypes.wrap)

