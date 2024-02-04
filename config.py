from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QPushButton, QLabel,QLineEdit,QProgressBar 
from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
import requests
import time
import sys
import re

class WorkerThread(QThread):
    # Define a signal to update the progress bar
    progress_signal = pyqtSignal(int)
    def run(self):
            self.progress_signal.emit(100)
         
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.login_completed = False
        self.setWindowTitle("URL Input")
        self.init_ui()
        self.login()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Enter league url:")
        self.radio_buttons = {
           'standings1': QRadioButton('Rookie'),
           'standings2': QRadioButton('Pro'),
           'standings3': QRadioButton('Elite') 
        }

        self.radio_buttons['standings3'].setChecked(True)
        layout.addWidget(label)

        self.url_entry = QLineEdit()
        layout.addWidget(self.url_entry)
        
        for radio in self.radio_buttons.values():
            layout.addWidget(radio)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.on_confirm_button)
        layout.addWidget(self.confirm_button)
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)  # Initially invisible
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        

    def login(self):
        # Perform the login process here
        # Example: Using Selenium to log in
        login_url = "https://igpmanager.com/index.php?action=send&addon=igp&type=login&jsReply=login&ajax=1"
        # Using a bot account for the login 
        login_data =  {'loginUsername':'cfg@account.mail',
                       'loginPassword':'config', 
                       'loginRemember': 'on',
                       'csrfName': '',
                       'csrfToken': ''}     
        response =  self.session.post(login_url, data=login_data)

        # Check if the login was successful
        if response.ok:
            print("Login successful!")
        else:
            print("Login failed. Status code:", response.status_code)
            print("Response content:", response.text)
        self.login_completed = True

    def update_progress(self, value):

        self.progress_bar.setValue(100)
        print("Process completed.")
        self.worker_thread.quit()
        self.progress_bar.setVisible(False) 

    def on_confirm_button(self):
        self.confirm_button.setVisible(False) 
        self.worker_thread = WorkerThread()
        self.worker_thread.progress_signal.connect(self.update_progress)
        self.worker_thread.start()
        self.progress_bar.setVisible(True)
        def fetch_manager(manager):
            url = f"https://igpmanager.com/index.php?action=fetch&d=profile&manager={manager['id']}&csrfName=&csrfToken="
            response = self.session.get(url)
            return response.json()
        def download_cars():
            with open('cars.txt', 'r',encoding='utf-8') as file:
                lines = file.readlines()
            if len(lines)==0:
                return   
            lines_number_progress = int(1/len(lines)*30)
            for line in lines:
                name, url = line.strip().split(',')
                file_name = f"{name}.png"
                response = requests.get(url)
                if response.status_code == 200:
                    with open(('assets/cars/'+file_name), 'wb') as image_file:
                        image_file.write(response.content)
                    self.progress_bar.setValue(lines_number_progress+self.progress_bar.value())
                else:
                    print(f"Failed to download {file_name} from {url} (Status code: {response.status_code})")        
        def fetch_driver(driverId):
            url = f"https://igpmanager.com/index.php?action=fetch&d=driver&id={driverId}&csrfName=&csrfToken="
            response = self.session.get(url)
            return response.json()
        def save_colors(managers):
            with open('colors.txt', 'w') as file:
                for item in managers:
                    for driver in item['drivers']:
                        file.write(f"{driver['abbr_name']}:{item['color']}\n")
        def save_liveries_links(managers):
            with open('cars.txt', 'w') as file:
                for item in managers:
                    for driver in item['drivers']:
                        file.write(f"{driver['abbr_name']},{driver['livery']}\n")
            download_cars()        
        def save_full_stats(managers): 
              with open('Managers&Drivers.txt', 'w') as file:
                file.write(f"Team,Manager,Country,Driver,Abbr,Livery,Talent,Grade,Special,Rating,FavTrack,Height,Age,BMI,Color\n")              
                for item in managers:
                    for driver in item['drivers']:
                        file.write(f"{item['team']},{item['name']},{driver['country']},{driver['dName']},{driver['abbr_name']},{driver['livery']},{driver['sTalent']},{driver['special']},{driver['sSpecial']['name']},{driver['starRating']},{driver['favTrack']},{driver['sHeight']},{driver['sAge']},{driver['sBmi']},{item['color']}\n")              
        if not self.login_completed:
             time.sleep(5)
             self.on_confirm_button()
             return
         
        url = self.url_entry.text()
        league_id = re.findall(r'\d+', url)
        for option, radio in self.radio_buttons.items():
            if radio.isChecked():
                tier = option

        league_url = f'https://igpmanager.com/index.php?action=fetch&p=league&id={league_id[0]}&csrfName=&csrfToken='

        response =  self.session.get(league_url)
        if response.status_code == 200:
            json_data = response.json()
            soup = BeautifulSoup(json_data['vars'][tier], 'html.parser')
            h2_text = soup.select_one('h2').text
            league_max_cars = int(h2_text.split('/')[1].strip())
            managers_rows = soup.find_all('tr')
            managers_number = len(managers_rows)
            managers = []
            for manager in managers_rows:
                match = re.search(r'#([0-9A-Fa-f]{3,6})\b', str(manager.td))
                color = match.group(0) if match else '#000000'
                team = manager.contents[1].span.text
                name = manager.contents[1].contents[3].strip()
                manager_id = re.findall(r'\d+', manager.a['href'])[0]
                managers.append({'team': team, 'color': color, 'name': name, 'id': manager_id})
            i = 1
            for manager in managers:
                manager_result = fetch_manager(manager)
                driver_id ={}
                soup = BeautifulSoup(manager_result['vars']['driver1'], 'html.parser')
                self.progress_bar.setValue(int(i/managers_number*70))
                i+=1
                #using driver id as key and the abbr name as value
                driver_id[re.findall(r'\d+',soup.a['href'])[0]] = soup.text.strip()

                #add second driver if league is 2 cars
                if league_max_cars == 16:
                    soup = BeautifulSoup(manager_result['vars']['driver2'], 'html.parser')
                    driver_id[re.findall(r'\d+',soup.a['href'])[0]] = soup.text.strip()
                
                manager_driver_stats = []
                for id in driver_id.keys():
                   result = fetch_driver(int(id))
                   driver_attr = {
                   'abbr_name' : driver_id[id],
                   'dName' : BeautifulSoup(result['vars']['dName'], 'html.parser').text.strip(),
                   'favTrack': BeautifulSoup(result['vars']['favTrack'], 'html.parser').text.strip(),
                   'sTalent' : BeautifulSoup(result['vars']['sTalent'], 'html.parser').text.strip(),
                   'sHeight' : result['vars']['sHeight'],
                   'sAge' : BeautifulSoup(result['vars']['sAge'], 'html.parser').text.strip(),
                   'country': BeautifulSoup(result['vars']['dName'], 'html.parser').img['class'][1][2:],
                   'starRating' : BeautifulSoup(result['vars']['starRating'], 'html.parser').contents[1].text.strip(" '()"),
                   'sBmi' : BeautifulSoup(result['vars']['sBmi'], 'html.parser').span['class'][1].split('-')[1],
                   'tName' : BeautifulSoup(result['vars']['tName'], 'html.parser').text.strip(),
                   'sSpecial' : { 'name': BeautifulSoup(result['vars']['sSpecial'], 'html.parser').text.strip(), 'grade': BeautifulSoup(result['vars']['sSpecial'], 'html.parser').span['class'][0] }
                   }
                   livery = BeautifulSoup(manager_result['vars']['liveryS'], 'html.parser').img['src']
                   special={'specialA0':"",'specialA1':"Common",'specialA2':"Rare",'specialA3':"Legendary"}
                   bmi ={"red":"❌","orange":"❎","green":"✅"}
                   
                   driver_attr['livery'] = livery
                   driver_attr['special'] = special[driver_attr['sSpecial']['grade']]
                   manager_driver_stats.append(driver_attr)
                manager['drivers'] = manager_driver_stats 
            
            save_colors(managers)
            save_liveries_links(managers)
            save_full_stats(managers)
            self.progress_bar.setValue(100)
            self.confirm_button.setVisible(True)      
        else:
            print(f"Error: {response.status_code}")
global_signal = WorkerThread()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
