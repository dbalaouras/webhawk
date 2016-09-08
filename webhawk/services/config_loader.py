import os

from lib import common

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2016, Stek.io"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))


class ConfigLoader(object):
    """
    WebHawk Configuration Abstraction
    """

    def __init__(self, cli_options=None):
        """
        Class Initializer

        :param cli_options: (optional) Command line options
        """

        # Initialize instance variables
        self._cli_options = cli_options
        self._config_cache = {}
        self._file_config = None

        # We always load the default yaml file
        config_file_csv = "%s/../../config/config.yaml" % __abs_dirpath__

        # Override config if an additional config file is supplied
        config_file = self._get_configuration("config_file")
        if config_file:
            config_file_csv += ",%s" % config_file

        # Load config from file
        self._file_config = self._sanitize_config(common.load_config(config_file_csv))

    def _sanitize_config(self, config):
        """
        Validates a configuration dictionary
        :param config:
        :return:
        """
        # Ensure we have a path starting with a slash
        if not config["base_path"] or config["base_path"][:1] != "/":
            config["base_path"] = "/%s" % config["base_path"]

        return config

    def _get_configuration(self, name):
        """
        Get configuration from: command line options, OR environment OR config file

        :param name:
        :return: The configuration value if found; None otherwise
        """

        # Initialize return value
        value = None

        if not self._config_cache.get(name, None):

            # Try cli options first
            if value is None and self._cli_options:
                value = getattr(self._cli_options, name, None)

            # Try environment next
            if value is None:
                value = os.environ.get("WEBHAWK_%s" % name.upper(), None)

            # Finally, try existing config
            if value is None and self._file_config:
                value = self._file_config.get(name, None)

            # Store value in local cache
            self._config_cache[name] = value

        else:
            value = self._config_cache[name]

        return value

    def __getitem__(self, name):
        """
        Load a configuration by name
        :param name: The name of the configuration
        :return: The
        """
        return self._get_configuration(name=name)
