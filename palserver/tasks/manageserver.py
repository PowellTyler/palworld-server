from tasks.task import Task

class ManageServerTask(Task):

    def __init__(self, server):
        super().__init__()
        self._server = server

    def handler(self):
        self._server.start_server()