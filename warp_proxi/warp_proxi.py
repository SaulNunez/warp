from flask import Flask, request, render_template
from warp_proxi.html_render.service import process_wap_request

app = Flask(__name__)

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/wml_to_html')
def convert():
   if "wml_url" in request.args:
      url = request.args["wml_url"]
      representation = process_wap_request(url)
      return render_template("convert.html", document=representation)

if __name__ == "__main__":
    app.run(debug=True)
