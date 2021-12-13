def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    sns.histplot(np.array([1, 2, 3, 4, 5]))

    plt.show()


plot()
