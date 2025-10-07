from xml.sax import ContentHandler

from wap.representation.html.table import TableColumn, TableElement, TableRow
from wap.representation.html.text import AHtmlElement, BigTextHtmlElement, BoldTextHtmlElement, ItalicTextElement, ParagraphHtmlElement, SmallTextHtmlElement, StrongTextHtmlElement, TextHtmlSubElement
from wap.representation.markup import Card, Deck, WMLElement
from wap.representation.navigation import AnchorElement, GoElement, NoOpElement, PrevElement, RefreshElement


class WMLParser(ContentHandler):
    def __init__(self):
        super().__init__()
        self.data = Deck()
        # Add current card shorthand to prevent having to hunt down current card
        self._current_card: Card = None
        # Add current node shorthand to prevent having to hunt down current node
        self._current_node_rep: WMLElement = None
        self.current_element: str = ""
        self.inner_text: str = ""

    def startElement(self, name, attrs):
        self.current_element = name
        match name:
            case "card":
                self._current_card = Card(attrs["id"], attrs["title"])
                self.data.cards.append(self._current_card)
            case "p":
                self._current_node_rep = self._process_paragraph(attrs, self._current_card)
                self._current_card.children.append(self._current_node_rep)
            case "anchor":
                self._current_node_rep = AnchorElement()
            case "go":
                if isinstance(self._current_node_rep, AnchorElement):
                    self._process_go_node(attrs, self._current_node_rep)
            case "prev":
                if isinstance(self._current_node_rep, AnchorElement):
                    self._process_prev_node(attrs, self._current_node_rep)
            case "refresh":
                if isinstance(self._current_node_rep, AnchorElement):
                    self._process_go_node(attrs, self._current_node_rep)

    def _process_paragraph(self, attrs, parent: Card):
        element = ParagraphHtmlElement(parent=parent)
        if "align" in attrs:
            element.alignalign_from_str(attrs["align"])
        if "mode" in attrs:
            element.mode_from_str(attrs["mode"])
        return element

    def _process_go_node(self, attrs, parent: AnchorElement):
        if "href" in attrs:
            element = GoElement(attrs["href"], parent=parent)
            if "method" in attrs:
                element.method_from_str(attrs["method"])
        else:
            element = NoOpElement()
        return element
    
    def _process_prev_node(self, parent: AnchorElement):
        return PrevElement(parent=parent)
    
    def _process_refresh_node(self, parent: AnchorElement):
        return RefreshElement(parent=parent)
    
    def _process_table_column(self, parent: TableRow):
        return TableColumn(parent=parent)
    
    def _process_table_row(self, parent: TableElement):
        return TableRow(parent=parent)
    
    def _process_table(self, parent: ParagraphHtmlElement, attrs):
        return TableElement(attrs.get("columns", 0), attrs.get("align", "L"), parent = parent)
    
    def _process_a_node(self, parent: ParagraphHtmlElement, attrs):
        return AHtmlElement(attrs.get("href", ""), parent=parent)
    
    def _process_small_html_node(self, parent:ParagraphHtmlElement):
        return SmallTextHtmlElement(parent)
    
    def _process_big_html_node(self, parent:ParagraphHtmlElement):
        return BigTextHtmlElement(parent)
    
    def _process_italic_html_node(self, parent:ParagraphHtmlElement):
        return ItalicTextElement(parent)

    def _process_strong_html_node(self, parent:ParagraphHtmlElement):
        return StrongTextHtmlElement(parent)

    def _process_bold_html_node(self, parent:ParagraphHtmlElement):
        return BoldTextHtmlElement(parent)

    def endElement(self, name):
        if self.current_element == name and self.inner_text:
            if self.current_element == "card":
                self._current_card = None
            elif isinstance(self._current_node_rep, TextHtmlSubElement):
                self._current_node_rep.content = self.inner_text

    def characters(self, content):
        if self.current_element:
            self.inner_text += content.strip()
        if self.current_element == "p":
            self._current_node_rep.children.append(self.inner_text)
        self.inner_text = ""
        self.current_element = ""
