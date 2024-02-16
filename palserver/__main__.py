from time import sleep
from tasks.task import Task
from server import Server


class ServerManager(Task):

    def handler(self):
        server = Server()
        server.start_server()

        while True:
            sleep(10)

server_manager = ServerManager()
server_manager.start()
