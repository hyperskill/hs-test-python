def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(np.array([1, 2, 3]))

    plt.show()


plot()
