import csv,sys,re
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget,QLineEdit,QHBoxLayout
from PyQt5.QtGui import QIntValidator
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.animation import FuncAnimation
import os
from scipy.stats import rankdata

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')





#config
background_color = '#31333b'
font_size = 12 
default_color = 'white'





# Initialize variables to store data
track = ""
fuel, tyre, results_date = [], [], []
rules = {}
driver_data = {}
tyre = {'Super soft tyres': '#d66e67','Soft tyres': '#D9C777','Medium tyres': '#c9c9c9','Hard tyres': '#e77b00','Intermediate wet tyres': '#82a674','Full wet tyres': '#4786b3'}
color_mapping = {}
default_border_settings = {
    'figure.subplot.left': 0.088,
    'figure.subplot.right': .992,
    'figure.subplot.bottom': 0.015,
    'figure.subplot.top': 0.960,
}
plt.rcParams.update(default_border_settings)
with open("colors.txt", "r",encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        if line:
            name, color_hex = line.split(":")
            color_mapping[name.strip()] = color_hex.strip()
def toMs(time_duration):
    match = re.match(r'\+ (\d+):(\d+\.\d+)', time_duration)
    if match:
        minutes, seconds = map(float, match.groups())
        milliseconds = (minutes * 60 + seconds) * 1000
        return milliseconds
    else:
        return time_duration
def get_brightness(rgba_color):
    r, g, b, _ = rgba_color
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    return brightness
with open('full_report.csv', 'r',encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)

    track = next(csv_reader, None)[1]
    rules_row = next(csv_reader, None)

    for i in range(0, len(rules_row), 2):
        key = rules_row[i]
        value = rules_row[i + 1]
        rules[key.lower()] = value.lower() 
    # Read the third row
    results_date = next(csv_reader, None)

    for row in csv_reader:
        if len(row) >= 1:
         driver_name = row[0]
         if driver_name in driver_data:
                if(row[2] == "PIT"):
                    pit_info = row[3].split("/")
                    driver_data[driver_name]["Lap"][-1] = [driver_data[driver_name]["Lap"][-1],pit_info[1].strip(),pit_info[0].strip()]
                else:
                    driver_data[driver_name]["Lap"].append(row[2])
                    driver_data[driver_name]["Lap Time"].append(row[3])
                    if(row[4]=="-"):row[4]='0'
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
                    "Lap": [["0",row[3]]],
                    "Race Position": [row[6]]
                }
    def time_str_to_timedelta(time_str):
        minutes, seconds = map(float, time_str.split(":"))
        return timedelta(minutes=minutes, seconds=seconds)
    for driver in driver_data:
        driver_data[driver]
        indexes = [i for i, item in enumerate(driver_data[driver]["Lap"][1:]) if isinstance(item, list)]

        valid_indexes = []
        print(driver,indexes)
        for i in indexes:
            if i >= 2 and i <= len(driver_data[driver]["Lap"]) - 4:
                if i - 2 not in indexes and i - 1 not in indexes and i + 1 not in indexes and i + 2 not in indexes:
                    valid_indexes.append(i + 1)  # Adding 1 to adjust for the exclusion of the first element
        driver_data[driver]["Box Time Lost"] = []
        for index in valid_indexes:
            a = driver_data[driver]["Lap Time"][index]
            b = driver_data[driver]["Lap Time"][index+1]
            c = driver_data[driver]["Lap Time"][index-1]
            d = driver_data[driver]["Lap Time"][index+2]
            time_lost = (time_str_to_timedelta(a) + time_str_to_timedelta(b)) - (time_str_to_timedelta(c) + time_str_to_timedelta(d))
            total_seconds = time_lost.total_seconds()
            minutes = int(total_seconds // 60)
            seconds = total_seconds % 60
            driver_data[driver]["Box Time Lost"].append(total_seconds)
        if(len(driver_data[driver]["Box Time Lost"])==0): 
            driver_data[driver]["Box Time Lost"].append(20)                    
csv_file.close()
def basic_graph():
    figure, ax = plt.subplots()
    figure.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    figure.canvas.manager.window.showMaximized()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(labelrotation=0, labelcolor='white', labelsize=font_size)
   
    return(figure,ax)  
class OvertakesWindow(QWidget):
    def __init__(self,lap):
        super().__init__()
        self.lap = lap
        self.initUI()

    def initUI(self):
        self.figure, self.ax = basic_graph()
    def plot_graph(self):

        overtakeslist = []
        qualilist = []
        endlaplist = []
        starting_tyre = []
        names = list(driver_data)
        
        
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

        print(color_mapping)
        print(sorted_values)
        label_colors = [color_mapping.get(name,default_color) for name in sorted_names]

        plt.barh(sorted_names, sorted_values, color=label_colors)
       
        for label, color in zip(self.ax.get_yticklabels(), label_colors):
            label.set_bbox({'facecolor': color, 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
        for label in self.ax.get_yticklabels():
            background_color = label.get_bbox_patch().get_facecolor()
            brightness = get_brightness(background_color)
            if brightness < 0.5: 
                label.set_color('white')
            else:
                label.set_color('black')

               
        for i, driver in enumerate(sorted_names):
            img_path = f'downloaded_images/{driver}.png'  
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
                pass 
        
        plt.xlim(sorted_values[-1]-1, sorted_values[0]+1)
        plt.yticks(weight='bold')
        
        self.ax.set_yticks(np.arange(len(sorted_names)))
        self.ax.get_xaxis().set_visible(False)
        ax2 = self.ax.twinx()
        ax2.barh(sorted_names, sorted_values, alpha=0) 
        ax2.spines['right'].set_position(('axes',0))  
   
        ax2.set_yticklabels( (sorted_values), fontweight='bold' )

        for label in ax2.get_yticklabels():
            int_label = int(label.get_text())
            if int_label > 0:
                label.set_bbox({'facecolor': "#ba5e5e", 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
            elif int_label < 0:
                label.set_bbox({'facecolor': "#5eba7d", 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
            else:
                label.set_bbox({'facecolor': "#f1f2f3", 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
        ax2.set_yticklabels( abs(sorted_values) )
        ax2.tick_params(labelcolor='white', labelsize=font_size)
        for label in ax2.get_yticklabels():
            background_color = label.get_bbox_patch().get_facecolor()
            brightness = get_brightness(background_color)
            if brightness < 0.7: 
                label.set_color('white')
            else:
                label.set_color('black')
        self.ax.invert_xaxis()
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.spines['left'].set_visible(False)
    
        plt.show()

class PitTimesWindow():
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
         self.figure, self.ax = basic_graph()
       

    def plot_graph(self):
        
        medians = {name: int(sorted(driver_data[name]["Box Time Lost"])[len(driver_data[name]["Box Time Lost"]) // 2]* 10) / 10.0 for name in driver_data}
        sorted_data = dict(sorted(driver_data.items(), key=lambda item: medians[item[0]]))


        names = list(sorted_data)
        label_colors = [color_mapping.get(name,default_color) for name in names]
        times = [sorted_data[name]["Box Time Lost"] for name in names]

        boxes =plt.boxplot(times, labels=names, vert=False, patch_artist=True)
        ax2 = plt.twinx()

        box =ax2.boxplot(times,labels=names, vert=False)
        for element in ['medians', 'whiskers', 'caps','boxes','fliers']:
            for item in box[element]:
                item.set_alpha(0.0) 

        for label, color in zip(self.ax.get_yticklabels(), label_colors):
            label.set_bbox({'facecolor': color, 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
        for label in self.ax.get_yticklabels():
            background_color = label.get_bbox_patch().get_facecolor()
            brightness = get_brightness(background_color)
            if brightness < 0.5:  
                label.set_color('white')
            else:
                label.set_color('black')
        # Set the box colors
        for box, color in zip(boxes['boxes'], label_colors):
            box.set(facecolor=color)
        for i, (whisker1, whisker2, fliers,cap1,cap2) in enumerate(zip(boxes['whiskers'][::2], boxes['whiskers'][1::2],boxes['fliers'],boxes["caps"][::2],boxes["caps"][1::2])):
            cap1.set(color=label_colors[i])
            cap2.set(color=label_colors[i])
            whisker1.set(color=label_colors[i])
            whisker2.set(color=label_colors[i])
            fliers.set(marker='o', color=label_colors[i], markersize=8, markerfacecolor=label_colors[i], markeredgecolor='black', linestyle='none')
        

        ax2.spines['right'].set_position(('axes',0))  
   
        sorted_medians = dict(sorted(medians.items(), key=lambda item: item[1]))
        ax2.set_yticklabels(sorted_medians.values())
        ax2.tick_params(labelcolor='white', labelsize=font_size)
        average_median = np.mean(list(medians.values()))
        plt.axvline(x=average_median, color='#5865F2', linestyle='--', label=f'Average Median ({average_median:.2f})',alpha =1)
        plt.text(average_median, len(driver_data)+1, 'Average Median', fontsize=12, ha='center', va='center', color="white",bbox=dict(facecolor='#5865F2',edgecolor= 'none', boxstyle='round'))
        self.ax.text(average_median, -0.1, f"{average_median:.1f}", fontsize=12, ha='center', va='center', color="white",bbox=dict(facecolor='#5865F2',edgecolor= 'none', boxstyle='round'))
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        #ax2.spines['bottom'].set_visible(False)
        ax2.spines['left'].set_visible(False)
        plt.yticks(weight='bold')
        self.ax.set_yticklabels(names,fontweight='bold')
        plt.show()
        
class PitRecap():
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.figure, self.ax = basic_graph()
        self.ax.xaxis.set_ticks_position('top')
        self.ax.xaxis.set_label_position('top')
        
        
    def plot_graph(self):
        drivers_to_remove  = []
        race_laps = max(len(driver["Race Position"]) for driver in driver_data.values())
        def get_last_lap_time(driver_name,driver):
            if(len(driver["Race Position"])<race_laps):
                drivers_to_remove.append(driver_name)
                return 99
            else:
                return  int(driver["Race Position"][-1])
        sorted_drivers = sorted(driver_data.items(), key=lambda x: get_last_lap_time(x[0],x[1]))
        sorted_driver_data = dict(sorted_drivers)
        for key in drivers_to_remove:
            if key in sorted_driver_data:
                del sorted_driver_data[key]

        plt.xticks(np.arange(len(sorted_drivers[0][1]["Lap"]),step=1))
        self.ax.set_xlim(-1, len(sorted_drivers[0][1]["Lap"]))
        self.ax.set_ylim(-.5,len(sorted_drivers))
        pit_history = []
        for driver in (sorted_driver_data):    
            sublists = [item for item in sorted_driver_data[driver]["Lap"] if isinstance(item, list)]
            sublists.append([sorted_driver_data[driver]["Lap"][-1]])
            pit_history.append(sublists)
        pit_history_laps_list = []
        for item in (pit_history):
            pit = []
            for i in range(len(item) - 1):
                diff = int(item[i + 1][0]) - int(item[i][0])
                color = item[i][1]
                pit.append([diff, tyre[color.split("/")[0].strip()]])
            pit_history_laps_list.append(pit)

        bottoms = [0] * len(sorted_driver_data)
        for data, label in zip(pit_history_laps_list, list(sorted_driver_data)):
            for item in data:
                size, color = item
                bar =self.ax.barh(label, size, color=color, left=bottoms[list(sorted_driver_data).index(label)],height=0.5)
              
                bottoms[list(sorted_driver_data).index(label)] += size
                text_x = -size + bottoms[list(sorted_driver_data).index(label)]
                
                img_path = f'tyres/{color}.png'
                image = plt.imread(img_path)
                


                imagebox = OffsetImage(image, zoom=0.2) 
                imagebox.image.axes = self.ax
                ab = AnnotationBbox(imagebox, (text_x,bar[0].get_y() + bar[0].get_height() / 2), frameon=False)
                self.ax.add_artist(ab)
                self.ax.text(text_x, bar[0].get_y() + bar[0].get_height() / 2, str(size), ha='center', va='center', color='white', weight="bold",fontsize=10)
            
        label_colors = [color_mapping.get(name,default_color) for name in list(sorted_driver_data)]

        for label, color in zip(self.ax.get_yticklabels(), label_colors):
            label.set_bbox({'facecolor': color, 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})

        self.ax.tick_params(labelrotation=0, labelsize=font_size)
        for label in self.ax.get_yticklabels():
            background_color = label.get_bbox_patch().get_facecolor()
            brightness = get_brightness(background_color)
            if brightness < 0.5:  
                label.set_color('white')
            else:
                label.set_color('black') 
        plt.yticks(weight='bold')
        self.ax.tick_params(axis='x', labelcolor='white')
       
        xticks = self.ax.get_xticks()
        xticklabels = list(map(str, xticks)) 
        xticklabels[0] = 'Start'
        self.ax.set_xticks(xticks, xticklabels)
                
        self.ax.invert_yaxis()

        plt.show()
class Overtakes():
    def __init__(self):
        super().__init__()
        self.initUI()
        self.data_dict = {}
        with open('overtakes.csv', 'r',encoding='utf-8') as file:
             csv_reader = csv.reader(file)
              # Iterate over each row in the CSV file
             for row in csv_reader:
      
                if len(row) >= 2:
            
                    key = row[0].strip()  # Remove any leading/trailing whitespace
                    value = int(row[1])  # Convert the value to a float if needed
            
                    self.data_dict[key] = value
        self.sorted_items = sorted(self.data_dict.items(), key=lambda x: x[1],reverse=True)
        print(self.sorted_items)
    def initUI(self):
        self.figure, self.ax = basic_graph()
        self.ax.xaxis.set_ticks_position('top')
        self.ax.xaxis.set_label_position('top')
    def plot_graph(self):
        
        
        names =  np.array([item[0] for item in self.sorted_items])
        sorted_values = np.array([item[1] for item in self.sorted_items])

        label_colors = [color_mapping.get(name,default_color) for name in names]

        plt.barh(names, sorted_values, color=label_colors)
       
        for label, color in zip(self.ax.get_yticklabels(), label_colors):
            label.set_bbox({'facecolor': color, 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
        for label in self.ax.get_yticklabels():
            background_color = label.get_bbox_patch().get_facecolor()
            brightness = get_brightness(background_color)
            if brightness < 0.5: 
                label.set_color('white')
            else:
                label.set_color('black')

               
        for i, driver in enumerate(names):
            img_path = f'downloaded_images/{driver}.png'  
            try:
                label_color = self.ax.get_yticklabels()[i].get_color()
                img = plt.imread(img_path)
                imagebox = OffsetImage(img, zoom=0.15)
                if sorted_values[i]<0:
                    ab = AnnotationBbox(imagebox, (sorted_values[i], i), frameon=False,box_alignment=(0,0.5))
                   # self.ax.text(sorted_values[i]/2, i, ">"*abs(sorted_values[i]), va='center', ha= "center", color=label_color,fontsize=font_size,weight='bold')
                elif sorted_values[i]>0:  
                    ab = AnnotationBbox(imagebox, (sorted_values[i], i), frameon=False,box_alignment=(1,0.5))
                    #self.ax.text(sorted_values[i]/2, i, "<"*abs(sorted_values[i]), va='center', ha= "center", color=label_color,fontsize=font_size,weight='bold')
                else:
                    ab = AnnotationBbox(imagebox, (sorted_values[i], i), frameon=False,box_alignment=(0,0.5))  
                self.ax.add_artist(ab)
            except FileNotFoundError:
                pass 
        
        plt.xlim(sorted_values[-1]-1, sorted_values[0]+1)
        plt.yticks(weight='bold')
        
        self.ax.set_yticks(np.arange(len(names)))
        self.ax.get_xaxis().set_visible(False)
        ax2 = self.ax.twinx()
        ax2.barh(names, sorted_values, alpha=0) 
        ax2.spines['right'].set_position(('axes',0))  
   
        ax2.set_yticklabels( (sorted_values), fontweight='bold' )

        for label in ax2.get_yticklabels():
            int_label = int(label.get_text())
            if int_label > 0:
                label.set_bbox({'facecolor': "#ba5e5e", 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
            elif int_label < 0:
                label.set_bbox({'facecolor': "#5eba7d", 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
            else:
                label.set_bbox({'facecolor': "#f1f2f3", 'pad': 0.2, 'edgecolor': 'none', 'boxstyle': 'round'})
        ax2.set_yticklabels( abs(sorted_values) )
        ax2.tick_params(labelcolor='white', labelsize=font_size)
        for label in ax2.get_yticklabels():
            background_color = label.get_bbox_patch().get_facecolor()
            brightness = get_brightness(background_color)
            if brightness < 0.7: 
                label.set_color('white')
            else:
                label.set_color('black')
        self.ax.invert_xaxis()
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_visible(False)
        ax2.spines['left'].set_visible(False)
    
        plt.show()
class RaceVisualized():
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        
  
    def plot_graph(self):
        # Generate lap numbers as a range
        incremental_value = 0  # Initialize the incremental value
        for key, value in driver_data.items():
            for i in range(len(value['Gap'])):
                if value['Gap'][i] == 'Q':
                    value['Gap'][i] = str(incremental_value)  # Replace 'Q' with the current incremental value
                    incremental_value += 0.3  # Increment the value for the next 'Q'
        # Extract all gaps at all positions
        #gaps_at_all_positions = [[float(toMs(info['Gap'][i])) for i in range(len(info['Gap']))] for info in driver_data.values()]
        # Create a list of names
        names = list(driver_data.keys())

        # Interpolate the data for smoother animation
        max_length = max(len(item['Gap']) for item in driver_data.values())
        # Specify the number of frames (interpolated values) to add
        num_frames = 24
        # Initialize an empty result array with the adjusted length
        adjusted_length = max_length + num_frames * (max_length - 1)
        interpolated_data = [[] for _ in range(adjusted_length)]

        # Interpolate and fill in the result array
        for key, item in driver_data.items():
            gap_array = [float(toMs(value)) for value in item['Gap']]  # Convert values to float
            x = np.arange(len(gap_array))
            x_interp = np.linspace(0, len(gap_array) - 1, adjusted_length)  # Interpolation positions
            gap_interp = np.interp(x_interp, x, gap_array)  # Perform linear interpolation
            for i, value in enumerate(gap_interp):
                interpolated_data[i].append(value)


        def calculate_average(arr):
            if len(arr) == 0:
                return 0  # Avoid division by zero if the array is empty.
            else:
                total = sum(arr)
                average = total / len(arr)
                return average
        def update(frame):
            self.ax.cla()
            current_positions = interpolated_data[frame]
            average = calculate_average(current_positions)
            plt.xlim(right=average*2) 
            plt.xlim(left=-7000) 
            plt.ylim(-3,23)  # Set y-axis limits from 0 to 20  
            self.ax.grid(axis='y', linestyle='--', alpha=0.6)
            self.fig.gca().invert_xaxis()
            self.fig.gca().invert_yaxis()
            # Plot the current frame
            #print(interpolated_data[frame])
            
            for i in range(len(names)):

                if(current_positions[i]>100000):
                    print('-------------->',current_positions[i],names[i])
                    #return
                maxE = max(current_positions)
                if (maxE>50000):
                    maxE = 50000
                rankings = rankdata(current_positions)
                y_pos = rankings[i]
                #y_pos =np.interp(current_positions[i], [0, maxE], [0, len(names) - 1])
                
                
                self.ax.plot(current_positions[i], y_pos, 'o', markersize=10, color='skyblue')
                self.ax.annotate(names[i], (current_positions[i], y_pos), xytext=(5, 0), textcoords='offset points', va='center')
                img_path = f'downloaded_images/{names[i]}.png'  
                try:
                    #label_color = self.ax.get_yticklabels()[i].get_color()
                    img = plt.imread(img_path)
                    imagebox = OffsetImage(img, zoom=0.15)
                    ab = AnnotationBbox(imagebox, (current_positions[i], y_pos), frameon=False,box_alignment=(0,0.5))
                    self.ax.add_artist(ab)
                except FileNotFoundError:
                    pass 
            #clear_terminal()    
            print('frame',frame+1)            
            self.ax.set_xlabel('Gap Values (ms)')
            self.ax.set_title(f'Frame {frame + 1}/{len(interpolated_data)}')    

        print('starting')
        
        self.ani= FuncAnimation(plt.gcf(), update, frames=len(interpolated_data), repeat=False, interval=100,blit=True)
        plt.tight_layout()
        plt.show()
        self.ani.save('orbita.mp4', writer='ffmpeg', fps=24)
        


        
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()   

    def initUI(self):
        input_field = QLineEdit(self)
        # Create three buttons
        button1 = QPushButton('Overtakes at the end of lap', self)
        button2 = QPushButton('pit time loss', self)
        button3 = QPushButton('strategy', self)
        button4 = QPushButton('manual overtakes', self)
        #button5 = QPushButton('Race visualized', self)

        validator = QIntValidator(0, 99)
        input_field.setValidator(validator)
        input_field.setText('2')
        input_field.setMaximumWidth(30)

        button1_layout = QHBoxLayout()
        button1_layout.addWidget(button1)
        button1_layout.addWidget(input_field)

        vbox = QVBoxLayout()
        vbox.addLayout(button1_layout)
        vbox.addWidget(button2)
        vbox.addWidget(button3)
        #vbox.addWidget(button5)
        vbox.addWidget(button4)
        button1.clicked.connect(lambda: self.open_graph_window(input_field))
        button2.clicked.connect(lambda: self.open_graph_window_pit_times())
        button3.clicked.connect(lambda: self.open_graph_window_pit_recap())
        button4.clicked.connect(lambda: self.open_graph_window_overtakes())
        #button5.clicked.connect(lambda: self.open_graph_race())
        self.setLayout(vbox)

        self.setWindowTitle('iGP Graphs')
       
    def open_graph_window(self,lap):
        self.graph_window = OvertakesWindow(lap)
        self.graph_window.plot_graph()

    def open_graph_window_pit_times(self):
        self.graph_window = PitTimesWindow()
        self.graph_window.plot_graph()

    def open_graph_window_pit_recap(self):
        self.graph_window = PitRecap()
        self.graph_window.plot_graph()
    def open_graph_window_overtakes(self):
        self.graph_window = Overtakes()
        self.graph_window.plot_graph()
    def open_graph_race(self):
        self.graph_window = RaceVisualized()
        self.graph_window.plot_graph()
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

