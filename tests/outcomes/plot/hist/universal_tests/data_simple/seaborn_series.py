def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    ser = pd.Series(data=np.array([1, 2, 3, 4, 5]))

    sns.histplot(ser, bins=10)

    plt.show()


plot()
