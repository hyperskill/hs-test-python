def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    plt.hist((1, 2, 3, 4, 5))
    plt.show()


plot()
