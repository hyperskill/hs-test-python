import os
import re
import signal
import subprocess
from functools import partial
from time import sleep
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, build_opener
from hstest.stage_test import StageTest
from hstest.check_result import CheckResult
from hstest.test_case import TestCase


class DjangoTest(StageTest):

    _kill = os.kill
    process = None

    def run(self):
        if self.process is None:
            self.process = subprocess.Popen([self.file_to_test, 'runserver'])

    def after_all_tests(self):
        if self.process is not None:
            self._kill(self.process.pid, signal.SIGINT)


class HypercarWelcomeToServiceTest(DjangoTest):

    def get_welcome_page(self) -> CheckResult:
        for _ in range(3):
            try:
                main_page = urlopen('http://localhost:8000/welcome').read().decode()
                if 'Welcome to the Hypercar service' in main_page:
                    return CheckResult.true()
                return CheckResult.false(
                    'Main page should contain "Welcome to the Hypercar service" line'
                )
            except (URLError, HTTPError):
                sleep(2)
        return CheckResult.false(
            'Cannot connect to the /welcome page.'
        )

    def generate(self):
        return [
            TestCase(attach=self.get_welcome_page),
        ]

    def check(self, reply, attach):
        return attach()


class HypercarClientMenuTest(DjangoTest):
    ELEMENT_PATTERN = '''<a[^>]+href=['"](?P<href>[a-zA-Z/_]+)['"][^>]*>'''

    def get_client_menu_page(self) -> CheckResult:
        for _ in range(3):
            try:
                page = urlopen('http://localhost:8000/menu').read().decode()
                links = re.findall(self.ELEMENT_PATTERN, page)
                for link in (
                    '/get_ticket/change_oil',
                    '/get_ticket/inflate_tires',
                    '/get_ticket/make_diagnostics',
                ):
                    if link not in links:
                        return CheckResult.false(
                            f'Menu page should contain <a> element with href {link}'
                        )
                return CheckResult.true()
            except (URLError, HTTPError):
                sleep(2)
        return CheckResult.false(
            'Cannot connect to the main page.'
        )

    def generate(self):
        return [
            TestCase(attach=self.get_client_menu_page),
        ]

    def check(self, reply, attach):
        return attach()


class HypercarElecronicQueueTest(DjangoTest):

    def get_welcome_page(self) -> CheckResult:
        for _ in range(3):
            try:
                main_page = urlopen('http://localhost:8000/welcome').read().decode()
                if 'Welcome to the Hypercar service' in main_page:
                    return CheckResult.true()
                return CheckResult.false(
                    'Main page should contain "Welcome to the Hypercar service" line'
                )
            except (URLError, HTTPError):
                sleep(2)
        return CheckResult.false(
            'Cannot connect to the /welcome page.'
        )

    def get_ticket(self, service: str, content: str) -> CheckResult:
        try:
            page = urlopen(f'http://localhost:8000/get_ticket/{service}').read().decode()
            if content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {content} on /get_ticket/{service} page'
                )
        except (URLError, HTTPError):
            return CheckResult.false(
                f'Cannot connect to the /get_ticket/{service} page.'
            )

    def generate(self):
        return [
            TestCase(attach=self.get_welcome_page),
            TestCase(attach=partial(
                self.get_ticket,
                'inflate_tires',
                'Please wait around 0 minutes'
            )),
            TestCase(attach=partial(
                self.get_ticket,
                'change_oil',
                'Please wait around 0 minutes'
            )),
            TestCase(attach=partial(
                self.get_ticket,
                'change_oil',
                'Please wait around 2 minutes'
            )),
            TestCase(attach=partial(
                self.get_ticket,
                'inflate_tires',
                'Please wait around 9 minutes'
            )),
            TestCase(attach=partial(
                self.get_ticket,
                'make_diagnostics',
                'Please wait around 14 minutes'
            )),
        ]

    def check(self, reply, attach):
        return attach()


class HypercarOperatorMenuTest(DjangoTest):
    SERVICE_TO_MESSAGE = {
        'change_oil': 'Change oil queue',
        'inflate_tires': 'Inflate tires queue',
        'make_diagnostics': 'Make diagnostics queue',
    }

    def get_welcome_page(self) -> CheckResult:
        for _ in range(3):
            try:
                main_page = urlopen('http://localhost:8000/welcome').read().decode()
                if 'Welcome to the Hypercar service' in main_page:
                    return CheckResult.true()
                return CheckResult.false(
                    'Main page should contain "Welcome to the Hypercar service" line'
                )
            except (URLError, HTTPError):
                sleep(2)
        return CheckResult.false(
            'Cannot connect to the /welcome page.'
        )

    def get_ticket(self, service: str, content: str) -> CheckResult:
        try:
            page = urlopen(f'http://localhost:8000/get_ticket/{service}').read().decode()
            if content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {content} on /get_ticket/{service} page'
                )
        except (URLError, HTTPError):
            return CheckResult.false(
                f'Cannot connect to the /get_ticket/{service} page.'
            )

    def check_menu(self, service: str, content: str, menu_content: str) -> CheckResult:
        try:
            result = self.get_ticket(service, content)
            if not result.result:
                return result

            page = urlopen(f'http://localhost:8000/processing').read().decode()
            if menu_content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {menu_content} on /processing page'
                )
        except (URLError, HTTPError):
            return CheckResult.false(
                f'Cannot connect to the /processing page.'
            )

    def generate(self):
        return [
            TestCase(attach=self.get_welcome_page),
            TestCase(attach=partial(
                self.check_menu,
                'inflate_tires',
                'Please wait around 0 minutes',
                'Inflate tires queue: 1'
            )),
            TestCase(attach=partial(
                self.check_menu,
                'change_oil',
                'Please wait around 0 minutes',
                'Change oil queue: 1'
            )),
            TestCase(attach=partial(
                self.check_menu,
                'change_oil',
                'Please wait around 2 minutes',
                'Change oil queue: 2'
            )),
            TestCase(attach=partial(
                self.check_menu,
                'inflate_tires',
                'Please wait around 9 minutes',
                'Inflate tires queue: 2'
            )),
            TestCase(attach=partial(
                self.check_menu,
                'make_diagnostics',
                'Please wait around 14 minutes',
                'Make diagnostics queue: 1'
            )),
        ]

    def check(self, reply, attach):
        return attach()


class HypercarServeNextTest(DjangoTest):
    SERVICE_TO_MESSAGE = {
        'change_oil': 'Change oil queue',
        'inflate_tires': 'Inflate tires queue',
        'make_diagnostics': 'Make diagnostics queue',
    }

    def get_welcome_page(self) -> CheckResult:
        for _ in range(3):
            try:
                main_page = urlopen('http://localhost:8000/welcome').read().decode()
                if 'Welcome to the Hypercar service' in main_page:
                    return CheckResult.true()
                return CheckResult.false(
                    'Main page should contain "Welcome to the Hypercar service" line'
                )
            except (URLError, HTTPError):
                sleep(2)
        return CheckResult.false(
            'Cannot connect to the /welcome page.'
        )

    def get_ticket(self, service: str, content: str) -> CheckResult:
        try:
            page = urlopen(f'http://localhost:8000/get_ticket/{service}').read().decode()
            if content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {content} on /get_ticket/{service} page'
                )
        except (URLError, HTTPError):
            return CheckResult.false(
                f'Cannot connect to the /get_ticket/{service} page.'
            )

    def check_menu(self, service: str, content: str, menu_content: str) -> CheckResult:
        try:
            result = self.get_ticket(service, content)
            if not result.result:
                return result

            page = urlopen(f'http://localhost:8000/processing').read().decode()
            if menu_content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {menu_content} on /processing page'
                )
        except (URLError, HTTPError):
            return CheckResult.false(
                f'Cannot connect to the /processing page.'
            )

    def check_next(self, service: str, content: str, menu_content: str,
                   next_content: str, make_process: bool) -> CheckResult:
        try:
            result = self.check_menu(service, content, menu_content)
            if not result.result:
                return result

            if make_process:
                result = self.process_ticket()
                if not result.result:
                    return result

            page = urlopen('http://localhost:8000/next').read().decode()

            if next_content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {next_content} on /next page'
                )
        except (URLError, HTTPError):
            return CheckResult.false(
                f'Cannot connect to the /next page.'
            )

    def process_ticket(self):
        response = urlopen(f'http://localhost:8000/processing')
        csrf_options = re.findall(
            b'<input[^>]+value="(?P<csrf>\w+)"[^>]*>', response.read()
        )
        if not csrf_options:
            return CheckResult.false(
                'Add csrf_token to your form'
            )
        set_cookie = response.headers.get('Set-Cookie')
        opener = build_opener()
        opener.addheaders.append(('Cookie', set_cookie))
        try:
            opener.open(
                'http://localhost:8000/processing',
                data=urlencode({'csrfmiddlewaretoken': csrf_options[0]}).encode()
            )
        except HTTPError:
            return CheckResult.false(
                'Cannot send POST request to /processsing page'
            )
        return CheckResult.true()

    def generate(self):
        return [
            TestCase(attach=self.get_welcome_page),
            TestCase(attach=partial(
                self.check_next,
                'inflate_tires',
                'Please wait around 0 minutes',
                'Inflate tires queue: 1',
                'Waiting for the next client',
                False
            )),
            TestCase(attach=partial(
                self.check_next,
                'change_oil',
                'Please wait around 0 minutes',
                'Change oil queue: 1',
                'Waiting for the next client',
                False
            )),
            TestCase(attach=partial(
                self.check_next,
                'change_oil',
                'Please wait around 2 minutes',
                'Change oil queue: 2',
                'Next ticket #2',
                True
            )),
            TestCase(attach=partial(
                self.check_next,
                'inflate_tires',
                'Please wait around 7 minutes',
                'Inflate tires queue: 2',
                'Next ticket #3',
                True
            )),
            TestCase(attach=partial(
                self.check_next,
                'make_diagnostics',
                'Please wait around 10 minutes',
                'Make diagnostics queue: 1',
                'Next ticket #1',
                True
            )),
        ]

    def check(self, reply, attach):
        return attach()
