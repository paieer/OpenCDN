from resources.app import app

VERSION = "v0.10 unstable beta"
RAW_VERSION = 10


@app.flask.route("/")
def index_version():
    return f"OpenCDN on {VERSION} - <a href=\"https://github.com/AdriBloober/OpenCDN\">GitHub Repository</a>\n{RAW_VERSION}"
