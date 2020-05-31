"""
open_cdn.server
~~~~~~~~~~~~

This module implements the config parsing.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

import string

from resources.config_parser import run_config, write_default_config
from resources.argument_parser import args
from random import choice as rand_choice
from string import ascii_letters


class Config:
    """The default Config obeject."""

    """The Host of the server."""
    HOST = "127.0.0.1"
    """The Port of the server."""
    PORT = 80
    """If THREADED enabled, the flask server will be started with threaded=True."""
    THREADED = True  # recommend
    """Debug is not recommend, because the server have own error management."""
    DEBUG = False  # do not use debug in production
    """In this directory all logs will be written."""
    LOG_DIRECTORY = "logs/"
    """The filename of the log file."""
    LOG_FILENAME = "log_%m_%d_%y.log"
    """The whitelist of file suffixes (Only enabled, if FILE_SUFFIX_TYPE is 'whitelist')."""
    WHITELIST_FILE_SUFFIX = ["png", "jpg", "jpeg", "zip", "gz", "tar"]
    """The blacklist of file suffixes (Only enabled, if FILE_SUFFIX_TYPE is 'blacklist')."""
    BLACKLIST_FILE_SUFFIX = ["exe"]
    """The type/mopde of the suffix filtering: 'blacklist' or 'whitelist'."""
    FILE_SUFFIX_TYPE = "blacklist"
    """The Key for the server. The key is a part of the encrypting key. Attention: If you change it, all files, 
    that have been encrypted with the old key, become undecryptable. Please backup this key!
    In the default configuration, the SERVER_KEY would be created automatically.
    """
    SERVER_KEY = "[RANDOM]"
    """The directory where the files would be saved."""
    DATA_DIRECTORY = "data/"
    """The length of the random encrypting key."""
    RANDOM_KEY_LENGTH = 15
    """The hash algo for the encrypting keys. The hashed key is the identifier of any file."""
    HASH_ALGO = "sha3_256"
    """Maximum of size of the file to be uploaded."""
    MAX_FILE_BYTES = 1024 * 1024 * 50  # 5 mb
    """The length of the random private key.
    The client needs the private key to do actions with the file: For example delete it."""
    RANDOM_PRIVATE_KEY_LENGTH = 15
    """Allowed Characters for the filename."""
    ALLOWED_FILENAME_CHARACTERS = (
        string.ascii_letters + "1234567890" + ",;.:-_<>!\"§$%&()=?\\`´|#'+*@€.ß "
    )
    """Allowed Characters for the group name."""
    ALLOWED_GROUPNAME_CHARACTERS = (
        string.ascii_letters + "1234567890" + ",;.:-_<>!\"§$%&()=?\\|#'+*@€.ß "
    )
    """If proxy redirecting is enabled, the log will not print the remote_addr, but the CF-Connecting-IP or the 
    X-Forwarded-For header. """
    PROXY_REDIRECTING = False
    """The length of the authentication token."""
    RANDOM_AUTHENTICATION_TOKEN_LENGTH = 20
    """If this attribute is enabled, the client needs a valid authentication token to upload files."""
    AUTHENTICATION_FOR_UPLOADING_REQUIRED = False


config = Config()
config.SERVER_KEY = ""
for i in range(5):
    config.SERVER_KEY += rand_choice(list(ascii_letters + "1234567890"))


if args.reset_configuration:
    write_default_config(config, args.configuration_file)
    print("Configuration has been reset")
config = run_config(config, args.configuration_file)


if "/" in config.ALLOWED_FILENAME_CHARACTERS or "/" in config.ALLOWED_GROUPNAME_CHARACTERS:
    raise ValueError("'/' can not be a part of ALLOWED_FILENAME_CHARACTERS or ALLOWED_GROUPNAME_CHARACTERS.")
