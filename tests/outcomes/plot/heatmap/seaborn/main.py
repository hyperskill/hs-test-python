def plot():
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import seaborn as sns
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))

    harvest = np.array(
        [
            [0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
            [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
            [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
            [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
            [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
            [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
            [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3],
        ]
    )

    ax = sns.heatmap(harvest, center=0)

    plt.show()


plot()
