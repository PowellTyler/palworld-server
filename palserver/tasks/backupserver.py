import os
import datetime
import subprocess
from time import sleep

from log import log
from config import config
from tasks.task import Task


class BackupServerTask(Task):

    def handler(self):
        if config['app']['auto_backup'] <= 0:
            log.info('event=backup_server_task event_result=will_not_start event_details=config_not_set')
            return

        log.info('event=backup_server_task event_details=started')

        next_check = datetime.datetime.now() + datetime.timedelta(hours=config['app']['auto_backup'])

        while True:
            if datetime.datetime.now() >= next_check:
                log.info('event=backup_server_task event_details=about_to_perform')
                self._perform_backup()
                self._clean_backup_directory()
                next_check = datetime.datetime.now() + datetime.timedelta(hours=config['app']['auto_backup'])
            sleep(10)

    def _clean_backup_directory(self):
        backup_dir = config['app']['backup_dir']
        filenames = [entry.name for entry in sorted(os.scandir(backup_dir), key=lambda x: x.stat().st_mtime, reversed=True)]

        for name in filenames:
            os.remove(os.path.join(config['app']['backup_dir'], name))

    def _perform_backup(self):
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        app_id = config['steamcmd']['app_id']
        backup_path = os.path.join(config['app']['backup_dir'], f'steam-app-{app_id}_{now}.tar.gz')
        backup_directories = ' '.join([
            os.path.join(config['root'], 'server'),
            os.path.join(config['root'], 'storage'),
            os.path.join(config['root'], 'config')
        ])

        # TODO: Handle errors
        command = f'tar -czf {backup_path} {backup_directories}'
        run_server = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = run_server.communicate()

        log.info(f'event=perform_backup event_result=success backup="{backup_path}"')