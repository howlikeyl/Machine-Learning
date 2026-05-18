import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix  
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
x = df.drop('Survived', axis = 1)
y = df['Survived']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 33)

model = LogisticRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(model.score(x_train, y_train))
print(model.score(x_test, y_test))

