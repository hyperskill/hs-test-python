def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    ser = pd.Series(data=np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    by = pd.Series(data=np.array([1, 2, 1, 2, 1, 2, 1, 2, 1, 2]))

    ser.hist(by=by)

    plt.show()


plot()
