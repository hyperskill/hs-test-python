import platform

from hstest.testing.execution_options import inside_docker


def get_report():
    if not inside_docker:
        name_os = platform.system() + " " + platform.release()
        python = platform.python_version()
        implementation = platform.python_implementation()
        return (
            'Submitted via IDE\n'
            '\n'
            f'OS {name_os}\n'
            f'{implementation} {python}\n'
            f'Testing library version 6'
        )
    else:
        return 'Submitted via web'
