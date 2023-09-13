import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
import numpy as np


values = [-3, -1, 0, 0, 1, 3, 7]
cmap = LinearSegmentedColormap.from_list('custom_colormap', ['#FF0000', '#00FF00'], N=256)
fig, ax = plt.subplots(figsize=(6, 2))
norm = Normalize(vmin=min(values), vmax=max(values))
normalized_values = [norm(val) for val in values]

cbar = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax, orientation='horizontal')
cbar.set_label('Label Values')
plt.show()
