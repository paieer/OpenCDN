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
    sleep(0.5)
    run_api_with_authentication_required()
    return jsonify({"status": "success"})
