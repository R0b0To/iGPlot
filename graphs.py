import csv,sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget,QLineEdit,QHBoxLayout
from PyQt5.QtGui import QIntValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.font_manager as fm  # For font management
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


# Initialize variables to store data
track = ""
fuel = []
tyre = []
results_date = []
rules = {}
driver_data = {}
tyre = {'Super soft tyres': '#d66e67',
          'Soft tyres': '#D9C777',
          'Medium tyres': '#c9c9c9',
          'Hard tyres': '#e77b00',
          'Intermediate wet tyres': 'green',
          'Full wet tyres': 'blue'}
# Function to calculate brightness of a color
def get_brightness(rgba_color):
    r, g, b, _ = rgba_color
    # Calculate brightness using the formula: brightness = 0.299*R + 0.587*G + 0.114*B
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    return brightness
with open('full_report.csv', 'r',encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Read the first row
    track = next(csv_reader, None)[1]
    # Read the second row
    rules_row = next(csv_reader, None)

    for i in range(0, len(rules_row), 2):
        key = rules_row[i]
        value = rules_row[i + 1]
        rules[key.lower()] = value.lower() 
    # Read the third row
    results_date = next(csv_reader, None)

    for row in csv_reader:
         # Ensure the row has elements to extract data
        if len(row) >= 1:
         driver_name = row[0]
         # Check if the driver name is already in the dictionary
         if driver_name in driver_data:
                if(row[2] == "PIT"):
                    pit_info = row[3].split("/")
                    driver_data[driver_name]["Lap"][-1] = [driver_data[driver_name]["Lap"][-1],pit_info[1].strip(),pit_info[0].strip()]
                else:
                    driver_data[driver_name]["Lap"].append(row[2])
                    driver_data[driver_name]["Lap Time"].append(row[3])
                    driver_data[driver_name]["Gap"].append(row[4])
                    driver_data[driver_name]["Average Speed"].append(row[5])
                    driver_data[driver_name]["Race Position"].append(row[6])
               
         else:
                # If the driver doesn't exist, create a new entry with the driver's data as a list
                driver_data[driver_name] = {
                    "Team": row[1],
                    "Lap Time":["Q"], #Q is for qualifying
                    "Gap":["Q"],
                    "Average Speed":["Q"], 
                    "Lap": [["Q",row[3]]],
                    "Race Position": [row[6]]
                }             
csv_file.close()

class OvertakesWindow(QWidget):
    def __init__(self,lap):
        super().__init__()
        self.lap = lap
        self.initUI()

    def initUI(self):
        # Create a Matplotlib figure and axis for the graph
        font = fm.FontProperties(fname='Roboto.ttf') 
        self.figure, self.ax = plt.subplots()
        self.figure.set_facecolor('#31333b')
        self.ax.set_facecolor('#31333b')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.tick_params(labelrotation=0, labelcolor='white', labelsize=12)
        self.canvas = FigureCanvas(self.figure)
        
        # Create a vertical layout for the graph
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Graph Window')
        self.setGeometry(400, 400, 1200, 800)  # (x, y, width, height)

    def plot_graph(self):
        # Create sample data (a simple sine wave)
        # Data
        # Create a figure with a specified background color
        
        color_mapping = {}
        with open("colors.txt", "r",encoding='utf-8') as file:
             for line in file:
                line = line.strip()
                if line:
                    name, color_hex = line.split(":")
                    color_mapping[name.strip()] = color_hex.strip()
        overtakeslist = []
        qualilist = []
        endlaplist = []
        starting_tyre = []
        names = list(driver_data)
        
        
        # Iterate over the keys and values of the dictionary
        for key, value in driver_data.items():
            quali = int(driver_data[key]["Race Position"][0])
            if(len(driver_data[key]["Race Position"])>int(self.lap.text())):
             endlap = int(driver_data[key]["Race Position"][int(self.lap.text())])         
            else:
             endlap = int(driver_data[key]["Race Position"][-1])
            overtakes =  endlap - quali
            
            starting_tyre.append(tyre[driver_data[key]["Lap"][0][1].split('/')[0].strip()])
            qualilist.append(quali)
            endlaplist.append(endlap)
            overtakeslist.append(overtakes)
    
        


        int_array1 = np.array(overtakeslist, dtype=int)
        sorted_values = np.sort(int_array1)[::-1]
        sorted_qualilist = np.array(qualilist)[int_array1.argsort()][::-1]
        sorted_endlaplist = np.array(endlaplist)[int_array1.argsort()][::-1]
        sorted_names= np.array(names)[int_array1.argsort()][::-1]

        label_colors = [color_mapping[name] for name in sorted_names]
        #fig = plt.figure(figsize=(8, 6), facecolor='lightgray')
        # Create a bar chart
        plt.barh(sorted_names, sorted_values, color=label_colors)
        # Set background colors for y-axis labels based on driver colors
        for label, color in zip(self.ax.get_yticklabels(), label_colors):
            label.set_bbox({'facecolor': color, 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
        # Automatically choose font color based on background color brightness
        for label in self.ax.get_yticklabels():
            background_color = label.get_bbox_patch().get_facecolor()
            brightness = get_brightness(background_color)
            if brightness < 0.5:  # You can adjust the threshold as needed
                label.set_color('white')
            else:
                label.set_color('black')

        font_size = 12        
        # Add images for each driver
        for i, driver in enumerate(sorted_names):
            img_path = f'downloaded_images/{driver}.png'  # Assuming images are in a folder named "images"
            try:
                label_color = self.ax.get_yticklabels()[i].get_color()
                img = plt.imread(img_path)
                imagebox = OffsetImage(img, zoom=0.15)
                if sorted_values[i]<0:
                    ab = AnnotationBbox(imagebox, (sorted_values[i], i), frameon=False,box_alignment=(0,0.5))
                    self.ax.text(0, i, "P"+str(sorted_qualilist[i]), va='center', ha= "left", color=label_color, fontsize=font_size,weight='bold')
                    self.ax.text(sorted_values[i], i, "P"+str(sorted_endlaplist[i]), va='center', ha= "right", color=label_color,fontsize=font_size,weight='bold')
                    self.ax.text(sorted_values[i]/2, i, ">"*abs(sorted_values[i]), va='center', ha= "center", color=label_color,fontsize=font_size,weight='bold')
                elif sorted_values[i]>0:  
                    ab = AnnotationBbox(imagebox, (sorted_values[i], i), frameon=False,box_alignment=(1,0.5))
                    self.ax.text(0, i, "P"+str(sorted_qualilist[i]), va='center', ha= "right", color=label_color,fontsize=font_size,weight='bold')
                    self.ax.text(sorted_values[i], i, "P"+str(sorted_endlaplist[i]), va='center', ha= "left", color=label_color,fontsize=font_size,weight='bold')
                    self.ax.text(sorted_values[i]/2, i, "<"*abs(sorted_values[i]), va='center', ha= "center", color=label_color,fontsize=font_size,weight='bold')
                else:
                    ab = AnnotationBbox(imagebox, (sorted_values[i], i), frameon=False,box_alignment=(0,0.5))  
                self.ax.add_artist(ab)
            except FileNotFoundError:
                pass  # If image file not found, continue without adding an image
            
        plt.xlim(sorted_values[-1]-1, sorted_values[0]+1)
        plt.yticks(weight='bold')
        
        self.ax.set_yticks(np.arange(len(sorted_names)))
        self.ax.get_xaxis().set_visible(False)
        ax2 = self.ax.twinx()
        ax2.barh(sorted_names, sorted_values, alpha=0) 
        ax2.spines['right'].set_position(('axes',0))  # Adjust the position of the right axis
   
        ax2.set_yticklabels( (sorted_values) )

        for label in ax2.get_yticklabels():
            int_label = int(label.get_text())
            if int_label > 0:
                label.set_bbox({'facecolor': "#ba5e5e", 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
            elif int_label < 0:
                label.set_bbox({'facecolor': "#5eba7d", 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
            else:
                label.set_bbox({'facecolor': "#f1f2f3", 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
        ax2.set_yticklabels( abs(sorted_values) )
        ax2.tick_params(labelcolor='white', labelsize=12)
        for label in ax2.get_yticklabels():
            background_color = label.get_bbox_patch().get_facecolor()
            brightness = get_brightness(background_color)
            if brightness < 0.7:  # You can adjust the threshold as needed
                label.set_color('white')
            else:
                label.set_color('black')
        self.ax.invert_xaxis()
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        ax2.set_xlabel('Position')
        plt.title("Overtakes at the end of lap "+self.lap.text(),color="white",fontsize=16,weight='bold')
        #plt.show()
        # Redraw the canvas
        self.canvas.draw()
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()   

    def initUI(self):
        input_field = QLineEdit(self)
        # Create three buttons
        button1 = QPushButton('Overtakes at the end of lap', self)
        button2 = QPushButton('Button 2', self)
        button3 = QPushButton('Button 3', self)

        # Create a validator to accept only integers from 0 to 99 (2 digits)
        validator = QIntValidator(0, 99)
        input_field.setValidator(validator)
        input_field.setText('2')
        # Set the maximum width for the input field to display only 2 characters
        input_field.setMaximumWidth(30)

        # Create a horizontal layout for the first button and input field
        button1_layout = QHBoxLayout()
        button1_layout.addWidget(button1)
        button1_layout.addWidget(input_field)

        # Create a vertical layout and add buttons to it
        vbox = QVBoxLayout()
        vbox.addLayout(button1_layout)
        vbox.addWidget(button2)
        vbox.addWidget(button3)

         # Connect the button click event to the print_value function
        button1.clicked.connect(lambda: self.open_graph_window(input_field))

        # Set the layout for the window
        self.setLayout(vbox)

        # Set window properties
        self.setWindowTitle('iGP Graphs')
        #self.setGeometry(100, 100, 400, 200)  # (x, y, width, height)
    def open_graph_window(self,lap):
        self.graph_window = OvertakesWindow(lap)
        self.graph_window.plot_graph()
        self.graph_window.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

