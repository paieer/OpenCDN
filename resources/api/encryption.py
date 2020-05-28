import hashlib
import string
import random

from Crypto.Cipher import AES
from pbkdf2 import PBKDF2

from resources.config import config


def generate_random_key(length):
    key = ""
    while len(key) < length:
        key += random.choice(list(string.ascii_letters + "01234567890"))
    return key


def hash_key(key: str):
    h = hashlib.new(config.HASH_ALGO)
    h.update(key.encode("utf-8"))
    return h.hexdigest()


def make_aes(key: bytes):
    b = PBKDF2(config.SERVER_KEY, key).read(48)
    return AES.new(b[:32], AES.MODE_CFB, iv=b[32:])


def encrypt(content: bytes, key: str):
    aes = make_aes(key.encode("utf-8"))
    content_length = 16 - (len(content) % 16)
    content += bytes([content_length]) * content_length
    return aes.encrypt(content)


def decrypt(content: bytes, key: str):
    aes = make_aes(key.encode("utf-8"))
    decrypted_content = aes.decrypt(content)
    return decrypted_content[: -decrypted_content[-1]]


def get_data_directory() -> str:
    data_dir = config.DATA_DIRECTORY
    if data_dir == "":
        data_dir = "data/"
    if not data_dir.endswith("/"):
        data_dir += "/"
    return data_dir