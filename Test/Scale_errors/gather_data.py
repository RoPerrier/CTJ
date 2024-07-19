# Import necessary libraries
import numpy as np
import pandas as pd
from CTJ import CTJ

# Initialize lists to store results for the CTJ method
errors_ctj_scale = []
acc_ctj_scale = []
ite_ctj_scale = []
pb_ctj = np.zeros(1000)  # Array to count occurrences of errors

# Define the colors and their corresponding values
colors = [('black', 0), ('g1', 160), ('g2', 106), ('g3', 209),
           ('g4', 80), ('g5', 135), ('white', 255)]

# Loop to perform 1000 iterations
for j in range(1000):
    # Perform the CTJ method
    _, i, a, b, _ = CTJ(
        [0, 'black'], [255, 'white'],
        [color[0] for color in colors],
        true_values=[color[1] for color in colors],
        max_accuracy=0.95,
        max_iteration=200,
        sensibility=(0, 1, 0.5)
    )
    # Store results
    errors_ctj_scale.append(int(b[1]))
    acc_ctj_scale.append(a)
    ite_ctj_scale.append(i)
    # Update the occurrence counter for errors
    if b[1] < 1000:
        pb_ctj[int(b[1])] += 1
    # Print the current iteration number
    print(j)

# Create a DataFrame to store the results
data = {
    'errors': errors_ctj_scale,
    'acc': acc_ctj_scale,
    'ite': ite_ctj_scale
}

df = pd.DataFrame(data)

# Calculate mean accuracy and iterations grouped by error count
acc_mean_ctj_scale = df.groupby('errors')['acc'].mean()
ite_mean_ctj_scale = df.groupby('errors')['ite'].mean()

# Get the unique error values
errors_ctj_scale = acc_mean_ctj_scale.index

# Specify the output file name
output_file = 'test.csv'

# Prepare data for output
data = {
    "number_of_errors": errors_ctj_scale,
    "accuracy": acc_mean_ctj_scale,
    "iteration": ite_mean_ctj_scale,
    "occurrence": [pb_ctj[i] for i in errors_ctj_scale],
}

# Write the data to a CSV file
with open(output_file, mode='w') as file:
    for key, values in data.items():
        line = f"{key}:" + "\t".join(map(str, values)) + "\n"
        file.write(line)

print(f"Data written to {output_file}")
