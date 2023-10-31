import os,requests
script_directory = os.path.dirname(os.path.abspath(__file__))
output_directory = os.path.join(os.getcwd(), 'downloaded_images')
os.makedirs(output_directory, exist_ok=True)
print("Script directory:", script_directory)
print(output_directory)
file_path = os.path.join(script_directory, "cars.txt")

with open(file_path, 'r',encoding='utf-8') as file:
    lines = file.readlines()

for line in lines:
    name, url = line.strip().split(',')
    file_name = f"{name}.png"
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(output_directory, file_name), 'wb') as image_file:
            image_file.write(response.content)
        print(f"Downloaded {file_name}")
    else:
        print(f"Failed to download {file_name} from {url} (Status code: {response.status_code})")
