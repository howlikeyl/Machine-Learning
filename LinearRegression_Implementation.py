import numpy as np

# prediction function: calculate y_hat = wx + b
def prediction(w, x, b):
    return w * x + b

# cost function: measure how wrong our prediction is
# formula: J(w,b) = (1/2m) * Σ(y_hat - y)²
def cost_function(x, y, w, b):
    j_wb = 0
    total_training = len(x)
    for i in range(total_training):
        y_hat = prediction(w, x[i], b)       # get prediction for each sample
        j_wb += (y_hat - y[i]) ** 2          # sum up squared errors
    return j_wb / (2 * total_training)        # average the errors

# compute gradient: find which direction to move w and b to reduce cost
# formula: dj/dw = (1/m) * Σ(y_hat - y) * x
# formula: dj/db = (1/m) * Σ(y_hat - y)
def compute_gradient(x, y, w, b):
    m = len(x)
    dj_dw = 0
    dj_db = 0
    for i in range(m):
        f_wb = prediction(w, x[i], b)        # prediction for sample i
        dj_dw += (f_wb - y[i]) * x[i]        # accumulate gradient for w
        dj_db += (f_wb - y[i])               # accumulate gradient for b
    dj_dw = dj_dw / m                        # average gradient for w
    dj_db = dj_db / m                        # average gradient for b
    return dj_dw, dj_db

# gradient descent: repeatedly update w and b to minimize cost
# formula: w = w - alpha * dj/dw
# formula: b = b - alpha * dj/db
def gradient_descent(x, y, w, b, alpha, num_iters):
    for i in range(num_iters):               # repeat for num_iters steps
        dj_dw, dj_db = compute_gradient(x, y, w, b)  # get gradients
        w = w - alpha * dj_dw               # update w
        b = b - alpha * dj_db               # update b
    return w, b

# ----------------------------
# Tests
# ----------------------------
def test_prediction():
    result = prediction(3, 2, 5)
    assert result == 11, f"Expected 11, got {result}"
    print("PASS test_prediction")

def test_cost_zero_on_perfect_fit():
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([3.0, 6.0, 9.0])           # y = 3x exactly, cost should be 0
    cost = cost_function(x, y, w=3, b=0)
    assert cost == 0.0, f"Expected 0, got {cost}"
    print("PASS test_cost_zero_on_perfect_fit")

def test_cost_is_positive():
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([1.0, 2.0, 3.0])
    cost = cost_function(x, y, w=0, b=0)
    assert cost >= 0, "Cost should never be negative"
    print("PASS test_cost_is_positive")

def test_cost_decreases():
    np.random.seed(0)
    x = np.random.randn(100)
    y = 2 * x + 4
    cost_before = cost_function(x, y, 0, 0)           # cost before training
    w, b = gradient_descent(x, y, 0, 0, 0.01, 100)   # train
    cost_after = cost_function(x, y, w, b)             # cost after training
    assert cost_after < cost_before, f"Cost should decrease, before: {cost_before:.4f} after: {cost_after:.4f}"
    print("PASS test_cost_decreases")

# ----------------------------
# Run all tests
# ----------------------------
test_prediction()
test_cost_zero_on_perfect_fit()
test_cost_is_positive()
test_cost_decreases()