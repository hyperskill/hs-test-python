from urllib.request import urlopen

from hstest.common.utils import clean_text
from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.stage.stage_test import StageTest
from hstest.test_case.attach.django_settings import DjangoSettings
from hstest.testing.runner.django_application_runner import DjangoApplicationRunner
from hstest.testing.settings import Settings


class DjangoTest(StageTest):
    runner = DjangoApplicationRunner()
    attach: DjangoSettings = DjangoSettings()

    test_database: str = attach.test_database
    use_database: bool = attach.use_database

    def __init__(self, args='', *, source: str = ''):
        super().__init__(args, source_name=source)
        self.attach.use_database = self.use_database
        loop_detector.working = False
        Settings.do_reset_output = False

    def read_page(self, link: str) -> str:
        """
        Deprecated, use get(...) instead
        """
        return clean_text(urlopen(link).read().decode())

    def get_url(self, link: str = ''):
        if link.startswith('/'):
            link = link[1:]
        return f'http://localhost:{self.attach.port}/{link}'

    def get(self, link: str) -> str:
        if not link.startswith('http://'):
            link = self.get_url(link)
        return clean_text(urlopen(link).read().decode())
