def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

    except ModuleNotFoundError:
        return

    series = pd.Series([0.330, 4.87, 5.97], index=['Mercury', 'Venus', 'Earth'])

    series.plot.pie()

    plt.show()


plot()
