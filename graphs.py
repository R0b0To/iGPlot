import csv

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
        
       
  
print(driver_data)
csv_file.close()


