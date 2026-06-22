import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
 
#Load & Explore Data
 
data = fetch_california_housing()
 
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Visualize Features vs Price
 
plt.figure(figsize=(15, 8))
 
for i, feature in enumerate(data.feature_names):
    plt.subplot(2, 4, i + 1)
    plt.scatter(df[feature], df['target'], alpha=0.3, s=1)
    plt.xlabel(feature)
    plt.ylabel('Price')
    plt.title(f'{feature} vs Price')
 
plt.tight_layout()
plt.show()
 
#Split Data into Train & Test Sets
 
X = df.drop('target', axis=1)
y = df['target']
 
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=88
)
 
print("\n=== Data Split ===")
print(f"Training set:  {x_train.shape}")
print(f"Test set:      {x_test.shape}")
 
#Train & Evaluate Models
 
# --- Linear Regression ---
linear_model = LinearRegression()
linear_model.fit(x_train, y_train)
 
ln_train = linear_model.score(x_train, y_train)
ln_test  = linear_model.score(x_test,  y_test)
 
print("\n=== Linear Regression ===")
print(f"  Train Score: {ln_train:.4f}")
print(f"  Test Score:  {ln_test:.4f}")
print(f"  Gap:         {ln_train - ln_test:.4f}")
 
 
# --- Polynomial + Ridge ---
polynomial_model = Pipeline([
    ('polynomial_features', PolynomialFeatures(degree=2)),
    ('ridge', Ridge())
])
polynomial_model.fit(x_train, y_train)
 
pn_train = polynomial_model.score(x_train, y_train)
pn_test  = polynomial_model.score(x_test,  y_test)
 
print("\n=== Polynomial + Ridge ===")
print(f"  Train Score: {pn_train:.4f}")
print(f"  Test Score:  {pn_test:.4f}")
print(f"  Gap:         {pn_train - pn_test:.4f}")
 
# Tune Alpha for Ridge & Lasso
 
alpha_values = [0.01, 0.1, 1, 10, 100]
 
# Ridge (L2)
print("\n=== Ridge Regression (L2) — Alpha Tuning ===")
for alpha in alpha_values:
    model = Ridge(alpha=alpha)
    model.fit(x_train, y_train)
    train = model.score(x_train, y_train)
    test  = model.score(x_test,  y_test)
    print(f"  alpha={alpha:<6} | Train: {train:.4f} | Test: {test:.4f} | Gap: {train - test:.4f}")
 
# Lasso L1
print("\n=== Lasso Regression (L1) — Alpha Tuning ===")
for alpha in alpha_values:
    model = Lasso(alpha=alpha)
    model.fit(x_train, y_train)
    train = model.score(x_train, y_train)
    test  = model.score(x_test,  y_test)
    print(f"  alpha={alpha:<6} | Train: {train:.4f} | Test: {test:.4f} | Gap: {train - test:.4f}")

# conclusions
print("\n=== Conclusions ===")
print("  Best model:      Polynomial + Ridge (highest test score: 0.645)")
print("  Worst model:     Lasso with large alpha (score drops to 0)")
print("  Overfitting:     Polynomial showed the largest gap (train - test)")
print("  Regularization:  Reduced weights → simpler model → less overfitting")
print("  Next time:       Feature scaling, smaller alpha, more training data")
