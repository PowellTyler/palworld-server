from time import sleep
import datetime
import subprocess
import requests
import os
import threading
from config import config
from log import log

_app_id = config['steamcmd']['app_id']
_verify_interval = int(config['app']['verify_interval'])
_save_interval = int(config['app']['save_interval'])
_steam_api_url = config['steamcmd']['api_url']
_storage_dir = config['app']['storage_dir']
_buildid_path = f'{_storage_dir}/buildid.info'
_rcon_label = config['rcon']['label']
_restart_in_progress = False


def _save():
    subprocess.run(['ARRCON', '-S', _rcon_label, 'save'])
    subprocess.run(['ARRCON', '-S', _rcon_label, 'broadcast Game_saved'])
    log.info('event=save_game event_details=rcon_command_sent')


def _restart_server():
    global _restart_in_progress
    if _restart_in_progress:
        return
    
    _restart_in_progress = True
    shutdown_time = int(config['app']['shutdown_time'])
    shutdown_time_seconds = shutdown_time * 60
    command = ['ARRCON', '-S', _rcon_label, f'shutdown {shutdown_time_seconds} Server_shutting_down_in_{shutdown_time}_minute(s)']
    subprocess.run(command)

    log.info('event=restart_server event_details=rcon_command_sent')

    delay = datetime.datetime.now() + datetime.timedelta(minutes=(shutdown_time - 1))
    complete_time = datetime.datetime.now() + datetime.timedelta(minutes=(shutdown_time + 1))

    while datetime.datetime.now() < delay:
        pass

    command = ['ARRCON', '-S', _rcon_label, 'broadcast Server_shutting_down_in_1_minute']
    subprocess.run(command)

    _save()

    while datetime.datetime.now() < complete_time:
        pass

    _restart_in_progress = False


def _update(build_id):
    update_command = f'{config["steamcmd"]["path"]} +login anonymous +app_update {_app_id} validate +quit'
    success_grep_command = 'grep Success!'
    update_process = subprocess.Popen(update_command.split(' '), stdout=subprocess.PIPE)
    grep_output = subprocess.check_output(success_grep_command.split(' '), stdin=update_process.stdout)
    update_process.wait()

    if grep_output != '':
        with open(_buildid_path, 'w') as f:
            f.write(build_id)
        return True
    else:
        # TODO: Log error
        return False


def _verify_needs_update():
    url = f'{_steam_api_url}info/{_app_id}'

    try:
        response = requests.get(url)
    except:
        log.error('event=verify_build_info event_result=failure event_details=unable_to_reach_host', exc_info=True)

    if not (200 <= response.status_code < 300):
        log.error(f'event=verify_build_info event_result=failure event_details=bad_response_code status_code={response.status_code}')
        return (False, '')
    
    data = response.json().get('data', {}).get(_app_id, {})
    build_id = data.get('depots', {}).get('branches', {}).get('public', {}).get('buildid')

    # We want to go ahead and try to update anyway if there are any issues
    # with reading the buildid file on the system
    if not os.path.exists(_buildid_path):
        log.info('event=verify_build_info event_result=success event_details=trigger_update_due_to_missing_buildinfo_file')
        return (True, build_id)

    try:
        with open(_buildid_path, 'r') as f:
            system_build_id = f.read()
    except Exception:
        log.error('event=verify_build_info event_result=failure event_details=unable_to_read_buildinfo_file', exc_info=True)
        return (False, build_id)
        
    trigger_update = build_id != system_build_id
    log.debug(f'event=verify_build_info event_result=success trigger_update={trigger_update} system_build_id={system_build_id} remote_build_id={build_id}')
    return (trigger_update, build_id)


def _validate_and_setup():
    if not os.path.exists(_storage_dir):
        os.makedirs(_storage_dir)

    assert os.path.exists(_storage_dir)

    output = subprocess.check_output(['ARRCON', '-l']).decode('utf-8')

    if _rcon_label not in output:
        ip = config['rcon']['ip']
        port = config['rcon']['port']
        password = config['rcon']['password']
        subprocess.run(['ARRCON', '-H', ip, '-P', port, '-p', password, '--save-host', _rcon_label])

    output = subprocess.check_output(['ARRCON', '-l']).decode('utf-8')
    assert _rcon_label in output


def _update_task():
    """
        The daemon task for checking if the server needs to be updated,
        saves and automatically restarts the Pal World server if
        an update is detected
    """
    log.info('event=update_task event_details=started_task')
    global _restart_in_progress
    next_verify_datetime = datetime.datetime.now()
    while True:
        if datetime.datetime.now() >= next_verify_datetime:
            needs_update, build_id = _verify_needs_update()
            if needs_update:
                updated = _update(build_id)
                if updated:
                    threading.Thread(target=_restart_server).start()
            next_verify_datetime = datetime.datetime.now() + datetime.timedelta(minutes=_verify_interval)
            log.debug(f'event=update_task event_details=scheduled_next_verify_time next_verify_datetime={next_verify_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
        sleep(10)


def _save_task():
    log.info('event=save_task event_details=started_task')
    next_save_datetime = datetime.datetime.now() + datetime.timedelta(minutes=_save_interval)

    while True:
        if datetime.datetime.now() >= next_save_datetime:
            next_save_datetime = datetime.datetime.now() + datetime.timedelta(minutes=_save_interval)
            _save()
            log.info(f'event=save_task event_details=scheduled_next_game_save next_save_datetime={next_save_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
        sleep(10)


def _restart_task():
    log.info('event=restart_task event_details=started_task')
    today = datetime.datetime.today()
    restart_hour = int(config['app']['restart_time'])
    next_restart = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=restart_hour, minute=0, second=0)
    next_restart += datetime.timedelta(hours=24)
    log.info(f'event=restart_task event_details=scheduled_next_server_restart next_restart={next_restart.strftime("%Y-%m-%d %H:%M:%S")}')

    while True:
        if datetime.datetime.now() >= next_restart:
            _restart_server()
            next_restart += datetime.timedelta(hours=24)
            log.info(f'event=restart_task event_details=scheduled_next_server_restart next_restart={next_restart.strftime("%Y-%m-%d %H:%M:%S")}')
        sleep(10)


def start():
    _validate_and_setup()
    log.info('event=startup event_details=system_validated_successfully')
    threading.Thread(target=_update_task, daemon=True).start()
    threading.Thread(target=_save_task, daemon=True).start()
    threading.Thread(target=_restart_task(), daemon=True).start()

    while True:
        sleep(10)
