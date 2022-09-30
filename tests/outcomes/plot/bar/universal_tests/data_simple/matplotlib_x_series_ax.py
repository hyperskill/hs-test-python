def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    ser = pd.Series(data=np.array([1, 2, 3, 4, 5]))
    height = pd.Series(data=np.array([2, 3, 4, 5, 6]))

    ax.bar(ser, height)
    plt.show()


plot()
