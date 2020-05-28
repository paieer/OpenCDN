from os import remove, rmdir
from os.path import exists

from resources.api.encryption import get_data_directory, hash_key
from resources.api.errors import FileDoesNotExists, AccessDenied, BadRequest
from flask import request

private_key_file_name = "private.key"


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
