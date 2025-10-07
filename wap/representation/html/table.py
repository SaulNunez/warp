from enum import StrEnum
from typing import List

from wap.representation.html.text import TextContent
from wap.representation.markup import WMLElement


class TableColumn(TextContent):
    pass

class TableRow(WMLElement):
    def __init__(self, parent):
        super().__init__(parent)
        self.columns: List[TableColumn] = []
    

class ColumnAlignment(StrEnum):
    left = 'l'
    right = 'r'
    center = 'c'

class TableElement:
    def __init__(self, columns: int, align: str, rows: List[TableRow] = []):
        self.columns = columns
        self._align = align
        self.rows = rows

    def column_alignment(self, index: int) -> ColumnAlignment:
        if len(self.align) <= index:
            return getattr(ColumnAlignment, 'l')
        else:
            if(self.align not in "lrc"):
                return getattr(ColumnAlignment, 'l')
            return getattr(ColumnAlignment, self.align[index])
