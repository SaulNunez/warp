from enum import StrEnum
from typing import List, Union
from warp.representation.markup import Card, HtmlElement

class TextContent(HtmlElement):
    def __init__(self, parent, content: str = ""):
        super().__init__(parent)
        self.content = content
    
    def __str__(self):
        return self.content

    def __repr__(self):
        return f"TextContent('{self.content}')"

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
    # Accept href first and parent as keyword to match how parser constructs it
    def __init__(self, href: str = "", parent=None):
        super().__init__(parent)
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
    def __init__(self, children: List[Union[str, TextContent]] = None, align=AlignTypes.left, mode=ModeTypes.no_wrap, parent: Card = None):
        super().__init__(parent)
        self.align = align
        self.mode = mode
        # avoid mutable default across instances
        self.children = [] if children is None else children
    
    def align_from_str(self, input: str):
        self.align = getattr(AlignTypes, input, AlignTypes.left)

    def mode_from_str(self, input: str):
        self.mode = getattr(ModeTypes, input, ModeTypes.wrap)

