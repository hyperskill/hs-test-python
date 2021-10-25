__all__ = [
    'StageTest',
    'DjangoTest',
    'FlaskTest',
    'MatplotlibTest'
]

from hstest.stage.django_test import DjangoTest
from hstest.stage.flask_test import FlaskTest
from hstest.stage.stage_test import StageTest
from hstest.stage.matplotlib_test import MatplotlibTest
