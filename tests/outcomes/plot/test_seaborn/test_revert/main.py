def plot():
    try:
        import seaborn as sns
        import numpy as np
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        return

    fig, ax = plt.subplots(figsize=(1, 2))
    df = sns.load_dataset("penguins")

    sns.displot(
        df, x="flipper_length_mm", col="species", row="sex",
        binwidth=3, height=3, facet_kws=dict(margin_titles=True),
    )

    sns.histplot(
        df, x="flipper_length_mm"
    )

    sns.lineplot(data=df, x="flipper_length_mm", y="flipper_length_mm")
    sns.lmplot(data=df, x="flipper_length_mm", y="flipper_length_mm")
    sns.scatterplot(data=df, x="flipper_length_mm", y="flipper_length_mm")

    sns.catplot(
        data=df, kind="bar",
        x="species", y="body_mass_g", hue="sex",
        ci="sd", palette="dark", alpha=.6, height=6
    )

    x = np.array(list("ABCDEFGHIJ"))
    y1 = np.arange(1, 11)
    sns.barplot(x=x, y=y1, palette="rocket", ax=ax)

    sns.violinplot(data=df, palette="Set3", bw=.2, cut=1, linewidth=1)

    flights_long = sns.load_dataset("flights")
    flights = flights_long.pivot("month", "year", "passengers")
    sns.heatmap(flights, annot=True, fmt="d", linewidths=.5, ax=ax)

    tips = sns.load_dataset("tips")
    sns.boxplot(x="day", y="total_bill",
                hue="smoker", palette=["m", "g"],
                data=tips)
    sns.despine(offset=10, trim=True)

    import matplotlib.pyplot as plt

    plt.show()


plot()
