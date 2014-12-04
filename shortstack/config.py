"""
Functions for retrieving configuration files

Most useful would be the 'configuration' function, which takes the name
of the configration, the directory it should be found in, and whether
or not it is considered optional.
"""

import os.path
import json


class ConfigMissing(Exception):
    """Thrown when a required configuration file is not found."""
    pass


def configuration_path(config_name, config_directory='_settings'):
    """
    Generate the path for a configuration file with config_name
    in config_directory.

    >>> configuration_path('foo')
    '_settings/foo.json'
    """
    return os.path.join(config_directory, config_name + '.json')


def configuration(config_name, config_directory=None, optional=False):
    """
    retrive a named configuration file, parsed as JSON into a dictionary
    """
    config_path = configuration_path(config_name, config_directory)
    if os.path.isfile(config_path):
        with open(config_path) as config_file:
            return json.load(config_file)
    elif optional:
        return {}

    raise ConfigMissing("No configuration %s.json in %s" % (config_name,
                                                            config_directory))
