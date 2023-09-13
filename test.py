import matplotlib.pyplot as plt
import numpy as np

# Your data
data = {
    "D Mansell": {"times": [26.373, 25.933, 26.511, 26.926]},
    "A Johnson": {"times": [27.123, 25.832, 27.456, 27.789]},
    "B Smith": {"times": [28.567, 29.012, 28.123, 28.456]}
}

# Calculate medians for each dataset
medians = {name: np.median(data[name]["times"]) for name in data}

# Sort the data by lower median
sorted_data = dict(sorted(data.items(), key=lambda item: medians[item[0]]))

# Extract names and times from the sorted data dictionary
names = list(sorted_data.keys())
times = [sorted_data[name]["times"] for name in names]

# Calculate the average median of all drivers
average_median = np.mean(list(medians.values()))

# Define custom colors for the boxes
box_colors = ['lightblue', 'lightgreen', 'lightcoral']

# Create a horizontal box plot for each name with custom box colors
plt.figure(figsize=(8, 6))

# Use patch_artist=True to access the box objects
boxes = plt.boxplot(times, labels=names, vert=False, patch_artist=True)

# Set the box colors
for box, color in zip(boxes['boxes'], box_colors):
    box.set(facecolor=color)

# Add a horizontal line for the average median
plt.axvline(x=average_median, color='red', linestyle='--', label=f'Average Median ({average_median:.2f})')

# Add median text annotations next to each box
for name, median in medians.items():
    plt.text(median, names.index(name) + 1, f'{median:.2f}', va='center', ha='left', color='black')

plt.title("Horizontal Box Plot of Average Time (Sorted by Lower Median)")
plt.xlabel("Average Time")
plt.ylabel("Name")
plt.grid(True)
plt.legend()  # Add a legend for the average median line

# Show the plot
plt.show()
