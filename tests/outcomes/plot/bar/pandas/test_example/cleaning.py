import matplotlib.pyplot as plt
import pandas as pd

# Upload data
df_ab = pd.read_csv('ab_test.csv')

# Plot dates
df_ab['date'] = df_ab['date'].astype('datetime64')
control = df_ab[df_ab['group'] == 'Control'].groupby(
    df_ab['date'].dt.day
).size().rename('Control')
experiment = df_ab[df_ab['group'] == 'Experimental'].groupby(
    df_ab['date'].dt.day
).size().rename('Experimental')

control.plot(kind="bar")
plt.xlabel("Day")
plt.ylabel("Number of sessions")
plt.show()

experiment.plot(kind="bar")
plt.xlabel("Day")
plt.ylabel("Number of sessions")
plt.show()
