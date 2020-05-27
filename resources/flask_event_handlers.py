from flask import Response, jsonify
from werkzeug import exceptions

from resources.api.errors import BasicError, BadRequest
from resources.app import app
from resources.logger import logger, LogType
from flask import request


@app.flask.after_request
def after_request_logging(response: Response):
    logger.log(
        LogType.INFO,
        f"Request from {request.remote_addr} to {request.path}:{request.method} with status {response.status}.",
    )
    return response


@app.flask.errorhandler(BasicError)
def basic_error_handler(e: BasicError):
    logger.log(
        LogType.INFO,
        f"Request with error from {request.remote_addr} with error {e.id}:{e.name}.",
    )
    return jsonify(e.to_json()), e.http_return


@app.flask.errorhandler(exceptions.BadRequest)
def bad_request_handling(_):
    return jsonify(BadRequest().to_json()), BadRequest.http_return
