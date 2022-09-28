def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    ax.hist(np.array([1, 2, 3, 4, 5]))
    plt.show()


plot()
