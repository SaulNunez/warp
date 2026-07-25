import unittest

from warp.representation.html.text import BigTextHtmlElement, \
    BoldTextHtmlElement, ItalicTextElement, ModeTypes, ParagraphHtmlElement, \
        SmallTextHtmlElement, StrongTextHtmlElement, UnderlineTextElement
from warp.wml import parse_from_file


class TestMarkupParsing(unittest.TestCase):
    def test_minimal_page(self):
        with open('./tests/example.wml', 'r') as file:
            deck = parse_from_file(file)
            card = deck.findCardById("carta1")
            self.assertIsNotNone(card)
            # Assert card values
            self.assertEqual(card.id, "carta1")
            self.assertEqual(card.title, "Carta")
            # Check children parsing
            self.assertEqual(len(card.children), 1)
            paragraph = card.children[0]
            # Check correct object is returned
            self.assertTrue(isinstance(paragraph, ParagraphHtmlElement))
            self.assertTrue(paragraph.mode, ModeTypes.wrap)

    def test_text_styling_page(self):
        with open('./tests/text_styles.wml', 'r') as file:
            deck = parse_from_file(file)
            card = deck.findCardById("card1")
            self.assertIsNotNone(card)
            self.assertEqual(card.title, "Text styles")
            self.assertEqual(len(card.children), 1)
            paragraph = card.children[0]
            self.assertTrue(isinstance(paragraph, ParagraphHtmlElement))
            self.assertEqual(len(paragraph.children), 7)
            self.assertEqual(paragraph.children[0], "These tags allow elements to have different font styles, but font is decided by the device:")
            self.assertIsInstance(paragraph.children[1], BoldTextHtmlElement)
            self.assertEqual(paragraph.children[1].content, "Bold text")
            self.assertIsInstance(paragraph.children[2], BigTextHtmlElement)
            self.assertIsInstance(paragraph.children[3], SmallTextHtmlElement)
            self.assertIsInstance(paragraph.children[4], ItalicTextElement)
            self.assertIsInstance(paragraph.children[5], StrongTextHtmlElement)
            self.assertIsInstance(paragraph.children[6], UnderlineTextElement)
    
    def test_table_parsing(self):
        with open('./tests/table.wml', 'r') as file:
            deck = parse_from_file(file)
            card = deck.findCardById("card_table")
            self.assertIsNotNone(card)
            self.assertEqual(len(card.children), 1)
            paragraph = card.children[0]
            self.assertEqual(len(paragraph.children), 1)
            table = paragraph.children[0]
            self.assertEqual(len(table.rows), 2)
            self.assertEqual(len(table.rows[0].columns), 3)
            self.assertEqual(table.rows[0].columns[0].content, "Column 1")
            self.assertEqual(table.rows[0].columns[1].content, "Column 2")
            self.assertEqual(table.rows[0].columns[2].content, "Column 3")

    def test_frogfind_wml_parsing(self):
        import urllib.request
        from warp.wml import parse_from_string

        req = urllib.request.Request(
            'http://frogfind.com',
            headers={'Accept': 'text/vnd.wap.wml'}
        )
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')

        deck = parse_from_string(content)
        self.assertIsNotNone(deck)
        self.assertGreater(len(deck.cards), 0)

        card = deck.findCardById("frogfind")
        self.assertIsNotNone(card)
        self.assertEqual(card.id, "frogfind")
        self.assertEqual(card.title, "FrogFind!")

        # Check postfield parsing inside anchor -> go
        from warp.representation.navigation import AnchorElement, GoElement, PostFieldElement
        paragraph = card.children[1]
        anchor = [c for c in paragraph.children if isinstance(c, AnchorElement)][0]
        go = [c for c in anchor.children if isinstance(c, GoElement)][0]
        self.assertEqual(len(go.postfields), 1)
        self.assertIsInstance(go.postfields[0], PostFieldElement)
        self.assertEqual(go.postfields[0].name, "q")
        self.assertEqual(go.postfields[0].value, "$(search)")




