def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    plt.bar([1, 2, 4, 6], 5)
    ax.bar([1, 2, 4, 6], 6)

    plt.barh([1, 2, 4, 6], 7)
    ax.barh([1, 2, 4, 6], 8)

    plt.show()


plot()
