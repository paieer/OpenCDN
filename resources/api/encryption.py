"""
open_cdn.server
~~~~~~~~~~~~

This module implements the encryption.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

import hashlib
import string
import random

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

from resources.config import config


def generate_random_key(length: int) -> str:
    """Generates a random key (e.g. private key or encrypting key).
    :param length: The length of the key.
    :return: The key itself (string).
    """
    key = ""
    while len(key) < length:
        key += random.choice(list(string.ascii_letters + "01234567890"))
    return key


def hash_key(key: str) -> str:
    """Hashes a key with the config.HASH_ALGO method.
    :param key: The raw key.
    :return: The hashed key.
    """
    h = hashlib.new(config.HASH_ALGO)
    h.update(key.encode("utf-8"))
    return h.hexdigest()


def make_aes(key: bytes):
    """Creates a new aes object with the key.
    :param key: The encrypting key.
    :return: AES Object.
    """
    b = PBKDF2(config.SERVER_KEY, key).read(48)
    return AES.new(b[:32], AES.MODE_CFB, iv=b[32:])


def encrypt(content: bytes, key: str) -> bytes:
    """Encrypts the content with the key (AES File encryption).
    :param content: The content to be encrypted.
    :param key: The key (string).
    :return: The encrypted content.
    """
    aes = make_aes(key.encode("utf-8"))
    content_length = 16 - (len(content) % 16)
    content += bytes([content_length]) * content_length
    return aes.encrypt(content)


def decrypt(content: bytes, key: str) -> bytes:
    """Decrypts the content.
    :param content: The encrypted content.
    :param key: The key (string).
    :return: The decrypted content.
    """
    aes = make_aes(key.encode("utf-8"))
    decrypted_content = aes.decrypt(content)
    return decrypted_content[: -decrypted_content[-1]]


def get_data_directory() -> str:
    """Gets the data directory.
    :return: The data directory with a '/' at the end.
    """
    data_dir = config.DATA_DIRECTORY
    if data_dir == "":
        data_dir = "data/"
    if not data_dir.endswith("/"):
        data_dir += "/"
    return data_dir
