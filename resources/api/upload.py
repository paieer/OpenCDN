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
from resources.logger import logger, LogType


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


def is_filename_valid(filename: str) -> bool:
    for f in filename:
        if f not in config.ALLOWED_FILENAME_CHARACTERS:
            return False
    return True


@app.flask.route("/upload", methods=["POST"])
def upload_method():
    if "file" not in request.files:
        raise NoFileInRequest()
    file = request.files["file"]
    if file.filename == "" or "/" in file.filename:
        raise InvalidFileName()
    if not is_file_suffix_valid(file.filename):
        raise InvalidFileSuffix()
    if not is_filename_valid(file.filename):
        raise InvalidFileName()
    filename = secure_filename(file.filename)
    key = generate_random_key(config.RANDOM_KEY_LENGTH)
    if "private_key" in request.form:
        private_key = request.form["private_key"]
    else:
        private_key = generate_random_key(config.RANDOM_PRIVATE_KEY_LENGTH)
    hashed_key = hash_key(key)
    hashed_private_key = hash_key(private_key)
    content = file.read()
    if len(content) > config.MAX_FILE_BYTES:
        raise FileToBig()
    out_directory = get_data_directory() + hashed_key
    mkdir(out_directory)
    with open(out_directory + "/" + filename, "wb") as file:
        file.write(encrypt(content, key))
    with open(out_directory + "/" + "private.key", "w") as file:
        file.write(hashed_private_key)
    logger.log(
        LogType.INFO,
        f"New upload from {request.remote_addr} to {hashed_key}/{filename} with filesize {len(content)}.",
    )
    return jsonify(
        {
            "key": key,
            "hashed_key": hashed_key,
            "filename": filename,
            "link": config.BASIC_OUT_LINK + f"/{key}/{filename}",
            "private_key": private_key,
        }
    )
