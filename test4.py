import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

data = {
    'kapoor': {'gap': ['0', '0', '0', '790', '0']},
    'smith': {'gap': ['0.3', '1200', '1200', '0', '1200']},
    'bob': {'gap': ['0.6', '2200.0', '3200.0', '4000', '2200']}
}

# Extract all gaps at all positions


# Create a list of names
names = list(data.keys())

# Define the number of interpolated frames between data points
max_length = max(len(item['gap']) for item in data.values())
# Specify the number of frames (interpolated values) to add
num_frames = 2
# Initialize an empty result array with the adjusted length
adjusted_length = max_length + num_frames * (max_length - 1)
interpolated_data = [[] for _ in range(adjusted_length)]

# Interpolate and fill in the result array
for key, item in data.items():
    gap_array = [float(value) for value in item['gap']]  # Convert values to float
    x = np.arange(len(gap_array))
    x_interp = np.linspace(0, len(gap_array) - 1, adjusted_length)  # Interpolation positions
    gap_interp = np.interp(x_interp, x, gap_array)  # Perform linear interpolation
    for i, value in enumerate(gap_interp):
        interpolated_data[i].append(value)
        
def update(frame):
    plt.clf()
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    # Plot the current frame
    current_positions = interpolated_data[frame]
    for i in range(len(names)):
        y_pos =np.interp(current_positions[i], [min(current_positions), max(current_positions)], [0, len(names) - 1])
        print(y_pos)
        plt.plot(current_positions[i], y_pos, 'o', markersize=10, color='skyblue')
        plt.annotate(names[i], (current_positions[i], y_pos), xytext=(5, 0), textcoords='offset points', va='center')

    plt.xlabel('Gap Values (ms)')
    plt.title(f'Frame {frame + 1}/{len(interpolated_data)}')

# Create an animation
print(interpolated_data)
ani = FuncAnimation(plt.gcf(), update, frames=len(interpolated_data), repeat=False, interval=100)
#ani.save('orbita.igf', writer='imagemagick', fps=10)
plt.show()


