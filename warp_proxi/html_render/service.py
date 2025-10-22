import os
import socket
from typing import List
from wap.wap import WMLParser
from wap_request.wap_request import request_wap
from warp_proxi.html_render.link_creator import ProxiLinkCreator
from warp_proxi.html_render.models import CardInformation, WmlDocumentInformation
from warp_proxi.html_render.render import RenderToHtml
import xml

def get_system_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

host = os.environ.get("HOST_DOMAIN", get_system_ip_address())

def process_wap_request(url: str) -> WmlDocumentInformation:
    status, text = request_wap(url)

    parser = xml.sax.make_parser()
    handler = WMLParser()
    parser.setContentHandler(handler)
    parser.parse(text)
    page = handler.data
      
    link_creator = ProxiLinkCreator(host)
    cards_representation: List[CardInformation] = []
    for card in page.cards: 
        contents = RenderToHtml(card, link_creator).generate()
        cards_representation.append((card.id, card.title, contents))
    
    return {'cards': cards_representation }