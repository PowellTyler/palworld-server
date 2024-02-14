import os
import configparser

__all__ = ['config']

_dir = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(f'{_dir}/config/config.ini')
