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


_module_path = os.path.dirname(os.path.abspath(__file__))

_base_config = configparser.ConfigParser()
_base_config.read(os.path.join(_module_path, 'config.ini'))

_config = configparser.ConfigParser()
_config.read('/var/lib/palserver/config/config.cfg')

config = _convert_to_dict(_base_config)
config.update(_convert_to_dict(_config))

# TODO: This could be generalized so that config.ini is a set of instructions on
#       what a config is suppose to be
#       Examples:
#           a = string(default='some-default-value')
#           b = integer(default=2, min=1, max=999)
#           c = boolean(default=False)
#           d = string_list(default=[])

# TODO: Retrieve root from environment variable?
config['root'] = '/var/lib/palserver'
config['module'] = _module_path
config['steamcmd']['retry_count'] = int(config['steamcmd']['retry_count'])
config['steamcmd']['retry_interval'] = int(config['steamcmd']['retry_interval'])
config['app']['auto_update'] = int(config['app']['auto_update'])
config['app']['auto_restart'] = int(config['app']['auto_restart'])
config['app']['auto_save'] = int(config['app']['auto_save'])
config['app']['auto_backup'] = int(config['app']['auto_backup'])
