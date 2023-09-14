import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Sample data
data = [[14, 'white'], [14, 'white'], [14, 'white'], [8, 'yellow']]

# Create a figure and axis
fig, ax = plt.subplots()

# Create a horizontal stacked bar chart
bottom = 0
for size, color in data:
    ax.barh(0, size, color=color, left=bottom)
    bottom += size


# List image files in the directory
image_files = [f for f in os.listdir('tyres') if f.endswith('.png')]  # Adjust the file extension as needed

# Loop through image files and add them to the plot
for i, image_file in enumerate(image_files):
    # Load the image
    image_path = os.path.join('tyres', image_file)
    image = plt.imread(image_path)

    # Create an OffsetImage with the loaded image
    imagebox = OffsetImage(image, zoom=0.1)  # Adjust the zoom factor as needed

    # Define the coordinates where you want to place each image
    image_x = 5 + i * 10  # Adjust the x-coordinate to separate the images
    image_y = 0  # Adjust the y-coordinate

    # Create an AnnotationBbox to display the image
    ab = AnnotationBbox(imagebox, (image_x, image_y), frameon=False)
    ax.add_artist(ab)

ax.set_xlabel('Category')
ax.set_ylabel('Value')
ax.set_title('Horizontal Stacked Bar Chart')

plt.show()
