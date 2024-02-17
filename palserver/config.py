import os
import configparser

__all__ = ['config']

# TODO: This could be generalized so that config.ini is a set of instructions on
#       what a config is suppose to be
#       Examples:
#           a = string(default='some-default-value')
#           b = integer(default=2, min=1, max=999)
#           c = boolean(default=False)
#           d = string_list(default=[])
config = configparser.ConfigParser()
config.read('/var/lib/palserver/config/config.ini')
config['env'] = {
    'root': '/var/lib/palserver',
    'module': os.path.dirname(os.path.abspath(__file__))
}
config['app']['auto_update'] = config['auto_update'].lower() == 'false'
