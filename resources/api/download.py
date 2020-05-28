from io import BytesIO
from os.path import exists

from flask import send_file, request, jsonify

from resources.api.authentication import authenticate, parse_authentication, delete_file
from resources.api.encryption import hash_key, decrypt
from resources.api.errors import FileDoesNotExists
from resources.app import app
from resources.config import config


@app.flask.route("/<string:key>/<string:filename>", methods=["GET", "DELETE"])
def download(key: str, filename: str):
    if request.method == "GET":
        hashed_key = hash_key(key)
        if "/" in key or "/" in filename or ".." in key:
            raise FileDoesNotExists()
        filepath = f"{config.DATA_DIRECTORY}{hashed_key}/{filename}"
        if not exists(filepath):
            raise FileDoesNotExists()
        with open(filepath, "rb") as file:
            content = file.read()
        decrypted_content = decrypt(content, key)
        file = BytesIO()
        file.write(decrypted_content)
        file.seek(0)
        return send_file(file, attachment_filename=filename)
    elif request.method == "DELETE":
        parse_authentication(key, filename)
        delete_file(key, filename)
        return jsonify({"status": "success"})
