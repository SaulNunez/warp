import unittest
import xml

from wap.representation.html.text import ModeTypes, ParagraphHtmlElement
from wap.wap import WMLParser


class TestMarkupParsing(unittest.TestCase):
    def test_minimal_page(self):
        with open('./tests/example.wml', 'r') as file:
            parser = xml.sax.make_parser()
            handler = WMLParser()
            parser.setContentHandler(handler)
            parser.parse(file)
            card = handler.data.findCardById("carta1")
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


