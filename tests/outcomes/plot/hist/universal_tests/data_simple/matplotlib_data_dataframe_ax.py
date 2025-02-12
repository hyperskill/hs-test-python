def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    df = pd.DataFrame(
        np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]), columns=["one", "two"]
    )

    ax.hist(x="one", data=df)
    plt.show()


plot()
