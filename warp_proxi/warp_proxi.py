import os
import xml
from flask import Flask, request, render_template
from wap.wap import WMLParser
from wap_request.wap_request import request_wap
from warp_proxi.html_render.link_creator import ProxiLinkCreator
from warp_proxi.html_render.render import RenderToHtml
import socket

def get_system_ip_address() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

host = os.environ.get("HOST_DOMAIN", get_system_ip_address())

app = Flask(__name__)

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/wml_to_html')
def convert():
   if "wml_url" in request.args:
      url = request.args["wml_url"]
      status, text = request_wap(url)

      parser = xml.sax.make_parser()
      handler = WMLParser()
      parser.setContentHandler(handler)
      parser.parse(text)
      page = handler.data
      
      link_creator = ProxiLinkCreator(host)
      cards_representation = []
      for card in page.cards: 
        cards_representation.append(RenderToHtml(card, link_creator).generate())
   return render_template("convert.html")

# run the application
if __name__ == "__main__":
    app.run(debug=True)
