from os import remove, rmdir
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
    InvalidAuthenticationToken,
)
from flask import request
import base64

from resources.config import config

private_key_file_name = "private.key"

authentication_tokens = []


def parse_authentication(key, filename):
    if "private_key" not in request.form:
        raise BadRequest()
    authenticate(hash_key(key), filename, request.form["private_key"])


def authenticate(key, filename, private_key):
    if not exists(get_data_directory() + key + "/" + filename):
        raise FileDoesNotExists()
    if not exists(get_data_directory() + key + "/" + private_key_file_name):
        raise AccessDenied()
    with open(get_data_directory() + key + "/" + private_key_file_name) as file:
        if hash_key(private_key) != file.read():
            raise AccessDenied()


def delete_file(key, filename):
    key_path = get_data_directory() + hash_key(key)
    remove(key_path + "/" + filename)
    remove(key_path + "/" + private_key_file_name)
    rmdir(key_path)


def create_authentication_token(key_identifier):
    if key_identifier not in config.KEYS:
        raise AuthenticationKeyNotFound()
    key = RSA.import_key(base64.b64decode(config.KEYS[key_identifier].encode("utf-8")))
    token = generate_random_key(config.RANDOM_AUTHENTICATION_TOKEN_LENGTH)
    authentication_tokens.append(hash_key(token))
    encrypted_token = base64.b64encode(
        PKCS1_OAEP.new(key).encrypt(token.encode("utf-8"))
    ).decode("utf-8")
    return encrypted_token


def check_token(hashed_token):
    for token in authentication_tokens:
        if token == hashed_token:
            return True
    return False


def run_api_with_authentication_required():
    if "authentication_token" not in request.form:
        raise ActionNeedsAuthenticationToken()
    if not check_token(hash_key(request.form["authentication_token"])):
        raise InvalidAuthenticationToken()


def delete_authentication_token(token):
    authentication_tokens.remove(hash_key(token))
