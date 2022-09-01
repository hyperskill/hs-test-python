def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

    except ModuleNotFoundError:
        return

    df = pd.DataFrame({'mass': [0.330, 4.87, 5.97],
                       'radius': [2439.7, 6051.8, 6378.1]},
                      index=['Mercury', 'Venus', 'Earth'])
    df.plot.pie(figsize=(5, 5), subplots=True, y='mass')

    plt.show()


plot()
