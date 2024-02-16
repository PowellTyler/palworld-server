import logging
from systemd.journal import JournalHandler
from config import config


_log_levels = {
        'INFO': logging.INFO,
        'WARN': logging.WARN,
        'DEBUG': logging.DEBUG,
        'ERROR': logging.ERROR
    }

log = logging.getLogger(config['logging']['service'])
log.addHandler(JournalHandler())
log.setLevel(_log_levels.get(config['logging']['level'], logging.INFO))
