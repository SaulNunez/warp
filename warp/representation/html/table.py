from enum import StrEnum
from typing import List

from warp.representation.html.text import ParagraphHtmlElement, TextContent
from warp.representation.markup import WMLElement


class TableColumn(TextContent):
    pass

class TableRow(WMLElement):
    def __init__(self, parent):
        super().__init__(parent)
        self.columns: List[TableColumn] = []
    
    def __str__(self):
        return ",".join([str(col) for col in self.columns])

    def __repr__(self):
        return f"TableRow({",".join([str(col) for col in self.columns])})"
    

class ColumnAlignment(StrEnum):
    left = 'l'
    right = 'r'
    center = 'c'

class TableElement(WMLElement):
    def __init__(self, columns: int, align: str, parent: ParagraphHtmlElement, rows: List[TableRow] = None):
        super().__init__(parent)
        self.columns = int(columns) if columns is not None else 0
        self._align = (align or "").lower()
        # avoid mutable default argument
        self.rows = [] if rows is None else rows

    def column_alignment(self, index: int) -> ColumnAlignment:
        # If alignment string is shorter than index, default to left
        if not self._align or index >= len(self._align):
            return ColumnAlignment.left
        ch = self._align[index]
        if ch not in ("l", "r", "c"):
            return ColumnAlignment.left
        return ColumnAlignment(ch)
    
    def __str__(self):
        return "\n".join([str(row) for row in self.rows])

    def __repr__(self):
        return f"Table({'\n'.join([str(row) for row in self.rows])})"
