from time import sleep
import threading


class Task:

    def __init__(self):
        self._task = threading.Thread(target=self.handler, daemon=True)

    @property
    def is_running(self):
        return self._task.is_alive()

    def handler(self):
        pass

    def start(self):
        self._task.start()


def start_main_loop():
    while True:
        sleep(10)
