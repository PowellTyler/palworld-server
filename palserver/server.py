import os
import requests
import subprocess
import datetime
from time import sleep
from config import config
from log import log
from rcon import RCON
from tasks.runserver import RunServerTask


class Server():

    def __init__(self):
        self._app_id = config['steamcmd']['app_id']
        self._shutdown_in_progress = False
        self._storage_dir = config['app']['storage_dir']
        self._buildid_path = f'{self._storage_dir}/buildid.info'
        self._game_root = config['server']['game_root']
        self._server_task = RunServerTask()
        self._stopped = True
        self.shutdown_time = int(config['app']['shutdown_time'])
        self.build_version = self._get_build_version_from_file()

    @property
    def is_installed(self):
        return os.path.exists(f'{config["server"]["game_root"]}/{config["server"]["command_path"]}')

    def start_server(self):
        if self._server_task.is_running:
            log.warn('event=server_start event_result=failure event_details=server_already_running')
            return
        
        log.debug('event=start_server event_details=about_to_perform')

        if not self.is_installed:
            self.install_or_update_server()

            if not self.is_installed:
                log.error('event=server_start result=failure event_details=unable_to_install_server_app')
                raise OSError('Unable to download server app')

        self.apply_config()
        self._server_task.start()
        self._stopped = False
        log.info('event=start_server result=success')

    def stop_server(self, immediate=False):
        if not self._server_task.is_running:
            return

        log.debug('event=stop_server event_details=about_to_perform')
        if self._shutdown_in_progress:
            if immediate:
                raise Exception('Cannot stop server immediately as it is in the process of shutting down')
            while self._shutdown_in_progress:
                sleep(1)
            return

        if not immediate:
            self._shutdown_in_progress = True
            shutdown_time_seconds = self.shutdown_time * 60
            RCON.instance.shutdown_server(shutdown_time_seconds)
            shutdown_time_10_seconds_remain = datetime.datetime.now() + datetime.timedelta(seconds=(shutdown_time_seconds - 11))

            while datetime.datetime.now() < shutdown_time_10_seconds_remain:
                sleep(1)
                pass

            RCON.instance.save()

            for i in reversed(range(10)):
                RCON.broadcast(f'SERVER_SHUTTING_DOWN_IN_{i+1}_SECONDS')
                sleep(1)

        while self._server_task.is_running:
            sleep(1)

        log.info('event=server_shutdown event_result=success')
        self._shutdown_in_progress = False
        self._stopped = True

    def restart_server(self):
        log.debug('event=server_restart event_details=about_to_perform')
        self.stop_server()
        self.start_server()

    def install_or_update_server(self):
        log.info(f'event=server_install_or_update event_details=started game_root={self._game_root}')
        install_command = f'su - steam -c "{config["steamcmd"]["path"]} +force_install_dir \"{self._game_root}\" +login anonymous +app_update {self._app_id} validate +quit"'
        install_process = subprocess.Popen(install_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        out, err = install_process.communicate()

        if 'Success!' in out:
            self._update_build_version_file()

    def apply_config(self):
        log.debug('event=server_apply_config event_details=about_to_perform')
        settings_template_path = os.path.join(config['module'], 'templates', 'palworld-settings.ini.template')
        server_settings_path = os.path.join(config['server']['game_root'], config['server']['settings_path'])

        try:
            with open(settings_template_path, 'r') as template_file:
                with open(server_settings_path, 'w') as settings_file:
                    settings_file.write(template_file.read().format(**config['palworld']))
            log.info(f'event=server_apply_config event_result=success config_path={server_settings_path}')
        except Exception:
            log.error('event=server_apply_config event_result=error event_details=unknown_error_possible_missing_permissions', exc_info=True)

    def keep_alive(self):
        """
            Tries to keep the server alive, this is ignored
            if the server is called to be stopped
        """
        if self._stopped:
            return

        while True:
            if not self._server_task.is_running and not self._stopped:
                log.warn('event=server_keep_alive event_details=server_closed_unexpectingly')
                self.start_server()
            sleep(10)

    def _get_build_version_from_file(self):
        if not os.path.exists(self._buildid_path):
            return None
        
        log.debug('event=server_get_build_version_from_file event_details=about_to_perform')

        try:
            with open(self._buildid_path, 'r') as buildinfo_file:
                build_info = buildinfo_file.read()
            return build_info
        except Exception:
            log.error('event=server_get_build_version event_result=failure event_details=unable_to_read_buildinfo_file', exc_info=True)

        return None
    
    def _update_build_version_file(self):
        """
            Retrieves the published build version and writes to file
        """
        log.info('event=server_update_build_version event_details=about_to_perform')

        url = f'{config["steamcmd"]["api_url"]}info/{self._app_id}'

        try:
            response = requests.get(url)
        except Exception:
            log.error('event=server_update_build_version event_result=failure event_details=unable_to_reach_host', exc_info=True)

        if not (200 <= response.status_code < 300):
            log.error(f'event=server_update_build_version event_result=failure event_details=bad_response_code status_code={response.status_code}')
            return

        data = response.json().get('data', {}).get(self._app_id, {})
        build_id = data.get('depots', {}).get('branches', {}).get('public', {}).get('buildid')
        self.build_version = build_id

        if not os.path.exists(self._storage_dir):
            os.makedirs(self._storage_dir)

        with open(self._buildid_path, 'w') as buildinfo_file:
            buildinfo_file.write(self.build_version)
