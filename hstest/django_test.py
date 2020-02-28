import os
import signal
import subprocess
from time import sleep
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
from hstest.stage_test import StageTest
from hstest.check_result import CheckResult


class DjangoTest(StageTest):

    _kill = os.kill
    port = '0'
    tryout_ports = ['8000', '8001', '8002', '8003', '8004']
    process = None

    def run(self):
        if self.process is None:
            self.__find_free_port()
            self.process = subprocess.Popen([
                self.file_to_test,
                'runserver', self.port, '--noreload',
            ])

    def check_server(self):
        if self.port == '0':
            return CheckResult.wrong(
                f'Please free one of the ports: {", ".join(self.tryout_ports)}'
            )

        for _ in range(15):
            try:
                urlopen(f'http://localhost:{self.port}/not-existing-link-by-default')
                return CheckResult.correct()
            except URLError as err:
                if isinstance(err, HTTPError):
                    return CheckResult.correct()
                sleep(1)
        else:
            return CheckResult.wrong(
                'Cannot start the ./manage.py runserver for 15 seconds'
            )

    def __find_free_port(self):
        for port in self.tryout_ports:
            try:
                urlopen(f'http://localhost:{port}')
            except URLError as err:
                if isinstance(err.reason, ConnectionRefusedError):
                    self.port = port
                    break

    def after_all_tests(self):
        if self.process is not None:
            try:
                self._kill(self.process.pid, signal.SIGINT)
            except ProcessLookupError:
                pass
