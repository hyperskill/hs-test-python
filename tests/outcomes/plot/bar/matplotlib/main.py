def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    plt.bar([1, 2, 4, 6], 5)
    ax.bar([1, 2, 4, 6], 6)

    plt.barh([1, 2, 4, 6], 7)
    ax.barh([1, 2, 4, 6], 8)

    plt.show()


plot()
