import numpy as np
# can call predict function, LinearRegression
# the function will return the prediction which is y_hat
def linearRegression (w, x, b):
  #formular f_w_b or y_hat = wx + b 
  return w * x + b

# find how off our prediction is from the actual target value y
def cost_function(x, y, w, b):
  #formular J(w,b) = (1/2m) * Σ(y_hat - y)²
  total_training = len(x)
  for i in range (total_training):
    y_hat = linearRegression(w, x[i], b)
    j_wb += (y_hat - y[i]) ** 2
  return j_wb/(2 * total_training)

# gradient descent function to find the local minimun
def gradient_descent(x, y, w, b, alpha, iteration):
  # formular:
  # w = w - α * dJ_wb/dw
  # b = b - α * dJ_wb/db
  d_w =  