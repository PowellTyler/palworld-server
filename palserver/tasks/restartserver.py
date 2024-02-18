import datetime
from time import sleep
from log import log
from config import config
from rcon import RCON
from tasks.task import Task


class RestartServerTask(Task):

    def __init__(self, server):
        super().__init__()
        self._server = server

    def handler(self):
        if config['app']['auto_restart'] <= 0:
            log.info('event=restart_server_task event_result=will_not_start event_details=config_not_set')
            return

        log.info('event=restart_server_task event_details=started')

        next_check = datetime.datetime.now() + datetime.timedelta(hours=config['app']['auto_restart'])

        while True:
            if datetime.datetime.now() >= next_check:
                log.debug('event=restart_server_task event_details=about_to_perform')
                self._server.restart_server()
                next_check = datetime.datetime.now() + datetime.timedelta(hours=config['app']['auto_restart'])
                log.info('event=restart_server_task event_result=success event_details=signal_sent')
            sleep(10)