Name: Senghak Heng

House Price Prediction

A machine learning project that predicts California housing prices using multiple regression techniques, including Linear, Ridge, Lasso, and Polynomial Regression.

Project Overview

This project explores supervised learning regression models to predict median house prices in California. The goal is to compare model performance and understand the impact of regularization on overfitting.

Technologies Used

- Python 3
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

Dataset

- Source: California Housing Dataset (built into scikit-learn)
- Rows: 20,640
- Features: 8 numerical features
- arget: Median house value (in $100,000s)

| Feature | Description |

| MedInc | Median income in block group |
| HouseAge | Median house age |
| AveRooms | Average number of rooms |
| AveBedrms | Average number of bedrooms |
| Population | Block group population |
| AveOccup | Average household members |
| Latitude | Block group latitude |
| Longitude | Block group longitude |

Steps

1. Explore Data — shape, features, missing values, statistics
2. Visualize — scatter plots of each feature vs price
3. Split Data — 80% train, 20% test
4. Train Models — Linear, Ridge, Lasso, Polynomial + Ridge
5. Tune Alpha — tested 5 alpha values for Ridge and Lasso
6. Evaluate — R² score and train/test gap analysis

---

Results

| Model | Train R² | Test R² | Gap |
|---|---|---|---|
| Linear Regression | 0.6079 | 0.5985 | 0.009 |
| Ridge (L2) | 0.6079 | 0.5985 | 0.009 |
| Lasso (L1) | 0.2928 | 0.2839 | 0.009 |
| Polynomial + Ridge | 0.6863 | 0.6451 | 0.041 |

Alpha Tuning (Lasso)

| Alpha | Train R² | Test R² |
|---|---|---|
| 0.01 | 0.604 | 0.594 |
| 0.1 | 0.547 | 0.535 |
| 1.0 | 0.293 | 0.284 |
| 10 | 0.0005 | 0.0001 |
| 100 | 0.0 | -0.0005 |

Findings

- Best model: Polynomial + Ridge (Test R² = 0.645)
- Why: The data has curved relationships that linear models cannot capture
- Lasso: aggressively zeroed out features at high alpha values — losing important information
- Ridge: was very stable across all alpha values
- Overfitting: was most visible in Polynomial model (gap = 0.041)

What I Learned

- How to detect overfitting using train/test gap
- How L1 (Lasso) and L2 (Ridge) regularization affect model weights
- Why higher alpha can cause underfitting in Lasso
- How Polynomial Features help capture non-linear relationships

---

How to Run

1. Clone the repository
```bash
git clone https://github.com/senghakheng/HousePricePrediction.git
cd HousePricePrediction
```

2. Install dependencies
```bash
pip install pandas numpy matplotlib scikit-learn
```

3. Run the script
```bash
python HousePricePrediction.py
```

Course: Built as part of **Andrew Ng's Machine Learning Specialization** — Course 1: Supervised Machine Learning.
