def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    ser = pd.Series(data=np.array([1, 2, 3, 4, 5]))

    ax.hist(ser)
    plt.show()


plot()
