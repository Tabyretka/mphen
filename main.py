import os
from flask import Flask, render_template, request
import parsers

app = Flask(__name__)


@app.route("/")
def index():
    q = request.args.get('q')
    if q:
        pap = parsers.papir_parse(query=q)
        zone = parsers.zone_parse(query=q)
        return render_template("search_results_page.html", pap=pap, zone=zone)
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == "__main__":
    main()
