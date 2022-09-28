def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns
    except ModuleNotFoundError:
        return

    n = 10000
    df = pd.DataFrame({
        'x': np.random.randn(n),
        'y': np.random.randn(n)
    })
    ax = df.plot.hexbin(x='x', y='y', gridsize=20)

    plt.show()


plot()
