import string

from resources.config_parser import run_config, write_default_config
from resources.argument_parser import args
from random import choice as rand_choice
from string import ascii_letters


class Config:
    HOST = "127.0.0.1"
    PORT = 80
    THREADED = True  # recommend
    DEBUG = False  # do not use debug in production
    LOG_DIRECTORY = "logs/"
    LOG_FILENAME = "log_%m_%d_%y.log"
    WHITELIST_FILE_SUFFIX = ["png", "jpg", "jpeg", "zip", "gz", "tar"]
    BLACKLIST_FILE_SUFFIX = ["exe"]
    FILE_SUFFIX_TYPE = "blacklist"
    SERVER_KEY = "[RANDOM]"
    DATA_DIRECTORY = "data/"
    RANDOM_KEY_LENGTH = 15
    HASH_ALGO = "sha3_256"
    BASIC_OUT_LINK = f"http://{HOST}:{PORT}"
    MAX_FILE_BYTES = 1024 * 1024 * 50  # 5 mb
    RANDOM_PRIVATE_KEY_LENGTH = 15
    ALLOWED_FILENAME_CHARACTERS = (
        string.ascii_letters + "1234567890" + ",;.:-_<>!\"§$%&()=?\\`´|#'+*@€.ß "
    )
    PROXY_REDIRECTING = False
    RANDOM_AUTHENTICATION_TOKEN_LENGTH = 20
    AUTHENTICATION_FOR_UPLOADING_REQUIRED = False


config = Config()
config.SERVER_KEY = ""
for i in range(5):
    config.SERVER_KEY += rand_choice(list(ascii_letters + "1234567890"))


if args.reset_configuration:
    write_default_config(config, args.configuration_file)
    print("Configuration has been reset")
config = run_config(config, args.configuration_file)


if "/" in config.ALLOWED_FILENAME_CHARACTERS:
    raise ValueError("'/' can not be a part of ALLOWED_FILENAME_CHARACTERS.")
