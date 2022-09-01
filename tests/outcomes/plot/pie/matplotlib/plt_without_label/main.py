def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    plt.pie([0.330, 4.87, 5.97])

    plt.show()


plot()
