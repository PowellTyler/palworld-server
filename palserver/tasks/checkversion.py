import datetime
from time import sleep
from log import log
from config import config
from tasks.task import Task


class CheckVersionTask(Task):

    def __init__(self, server):
        super().__init__()
        self._server = server

    def handler(self):
        if config['app']['auto_update'] <= 0:
            log.info('event=check_version_task event_result=will_not_start event_details=config_not_set')
            return

        log.info('event=check_version_task event_details=started')

        next_check = datetime.datetime.now() + datetime.timedelta(minutes=config['app']['auto_update'])

        while True:
            if datetime.datetime.now() >= next_check:
                log.debug('event=check_version_task event_details=about_to_perform')
                latest_build_version = self._server.get_latest_build_version()

                if latest_build_version is None:
                    log.warn('event=check_version_task event_result=failure event_details=unable_to_retrieve_latest_build_version')

                elif str(latest_build_version) != str(self._server.build_version):
                    log.info(f'event=check_version_task event_details=server_is_outdated old_version={self._server.build_version} new_version={latest_build_version}')
                    self._server.install_or_update_server()
                    self._server.restart_server()
                    next_check = datetime.datetime.now() + datetime.timedelta(minutes=config['app']['auto_update'])
                else:
                    log.info('event=check_version_task event_details=server_up_to_date')
            sleep(10)

        