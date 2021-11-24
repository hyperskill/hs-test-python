def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    plt.hist([1, 2, 3, 4, 5])
    ax.hist([1, 2, 3, 4, 5])

    plt.show()


plot()
