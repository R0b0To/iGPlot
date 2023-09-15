import matplotlib.pyplot as plt
import numpy as np

# Create some example data that starts at x = 0
x = np.arange(0, 6)  # Data starts at x = 0
y = [1, 4, 2, 5, 3, 6]

# Create the first set of axes
fig, ax1 = plt.subplots()

# Plot the data on the first set of axes
ax1.plot(x, y, label='Y1', color='b')
ax1.set_xlabel('X-axis')

# Set the x-axis limits to start at x = -1
ax1.set_xlim(-1, max(x))  # Adjust the x-axis limits to start at -1

# Change the label of the first tick to "Start at the coords (0,0)"
new_xticklabels = ["Start at the coords (0,0)"] + [str(val) for val in x[1:]]
ax1.set_xticklabels(new_xticklabels)

# Add a legend
ax1.legend(loc='upper left')

plt.show()
