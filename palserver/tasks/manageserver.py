from time import sleep
from tasks.task import Task
from tasks.backupserver import BackupServerTask
from tasks.checkversion import CheckVersionTask
from tasks.saveserver import SaveServerTask
from tasks.restartserver import RestartServerTask


class ManageServerTask(Task):

    def __init__(self, server):
        super().__init__()
        self._server = server

    def handler(self):
        self._server.start_server()

        BackupServerTask().start()
        CheckVersionTask(server=self._server).start()
        SaveServerTask().start()
        RestartServerTask(server=self._server).start()

        self._server.keep_alive()