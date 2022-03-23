__all__ = [
    'StageTest',
    'DjangoTest',
    'FlaskTest',
    'PlottingTest',
    'SQLTest'
]

from hstest.stage.django_test import DjangoTest
from hstest.stage.flask_test import FlaskTest
from hstest.stage.stage_test import StageTest
from hstest.stage.sql_test import SQLTest

try:
    from hstest.stage.plotting_test import PlottingTest
except ImportError:
    PlottingTest = None
