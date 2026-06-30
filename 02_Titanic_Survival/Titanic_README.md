Name : Senghak Heng

Titanic Survival Prediction

A machine learning project that predicts whether a passenger survived the Titanic disaster using binary classification techniques including Logistic Regression and Random Forest.

Project Overview

This project builds a classification model to predict Titanic passenger survival. The goal is to explore data cleaning, feature engineering, and compare classification model performance using real-world messy data from Kaggle.

Technologies Used

- Python 3
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

Dataset

- Source: Titanic - Machine Learning from Disaster (Kaggle)
- Rows: 891 passengers
- Features: 11 columns including Age, Sex, Pclass, Fare, Embarked
- Target: Survived (0 = No, 1 = Yes)

Variable descriptions:

- Survived: Survival (0 = No, 1 = Yes)
- Pclass: Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)
- Sex: Gender of passenger
- Age: Age in years
- SibSp: Number of siblings/spouses aboard
- Parch: Number of parents/children aboard
- Fare: Passenger fare
- Embarked: Port of embarkation (S, C, Q)

Steps

1. Explore Data — shape, features, missing values, statistics
2. Visualize — survival rate, gender vs survival, class vs survival, age distribution
3. Clean Data — drop Cabin (77% missing), fill Age with mean, drop 2 missing Embarked rows
4. Feature Engineering — drop irrelevant columns, convert Sex and Embarked to numbers
5. Split Data — 80% train, 20% test
6. Train Models — Logistic Regression and Random Forest
7. Evaluate — confusion matrix, precision, recall, F1-score

Results

Logistic Regression:
- Train Score: 0.799
- Test Score: 0.814
- Gap: 0.015 (good generalization, no overfitting)

Random Forest:
- Train Score: 0.986
- Test Score: 0.826
- Gap: 0.160 (overfitting detected)

Confusion Matrix (Logistic Regression):
- True Negative: 97 (correctly predicted died)
- True Positive: 48 (correctly predicted survived)
- False Positive: 14 (predicted survived but died)
- False Negative: 19 (predicted died but survived)


Findings

- Best model: Random Forest (Test Score = 0.826) but shows overfitting
- Most reliable model: Logistic Regression (smaller gap, more stable)
- Most important features: Sex, Pclass, Age
- Females survived at 74% rate vs only 20% for males
- 1st class passengers survived at 63% rate vs 24% for 3rd class
- Children under 10 had higher survival rate than adults
- Dataset is imbalanced (62% died, 38% survived) — accuracy alone is misleading

What I Learned

- How to clean and prepare real-world messy data
- How to convert categorical features (text) to numbers
- How to evaluate classification models using precision, recall and F1-score
- Why accuracy alone is misleading on imbalanced datasets
- How Random Forest differs from a single Decision Tree

How to Run

1. Clone the repository

git clone https://github.com/howlikeyl/Machine-Learning.git
cd Machine-Learning/02_Titanic_Survival

2. Install dependencies

pip install pandas numpy matplotlib seaborn scikit-learn

3. Run the script

python Titanic_Survivor.py


Course: Built as part of Andrew Ng's Machine Learning Specialization — Course 1: Supervised Machine Learning.
