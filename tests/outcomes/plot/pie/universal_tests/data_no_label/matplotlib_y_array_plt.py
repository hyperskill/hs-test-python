def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return
    plt.pie([1, 2, 3])

    plt.show()


plot()
