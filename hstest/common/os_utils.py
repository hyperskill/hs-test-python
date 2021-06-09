import platform


def is_windows():
    return platform.system() == 'Windows'


def is_mac():
    return platform.system() == 'Darwin'


def is_linux():
    return platform.system() == 'Linux'
