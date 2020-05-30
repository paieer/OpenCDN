"""
open_cdn.server
~~~~~~~~~~~~

This module implements the authentication.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""
from os import remove, rmdir, mkdir
from os.path import exists

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

from resources.api.encryption import get_data_directory, hash_key, generate_random_key
from resources.api.errors import (
    FileDoesNotExists,
    AccessDenied,
    BadRequest,
    AuthenticationKeyNotFound,
    ActionNeedsAuthenticationToken,
    InvalidAuthenticationToken, GroupDoesNotExists,
)
from flask import request
import base64

from resources.config import config

private_key_file_name = "private.key"

"""All authentication token will saved in this list."""
authentication_tokens = []


def get_group_directory() -> str:
    """Gets the group directory and create it if it not exists."""
    group_directory = get_data_directory() + "groups"
    if not exists(group_directory):
        mkdir(group_directory)
    return group_directory


def parse_authentication(key: str, filename: str):
    """Parses the authentication (private_key) from a request.
    Errors: :class:`FileDoesNotExists`, :class:`AccessDenied`.
    :param key: The key of the target file.
    :param filename: The filename of the file.
    :return
    """
    if "private_key" not in request.form:
        raise BadRequest()
    authenticate(hash_key(key), filename, request.form["private_key"])


def authenticate(key: str, filename: str, private_key: str):
    """Authenticates with the private_key.
    :param key: The key of the target file.
    :param filename: The filename of the file.
    :param private_key: The private_key of the file.
    """
    if not exists(get_data_directory() + key + "/" + filename):
        raise FileDoesNotExists()
    if not exists(get_data_directory() + key + "/" + private_key_file_name):
        raise AccessDenied()
    with open(get_data_directory() + key + "/" + private_key_file_name) as file:
        if hash_key(private_key) != file.read():
            raise AccessDenied()


def delete_file(key: str, filename: str):
    """Deletes a file (not authenticated)
    :param key: The key of the file.
    :param filename: The filename of the file.
    :return:
    """
    key_path = get_data_directory() + hash_key(key)
    remove(key_path + "/" + filename)
    remove(key_path + "/" + private_key_file_name)
    rmdir(key_path)


def create_authentication_token(key_identifier: str) -> str:
    """Creates new encrypted authentication token.
    :param key_identifier: The identifier of the key (The key variable key name on the server configuration).
    :return:
    """
    if key_identifier not in config.KEYS:
        raise AuthenticationKeyNotFound()
    key = RSA.import_key(base64.b64decode(config.KEYS[key_identifier].encode("utf-8")))
    token = generate_random_key(config.RANDOM_AUTHENTICATION_TOKEN_LENGTH)
    authentication_tokens.append(hash_key(token))
    encrypted_token = base64.b64encode(
        PKCS1_OAEP.new(key).encrypt(token.encode("utf-8"))
    ).decode("utf-8")
    return encrypted_token


def check_token(hashed_token: str) -> bool:
    """Checks if a token is valid.
    :param hashed_token: The hashed authentication token.
    :return: True if the token is valid and False if the token is invalid.
    """
    for token in authentication_tokens:
        if token == hashed_token:
            return True
    return False


def run_api_with_authentication_required():
    """Runs the api with authentication requirement.
    Errors: :class:`ActionNeedsAuthenticationToken`, :class:`InvalidAuthenticationToken`.
    """
    if "authentication_token" not in request.form:
        raise ActionNeedsAuthenticationToken()
    if not check_token(hash_key(request.form["authentication_token"])):
        raise InvalidAuthenticationToken()


def delete_authentication_token(token: str):
    """Deletes an authentication token
    :param token: The authentication token to be deleted.
    """
    authentication_tokens.remove(hash_key(token))


def authenticate_group(group_name: str, private_key: str):
    """Authenticates group with private_key.
    :param group_name: The name of the group.
    :param private_key: The private_key of the group
    """
    if not exists(get_group_directory() + "/" + group_name):
        raise GroupDoesNotExists()
    with open(
        get_group_directory() + "/" + group_name + "/" + private_key_file_name, "r"
    ) as file:
        if not file.read().replace("\n", "") == hash_key(private_key):
            raise AccessDenied()

