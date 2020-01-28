import os
import builtins
import signal
from hstest.exceptions import ExitException


class ExitHandler:
    _builtins_quit = builtins.quit
    _builtins_exit = builtins.exit
    _os_kill = os.kill
    _os__exit = os._exit
    _os_killpg = os.killpg
    _signal_pthread_kill = signal.pthread_kill
    _signal_siginterrupt = signal.siginterrupt

    _exit_func = lambda *x, **y: ExitException.throw()

    @staticmethod
    def replace_exit():
        builtins.quit = ExitHandler._exit_func
        builtins.exit = ExitHandler._exit_func
        os.kill = ExitHandler._exit_func
        os._exit = ExitHandler._exit_func
        os.killpg = ExitHandler._exit_func
        signal.pthread_kill = ExitHandler._exit_func
        signal.siginterrupt = ExitHandler._exit_func

    @staticmethod
    def revert_exit():
        builtins.quit = ExitHandler._builtins_quit
        builtins.exit = ExitHandler._builtins_exit
        os.kill = ExitHandler._os_kill
        os._exit = ExitHandler._os__exit
        os.killpg = ExitHandler._os_killpg
        signal.pthread_kill = ExitHandler._signal_pthread_kill
        signal.siginterrupt = ExitHandler._signal_siginterrupt
