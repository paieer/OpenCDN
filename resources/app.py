"""
open_cdn.server
~~~~~~~~~~~~

This module implements the app import and default logger disabling.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

from os import mkdir
from os.path import exists

from flask import Flask
from resources.config import config
from resources.logger import logger, LogType


class App:
    """The app with the flask app and run function."""
    """The flask app."""
    flask = Flask(__name__)

    def run_app(self):
        """Runs the app.
        :return:
        """
        if not exists(config.DATA_DIRECTORY):
            mkdir(config.DATA_DIRECTORY)

        # log the running information
        logger.log(
            LogType.HIGH, f"Server running on 'http://{config.HOST}:{config.PORT}'!"
        )
        try:
            self.flask.config["PROPAGATE_EXCEPTIONS"] = True
            self.flask.run(
                host=config.HOST,
                port=config.PORT,
                threaded=config.THREADED,
                debug=config.DEBUG,
            )
        except PermissionError:
            logger.log(
                LogType.CRITICAL,
                f"Permission denied for running on host 'http://{config.HOST}:{config.PORT}'",
            )
        except KeyboardInterrupt:
            logger.log(LogType.HIGH, "OpenCDN exited bye KeyboardInterrupt", True)
            print("Bye!")
            exit(0)


app = App()

# import api definition files.

from resources import flask_event_handlers
from resources.api import upload, download, authentication_api, version, groups

app.run_app()
