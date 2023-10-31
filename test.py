import matplotlib.pyplot as plt

# Sample data
x = [1, 2, 3, 4, 5]
y = [10, 15, 13, 35, 17]

# Create a plot with specified axis limits
plt.plot(x, y, 'ro-')  # 'ro-' specifies red color, circles for markers, and solid lines
plt.axis([0, 6, 0, 20])  # Set x-axis limits from 0 to 6 and y-axis limits from 0 to 20

# Show the plot
plt.show()
