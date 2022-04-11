def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    ax.boxplot([[1, 2, 3, 4],[2, 2, 3]])
    plt.show()

    plt.boxplot([1, 2, 3, 4])
    plt.show()


plot()
