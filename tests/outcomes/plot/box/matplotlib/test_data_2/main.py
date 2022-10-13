import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

general = pd.read_csv("test/general.csv")
prenatal = pd.read_csv("test/prenatal.csv")
sports = pd.read_csv("test/sports.csv")
prenatal.columns = general.columns
sports.columns = general.columns
df = pd.concat([general, prenatal, sports], ignore_index=True)
df.drop('Unnamed: 0', inplace=True, axis=1)
df.dropna(how='all', inplace=True)
df.gender.replace({'female': 'f', 'woman': 'f', 'man': 'm', 'male': 'm'}, inplace=True)
df.loc[df['hospital' == prenatal].index, 'gender'] = df.loc[df['hospital' == prenatal].index, 'gender'].fillna('f')
df.loc[:, ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']] = df.loc[:, ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']].fillna(0)

# this figure tests see as 6 figures
# pandas
# df.plot(y='age', kind='box')
# plt.show()

# pie chart
# pandas
df.diagnosis.value_counts().plot(kind='pie')
plt.show()

# seaborn
sns.violinplot(x='height', data=df)
plt.show()

print('The answer to the 1st question: 15 - 35')
print(f'The answer to the 2nd question: pregnancy')
print('The answer to the 3rd question: something')
