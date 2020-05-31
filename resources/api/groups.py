"""
open_cdn.server
~~~~~~~~~~~~

This module implements the api group management.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""
import shutil
from io import BytesIO
from os import mkdir, listdir, remove
from os.path import exists

from flask import request, jsonify, send_file

from resources.app import app
from resources.api.authentication import (
    get_group_directory,
    authenticate_group,
    run_api_with_authentication_required,
)
from resources.api.encryption import (
    hash_key,
    generate_random_key,
    decrypt,
)
from resources.api.errors import (
    BadRequest,
    GroupDoesNotExists,
    GroupAlreadyExists,
    FileDoesNotExists,
    InvalidGroupName,
)
from resources.config import config


def is_group_name_valid(group_name: str) -> bool:
    """Check if the group name is valid.
    :param group_name: The group_name to be validated.
    :return: True if the group_name is valid and False if not.
    """
    if ".." in group_name or "/" in group_name:
        return False
    for c in group_name:
        if c not in config.ALLOWED_GROUPNAME_CHARACTERS:
            return False
    return True


@app.flask.route("/group/<string:name>", methods=["PUT", "POST", "DELETE"])
def group(name: str):
    """Show, Create and Delete groups.
    :param name: The name of the group.

    Show Group: (PUT)
    ==========
    Requires: private_key (the private_key of the group), key (the key of the group).
    Errors: :class:`GroupDoesNotExists`, :class:`ActionDenied`.
    Returns: error or json {
                'hashed_key': 'the key, but hashed.',
                'files': 'List of filenames, which are saved in this group.',
            }

    Create Group: (POST)
    ==========
    Optional: private_key: The private_key of the group (if the private_key is not set,
        the server will generate it itself), If authentication is enabled, you must set the authentication form values.
    Errors: :class:`ActionNeedsAuthenticationToken`, :class:`InvalidAuthenticationToken`, :class:`InvalidGroupName`,
        :class:`GroupAlreadyExists`
    Return: error or json {
                'name': 'The name of the group.',
                'key': 'The key of the group.',
                'hashed_key': 'The key of the group, but hashed',
                'private_key': 'The private key of the group.'
            }

    Delete Group: (DELETE)
    Requires: private_key (the private_key of the group).
    Errors: :class:`GroupDoesNotExists`, :class:`ActionDenied`.
    Returns: error or success json.
    ==========


    """
    if request.method == "PUT":
        if not is_group_name_valid(name):
            raise GroupDoesNotExists()
        path = get_group_directory() + f"/{name}"
        if not exists(path):
            raise GroupDoesNotExists()
        if "private_key" not in request.form or "key" not in request.form:
            raise BadRequest()
        key = request.form["key"]
        hashed_key = hash_key(key)
        private_key = request.form["private_key"]
        authenticate_group(name, private_key)
        if not exists(path + "/" + hashed_key):
            raise GroupDoesNotExists()
        informations = {
            "hashed_key": hashed_key,
            "files": listdir(path + "/" + hashed_key),
        }
        return jsonify(informations)
    elif request.method == "POST":
        if config.AUTHENTICATION_FOR_UPLOADING_REQUIRED:
            run_api_with_authentication_required()
        if not is_group_name_valid(name):
            raise InvalidGroupName()
        path = get_group_directory() + f"/{name}"
        if exists(path):
            raise GroupAlreadyExists()
        if "private_key" in request.form:
            private_key = request.form["private_key"]
        else:
            private_key = generate_random_key(config.RANDOM_PRIVATE_KEY_LENGTH)
        key = generate_random_key(config.RANDOM_KEY_LENGTH)
        hashed_key = hash_key(key)
        mkdir(path)
        mkdir(path + "/" + hashed_key)
        with open(path + "/private.key", "w") as private_file:
            private_file.write(hash_key(private_key))
        return jsonify(
            {
                "name": name,
                "key": key,
                "hashed_key": hashed_key,
                "private_key": private_key,
            }
        )
    elif request.method == "DELETE":
        if "private_key" not in request.form:
            raise BadRequest()
        private_key = request.form["private_key"]
        authenticate_group(name, private_key)
        path = get_group_directory() + f"/{name}"
        shutil.rmtree(path)
        return jsonify({"status": "success"})


@app.flask.route(
    "/<string:name>/<string:key>/<string:filename>", methods=["GET", "DELETE"]
)
def download_group_file(name: str, key: str, filename: str):
    """Download a group file. Attention: Do not share a group file link, because every file in the group is encrypted
    with the same key. With this file and all filenames the client can download every file from the group. With the
    link nobody can look or delete a group.
    :param name: The name of the group.
    :param key: The encrypting key of the group.
    :param filename: The name of the file.

    Download: (GET)
    ===========

    Errors: :class:`FileDoesNotExists`.
    Returns: error or the raw content of the file.

    Delete: (DELETE)
    ===========

    Requires: private_key (the private_key of the group).
    Errors: :class:`FileDoesNotExists`, :class:`AccessDenied`.
    Returns: error or success json.
    """
    if not is_group_name_valid(name):
        raise FileDoesNotExists()
    if ".." in filename or "/" in filename:
        raise FileDoesNotExists()
    hashed_key = hash_key(key)
    path = f"{get_group_directory()}/{name}/{hashed_key}"
    if not exists(path):
        raise FileDoesNotExists()
    file_path = f"{path}/{filename}"
    if not exists(file_path):
        raise FileDoesNotExists()
    if request.method == "GET":
        with open(file_path, "rb") as file:
            content = file.read()
        decrypted_content = decrypt(content, key)
        file = BytesIO()
        file.write(decrypted_content)
        file.seek(0)
        return send_file(file, attachment_filename=filename)
    elif request.method == "DELETE":
        if "private_key" not in request.form:
            raise BadRequest()
        private_key = request.form["private_key"]
        authenticate_group(name, private_key)
        remove(file_path)
        return jsonify({"status": "success"})
