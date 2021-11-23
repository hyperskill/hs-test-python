def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

    except ModuleNotFoundError:
        return

    df = pd.DataFrame({
        'x': [1, 2, 2.5, 3, 3.5, 4, 5],
        'y': [4, 4, 4.5, 5, 5.5, 6, 6],
    })

    df.plot.kde(x='y')
    df.plot.kde(y='x')
    df.plot.kde()
    df.plot.density(x='y')
    df.plot.density(y='x')
    df.plot.density()

    plt.show()


plot()
