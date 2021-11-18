def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    plt.pie([0.330, 4.87, 5.97], labels=['Mercury', 'Venus', 'Earth'])
    ax.pie([2439.7, 6051.8, 6378.1], labels=['Mercury', 'Venus', 'Earth'])

    plt.show()


plot()
