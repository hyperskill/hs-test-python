def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    ser = pd.Series(data=np.array([1, 2, 3]), index=["Mercury", "Venus", "Earth"])
    ser.plot(kind="pie")

    plt.show()


plot()
