from singleton import Singleton
from config import config
import subprocess
from log import log


class RCON(metaclass=Singleton):

    def __init__(self):
        self._label = config['rcon']['label']
        output = subprocess.check_output(['ARRCON', '-l']).decode('utf-8')

        if config['rcon']['label'] not in output:
            ip = config['rcon']['ip']
            port = config['rcon']['port']
            password = config['rcon']['password']
            subprocess.run(['ARRCON', '-H', ip, '-P', port, '-p', password, '--save-host', config['rcon']['label']])

    def _run(self, command, *args):
        # TODO: Handle errors from running RCON command
        command_params = ' '.join(args)
        rcon_command = f'\"{command} {command_params}\"'
        full_command = ['ARRCON', '-S', self._label, rcon_command]
        process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        return out

    def save(self):
        self._run('save')

    def broadcast(self, message='HELLO_WORLD'):
        self._run('broadcast', message)
        log.info(f'event=rcon_broadcast event_details=message_broadcasted message={message}')
        
    def kick_player(self, uuid):
        self._run('kickplayer', uuid)
        log.info(f'event=rcon_kick_player event_details=player_kicked player_uuid={uuid}')

    def ban_player(self, uuid):
        self._run('banplayer', uuid)
        log.info(f'event=rcon_ban_player event_details=player_banned player_uuid={uuid}')

    def show_players(self):
        return self._run('showplayers')

    def get_server_info(self):
        return self._run('info')

    def shutdown_server(self, seconds=60, message=None):
        broadcast_message = message
        if broadcast_message is None:
            broadcast_message = f'SERVER_SHUTTING_DOWN_IN_{seconds}_SECONDS'
        self._run('shutdown', seconds, message)
        log.info(f'event=rcon_shutdown_server event_details=server_going_down shutdown_time={seconds} message={broadcast_message}')
