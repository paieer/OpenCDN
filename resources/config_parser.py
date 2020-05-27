import configparser
import os.path


class RequiredSetting:
    pass


class RequiredSettingIsNone(Exception):
    pass


def filter_config_attribute(attribute_name: str) -> bool:
    blocked_attributes = []
    return (
        not attribute_name in blocked_attributes
        and attribute_name.upper() == attribute_name
        and not attribute_name.startswith("__")
    )


def read_boolean(input: str) -> bool:
    input = input.lower()
    if input in ("yes", "y", "true"):
        return True
    elif input in ("no", "n", "false"):
        return False
    else:
        raise ValueError(f"The boolean {input} can not be parsed!")


def read_list(input: str) -> list:
    splitted = input.split(",")
    return splitted


def parse_config_object(config, filepath):
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
    return config


def write_boolean(input: bool) -> str:
    if input:
        return "yes"
    else:
        return "no"


def write_list(list: list) -> str:
    out = ""
    for l in list:
        if len(out) == 0:
            out += l
        else:
            out += "," + l
    return out


def write_default_config(config, filepath):
    conf = configparser.ConfigParser(interpolation=None)
    conf["ServerConfiguration"] = {}
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


def run_config(config, filepath):
    if not os.path.exists(filepath):
        write_default_config(config, filepath)
        print(f"Default configuration file created at {filepath}")
    return parse_config_object(config, filepath)
