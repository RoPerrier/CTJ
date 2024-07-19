import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit

def read_data(line):
    key, values = line.strip().split(':')
    values = list(map(float, values.split(',')))
    return key, values

with open('threshold.csv', 'r') as f:
    lines = f.readlines()

data = {}

for line in lines:
    key, values = read_data(line)
    data[key] = values

threshold = data['threshold']
number_of_errors_acj = data['number_of_errors_acj']
number_of_errors_acj_Entropy = data['number_of_errors_acj_Entropy']
number_of_errors_ctj = data['number_of_errors_ctj']
accuracy_acj = data['accuracy_acj']
accuracy_acj_Entropy = data['accuracy_acj_Entropy']
accuracy_ctj = data['accuracy_ctj']
iteration_acj = data['iteration_acj']
iteration_acj_Entropy = data['iteration_acj_Entropy']
iteration_ctj = data['iteration_ctj']

def plot_regression(x, y, label, marker,i):
    x=np.array(x)
    y=np.array(y)
    x = x.reshape(-1, 1)
    model = LinearRegression().fit(x, y)
    y_pred = model.predict(x)
    plt.plot(x[:i], y_pred[:i], label=f'{label} (linear regression)', marker = marker)
    b = model.coef_[0]
    a = model.intercept_
    print(a,b)
    return a,b

nb_values_plotted = 9

print("Accuracy")
a1, b1 = plot_regression(threshold, accuracy_acj, label="ACJ inversion error", marker='x',i=nb_values_plotted)
a2, b2 = plot_regression(threshold, accuracy_acj_Entropy, label="ACJ variant inversion error", marker='1',i=nb_values_plotted)
a3, b3 = plot_regression(threshold, accuracy_ctj, label="CTJ inversion error", marker='s',i=nb_values_plotted)

plt.title("Model accuracy based on a\njudge's perception threshold", fontsize = 14)
plt.xlabel("Perception threshold", fontsize = 12)
plt.ylabel('Accuracy', fontsize = 12)
plt.legend()

plt.show()

print("Iteration")
# Plot iteration
a1, b1 = plot_regression(threshold, iteration_acj, label="ACJ inversion error", marker='x', i=nb_values_plotted)
a2, b2 = plot_regression(threshold, iteration_acj_Entropy, label="ACJ variant inversion error", marker='1', i=nb_values_plotted)

def plot_exp_regression(x, y, label, marker,i):
    def exp_func(x, a, b):
        return a * np.exp(b * np.array(x))

    popt_exp, _ = curve_fit(exp_func, x, y, p0=(1, 0.1))
    y_pred_exp = exp_func(x, *popt_exp)
    a, b = popt_exp
    print(a,b)
    plt.plot(x[:i], y_pred_exp[:i], label=f'{label} (exponential regression)', marker=marker)
    return a,b
    
a3, b3 = plot_exp_regression(threshold, iteration_ctj, label="CTJ inversion error", marker='s', i=nb_values_plotted)

plt.title("Number of model iterations based on a\njudge's perception threshold", fontsize = 14)
plt.xlabel("Perception threshold", fontsize = 12)
plt.ylabel("Number of iterations", fontsize = 12)
plt.legend()

plt.show()

print("Iteration")
# Plot iteration
a1, b1 = plot_exp_regression(threshold, number_of_errors_acj, label="ACJ inversion error", marker='x',i=nb_values_plotted)
a2, b2 = plot_exp_regression(threshold, number_of_errors_acj_Entropy, label="ACJ variant inversion error", marker='1',i=nb_values_plotted)
a3, b3 = plot_exp_regression(threshold, number_of_errors_ctj, label="CTJ inversion error", marker='s',i=nb_values_plotted)

plt.title("Number of model errors based on a\njudge's perception threshold", fontsize = 14)
plt.xlabel("Perception threshold", fontsize = 12)
plt.ylabel("Number of errors", fontsize = 12)
plt.legend()

plt.show()
