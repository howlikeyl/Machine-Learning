# Titanic Survival Prediction
# Topic:  Binary Classification, Logistic Regression,
#         Data Cleaning, Feature Engineering

# --- Imports ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

# Load the Titanic training dataset from CSV file
df = pd.read_csv("/Users/senghakheng/Documents/titanic_survivor/train.csv")
# Drop Cabin column — 77% of values are missing, not useful
df = df.drop("Cabin", axis = 1)
# Fill missing Age values with the mean age (177 missing values)
df['Age'] = df['Age'].fillna(df['Age'].mean())
# Drop the 2 rows with missing Embarked values
df = df.dropna(subset = ['Embarked'])
# Drop columns that are not useful for predicting survival
df = df.drop(['PassengerId', 'Ticket', 'Name'], axis = 1)
# Convert Sex from text to numbers beacuse models can only read numbers
# male = 0, female = 1
df['Sex'] = df['Sex'].map({'male' : 0, 'female' : 1})
# Convert Embarked from text to numbers
# S (Southampton) = 0, C (Cherbourg) = 1, Q (Queenstown) = 2
df['Embarked'] = df["Embarked"].map({ 'S': 0, 'C': 1, 'Q': 2 })


# Visualize Data
# Plot 1: Overall survival count, shows imbalanced dataset (62% died, 38% survived)
sns.countplot(x = 'Survived', data = df)
# Plot 2: Survival by gender — females survived much more than males
sns.countplot(x = 'Survived', hue = "Sex", data = df)
# Plot 3: Survival by passenger class, 1st class survived most, 3rd class died most
sns.countplot(x = 'Survived', hue = 'Pclass', data = df)
# Plot 4: Age distribution by survival, children (0-10) had higher survival rate
sns.histplot(x = 'Age', hue = 'Survived', data = df, bins = 30)


# Split Data & Train Models
# Separate features (X) and target variable (y)
# X = all columns except Survived, y = Survived column only
x = df.drop('Survived', axis = 1)
y = df['Survived']

# Split data into 80% training and 20% test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 33)

# Train Logistic Regression model, good for binary classification
model = LogisticRegression()
model.fit(x_train, y_train)

# Train Random Forest model — ensemble of 100 decision trees
model_rf = RandomForestClassifier(n_estimators = 100)
model_rf.fit(x_train, y_train)


# Evaluate Models
# Get predictions from Logistic Regression on test set
y_pred = model.predict(x_test)

# Confusion Matrix — shows TP, TN, FP, FN breakdown
# [[TN FP]
#  [FN TP]]
print(confusion_matrix(y_test, y_pred))

# Classification Report
# Precision: when model predicts survived, how often is it right?
# Recall: of all actual survivors, how many did model catch?
print(classification_report(y_test, y_pred))

# Compare train vs test scores to check for overfitting
# Logistic Regression
print(f"Train_LogisticRegression: {(model.score(x_train, y_train))}")
print(f"Test_LogisticRegression: {(model.score(x_test, y_test))}")
print (f"Gap_LogisticRegression: {(model.score(x_train, y_train) - model.score(x_test, y_test))}")
# Random Forest
print(f"Train_rf: {(model_rf.score(x_train, y_train))}")
print(f"Test_rf: {(model_rf.score(x_test, y_test))}")
print (f"Gap_rf: {(model_rf.score(x_train, y_train) - model_rf.score(x_test, y_test))}")
# Display all plots
plt.show()