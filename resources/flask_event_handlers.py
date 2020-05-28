from typing import List

from flask import Response, jsonify
from werkzeug import exceptions

from resources.api.encryption import hash_key
from resources.api.errors import BasicError, BadRequest
from resources.app import app
from resources.config import config
from resources.logger import logger, LogType
from flask import request
import re


def handle_request_path(path):
    regex = rf"\/[\w{config.ALLOWED_FILENAME_CHARACTERS}]+"
    matches = re.finditer(regex, path, re.MULTILINE)
    match_list: List[re.Match] = []
    for match in matches:
        match_list.append(match)
    if len(match_list) == 2 and "." in match_list[1].group():
        # This is a key request and the key would be censored (hashed)
        key = hash_key(match_list[0].group()[1:])
        return f"/{key}{match_list[1].group()}"
    return path


@app.flask.after_request
def after_request_logging(response: Response):
    logger.log(
        LogType.INFO,
        f"Request from {request.remote_addr} to {handle_request_path(request.path)}:{request.method} with status {response.status}.",
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
