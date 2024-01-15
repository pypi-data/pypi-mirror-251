"""Allow to define user config path and set config variables."""

# maybe using the configparser module would be a better idea.

import os
import shutil
import pkgutil


PKG_NAME = "scibib"


def config_dir():
    """Define the path to the configuration directory."""
    # OSwise choice of config directory
    user_config_dir = os.path.join(os.path.expanduser("~"), ".config")
    if os.name == "nt":
        user_config_dir = os.get_env("%LOCALAPPDATA%", user_config_dir)
    user_config_dir = os.path.join(user_config_dir, PKG_NAME)
    return user_config_dir


def config_file():
    return os.path.join(config_dir(), PKG_NAME + "_config.py")



def set_value(config_file: str, key: str, value: str):
    """Set KEY to value in config file

    Args:
        config_file (str): path to configuration file
        key (str): the variable name to be set in config file
        value (str): the value to prescribe for key
            a line "key = value" will be set in the config file.
    """
    with open(config_file) as f:
        config_lines = f.readlines()
    for i in range(len(config_lines)):
        if key + "=" in config_lines[i].replace(" ", "").split("#")[0]:
            key_index = i
            break
        elif i == len(config_lines) - 1:
            config_lines.append("")
            key_index = i + 1
            break
    config_lines[key_index] = key + " = '" + value + "'\n"
    with open(config_file, "w") as f:
        f.write("".join(config_lines))



def choose_config_value(
    user_config_file: str,
    key: str,
    default_value: str | None = None,
):
    """Have the user put user data path in user_config_file.

    Args:
        user_config_file (str): The config file in which the value will be set.
        key (str): the variable name to be set in config file
            a line "key = chosen_value" will be set in the config file.
        default_value: (str | None) = A default value. Defaults to None.
    """

    input_string = "Please provide the value for " + key + " in your config file.\n"
    if default_value is not None:
        input_string += (
            "Simply hit enter if you wish to use the default value below.\n"
            + default_value
        )

    chosen_value = input(input_string)
    if chosen_value == "":
        chosen_value = default_value
    if chosen_value is None:
        choose_config_value(user_config_file, key, default_value)
    else:
        set_value(user_config_file, key, chosen_value)


def key_is_set(config_file: str,key:str):
    """Check if key is set in config_file

    Args:
        config_file (str): full path to the config file
        key (str): variable name we are checking

    Returns:
        bool: Tue if a line key=value appears in the config file, False otherwise.
    """
    with open(config_file) as f:
        config_lines = f.readlines()
    for line in config_lines:
        if key + "=" in line.replace(" ", "").split("#")[0]:
            return True
    return False


def _create_directory(directory: str) -> None:
    """Create local directory if it does not exist.

    Args:
        directory (str): Desired absolute path to the directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def config_management(
    keys: list[str], reset=False, default_vals: None | list[str | None] = None
):
    """Ensure the setting/resetting of all keys in local config file.

    Args:
        keys (list[str]): variable names to set in config file.
        reset (bool, optional): If the values are to be reset
            even when already set. Defaults to False.
    """
    if default_vals is None:
        default_vals = [None] * len(keys)
    if len(keys) != len(default_vals):
        raise ValueError("default_vals and keys should have the same length.")

    user_config_dir = config_dir()
    user_config_file = config_file()

    # The following will allow to reach the data within the package directory
    package_dir = os.path.dirname(pkgutil.resolve_name(__name__).__file__)

    config_template = os.path.join(package_dir, "config_template.py")

    if not os.path.exists(user_config_file) or reset:
        _create_directory(user_config_dir)
        shutil.copyfile(config_template, user_config_file)

    for key, default in zip(keys, default_vals):
        if (not key_is_set(user_config_file,key)) or reset:
            choose_config_value(user_config_file, key, default)
