import matplotlib.pyplot as plt
import pandas as pd

# Upload data
df_ab = pd.read_csv("ab_test.csv")

# Plot session duration with pandas features
df_ab.hist(column="session_duration", by=df_ab["group"], bins=10)
plt.suptitle("Session duration")
plt.show()

# Plot session duration with matplotlib subplots
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("Subplots for session duration")
ax1.hist(df_ab[df_ab["group"] == "Control"]["session_duration"])
ax2.hist(df_ab[df_ab["group"] == "Experimental"]["session_duration"])
plt.show()
