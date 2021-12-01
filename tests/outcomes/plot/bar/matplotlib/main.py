def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    plt.bar([1, 2, 4, 6], 100)
    ax.bar([1, 2, 4, 6], 200)

    plt.barh([1, 2, 4, 6], 100)
    ax.barh([1, 2, 4, 6], 200)

    plt.show()


plot()
