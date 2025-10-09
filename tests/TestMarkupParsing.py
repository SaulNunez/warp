import unittest
import xml

from wap.representation.html.text import BigTextHtmlElement, BoldTextHtmlElement, ItalicTextElement, ModeTypes, ParagraphHtmlElement, SmallTextHtmlElement, StrongTextHtmlElement, UnderlineTextElement
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

    def test_text_styling_page(self):
        with open('./tests/text_styles.wml', 'r') as file:
            parser = xml.sax.make_parser()
            handler = WMLParser()
            parser.setContentHandler(handler)
            parser.parse(file)
            card = handler.data.findCardById("card1")
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
            parser = xml.sax.make_parser()
            handler = WMLParser()
            parser.setContentHandler(handler)
            parser.parse(file)
            card = handler.data.findCardById("card_table")
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



