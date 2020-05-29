from os import mkdir
from os.path import exists

from flask import Flask
from resources.config import config
from resources.logger import logger, LogType


class App:
    flask = Flask(__name__)

    def run_app(self):
        if not exists(config.DATA_DIRECTORY):
            mkdir(config.DATA_DIRECTORY)

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
from resources import flask_event_handlers
from resources.api import upload, download, authentication_api, version

app.run_app()
