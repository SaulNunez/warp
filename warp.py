
from typing import TextIO
import xml
from wap.representation.markup import Deck
from wap.wap import WMLParser


def parse_from_file(file: TextIO) -> Deck:
    parser = xml.sax.make_parser()
    handler = WMLParser()
    parser.setContentHandler(handler)
    parser.parse(file)
    return handler.data

def parse_from_string(contents: str) -> Deck:
    parser = xml.sax.make_parser()
    handler = WMLParser()
    parser.setContentHandler(handler)
    parser.parseString(contents)
    return handler.data