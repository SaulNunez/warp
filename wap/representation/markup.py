from typing import List, TypedDict


class WMLElement:
    def __init__(self, parent=None):
        self.parent: WMLElement = parent

class HtmlElement(WMLElement):
    pass

class Card(WMLElement):
    def __init__(self, id: str, title: str, parent: WMLElement = None):
        super().__init__(parent)
        self.id = id
        self.title = title
        self.children: List[HtmlElement] = []

class Deck():
    def __init__(self):
        self.cards: List[Card] = []

    def findCardById(self, id: str):
        for card in self.cards:
            if card.id == id:
                return card

