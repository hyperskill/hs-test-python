def plot():
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie((1, 2, 3), labels=["Mercury", "Venus", "Earth"])

    plt.show()


plot()
