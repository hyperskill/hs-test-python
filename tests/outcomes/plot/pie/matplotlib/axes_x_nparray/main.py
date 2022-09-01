def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(np.array([0.330, 4.87, 5.97]), labels=['Mercury', 'Venus', 'Earth'])

    plt.show()


plot()
