import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QLineEdit,QHBoxLayout
from PyQt5.QtGui import QIntValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.font_manager as fm  # For font management
from matplotlib.patches import FancyBboxPatch,PathPatch,Polygon
from matplotlib.path import Path


# Initialize variables to store data
track = ""
fuel = []
tyre = []
results_date = []
rules = {}
driver_data = {}

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
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.figure.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.tick_params(labelrotation=0, labelcolor='white', labelsize=12)
        self.canvas = FigureCanvas(self.figure)
        
        # Create a vertical layout for the graph
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Graph Window')
        self.setGeometry(200, 200, 600, 400)  # (x, y, width, height)

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
        names = list(driver_data)

        
        # Iterate over the keys and values of the dictionary
        for key, value in driver_data.items():
            quali = int(driver_data[key]["Race Position"][0])
            endlap = int(driver_data[key]["Race Position"][2])
            overtakes = endlap - quali
            
            qualilist.append(quali)
            endlaplist.append(endlap)
            overtakeslist.append(overtakes)

        # Sort the data by values in ascending order
        
        int_array1 = np.array(overtakeslist, dtype=int)
        sorted_values = np.sort(int_array1)[::-1]
        sorted_qualilist = np.array(qualilist)[int_array1.argsort()][::-1]
        sorted_endlaplist = np.array(endlaplist)[int_array1.argsort()][::-1]
        sorted_names= np.array(names)[int_array1.argsort()][::-1]

        label_colors = [color_mapping[name] for name in sorted_names]
        #fig = plt.figure(figsize=(8, 6), facecolor='lightgray')
        # Create a bar chart
        plt.barh(sorted_names, sorted_values, color=label_colors)
        fontsize = 12  # Adjust this value to change the font size
        fontweight = 'bold'  # Set to 'bold' for bold text
        bbox_color = 'lightcoral'
        text = ""
        arrow_gain_properties = dict(arrowstyle="->", facecolor='red', edgecolor='green')
        arrow_lose_properties = dict(arrowstyle="<-", facecolor='red', edgecolor='red')
        arrows_location = 8
        for i in range(len(sorted_names)):
            x = sorted_values[i]
            y = sorted_names[i]
            if x < 0:
                plt.text(x, i, str(abs(x)), va='center', ha='right', color="white",fontsize=fontsize,fontweight=fontweight)
                plt.text(0.3, i, y, va='center', ha='left', color="white",fontsize=fontsize,fontweight=fontweight)
                plt.text(arrows_location, i, sorted_qualilist[i], va='center', ha='right', color="white",fontsize=fontsize,fontweight=fontweight)
                plt.annotate(text, xy=(arrows_location+1, y), xytext=(arrows_location+0.1, y),arrowprops=arrow_gain_properties)
                plt.text(arrows_location+1.1, i, sorted_endlaplist[i], va='center', ha='left', color="white",fontsize=fontsize,fontweight=fontweight)

            elif x > 0:
                plt.text(x, i, str(abs(x)), va='center', ha='left',color="white",fontsize=fontsize, fontweight=fontweight)
                plt.text(-0.3, i, y, va='center', ha='right', color="white",fontsize=fontsize,fontweight=fontweight)
                plt.text(-arrows_location, i, sorted_qualilist[i], va='center', ha='left', color="white",fontsize=fontsize,fontweight=fontweight)
                plt.annotate(text, xy=(-arrows_location-0.1, y), xytext=(-arrows_location-1, y),arrowprops=arrow_lose_properties)
                plt.text(-arrows_location-1.1, i, sorted_endlaplist[i], va='center', ha='right', color="white",fontsize=fontsize,fontweight=fontweight)
            else:
                #plt.text(0, i, '0', va='center', ha='center',color="white",fontsize=fontsize, fontweight=fontweight)
                plt.text(0, i, y, va='center', ha='center', color="white",fontsize=fontsize,fontweight=fontweight)


        # Add labels and a title
        plt.axis("off")
        plt.ylabel('Driver', fontname="Comic Sans MS")
        plt.title("Overtakes at the end of lap "+self.lap.text(),color="white")
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
        print(driver_data["E Tanolo"]["Race Position"][int(lap.text())])
        self.graph_window = OvertakesWindow(lap)
        self.graph_window.plot_graph()
        self.graph_window.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

