import subprocess
from log import log
from tasks.task import Task
from config import config


class RunServerTask(Task):

    def handler(self):
        log.info('event=run_server_task event_details=about_to_start')
        command = f'{config["server"]["game_root"]}/{config["server"]["command_path"]} -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS'
        run_server = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        out, err = run_server.communicate()
        log.info(f'event=run_server_task event_details=exited stdout={out} stderr={err}')
