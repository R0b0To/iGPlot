import os
import requests

# Create a directory to store the downloaded images
output_directory = os.path.join(os.path.dirname(os.getcwd()), 'downloaded_images')
os.makedirs(output_directory, exist_ok=True)

# Read the list of names and URLs from the text file
with open('cars.txt', 'r',encoding='utf-8') as file:
    lines = file.readlines()

# Iterate through the lines in the text file
for line in lines:
    name, url = line.strip().split(',')
    # Create the file name for the image using the first name
    file_name = f"{name}.png"

    # Download the image from the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the image to the output directory
        with open(os.path.join(output_directory, file_name), 'wb') as image_file:
            image_file.write(response.content)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {file_name} from {url} (Status code: {response.status_code})")
