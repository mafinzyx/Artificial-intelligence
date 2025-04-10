import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data

data = get_data()
inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

X = np.hstack((np.ones((len(x_train), 1)), x_train.reshape(-1, 1)))
Y = y_train.reshape(-1,1)

theta_best = np.linalg.solve(X.T @ X, X.T @ Y)
print("Closed-form solution:", theta_best)

def mse(y_pred, y):
    return np.mean((y_pred-y)**2)

# calculate errors
y_pred = X @ theta_best
mse_train = mse(y_pred,Y)
print("MSE (closed form) TRAIN\t",mse_train)

X_test = np.hstack((np.ones((len(x_test), 1)), x_test.reshape(-1, 1)))
Y_test = y_test.reshape(-1,1)

y_pred_test = X_test @ theta_best
mse_test = mse(y_pred_test,Y_test)

print("MSE (closed form) TEST\t",mse_test)

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

x_mean = np.mean(x_train)
x_std  = np.std(x_train)
y_mean = np.mean(y_train)
y_std  = np.std(y_train)

# standardize x_train and y_train for learning
x_train = (x_train - x_mean) / x_std
y_train = (y_train - y_mean) / y_std

X = np.hstack((np.ones((len(x_train), 1)), x_train.reshape(-1, 1)))
Y = y_train.reshape(-1,1)

# calculate theta using Batch Gradient Descent   
theta_best = np.random.randn(2, 1)
learning_rate = 0.001
m = X.shape[0]

for epoch in range(10000):
    y_pred = X @ theta_best
    gradient = (2/m) * X.T @ (y_pred - Y)
    theta_best -= learning_rate * gradient

theta_best = theta_best.flatten()
print("Gradient Descent solution:", theta_best)

# calculate error
x_standarized = (x_test - x_mean) / x_std
y_results = theta_best[1] * x_standarized + theta_best[0]
y_pred = (y_results * y_std) + y_mean

mse_gd = mse(y_pred, y_test)
print("MSE (Gradient Descent):", mse_gd)     

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
x_standarized = (x - x_mean) / x_std # standarize x
y_standarized = float(theta_best[0]) + float(theta_best[1]) * x_standarized
y = (y_standarized * y_std) + y_mean
plt.plot(x, y, color='red')
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()