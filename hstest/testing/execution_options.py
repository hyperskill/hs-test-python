import os
import sys

skip_slow: bool = '--skip_slow' in sys.argv
ignore_stdout: bool = '--ignore_stdout' in sys.argv
inside_docker: bool = '--inside_docker' in sys.argv or os.environ.get('INSIDE_DOCKER', '') == '1'
debug_mode: bool = '--debug_mode' in sys.argv or sys.gettrace() is not None
force_process_testing: bool = '--force_process_testing' in sys.argv
