def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    ax.hist(((1, 3, 5, 7, 9), (2, 4, 6, 8, 10)))
    plt.show()


plot()
