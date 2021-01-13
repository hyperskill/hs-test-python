import subprocess
import sys
from threading import Thread
from time import sleep


class PopenWrapper:
    def check_stdout(self):
        while self.alive:
            sleep(0.01)
            new_stdout = self.process.stdout.read(1)
            sys.stdout.write(new_stdout)
            self.stdout += new_stdout
            if self.process.returncode is not None:
                self.alive = False

    def check_stderr(self):
        while self.alive:
            sleep(0.01)
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
            stderr=subprocess.PIPE
        )

        self.stdout = ''
        self.stderr = ''
        self.alive = True

        Thread(target=lambda: self.check_stdout(), daemon=True).start()
        Thread(target=lambda: self.check_stderr(), daemon=True).start()

    def terminate(self):
        self.alive = False
        self.process.terminate()

    def is_error_happened(self) -> bool:
        return self.process.returncode is not None and len(self.stderr) > 0
