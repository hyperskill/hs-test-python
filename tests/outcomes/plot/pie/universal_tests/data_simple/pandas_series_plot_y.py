def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    ser = pd.Series(data=np.array([1, 2, 3]), index=['Mercury', 'Venus', 'Earth'])
    ser.plot.pie()

    plt.show()


plot()
