def plot():
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots()

    df = pd.DataFrame(np.array([1, 2, 3, 4, 5]),
                      columns=['one'])

    ax.hist(df)
    plt.show()


plot()
