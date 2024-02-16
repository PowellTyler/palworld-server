import datetime
import traceback
import sys
from config import config

INFO = 'INFO'
WARN = 'WARN'
DEBUG = 'DEBUG'
ERROR = 'ERROR'


class Logger:

    _level_value_map = {
            DEBUG: 0,
            INFO: 1,
            WARN: 2,
            ERROR: 3
        }
    
    _log_path = f'/var/log/{config["logging"]["service"]}/access.log'

    def __init__(self, service_name):
        self.service_name = service_name
        self.set_level(INFO)

    def _log(self, level, message, exc_info=False):
        with open(self._log_path, 'a') as log_file:
            log_file.write(f'{datetime.datetime.now().strftime("%b %d %H:%M%S")} {self.service_name} [{level}] {message}')
            if exc_info:
                log_file.write(f'{datetime.datetime.now().strftime("%b %d %H:%M%S")} {self.service_name} [{level}] {traceback.format_exc()}')

    def set_level(self, level):
        if level not in [INFO, WARN, DEBUG, ERROR]:
            raise ValueError(f'Level must be {INFO}, {WARN}, {DEBUG}, or {ERROR}')

        self._level = level

    def debug(self, message, exc_info=False):
        if self._level_map[self._level] > self._level_map[DEBUG]:
            return
        
        self._log(DEBUG, message, exc_info)

    def info(self, message, exc_info=False):
        if self._level_map[self._level] > self._level_map[INFO]:
            return
        
        self._log(INFO, message, exc_info)

    def warn(self, message, exc_info=False):
        if self._level_map[self._level] > self._level_map[WARN]:
            return
        
        self._log(WARN, message, exc_info)

    def error(self, message, exc_info=False):
        if self._level_map[self._level] > self._level_map[ERROR]:
            return
        
        self._log(ERROR, message, exc_info)

log = Logger(config['logging']['service'])
log.set_level(config['logging']['level'])
