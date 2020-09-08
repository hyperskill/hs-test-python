import os
import shutil
import signal
import subprocess
import sys
from time import sleep
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
from hstest.stage_test import StageTest
from hstest.check_result import CheckResult
from hstest.exceptions import UnexpectedError

EMPTY_DATABASE = 'empty.sqlite3'
TEST_DATABASE = 'db.test.sqlite3'


class DjangoTest(StageTest):
    _kill = os.kill
    port = '0'
    tryout_ports = ['8000', '8001', '8002', '8003', '8004']
    process = None

    def run(self):
        if self.process is None:
            self.__find_free_port()
            self.__prepare_database()
            self.process = subprocess.Popen([
                sys.executable, self.path_to_test,
                'runserver', self.port, '--noreload',
            ])

    def __prepare_database(self):
        if os.path.exists(EMPTY_DATABASE):
            shutil.copyfile(EMPTY_DATABASE, TEST_DATABASE)
            os.environ['HYPERSKILL_TEST_DATABASE'] = TEST_DATABASE
            migrate = subprocess.Popen(
                [sys.executable, self.path_to_test, 'migrate'],
                stderr=subprocess.PIPE
            )
            exit_code = migrate.wait()
            if exit_code != 0:
                raise UnexpectedError(migrate.stderr.read().decode())

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
                "Django server hasn't started within 15 seconds time limit"
            )

    def __find_free_port(self):
        for port in self.tryout_ports:
            try:
                urlopen(f'http://localhost:{port}')
            except URLError as err:
                if isinstance(err.reason, ConnectionRefusedError):
                    self.port = port
                    break
            except ConnectionResetError:
                pass

    def read_page(self, link: str) -> str:
        return urlopen(link).read().decode().replace('\u00a0', ' ')

    def after_all_tests(self):
        if self.process is not None:
            try:
                self._kill(self.process.pid, signal.SIGINT)
            except ProcessLookupError:
                pass
