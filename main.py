import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import requests
import json

#response = requests.get("https://google.com/")
#print("Reponse status code:", response.status_code)

#League of Builds API Key 06/05: RGAPI-e044cb80-7fb9-400a-ba21-9e451226a26f
#Dev APi Key 06/05: RGAPI-296164da-ca7e-4703-9f51-f41ba423d61d


#Dev Key
#riotResponse = requests.get("https://nal.api.riotgames.com/lol/summoner/v4/summoners/by-name/Doublelift?api_key=RGAPI-296164da-ca7e-4703-9f51-f41ba423d61d")
#LoB Key
riotResponse = requests.get("https://nal.api.riotgames.com/lol/summoner/v4/summoners/by-name/Doublelift?api_key=RGAPI-e044cb80-7fb9-400a-ba21-9e451226a26f")
#print(riotResponse)
#print(type(riotResponse.json()))
#print(riotResponse.json())
#print(json.dumps(riotResponse.json()))

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Test Window")

        label = QLabel("Test Label")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)


#app = QApplication([])

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()