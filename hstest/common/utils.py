import platform

from hstest.testing.execution_options import inside_docker

failed_msg_start = '#educational_plugin FAILED + '
failed_msg_continue = '#educational_plugin '
success_msg = '#educational_plugin test OK'


def failed(message: str):
    """ Reports failure """
    lines = message.splitlines()
    print('\n' + failed_msg_start + lines[0])
    for line in lines[1:]:
        print(failed_msg_continue + line)
    return -1, message


def passed():
    """ Reports success """
    print('\n' + success_msg)
    return 0, 'test OK'


def clean_text(text: str) -> str:
    return (
        text.replace('\r\n', '\n')
            .replace('\r', '\n')
            .replace('\u00a0', '\u0020')
    )


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
            f'Testing library version 3.0.3'
        )
    else:
        return 'Submitted via web'
