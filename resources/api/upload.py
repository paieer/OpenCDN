"""
open_cdn.server
~~~~~~~~~~~~

This module implements the api uploading.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

from os import mkdir
from os.path import exists

from werkzeug.utils import secure_filename

from resources.api.authentication import (
    private_key_file_name,
    run_api_with_authentication_required, authenticate_group, get_group_directory,
)
from resources.api.encryption import (
    generate_random_key,
    hash_key,
    get_data_directory,
    encrypt,
)
from resources.api.groups import is_group_name_valid
from resources.app import app
from flask import request, jsonify
from resources.api.errors import (
    NoFileInRequest,
    InvalidFileName,
    InvalidFileSuffix,
    FileTooBig, BadRequest, GroupDoesNotExists, AccessDenied, FileAlreadyExists,
)
from resources.config import config
from resources.flask_event_handlers import get_real_ip
from resources.logger import logger, LogType


def is_file_suffix_valid(filename: str) -> bool:
    """Checks if the file suffix on a file is valid.
    :param filename:
    :return: True if the suffix is valid and False if the suffix is invalid.
    """
    if (
        "." not in filename
    ):  # if the file doesn't have any suffix (e.g. 'test'), the function returns False
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
    """Checks if the filename is valid (character checking).
    :param: The filename of the file with suffix.
    :return: True if the filename is valid and False if the filename is invalid.
    """
    for f in filename:
        if f not in config.ALLOWED_FILENAME_CHARACTERS:
            return False
    return True


@app.flask.route("/upload", methods=["POST"])
def upload_method():
    """The flask upload method for uploading.
    Requires: a 'file' file which contains the file to uploaded.
    Optional: If authentication is enabled, you must set the authentication form values.
              You can set 'private_key' to your private_key. If 'private_key' is not set,
              the server would generate a random private_key.
              Group Uploading:
              If you would like to update a file in a group you must hand over the 'group', 'private_key' and the 'key'
              of the group. The 'group' parameter is the group name. If you use group uploading following errors
              can be thrown: :class:`GroupDoesNotExists`, :class:`AccessDenied`.
    Errors: :class:`ActionNeedsAuthenticationToken`, :class:`InvalidAuthenticationToken`, :class:`NoFileInRequest`,
            :class:`InvalidFileName`, :class:`InvalidFileSuffix`, :class:`InvalidFileName`, :class:`FileTooBig`.
    Return: errors or json {
                'key': 'the_encrypting_key (string).',
                'hashed_key': 'the encrypting_key hashed (string).',
                'filename': 'the name of the file (string).',
                'private_key': 'the private_key of the file (string).',
            ]
    """
    if config.AUTHENTICATION_FOR_UPLOADING_REQUIRED:
        run_api_with_authentication_required()
    if "file" not in request.files:
        raise NoFileInRequest()
    file = request.files["file"]
    if file.filename == "" or "/" in file.filename or "\" in file.filename: # PTA protection
        raise InvalidFileName()
    if not is_file_suffix_valid(file.filename):
        raise InvalidFileSuffix()
    if not is_filename_valid(file.filename):
        raise InvalidFileName()
    group = None
    key = None
    if "group" in request.form:
        if "key" not in request.form or "private_key" not in request.form:
            raise BadRequest()
        group = request.form["group"]
        key = request.form["key"]
        if not is_group_name_valid(group):
            raise GroupDoesNotExists()
        authenticate_group(group, request.form["private_key"])
    filename = secure_filename(file.filename)
    if key is None:
        key = generate_random_key(config.RANDOM_KEY_LENGTH) # The encrypting key
    if "private_key" in request.form:
        private_key = request.form["private_key"]
    else:
        private_key = generate_random_key(config.RANDOM_PRIVATE_KEY_LENGTH)
    hashed_key = hash_key(key)
    hashed_private_key = hash_key(private_key)
    content = file.read()
    if len(content) > config.MAX_FILE_BYTES:
        raise FileTooBig()
    if group is None:
        out_directory = get_data_directory() + hashed_key
        mkdir(out_directory)
        with open(out_directory + "/" + filename, "wb") as file:
            file.write(encrypt(content, key))
        with open(out_directory + "/" + private_key_file_name, "w") as file:
            file.write(hashed_private_key)
        logger.log(
            LogType.INFO,
            f"New upload from {get_real_ip()} to {hashed_key}/{filename} with filesize {len(content)}.",
        )
        return jsonify(
            {
                "key": key,
                "hashed_key": hashed_key,
                "filename": filename,
                "private_key": private_key,
            }
        )
    else:
        files_directory = f"{get_group_directory()}/{group}/{hashed_key}"
        if not exists(files_directory):
            raise GroupDoesNotExists()
        if exists(files_directory + "/" + filename):
            raise FileAlreadyExists()
        with open(files_directory + "/" + filename, "wb") as file:
            file.write(encrypt(content, key))

        logger.log(
            LogType.INFO,
            f"New upload from {get_real_ip()} to (group) {group}/{hashed_key}/{filename} with filesize {len(content)}.",
        )
        return jsonify(
            {
                "key": key,
                "hashed_key": hashed_key,
                "filename": filename,
                "private_key": private_key,
                "group": group
            }
        )

