from .hack_matplotlib import hack_matplotlib
from .hack_seaborn import hack_seaborn
from .hack_pandas import hack_pandas


def hack(drawings):
    hack_matplotlib(drawings)
    hack_seaborn(drawings)
    hack_pandas(drawings)
