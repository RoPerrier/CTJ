import matplotlib.pyplot as plt
import pandas as pd

# Load the data from a CSV file into a DataFrame
data = pd.read_csv('real_test.csv')

# Extract unique values from the 'Judge' and 'Metric' columns
judges = data['Judge'].unique()
metrics = data['Metric'].unique()

models = ['Rubric', 'ACJ', 'ACJ variant', 'CTJ']

for metric in ['accuracy','time']:
    
    # Create a new figure with a specific size to add clarity
    plt.figure(figsize=(10, 6))
    
    # Loop through each model
    for model in models:
        # Filter the data to include only rows where 'Metric' is 'accuracy' and select only the columns for 'Judge' and the current model
        model_data = data[data['Metric'] == metric][['Judge', model]]
        
        # Plot the accuracy for the current model against the judges
        plt.plot(model_data['Judge'], model_data[model], marker='o', label=model)
    
    # Display the plot
    plt.title(f'{metric} depending on the judges')
    plt.xlabel('Judges')
    plt.ylabel(f'{metric}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()