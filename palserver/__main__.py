from tasks.manageserver import ManageServerTask
from tasks.task import start_main_loop
from server import Server


ManageServerTask(server=Server()).start()
start_main_loop()
