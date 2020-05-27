from io import BytesIO
from os.path import exists

from flask import send_file

from resources.api.encryption import hash_key, decrypt
from resources.api.errors import FileDoesNotExists
from resources.app import app
from resources.config import config


@app.flask.route("/<string:key>/<string:filename>")
def download(key: str, filename: str):
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
