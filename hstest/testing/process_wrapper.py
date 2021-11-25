import subprocess
import sys
from threading import Lock, Thread
from time import sleep
from typing import Optional

from psutil import NoSuchProcess, Process

from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.dynamic.security.exit_handler import ExitHandler
from hstest.dynamic.security.thread_group import ThreadGroup
from hstest.dynamic.system_handler import SystemHandler
from hstest.exception.outcomes import UnexpectedError


class ProcessWrapper:
    def __init__(self, *args, check_early_finish=False, register_output=True, register_io_handler=False):
        self.lock = Lock()

        self.args = args

        self.process: Optional[subprocess.Popen] = None
        self.ps: Optional[Process] = None

        self.stdout = ''
        self.stderr = ''
        self._alive = True
        self._pipes_watching = 0
        self.terminated = False

        self.cpu_load_history = []
        self.cpu_load_history_max = 2

        self.output_diff_history = []
        self.output_diff_history_max = 2

        self.initial_idle_wait = True
        self.initial_idle_wait_max = 10

        self.check_early_finish = check_early_finish
        self.register_output = register_output
        self.register_io_handler = register_io_handler
        self._group = None

    def start(self):
        command = ' '.join(map(str, self.args))

        if self.process is not None:
            raise UnexpectedError(f"Cannot start the same process twice\n\"{command}\"")

        try:
            self.process = subprocess.Popen(
                [str(a) for a in self.args],
                bufsize=0,
                universal_newlines=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                encoding='utf-8',
            )
        except Exception as e:
            from hstest import StageTest
            StageTest.curr_test_run.set_error_in_test(
                UnexpectedError(f"Cannot start process\n\"{command}\"", e))
            self._alive = False
            self.terminated = True
            return self

        self.ps = Process(self.process.pid)

        if self.register_io_handler:
            self._group = ThreadGroup()
            SystemHandler.install_handler(
                self,
                lambda: ThreadGroup.curr_group() == self._group,
                lambda: None
            )

        Thread(target=lambda: self.check_cpuload(), daemon=True, group=self._group).start()
        Thread(target=lambda: self.check_output(), daemon=True, group=self._group).start()
        Thread(target=lambda: self.check_stdout(), daemon=True, group=self._group).start()
        Thread(target=lambda: self.check_stderr(), daemon=True, group=self._group).start()

        return self

    def check_alive(self):
        if self._alive and self.process.returncode is not None:
            self._alive = False

    def check_pipe(self, read_pipe, write_pipe, write_stdout=False, write_stderr=False):
        pipe_name = "stdout" if write_stdout else "stderr"

        with self.lock:
            self._pipes_watching += 1

        OutputHandler.print(f'Start watching {pipe_name} '
                            f'Pipes watching = {self._pipes_watching}')

        while True:
            try:
                new_output = read_pipe.read(1)
            except ValueError:
                OutputHandler.print(f'Value error for {pipe_name}... ')
                if self.is_finished(need_wait_output=False):
                    break
                continue

            if write_stderr:
                OutputHandler.print(f'STDERR + {len(new_output)} symbols: {new_output}')

            if len(new_output) == 0:
                with self.lock:
                    self._pipes_watching -= 1

                OutputHandler.print(f'Out of {pipe_name}... '
                                    f'Maybe program terminated. Pipes watching = {self._pipes_watching}')

                if self._pipes_watching == 0:
                    OutputHandler.print(
                        f'Set alive = False for {pipe_name}... ')
                    self._alive = False
                    self.terminate()

                break

            try:
                if self.register_output:
                    write_pipe.write(new_output)
            except ExitException:
                OutputHandler.print(f'ExitException for {pipe_name}... ')
                self._alive = False
                self.terminate()
                break

            if write_stdout:
                self.stdout += new_output

            if write_stderr:
                self.stderr += new_output

    def check_stdout(self):
        self.check_pipe(self.process.stdout, sys.stdout, write_stdout=True)

    def check_stderr(self):
        self.check_pipe(self.process.stderr, sys.stderr, write_stderr=True)

    def check_cpuload(self):
        while self._alive:
            try:
                cpu_load = self.ps.cpu_percent()
                OutputHandler.print(f'Check cpuload - {cpu_load}')
                self.cpu_load_history.append(cpu_load)

                if self.initial_idle_wait and cpu_load > 1:
                    self.initial_idle_wait = False

                if self.initial_idle_wait and len(self.cpu_load_history) > self.initial_idle_wait_max:
                    self.initial_idle_wait = False

                if not self.initial_idle_wait and len(self.cpu_load_history) > self.cpu_load_history_max:
                    self.cpu_load_history.pop(0)

            except NoSuchProcess:
                OutputHandler.print('Check cpuload finished, waiting output')
                self.wait_output()
                OutputHandler.print('Check cpuload finished, set alive = false')
                self._alive = False
                break
            sleep(0.01)
            self.check_alive()

    def check_output(self):
        output_len_prev = len(self.stdout)

        while self._alive:
            output_len = len(self.stdout)
            diff = output_len - output_len_prev
            output_len_prev = output_len

            OutputHandler.print(f'Check output diff - {diff}. Curr = {output_len}, prev = {output_len_prev}')
            self.output_diff_history.append(diff)
            if len(self.output_diff_history) > self.output_diff_history_max:
                self.output_diff_history.pop(0)

            if self.initial_idle_wait and diff > 0:
                self.initial_idle_wait = False

            sleep(0.01)
            self.check_alive()

    def is_waiting_input(self) -> bool:
        if self.initial_idle_wait:
            return False

        program_not_loading_processor = (
            len(self.cpu_load_history) >= self.cpu_load_history_max
            and sum(self.cpu_load_history) < 1
        )

        program_not_printing_anything = (
            len(self.output_diff_history) >= self.output_diff_history_max
            and sum(self.output_diff_history) == 0
        )

        return program_not_loading_processor and program_not_printing_anything

    def register_input_request(self):
        if not self.is_waiting_input():
            raise RuntimeError('Program is not waiting for the input')
        self.cpu_load_history = []
        self.output_diff_history = []

    def is_finished(self, need_wait_output=True):
        if not self.check_early_finish:
            return not self._alive

        if not self._alive:
            return True

        try:
            is_running = self.ps.status() == 'running'
            if not is_running:
                self._alive = False
        except NoSuchProcess:
            self._alive = False

        if not self._alive and need_wait_output:
            OutputHandler.print('"is_finished" detected the process is dead, wait output')
            self.wait_output()
            OutputHandler.print('"is_finished" after waiting output, return True')

        return not self._alive

    def provide_input(self, stdin: str):
        self.process.stdin.write(stdin)

    def terminate(self):
        OutputHandler.print('Terminate called')

        with self.lock:
            if self.register_io_handler:
                SystemHandler.uninstall_handler(self)

            OutputHandler.print('Terminate - LOCK ACQUIRED')

            if self.terminated:
                OutputHandler.print(f'Terminate - finished')
                return

            OutputHandler.print('Terminate - BEFORE WAIT STDERR')

            self.wait_output()

            OutputHandler.print('Terminate - AFTER WAIT STDERR')

            self._alive = False

            OutputHandler.print('Terminate - SELF ALIVE == FALSE')

            is_exit_replaced = ExitHandler.is_replaced()
            if is_exit_replaced:
                ExitHandler.revert_exit()
                OutputHandler.print('Terminate - EXIT REVERTED')

            try:
                parent = Process(self.process.pid)
                OutputHandler.print(f'Terminate - parent == {parent}')
                for child in parent.children(recursive=True):
                    OutputHandler.print(f'Terminate - child kill {child}')
                    child.kill()
                OutputHandler.print(f'Terminate - parent kill {parent}')
                parent.kill()
            except NoSuchProcess:
                OutputHandler.print(f'Terminate - NO SUCH PROCESS')
                pass
            finally:
                OutputHandler.print(f'Terminate - finally before kill')
                self.process.kill()
                OutputHandler.print(f'Terminate - finally before wait')
                self.process.wait()

                self.process.stdout.close()
                self.process.stderr.close()
                self.process.stdin.close()

                if is_exit_replaced:
                    ExitHandler.replace_exit()
                    OutputHandler.print(f'Terminate - EXIT REPLACED AGAIN')

            self.terminated = True
            OutputHandler.print(f'Terminate - TERMINATED')
        OutputHandler.print(f'Terminate - finished')

    def wait_output(self):
        iterations = 50
        sleep_time = 50 / 1000

        curr_stdout = self.stdout
        curr_stderr = self.stderr
        while iterations != 0:
            sleep(sleep_time)
            if self.stderr == curr_stderr and self.stdout == curr_stdout:
                break
            curr_stderr = self.stderr
            curr_stdout = self.stdout
            iterations -= 1

    def wait(self):
        while not self.is_finished():
            sleep(0.01)
        self.wait_output()

    def is_error_happened(self) -> bool:
        return (
            not self._alive and len(self.stderr) > 0 and self.process.returncode != 0
            or 'Traceback' in self.stderr
        )
