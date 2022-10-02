def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(np.array([1, 2, 3]), labels=['Mercury', 'Venus', 'Earth'])

    plt.show()


plot()
