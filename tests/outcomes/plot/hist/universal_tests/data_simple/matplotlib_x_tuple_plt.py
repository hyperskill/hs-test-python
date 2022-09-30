def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    plt.hist((1, 2, 3, 4, 5))
    plt.show()


plot()
