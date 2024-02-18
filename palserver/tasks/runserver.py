import subprocess
from log import log
from tasks.task import Task
from config import config


class RunServerTask(Task):

    def handler(self):
        # TODO: It may be good to save the PID in a common file that we can
        #       look at to make sure a server instance isn't already running.
        run_server_path = f'{config["server"]["game_root"]}/{config["server"]["command_path"]}'
        command = f'su - steam -c "{run_server_path} -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS"'
        log.info(f'event=run_server_task event_details=about_to_start command={command}')
        run_server = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = run_server.communicate()
        log.info(f'event=run_server_task event_details=exited stdout={out} stderr={err}')
