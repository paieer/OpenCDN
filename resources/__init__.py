"""
open_cdn.server
~~~~~~~~~~~~

This module implements the app import and default logger disabling.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

import logging

log = logging.getLogger("werkzeug")
# Disable the default logger respectively set the logger level to Error.
log.setLevel(logging.ERROR)

from resources.app import app
