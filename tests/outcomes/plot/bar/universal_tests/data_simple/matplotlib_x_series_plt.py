def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    ser = pd.Series(data=np.array([1, 2, 3, 4, 5]))
    height = pd.Series(data=np.array([2, 3, 4, 5, 6]))

    plt.bar(ser, height)
    plt.show()


plot()
