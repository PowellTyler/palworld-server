import os
import configparser

__all__ = ['config']


def _convert_to_dict(config):
    d = {}
    for section in config.sections():
        d[section] = {}
        for key, val in config.items(section):
            d[section][key] = val
    return d

# TODO: This could be generalized so that config.ini is a set of instructions on
#       what a config is suppose to be
#       Examples:
#           a = string(default='some-default-value')
#           b = integer(default=2, min=1, max=999)
#           c = boolean(default=False)
#           d = string_list(default=[])

_config = configparser.ConfigParser()
_config.read('/var/lib/palserver/config/config.ini')

config = _convert_to_dict(_config)
config['root'] = '/var/lib/palserver'
config['module'] = os.path.dirname(os.path.abspath(__file__))
config['app']['auto_update'] = config['app']['auto_update'].lower() == 'false'
