import os.path
import json


class ConfigMissing(Exception):
    pass

def configuration_path(config_name, config_directory='_settings'):
    return os.path.join(config_directory, config_name + '.json')

def configuration(config_name, config_directory=None, optional=False):
    
    config_path = configuration_path(config_name, config_directory)
    if os.path.isfile(config_path):
        with open(config_path) as config_file:
            return json.load(config_file)
    elif optional:
        return {}

    raise ConfigMissing("No configuration %s.json in %s" % (config_name,
                config_directory))
