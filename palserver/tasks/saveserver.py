import datetime
from time import sleep
from log import log
from config import config
from rcon import RCON
from tasks.task import Task


class SaveServerTask(Task):

    def handler(self):
        if config['app']['auto_save'] <= 0:
            log.info('event=save_task event_result=will_not_start event_details=config_not_set')
            return

        log.info('event=save_task event_details=started')

        next_check = datetime.datetime.now() + datetime.timedelta(minutes=config['app']['auto_save'])

        while True:
            if datetime.datetime.now() >= next_check:
                RCON().save()
                next_check = datetime.datetime.now() + datetime.timedelta(minutes=config['app']['auto_save'])
                log.info('event=save_task event_result=success event_details=signal_sent')
            sleep(10)