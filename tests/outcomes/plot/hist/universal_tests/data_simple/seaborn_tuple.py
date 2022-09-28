def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import seaborn as sns
    except ModuleNotFoundError:
        return

    sns.histplot((1, 2, 3, 4, 5), bins=10)

    plt.show()


plot()
