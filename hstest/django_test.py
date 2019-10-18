import os
import signal
import subprocess
from hstest.stage_test import StageTest


class DjangoTest(StageTest):

    _kill = os.kill
    process = None

    def run(self):
        if self.process is None:
            self.process = subprocess.Popen([self.file_to_test, 'runserver'])

    def after_all_tests(self):
        if self.process is not None:
            self._kill(self.process.pid, signal.SIGINT)
