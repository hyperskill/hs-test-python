import subprocess
import sys
from threading import Thread
from time import sleep

from psutil import NoSuchProcess, Process

from hstest.dynamic.security.exit_handler import ExitHandler


class PopenWrapper:
    def check_stdout(self):
        while self.alive:
            new_stdout = self.process.stdout.read(1)
            sys.stdout.write(new_stdout)
            self.stdout += new_stdout
            if self.process.returncode is not None:
                self.alive = False

    def check_stderr(self):
        while self.alive:
            new_stderr = self.process.stderr.read(1)
            sys.stderr.write(new_stderr)
            self.stderr += new_stderr
            if self.process.returncode is not None:
                self.alive = False

    def __init__(self, *args):
        self.process = subprocess.Popen(
            [str(a) for a in args],
            bufsize=0,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8'
        )

        self.stdout = ''
        self.stderr = ''
        self.alive = True

        Thread(target=lambda: self.check_stdout(), daemon=True).start()
        Thread(target=lambda: self.check_stderr(), daemon=True).start()

    def wait_stderr(self):
        iterations = 50
        sleep_time = 50 / 1000

        curr_stderr = self.stderr
        while iterations != 0:
            sleep(sleep_time)
            if self.stderr == curr_stderr:
                break
            curr_stderr = self.stderr
            iterations -= 1

    def terminate(self):
        self.wait_stderr()

        self.alive = False
        is_exit_replaced = ExitHandler.is_replaced()
        if is_exit_replaced:
            ExitHandler.revert_exit()
        try:
            parent = Process(self.process.pid)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
        except NoSuchProcess:
            pass
        finally:
            if is_exit_replaced:
                ExitHandler.replace_exit()

    def is_error_happened(self) -> bool:
        return (
            self.process.returncode is not None and len(self.stderr) > 0
            or 'Traceback' in self.stderr
        )
