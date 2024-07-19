import matplotlib.pyplot as plt

def read_data(line):
    key, values = line.strip().split(':')
    values = list(map(float, values.split('\t')))
    return key, values

with open('error_scale_4.csv', 'r') as f:
    lines = f.readlines()

data = {}

for line in lines:
    key, values = read_data(line)
    data[key] = values

number_of_errors = data['number_of_errors']
accuracy = data['accuracy']
iteration = data['iteration']
occurence = data['occurence']

fig, ax1 = plt.subplots()

line1, = ax1.plot(number_of_errors, accuracy, 'bo', label='Accuracy')
ax1.set_xlabel('Number of Errors')
ax1.set_ylabel('Accuracy', color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
line2, = ax2.plot(number_of_errors, iteration, 'go', label='Iteration')
ax2.set_ylabel('Iteration', color='g')
ax2.tick_params(axis='y', labelcolor='g')

ax3 = ax1.twinx()

ax3.spines['right'].set_position(('outward', 60))  # Décaler de 60 points
line3, = ax3.plot(number_of_errors, occurence, 'ro', label='Occurrence')
ax3.set_ylabel('Occurrence', color='r')
ax3.tick_params(axis='y', labelcolor='r')

lines = [line1, line2, line3]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='center left', bbox_to_anchor=(0.3, 0.7))

plt.title('CTJ Scale Errors Analysis where error_value=|4|:\n Accuracy, Iteration, and Occurrence vs. Number of Errors')

plt.show()