def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    ser = pd.Series(data=np.array([1, 2, 3, 4, 5]))
    ser.hist()

    plt.show()


plot()
