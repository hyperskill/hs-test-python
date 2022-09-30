def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    plt.bar([1, 2, 3, 4, 5], [2, 3, 4, 5, 6])
    plt.show()


plot()
