from urllib.request import urlopen

from hstest.common.utils import clean_text
from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.stage_test import StageTest
from hstest.test_case.attach.django_settings import DjangoSettings
from hstest.testing.runner.django_application_runner import DjangoApplicationRunner
from hstest.testing.settings import Settings


class DjangoTest(StageTest):
    runner = DjangoApplicationRunner
    attach = DjangoSettings()

    TEST_DATABASE = 'db.test.sqlite3'
    use_database = attach.use_database

    def __init__(self, source_name: str = ''):
        super().__init__(source_name)
        self.attach.use_database = self.use_database
        loop_detector.working = False
        Settings.do_reset_output = False

    def read_page(self, link: str) -> str:
        return clean_text(urlopen(link).read().decode())
