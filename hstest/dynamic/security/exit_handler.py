import builtins
import os
import signal
import sys

from hstest.dynamic.security.exit_exception import ExitException


class ExitHandler:
    _saved = False
    _replaced = False

    _builtins_quit = None
    _builtins_exit = None
    _os_kill = None
    _os__exit = None
    _sys_exit = None
    _os_killpg = None
    _signal_pthread_kill = None
    _signal_siginterrupt = None

    _exit_func = lambda *x, **y: ExitException.throw()

    @staticmethod
    def is_replaced():
        return ExitHandler._replaced

    @staticmethod
    def replace_exit():
        if not ExitHandler._saved:
            ExitHandler._saved = True
            ExitHandler._builtins_quit = builtins.quit if hasattr(builtins, 'quit') else None
            ExitHandler._builtins_exit = builtins.exit if hasattr(builtins, 'exit') else None
            ExitHandler._os_kill = os.kill if hasattr(os, 'kill') else None
            ExitHandler._os__exit = os._exit if hasattr(os, '_exit') else None
            ExitHandler._os_killpg = os.killpg if hasattr(os, 'killpg') else None
            ExitHandler._sys_exit = sys.exit if hasattr(sys, 'exit') else None
            ExitHandler._signal_pthread_kill = signal.pthread_kill if hasattr(signal, 'pthread_kill') else None
            ExitHandler._signal_siginterrupt = signal.siginterrupt if hasattr(signal, 'siginterrupt') else None

        builtins.quit = ExitHandler._exit_func
        builtins.exit = ExitHandler._exit_func
        os.kill = ExitHandler._exit_func
        os._exit = ExitHandler._exit_func
        os.killpg = ExitHandler._exit_func
        sys.exit = ExitHandler._exit_func
        signal.pthread_kill = ExitHandler._exit_func
        signal.siginterrupt = ExitHandler._exit_func

        ExitHandler._replaced = True

    @staticmethod
    def revert_exit():
        if ExitHandler._replaced:
            builtins.quit = ExitHandler._builtins_quit
            builtins.exit = ExitHandler._builtins_exit
            os.kill = ExitHandler._os_kill
            os._exit = ExitHandler._os__exit
            os.killpg = ExitHandler._os_killpg
            sys.exit = ExitHandler._sys_exit
            signal.pthread_kill = ExitHandler._signal_pthread_kill
            signal.siginterrupt = ExitHandler._signal_siginterrupt

            ExitHandler._replaced = False
