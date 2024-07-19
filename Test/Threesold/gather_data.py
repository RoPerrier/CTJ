# Import necessary libraries
from CTJ import ACJ, CTJ
import numpy as np

# Define the colors and their corresponding values
colors = [('black', 0), ('g1', 160), ('g2', 106), ('g3', 209),
           ('g4', 80), ('g5', 135), ('white', 255)]

# Initialize lists to store results for ACJ and CTJ methods
errors_acj = []
acc_acj = []
ite_acj = []

errors_acj_E = []
acc_acj_E = []
ite_acj_E = []

errors_ctj = []
acc_ctj = []
ite_ctj = []

# Define the sensitivity thresholds
threesold = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]

# Loop through each threshold
for a in threesold:
    
    # Temporary lists to store intermediate results for each threshold
    errors_acj_temp = []
    acc_acj_temp = []
    ite_acj_temp = []
    
    errors_acj_E_temp = []
    acc_acj_E_temp = []
    ite_acj_E_temp = []
    
    errors_ctj_temp = []
    acc_ctj_temp = []
    ite_ctj_temp = []

    # Repeat 1000 iterations for each threshold
    for j in range(1000):
        # Perform ACJ without entropy
        _, i, ac, b, _ = ACJ(
            [0, 'black'], [255, 'white'],
            [color[0] for color in colors],
            true_values=[color[1] for color in colors],
            nb_judge=1,
            max_accuracy=0.95,
            max_iteration=500,
            sensibility=[a]
        )
        errors_acj_temp.append(int(b[0]))
        acc_acj_temp.append(ac)
        ite_acj_temp.append(i)
        
        # Perform ACJ with entropy
        _, i, ac, b, _ = ACJ(
            [0, 'black'], [255, 'white'],
            [color[0] for color in colors],
            true_values=[color[1] for color in colors],
            nb_judge=1, max_accuracy=0.95,
            max_iteration=500,
            sensibility=[a],
            entropy=True
        )
        errors_acj_E_temp.append(int(b[0]))
        acc_acj_E_temp.append(ac)
        ite_acj_E_temp.append(i)
        
        # Perform CTJ
        _, i, ac, b, _ = CTJ(
            [0, 'black'], [255, 'white'],
            [color[0] for color in colors],
            true_values=[color[1] for color in colors],
            max_accuracy=0.95,
            max_iteration=100,
            sensibility=(a, 0, 0)
        )
        errors_ctj_temp.append(int(b[0]))
        acc_ctj_temp.append(ac)
        ite_ctj_temp.append(i)
        
        # Print the current iteration and threshold
        print(j)
        print(a)
    
    # Calculate and store the mean results for the current threshold
    errors_acj.append(np.array(errors_acj_temp).mean())
    acc_acj.append(np.array(acc_acj_temp).mean())
    ite_acj.append(np.array(ite_acj_temp).mean())
    
    errors_acj_E.append(np.array(errors_acj_E_temp).mean())
    acc_acj_E.append(np.array(acc_acj_E_temp).mean())
    ite_acj_E.append(np.array(ite_acj_E_temp).mean())
    
    errors_ctj.append(np.array(errors_ctj_temp).mean())
    acc_ctj.append(np.array(acc_ctj_temp).mean())
    ite_ctj.append(np.array(ite_ctj_temp).mean())

# Create a DataFrame to store all the results
data = {
    'threesold': threesold,
    'number_of_errors_acj': errors_acj,
    'accuracy_acj': acc_acj,
    'iteration_acj': ite_acj,
    'number_of_errors_acj_Entropy': errors_acj_E,
    'accuracy_acj_Entropy': acc_acj_E,
    'iteration_acj_Entropy': ite_acj_E,
    'number_of_errors_ctj': errors_ctj,
    'accuracy_ctj': acc_ctj,
    'iteration_ctj': ite_ctj
}

# Specify the output file name
output_file = 'test.csv'

# Write the data to a CSV file
with open(output_file, mode='w') as file:
    for key, values in data.items():
        line = f"{key}:" + ",".join(map(str, values)) + "\n"
        file.write(line)

print(f"Data written to {output_file}")