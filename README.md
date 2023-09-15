
# iGPlot
Python-based application designed to extract, process, and visualize data from the [iGPlus extension](https://github.com/R0b0To/iGPlus)



## Run Locally

Clone the project

```
git clone https://github.com/R0b0To/iGPlot
```

Go to the project directory

```
cd igplot
```

Install dependencies

```
pip install -r requirements.txt
```
Download the "full_report.csv" file from the popup menu of the [iGPlus extension](https://github.com/R0b0To/iGPlus) after extracting race results, and replace with the example file of same name.

Start the application
```
py iGPlot
```
### Optional
To specify the color to be used for each driver open the "colors.txt" file and modify it to include the driver names and their corresponding colors.

To obtain the liveries from the links provided in the "cars.txt" file, you can execute the "download_cars.py" script located in the "download_cars" folder. 

You can utilize the "driverStats.js" script to extract data for all drivers. To do this, navigate to the iGP game league page using a web browser, open the developer tools (F12), and paste the provided JavaScript code into the console.

## Screenshots

![App Screenshot](https://i.imgur.com/5Eer9ed.png)
![App Screenshot](https://i.imgur.com/5mMyOK8.png)
![App Screenshot](https://i.imgur.com/LJEVJvy.png)


