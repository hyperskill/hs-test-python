def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    plt.boxplot([1, 2, 4])
    ax.boxplot([1, 2, 5])

    plt.show()


plot()
