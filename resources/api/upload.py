from os import mkdir

from werkzeug.utils import secure_filename

from resources.api.encryption import (
    generate_random_key,
    hash_key,
    get_data_directory,
    encrypt,
)
from resources.app import app
from flask import request, jsonify
from resources.api.errors import *


def is_file_suffix_valid(filename: str):
    if "." not in filename:
        return False
    suffix = filename.rsplit(".", 1)[1].lower()
    if config.FILE_SUFFIX_TYPE.lower() == "blacklist":
        return suffix not in [x.lower() for x in config.BLACKLIST_FILE_SUFFIX]
    elif config.FILE_SUFFIX_TYPE.lower() == "whitelist":
        return suffix in [x.lower() for x in config.WHITELIST_FILE_SUFFIX]
    else:
        raise ValueError(
            f"The FILE_SUFFIX_TYPE {config.FILE_SUFFIX_TYPE} should be 'blacklist' or 'whitelist'."
        )


@app.flask.route("/upload", methods=["POST"])
def upload_method():
    if "file" not in request.files:
        raise NoFileInRequest()
    file = request.files["file"]
    if file.filename == "" or "/" in file.filename:
        raise InvalidFileName()
    if not is_file_suffix_valid(file.filename):
        raise InvalidFileSuffix()
    filename = secure_filename(file.filename)
    key = generate_random_key()
    hashed_key = hash_key(key)
    content = file.read()
    if len(content) > config.MAX_FILE_BYTES:
        raise FileToBig()
    out_directory = get_data_directory() + hashed_key
    mkdir(out_directory)
    with open(out_directory + "/" + filename, "wb") as file:
        file.write(encrypt(content, key))

    return jsonify(
        {
            "key": key,
            "hashed_key": hashed_key,
            "filename": filename,
            "link": config.BASIC_OUT_LINK + f"/{key}/{filename}",
        }
    )
