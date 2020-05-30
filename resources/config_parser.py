"""
open_cdn.server
~~~~~~~~~~~~

This module implements the config parsing.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

import configparser
import os.path


class RequiredSetting:
    """A config variable contains this, if the setting variable is required and is not set by default."""
    pass


class RequiredSettingIsNone(Exception):
    """The setting is required, but was not set."""
    pass


def filter_config_attribute(attribute_name: str) -> bool:
    """Filter some not relevant config attributes.
    :param attribute_name: The name of the filtering attribute.
    :return: Returns false if the attribute is not relevant.
    """
    blocked_attributes = []
    return (
        not attribute_name in blocked_attributes
        and attribute_name.upper() == attribute_name
        and not attribute_name.startswith("__")
    )


def read_boolean(input: str) -> bool:
    """Reads a boolean from a config string
    :param input: The input string.
    :return: The boolean.
    """
    input = input.lower()
    if input in ("yes", "y", "true"):
        return True
    elif input in ("no", "n", "false"):
        return False
    else:
        raise ValueError(f"The boolean {input} can not be parsed!")


def read_list(input: str) -> list:
    """Reads a list of a input string
    :param input: The input string.
    :return: The output list: Can be [].
    The string must have the following syntax:
        first_element,second_element
    Attention: Spaces after the comma are not ignored.
    """
    splitted = input.split(",")
    return splitted


def parse_config_object(config, filepath: str):
    """Replace config attributes with attributes in the config file of the filepath.
    :param config: The config object. Replacement attributes must be written in upper case.
    :param filepath: The path to the opencdn configuration file.
    :return: The new config object (type input config).
    """
    conf = configparser.ConfigParser(interpolation=None)
    conf.read(filepath)
    for key in dir(config):
        if filter_config_attribute(key):
            new_content = conf["ServerConfiguration"].get(key, None)
            if new_content is not None:
                value = getattr(config, key)
                if type(value) == bool:
                    new_content = read_boolean(new_content)
                if type(value) == list:
                    new_content = read_list(new_content)
                setattr(config, key, type(getattr(config, key))(new_content))
            elif isinstance(getattr(config, key), RequiredSetting):
                raise RequiredSettingIsNone()
    setattr(config, "KEYS", conf["Keys"])
    return config


def write_boolean(input: bool) -> str:
    """Write boolean to string.
    True: 'yes' and False: 'no'.
    :param input: The input boolean.
    :return: The output string.
    """
    if input:
        return "yes"
    else:
        return "no"


def write_list(list: list) -> str:
    """Write list to string
    :param list: The input list.
    :return: The output string.
    """
    return ','.join(list)


def write_default_config(config, filepath: str):
    """Writes the default configuration to the configuration file at the filepath.
    Only upper case attributes, which not start with '_', will be written to the file.
    The file will be overwritten, but if the file exists, the keys will be take over.
    :param config: The config object.
    :param filepath: The path to the file.
    :return:
    """
    conf = configparser.ConfigParser(interpolation=None)
    conf["ServerConfiguration"] = {}
    if os.path.exists(filepath):
        c = configparser.ConfigParser(interpolation=None)
        c.read(filepath)
        conf["Keys"] = c["Keys"]
    else:
        conf["Keys"] = {}
    for key in dir(config):
        if key.startswith("_") or key.upper() != key:
            continue
        value = getattr(config, key)
        if type(value) == bool:
            value = write_boolean(value)
        if type(value) == list:
            value = write_list(value)
        if type(value) != str:
            value = str(value)
        conf["ServerConfiguration"][key] = value
    with open(filepath, "w") as file:
        conf.write(file)


def run_config(config, filepath: str):
    """Write/Read configuration.
    :param config: The config object with config attributes.
    :param filepath: Path to the configuration file.
    :return: New configuration file (config object type).
    """
    if not os.path.exists(filepath):
        write_default_config(config, filepath)
        print(f"Default configuration file created at {filepath}")
    return parse_config_object(config, filepath)