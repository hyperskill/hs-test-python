import os
import signal
import subprocess
from time import sleep
from urllib.error import URLError, HTTPError
from urllib.request import urlopen
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


class ExampleDjangoTest(DjangoTest):

    def get_main_page(self) -> CheckResult:
        for _ in range(3):
            try:
                main_page = urlopen('http://localhost:8000').read().decode()
                if 'Welcome to the Ticket service' in main_page:
                    return CheckResult.true()
                return CheckResult.false(
                    'Main page should contain "Welcome to the Ticket service" line'
                )
            except (URLError, HTTPError):
                sleep(2)
        return CheckResult.false(
            'Cannot connect to the main page.'
        )

    def get_ticket_page(self) -> CheckResult:
        try:
            ticket_page = urlopen('http://localhost:8000/tickets').read().decode()
        except (URLError, HTTPError):
            return CheckResult.false(
                'Cannot connect to the ticket page "/tickets".'
            )

        if 'Available tickets' in ticket_page:
            return CheckResult.true()
        return CheckResult.false(
            'Tickets page should contain "Available tickets" line'
        )

    def get_about_page(self) -> CheckResult:
        try:
            about_page = urlopen('http://localhost:8000/about').read().decode()
        except (URLError, HTTPError):
            return CheckResult.false(
                'Cannot connect to the about page "/about".'
            )

        if 'About' in about_page:
            return CheckResult.true()
        return CheckResult.false(
            'About page should contain "About" line'
        )

    def generate(self):
        return [
            TestCase(attach=self.get_main_page),
            TestCase(attach=self.get_ticket_page),
            TestCase(attach=self.get_about_page),
        ]

    def check(self, reply, attach):
        return attach()
