import json
import logging
import logging.config
import os

import yaml

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Dimi Balaouras - Stek.io"
__license__ = "Apache License 2.0, see LICENSE for more details."


def load_config(config_files_csv):
    """
    Loads configuration from multiple files provided via a comma separated set of files.
    The order of loading is preserved: the latter files will replace properties of earlier files.

    :param config_files_csv: A comma separated list of config files
    :return: A dictionary with the loaded configuration
    """
    # Initialize the config file
    config = {}

    # Get a list of files
    config_files = [config_file.strip() for config_file in config_files_csv.split(',')]

    # Update the config dictionary
    for config_file in config_files:
        add_config = load_config_file(config_file)
        if add_config:
            config = merge_dicts(config, add_config)
    return config


def load_config_file(config_file):
    """
    Loads a config file formatted either in yaml or json

    :param config_file: The path to the config file
    :return: The configuration dictionary
    """

    # Initialize the return object
    config = None

    # Extract the file extension
    filename, extension = os.path.splitext(config_file)

    # Pick the right deserializer
    try:

        if not os.path.isfile(config_file):
            raise IOError("%s is not a file." % config_file)

        deserializer = {
            ".yaml": yaml,
            ".json": json
        }[extension]

        # Deserialize the config
        config = deserializer.load(open(config_file))

    except KeyError:
        # TODO: use a logger her
        print("Invalid configuration file type: %s" % extension)

    return config


def get_logger(global_config, module_name, default_level=logging.DEBUG):
    """
    Retrieves a logger from the global config if one exists for the given module; otherwise, it creates one.
    :param global_config:
    :param module_name:
    :param default_level: The default logging level
    :return:
    """

    # Try using the config first
    if "python-logging" in global_config:

        logging.config.dictConfig(global_config["python-logging"])
        logger = logging.getLogger(module_name)
    else:

        # Create a custom logger
        logger = logging.getLogger(module_name)
        logger.setLevel(default_level)

        ch = logging.StreamHandler()
        ch.setLevel(default_level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add formatter to ch
        ch.setFormatter(formatter)

        # Add a logger
        logger.addHandler(ch)

    return logger


def merge_dicts(origin, patch):
    """
    Merge two dictionaries, w/o overwriting missing keys

    :param origin: The origin dictionary
    :param patch: The dictionary containing the diffs
    :return: The result of the merge: a new dictionary
    """

    for key in patch:
        if key in origin:
            if isinstance(origin[key], dict) and isinstance(patch[key], dict):
                merge_dicts(origin[key], patch[key])
            else:
                origin[key] = patch[key]
        else:
            origin[key] = patch[key]
    return origin


class Struct:
    """
    Class used as a convertor between objects and dictionaries
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)


def dict_to_object(dict):
    """
    Convert a dictionary to object
    :param dict: The dictionary to convert
    :return: the converted object
    """
    return Struct(**dict)


def print_logo():
    """
    Prints WebHawk's Logo in Ascii Art
    """

    logo = """
=====================================================
      _      __    __   __ __            __
     | | /| / /__ / /  / // /__ __    __/ /__
     | |/ |/ / -_) _ \/ _  / _ \`/ |/|/ /  '_/
     |__/|__/\__/_.__/_//_/\_,_/|__,__/_/\_\\

               WebHook MicroFramework
=====================================================
    """
    print(logo)
