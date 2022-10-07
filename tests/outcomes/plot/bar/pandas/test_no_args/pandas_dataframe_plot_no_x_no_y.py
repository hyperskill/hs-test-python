def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    df = pd.DataFrame({'lab': [2, 3, 4, 5, 6], 'val': [3, 4, 5, 6, 7]})

    df.plot.bar()

    plt.show()


plot()
