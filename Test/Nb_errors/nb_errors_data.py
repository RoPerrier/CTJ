import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

def read_data(line):
    key, values = line.strip().split(':')
    values = list(map(float, values.split(',')))
    return key, values

with open('30.csv', 'r') as f:
    lines = f.readlines()

data = {}

for line in lines:
    key, values = read_data(line)
    data[key] = values

number_of_errors = data['number_of_errors']
accuracy_acj = data['accuracy_acj']
accuracy_acj_Entropy = data['accuracy_acj_Entropy']
accuracy_ctj = data['accuracy_ctj']
iteration_acj = data['iteration_acj']
iteration_acj_Entropy = data['iteration_acj_Entropy']
iteration_ctj = data['iteration_ctj']
occurence_acj = data['occurence_acj']
occurence_acj_Entropy = data['occurence_acj_Entropy']
occurence_ctj = data['occurence_ctj']

def plot_regression(x, y, label, marker, i, w):
    x=np.array(np.linspace(0, 5, len(y)))
    y=np.array(y)
    x = x.reshape(-1, 1)
    model = LinearRegression().fit(x, y, sample_weight=w)
    y_pred = model.predict(x)
    plt.plot(np.linspace(0, i-1, i), y_pred[:i], label=f'{label} (linear regression)', marker = marker)
    b = model.coef_[0]
    a = model.intercept_
    print(a,b)
    return a,b

nb_values_plotted = 6
print("Accuracy")

#Plot accuracy
a1, b1 = plot_regression(number_of_errors, accuracy_acj, label="ACJ inversion error", marker='x', i=nb_values_plotted, w=occurence_acj[:len(number_of_errors)])
a2, b2 = plot_regression(number_of_errors, accuracy_acj_Entropy, label="ACJ variant inversion error", marker='1', i=nb_values_plotted, w=occurence_acj_Entropy[:len(number_of_errors)])

from scipy.optimize import curve_fit

def plot_log_regression(x, y, label, marker, i):
    def log_func(x, a, b):
        return a + b * np.log(x)
    
    popt_log, _ = curve_fit(log_func, np.arange(1, len(y) + 1), y)
    y_pred_log = log_func(np.arange(1, len(y) + 1), *popt_log)
    
    a, b = popt_log
    print(a,b)
    
    plt.plot(np.linspace(0, i-1, i), y_pred_log[:i], label=f'{label} (logarithmic regression)', marker=marker)
    return a,b

a3,b3 = plot_log_regression(number_of_errors, accuracy_ctj, label="CTJ inversion error", marker='s', i=nb_values_plotted)

plt.title("Model accuracy as a function\nof the number of errors", fontsize=16)
plt.xlabel("Number of errors", fontsize=14)
plt.ylabel('Accuracy', fontsize=14)
plt.legend()

plt.show()

print("Iteration")

# Plot iteration
a1, b1 = plot_regression(number_of_errors, iteration_acj, label="ACJ inversion error", marker='x', i=nb_values_plotted, w=occurence_acj[:len(number_of_errors)])
a2, b2 = plot_regression(number_of_errors, iteration_acj_Entropy, label="ACJ variant inversion error", marker='1', i=nb_values_plotted, w=occurence_acj_Entropy[:len(number_of_errors)])
a3, b3 = plot_regression(number_of_errors, iteration_ctj, label="CTJ inversion error", marker='s', i=nb_values_plotted, w=occurence_ctj[:len(number_of_errors)])

plt.title("Number of model iterations as a\nfunction of the number of errors", fontsize=16)
plt.xlabel("Number of errors", fontsize=14)
plt.ylabel("Number of iterations", fontsize=14)
plt.legend()

plt.show()

print("occurence")

# Plot proba
def plot_exp_regression(x, y, label, marker,i):
    def exp_func(x, a, b):
        return a * np.exp(b * np.array(x))

    popt_exp, _ = curve_fit(exp_func, x, y, p0=(1, 0.1))
    y_pred_exp = exp_func(x, *popt_exp)
    a, b = popt_exp
    print(a,b)
    plt.plot(np.linspace(0, i-1, i), y_pred_exp[:i], label=label, marker=marker)
    return a,b

plot_exp_regression(number_of_errors, np.array(occurence_acj)/sum(occurence_acj), label="ACJ inversion error", marker='x', i=nb_values_plotted)
plot_exp_regression(number_of_errors, np.array(occurence_acj_Entropy)/sum(occurence_acj_Entropy), label="ACJ variant inversion error", marker='1', i=nb_values_plotted)
plot_exp_regression(number_of_errors, np.array(occurence_ctj)/sum(occurence_ctj), label="CTJ inversion error", marker='s', i=nb_values_plotted)

plt.title("Probability of making errors", fontsize=16)
plt.xlabel("Number of errors", fontsize=14)
plt.ylabel("Probability", fontsize=14)
plt.legend()

plt.show()