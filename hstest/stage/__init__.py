__all__ = [
    'StageTest',
    'DjangoTest',
    'FlaskTest',
    'PlottingTest',
    'SQLTest',
]

from hstest.stage.django_test import DjangoTest
from hstest.stage.flask_test import FlaskTest
from hstest.stage.sql_test import SQLTest
from hstest.stage.stage_test import StageTest

try:
    from hstest.stage.plotting_test import PlottingTest
except ImportError:
    PlottingTest = None
