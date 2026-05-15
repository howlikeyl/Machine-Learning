import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/Users/senghakheng/Documents/titanic_survivor/train.csv")

df = df.drop("Cabin", axis = 1)
df['Age'] = df['Age'].fillna(df['Age'].mean())
df = df.dropna(subset = ['Embarked'])
df = df.drop(['PassengerId', 'Ticket', 'Name'], axis = 1)
df['Sex'] = df['Sex'].map({'male' : 0, 'female' : 1})
df['Embarked'] = df["Embarked"].map({ 'S': 0, 'C': 1, 'Q': 2 })
# sns.countplot(x = 'Survived', data = df)
# sns.countplot(x = 'Survived', hue = "Sex", data = df)
# sns.countplot(x = 'Survived', hue = 'Pclass', data = df)
# sns.histplot(x = 'Age', hue = 'Survived', data = df, bins = 30)
plt.show()
print(df.shape)
print(df.head())
print(df.info())
print(df.describe())
