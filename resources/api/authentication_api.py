"""
open_cdn.server
~~~~~~~~~~~~

This module implements the api authentication.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

from time import sleep

from resources.api.authentication import (
    create_authentication_token,
    run_api_with_authentication_required,
    delete_authentication_token,
)
from resources.api.errors import BadRequest
from resources.app import app
from flask import request, jsonify


@app.flask.route("/authentication", methods=["POST", "DELETE"])
def authentication_api():
    """The flask authenticate method for authenticate.
    Creating authentication token: (POST)
    ===================
    Requires: key_identifier: The identifier of the key (Key config variable key name).
    Errors: :class:`AuthenticationKeyNotFound`.
    Return: error or json {
                'encrypted_authentication_token': 'The encrypted authentication token.',
            }
    To use the authentication token, you must decrypt the token with you'r private key.
    Delete authentication token: (DELETE)
    ===================
    Requires: authentication form values.
    Errors: :class:`ActionNeedsAuthenticationToken`, :class:`InvalidAuthenticationToken`.
    Return: error or success json.
    """
    if request.method == "POST":
        if "key_identifier" not in request.form:
            raise BadRequest()
        key_identifier = request.form["key_identifier"]
        return jsonify(
            {
                "encrypted_authentication_token": create_authentication_token(
                    key_identifier
                )
            }
        )
    elif request.method == "DELETE":
        run_api_with_authentication_required()
        delete_authentication_token(request.form["authentication_token"])
        return {"status": "success"}


@app.flask.route("/authentication/test", methods=["POSt"])
def authentication_test():
    """Test a authentication token
    Attention: This action needs 0.5 seconds to proceed to block spam or bruteforcing so do not use it in production.
    Requires: authentication form values.
    Errors: :class:`ActionNeedsAuthenticationToken`, :class:`InvalidAuthenticationToken`.
    Return: error or success json.
    """
    sleep(0.5)
    run_api_with_authentication_required()
    return jsonify({"status": "success"})
