def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

    except ModuleNotFoundError:
        return

    df = pd.DataFrame([[1, 2], [2, 6]],
                      columns=['length', 'width'])
    df.plot.scatter(x='length',
                    y='width',
                    c='DarkBlue')

    df.plot(kind='scatter', x='length',
            y='width',
            c='DarkBlue')

    plt.show()


plot()
