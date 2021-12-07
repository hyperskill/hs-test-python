def plot():
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    plt.violinplot([[1, 2, 4], 2, 1])
    ax.violinplot([1, 2, 5])

    plt.show()


plot()
