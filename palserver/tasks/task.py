from time import sleep
from log import log
import threading


class Task:

    def __init__(self):
        self._task = None

    @property
    def is_running(self):
        return self._task is not None and self._task.is_alive()

    def handler(self):
        pass

    def start(self):
        if self.is_running:
            log.warn(f'event=start_task task="{self.__class__.__name__}" event_result=failure event_details=task_is_still_running')
            return

        self._task = threading.Thread(target=self.handler, daemon=True)
        self._task.start()


def start_main_loop():
    while True:
        sleep(10)
