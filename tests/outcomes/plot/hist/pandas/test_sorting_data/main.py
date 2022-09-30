def plot():
    try:
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    ser1 = pd.Series(data=np.array([3, 2, 1]))
    ser3 = pd.Series(data=np.array(['3', '2', '1']))
    ser4 = pd.Series(data=np.array([3.1, 2.1, 1]))
    ser5 = pd.Series(data=np.array(['b', 'a', 'c']))

    ser1.hist()
    ser3.hist()
    ser4.hist()
    ser5.hist()

    import matplotlib.pyplot as plt

    plt.show()


plot()
