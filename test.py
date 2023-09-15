import matplotlib.pyplot as plt
from tkinter import Tk

# Create your Matplotlib figure
fig, ax = plt.subplots()

# Your plotting code or other actions here
# For example:
# ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

# Create a Tkinter root window
root = Tk()

# Maximize the root window
root.state('zoomed')  # 'zoomed' maximizes the window

# Embed the Matplotlib figure in the Tkinter root window
canvas = plt.backends.backend_tkagg.FigureCanvasTk(fig, master=root)
canvas.get_tk_widget().pack(fill='both', expand=True)

# Show the plot
plt.show()
plt.tight_layout()