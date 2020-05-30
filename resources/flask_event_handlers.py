"""
open_cdn.server
~~~~~~~~~~~~

This module implements the flask events.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

from typing import List

from flask import Response, jsonify
from werkzeug import exceptions

from resources.api.encryption import hash_key
from resources.api.errors import BasicError, BadRequest, InternalServerError
from resources.app import app
from resources.config import config
from resources.logger import logger, LogType
from flask import request
import re


def get_real_ip() -> str:
    """Gets the real ip.
    If proxy redirecting is enabled, the function will return the real ip (X-Forwared-For or CF-Connecting-IP).
    :return: the ip as string.
    """
    ip = request.remote_addr
    if config.PROXY_REDIRECTING:
        if "CF-Connecting-IP" in request.headers:
            ip = request.headers["CF-Connecting-IP"]
        elif "X-Forwarded-For" in request.headers:
            ip = request.headers["X-Forwarded-For"]
    return ip


def handle_request_path(path):
    """Handles the request path. If the path contains a key (encrypting key),
    the key will be replaced with the hash of the key.
    :param path: The raw path of request: string.
    :return: The new path (string).
    """
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
def after_request_logging(response: Response) -> Response:
    """Logs the after request."""
    logger.log(
        LogType.INFO,
        f"Request from {get_real_ip()} to {handle_request_path(request.path)}:{request.method} with status {response.status}.",
    )
    return response


@app.flask.errorhandler(BasicError)
def basic_error_handler(e: BasicError):
    """Logs the error and return the error."""
    logger.log(
        LogType.INFO,
        f"Request with error from {get_real_ip()} with error {e.id}:{e.name}.",
    )
    return jsonify(e.to_json()), e.http_return


@app.flask.errorhandler(exceptions.BadRequest)
def bad_request_handling(_):
    """Return own bad request error."""
    return jsonify(BadRequest().to_json()), BadRequest.http_return


@app.flask.errorhandler(exceptions.InternalServerError)
def internal_server_error_handling(_):
    """Return own internal server error."""
    return jsonify(InternalServerError().to_json()), InternalServerError.http_return
