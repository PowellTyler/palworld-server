import os
import configparser

__all__ = ['config']

config = configparser.ConfigParser()
config.read('/etc/palserver/config.ini')
