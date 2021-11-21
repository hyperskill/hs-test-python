def plot():
    try:
        import pandas as pd
        import numpy as np
        import seaborn as sns
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    uniform_data = [
        [1, 2, 3],
        [7, 8, 9]
    ]

    fig, ax = plt.subplots(figsize=(1, 2))

    plt.imshow(uniform_data)
    ax.imshow(uniform_data)

    plt.show()


plot()
