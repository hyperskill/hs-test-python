def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

    except ModuleNotFoundError:
        return

    df = pd.DataFrame({
        'mass': [0.330, 4.87, 5.97],
        'radius': [2439.7, 6051.8, 6378.1]
    },
        index=['Mercury', 'Venus', 'Earth'])
    plot = df.plot.pie(figsize=(5, 5), subplots=True)

    plt.show()


plot()
