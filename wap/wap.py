from xml.sax import ContentHandler

from wap.representation.html.table import TableColumn, TableElement, TableRow
from wap.representation.html.text import AHtmlElement, BigTextHtmlElement, BoldTextHtmlElement, \
    ItalicTextElement, ParagraphHtmlElement, SmallTextHtmlElement, StrongTextHtmlElement, \
    TextContent, UnderlineTextElement
from wap.representation.markup import Card, Deck, WMLElement
from wap.representation.navigation import AnchorElement, GoElement, NoOpElement, \
    PrevElement, RefreshElement


class WMLParser(ContentHandler):
    def __init__(self):
        super().__init__()
        self.data = Deck()
        # Add current card shorthand to prevent having to hunt down current card
        self._current_card: Card = None
        # Add current node shorthand to prevent having to hunt down current node
        self._current_node_rep: WMLElement = None
        self._paragraph_element: ParagraphHtmlElement = None
        self.current_element: str = ""
        self.inner_text: str = ""
        self._table_element: TableElement = None

    def startElement(self, name, attrs):
        self.current_element = name
        match name:
            case "card":
                self._current_card = Card(attrs["id"], attrs["title"])
                self.data.cards.append(self._current_card)
            case "p":
                self._current_node_rep = self._process_paragraph(attrs, self._current_card)
                self._current_card.children.append(self._current_node_rep)
                self._paragraph_element = self._current_node_rep
            case "a":
                if self._paragraph_element and self.inner_text:
                    self._current_node_rep.children.append(self.inner_text)
                self._current_node_rep = self._process_a_node(self._paragraph_element, attrs)
                if self._paragraph_element:
                    self._paragraph_element.children.append(self._current_node_rep)
            case "table":
                self._table_element = self._process_table(self._paragraph_element, attrs)
                self._paragraph_element.children.append(self._table_element)
                self._current_node_rep = self._table_element
            case "tr":
                if self._table_element:
                    row = self._process_table_row(self._table_element)
                    self._table_element.rows.append(row)
                    self._current_node_rep = row
            case "td":
                if self._table_element:
                    column = self._process_table_column(self._current_node_rep)
                    self._table_element.rows[-1].columns.append(column)
                    self._current_node_rep = column
            case "strong" | "u" | "b" | "i" | "big" | "small":
                if self._paragraph_element and self.inner_text:
                    self._current_node_rep.children.append(self.inner_text)
                    self.inner_text = ""

                if name == "strong":
                    self._current_node_rep = StrongTextHtmlElement(self._paragraph_element)
                elif name == "u":
                    self._current_node_rep = UnderlineTextElement(self._paragraph_element)
                elif name == "b":
                    self._current_node_rep = BoldTextHtmlElement(self._paragraph_element)
                elif name == "i":
                    self._current_node_rep = ItalicTextElement(self._paragraph_element)
                elif name == "big":
                    self._current_node_rep = BigTextHtmlElement(self._paragraph_element)
                elif name == "small":
                    self._current_node_rep = SmallTextHtmlElement(self._paragraph_element)

                if self._paragraph_element:
                    self._paragraph_element.children.append(self._current_node_rep)
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
            element.align_from_str(attrs["align"])
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
        return TableElement(attrs.get("columns", 0), attrs.get("align", "L"), parent)
    
    def _process_a_node(self, parent: ParagraphHtmlElement, attrs):
        return AHtmlElement(attrs.get("href", ""), parent=parent)

    def endElement(self, name):
        if self.current_element == name and self.inner_text:
            if self.current_element == "card":
                self._current_card = None
            elif isinstance(self._current_node_rep, TextContent):
                self._current_node_rep.content = self.inner_text
            elif self._table_element:
                self._table_element = None

            if name == "p":
                self._paragraph_element = None
            elif name == "wml":
                self._current_node_rep = None
        self.inner_text = ""
        self.current_element = ""

    def characters(self, content):
        if self.current_element:
            self.inner_text += content.strip()

