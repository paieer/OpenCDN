"""
open_cdn.server
~~~~~~~~~~~~

This module implements the version management respectively the version return.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

from resources.app import app

"""The version name."""
VERSION = "v0.11 unstable beta"
"""The version as integer number."""
RAW_VERSION = 11


@app.flask.route("/")
def index_version() -> str:
    """Returns information about OpenCDN and '\n' the raw version integer number.
    Attention: The response is not json, but html/text.
    """
    return f'OpenCDN on {VERSION} - <a href="https://github.com/AdriBloober/OpenCDN">GitHub Repository</a>\n{RAW_VERSION}'
