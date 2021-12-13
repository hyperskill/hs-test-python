__all__ = [
    'StageTest',
    'DjangoTest',
    'FlaskTest',
    'PlottingTest',
]

from hstest.stage.django_test import DjangoTest
from hstest.stage.flask_test import FlaskTest
from hstest.stage.stage_test import StageTest

try:
    from hstest.stage.plotting_test import PlottingTest
except ImportError:
    pass
