import os
import re
import json
import hstest
import requests

from time import sleep
from typing import Callable
from datetime import datetime

failed_msg_start = '#educational_plugin FAILED + '
failed_msg_continue = '#educational_plugin '
success_msg = '#educational_plugin test OK'

latest_version_cache_file_name = 'version_cache.json'
dir_path = os.path.dirname(os.path.abspath(__file__))
cache_file_path = os.path.join(dir_path, latest_version_cache_file_name)


def failed(message: str, is_unittest: bool):
    """ Reports failure """
    if not is_unittest:
        lines = message.splitlines()
        print('\n' + failed_msg_start + lines[0])
        for line in lines[1:]:
            print(failed_msg_continue + line)
    return -1, message


def passed(is_unittest: bool):
    """ Reports success """
    if not is_unittest:
        print('\n' + success_msg)
    return 0, 'test OK'


def clean_text(text: str) -> str:
    return (
        text.replace('\r\n', '\n')
        .replace('\r', '\n')
        .replace('\u00a0', '\u0020')
    )


def try_many_times(times_to_try: int, sleep_time_ms: int, exit_func: Callable[[], bool]):
    while times_to_try > 0:
        times_to_try -= 1
        if exit_func():
            return True
        sleep(sleep_time_ms / 1000)
    return False


def _get_the_latest_version_from_github() -> str:
    github_url = 'https://raw.githubusercontent.com/hyperskill/hs-test-python/release/setup.py'
    pattern = re.compile('version\s*=\s*"([\d\.]+)"')

    response = requests.get(github_url)
    match = pattern.search(response.text)
    latest_version = match.group(1)
    with open(cache_file_path, 'w') as version_cache:
        version_cache.write(json.dumps({
            'version': latest_version,
            'time': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }, default=str))
    return latest_version


def _get_the_latest_library_version() -> str:
    cache_exp_time = 3600 * 2

    if os.path.exists(cache_file_path):
        with open(cache_file_path, 'r') as version_cache:
            version_json = json.loads(version_cache.read())
            cached_time = datetime.strptime(version_json['time'], '%Y-%m-%d %H:%M:%S')
            difference = datetime.utcnow() - cached_time
            if difference.seconds > cache_exp_time:
                return _get_the_latest_version_from_github()
            return version_json['version']
    else:
        return _get_the_latest_version_from_github()


def is_library_outdated() -> bool:
    try:
        latest_version = _get_the_latest_library_version()
        return latest_version != hstest.__version__
    except Exception as _:
        return False
