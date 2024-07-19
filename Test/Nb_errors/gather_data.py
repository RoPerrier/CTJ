# Import necessary libraries
from CTJ import ACJ, CTJ
import pandas as pd
import numpy as np

# Define the colors and their corresponding values
colors = [('black', 0), ('g1', 160), ('g2', 106), ('g3', 209),
           ('g4', 80), ('g5', 135), ('white', 255)]

# Initialize lists to store results for ACJ and CTJ methods
# ACJ
errors_acj = []
acc_acj = []
ite_acj = []
oc_acj = np.zeros(1000)  # Array to count occurrences of errors

# ACJ with entropy
errors_acj_E = []
acc_acj_E = []
ite_acj_E = []
oc_acj_E = np.zeros(1000)  # Array to count occurrences of errors

# CTJ
errors_ctj = []
acc_ctj = []
ite_ctj = []
oc_ctj = np.zeros(1000)  # Array to count occurrences of errors

# Loop to perform 1000 iterations
for j in range(1000):
    # Perform ACJ without entropy
    _, i, a, b, _ = ACJ(
        [0, 'black'], [255, 'white'],
        [color[0] for color in colors],
        true_values=[color[1] for color in colors],
        nb_judge=1,
        max_accuracy=0.95,
        max_iteration=1000,
        sensibility=[30]
    )
    # Store results
    errors_acj.append(int(b[0]))
    acc_acj.append(a)
    ite_acj.append(i)
    if b[0] < 1000:
        oc_acj[int(b[0])] += 1
        
    # Perform ACJ with entropy
    _, i, a, b, _ = ACJ(
        [0, 'black'], [255, 'white'],
        [color[0] for color in colors],
        true_values=[color[1] for color in colors],
        nb_judge=1,
        max_accuracy=0.95,
        max_iteration=200,
        sensibility=[30],
        entropy=True
    )
    errors_acj_E.append(int(b[0]))
    acc_acj_E.append(a)
    ite_acj_E.append(i)
    if b[0] < 1000:
        oc_acj_E[int(b[0])] += 1
      
    # Perform CTJ
    _, i, a, b, _ = CTJ(
        [0, 'black'], [255, 'white'],
        [color[0] for color in colors],
        true_values=[color[1] for color in colors],
        max_accuracy=0.95,
        max_iteration=200,
        sensibility=(30, 0, 0)
    )
    errors_ctj.append(int(b[0]))
    acc_ctj.append(a)
    ite_ctj.append(i)
    if b[0] < 1000:
        oc_ctj[int(b[0])] += 1

    # Print the current iteration number
    print(j)

# ACJ data processing
data = {
    'errors': errors_acj,
    'acc': acc_acj,
    'ite': ite_acj
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Calculate mean accuracy and iterations grouped by errors
acc_mean_acj = df.groupby('errors')['acc'].mean()
ite_mean_acj = df.groupby('errors')['ite'].mean()

# Get unique error values
errors_acj = acc_mean_acj.index

# ACJ with entropy data processing
data = {
    'errors': errors_acj_E,
    'acc': acc_acj_E,
    'ite': ite_acj_E
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Calculate mean accuracy and iterations grouped by errors
acc_mean_acj_E = df.groupby('errors')['acc'].mean()
ite_mean_acj_E = df.groupby('errors')['ite'].mean()

# Get unique error values
errors_acj_E = acc_mean_acj_E.index

# CTJ data processing
data = {
    'errors': errors_ctj,
    'acc': acc_ctj,
    'ite': ite_ctj
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Calculate mean accuracy and iterations grouped by errors
acc_mean_ctj = df.groupby('errors')['acc'].mean()
ite_mean_ctj = df.groupby('errors')['ite'].mean()

# Get unique error values
errors_ctj = acc_mean_ctj.index

# Prepare data for output
data = {
    'errors_acj': errors_acj,
    'accuracy_acj': acc_mean_acj,
    'iteration_acj': ite_mean_acj,
    'occurence_acj': [oc_acj[i] for i in errors_acj],
    'errors_acj_Entropy': errors_acj_E,
    'accuracy_acj_Entropy': acc_mean_acj_E,
    'iteration_acj_Entropy': ite_mean_acj_E,
    'occurence_acj_Entropy': [oc_acj_E[i] for i in errors_acj_E],
    'errors_ctj': errors_ctj,
    'accuracy_ctj': acc_mean_ctj,
    'iteration_ctj': ite_mean_ctj,
    'occurence_ctj': [oc_ctj[i] for i in errors_ctj]
}

# Specify the output file name
output_file = 'test.csv'

# Write the data to a CSV file
with open(output_file, mode='w') as file:
    for key, values in data.items():
        line = f"{key}:" + ",".join(map(str, values)) + "\n"
        file.write(line)

print(f"Data written to {output_file}")
