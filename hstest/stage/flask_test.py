from urllib.request import urlopen

from hstest.common.utils import clean_text
from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.exception.outcomes import UnexpectedError
from hstest.stage.stage_test import StageTest
from hstest.test_case.attach.flask_settings import FlaskSettings
from hstest.testing.runner.flask_application_runner import FlaskApplicationRunner
from hstest.testing.settings import Settings


class FlaskTest(StageTest):
    runner = FlaskApplicationRunner
    attach: FlaskSettings = FlaskSettings()

    def __init__(self, source_name: str = ''):
        super().__init__(source_name)
        loop_detector.working = False
        Settings.do_reset_output = False

        if self.source_name:
            sources = self.source_name

            if type(sources) != list:
                sources = [sources]

            for item in sources:
                if type(item) == str:
                    self.attach.sources += [(item, None)]
                elif type(item) == tuple:
                    if len(item) == 1:
                        self.attach.sources += [(item[0], None)]
                    else:
                        self.attach.sources += [item]

    def get_url(self, source: str = None):
        create_url = lambda port: f'http://localhost:{port}/'

        if len(self.attach.sources) == 1:
            return create_url(self.attach.sources[0][1])
        elif len(self.attach.sources) == 0:
            raise UnexpectedError(f'Cannot find sources')

        sources_fits = [i for i in self.attach.sources if i[0] == source]
        if len(sources_fits) == 0:
            raise UnexpectedError(f'Bad source: {source}')
        elif len(sources_fits) > 1:
            raise UnexpectedError(f'Multiple sources ({len(sources_fits)}) found: {source}')

        return create_url(sources_fits[0][1])

    def get(self, link: str, source: str = None) -> str:
        if link.startswith('/'):
            link = link[1:]

        if not link.startswith('http://'):
            link = self.get_url(source) + link

        return clean_text(urlopen(link).read().decode())
