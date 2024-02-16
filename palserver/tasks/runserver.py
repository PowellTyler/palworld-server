import subprocess
from tasks.task import Task
from config import config


class RunServerTask(Task):

    def handler(self):
        command = f'{config["server"]["game_root"]}/{config["server"]["command_path"]}'
        subprocess.run([command, '-useperfthreads', '-NoAsyncLoadingThread', '-UseMultithreadForDS'])
