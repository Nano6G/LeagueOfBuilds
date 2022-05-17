import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from riotwatcher import LolWatcher, ApiError

import champions

import requests
import json
#import riotwatcher


APIKeyFile = open("RiotAPIKey.txt", "r")

RiotAPIKey = APIKeyFile.read()
key = LolWatcher('' + RiotAPIKey)
region = 'euw1'

#me = key.summoner.by_name(region, 'Dump Gubbler')
#print(me)
#my_ranked_stats = key.league.by_summoner(region, me['id'])
#print(my_ranked_stats)

versions = key.data_dragon.versions_for_region(region)
champions_version = versions['n']['champion']

current_champ_list = key.data_dragon.champions(champions_version)
#Gets dictionary of champions
champ_data = current_champ_list.get('data')

#Items from API
items = key.data_dragon.items(champions_version)
item_dict = {}
currentItem = ''
currentTags = []
for key, value in items.items():
    if type(value) is dict:
        if list(value.keys())[0] == '1001':
            for key, value in value.items():
                print(key)
                #print(value)
                if 'inStore' not in value.keys() and key > '3000':
                    for key, value in value.items():
                        #print(key)
                        #print(value)
                        if key == 'name':
                            currentItem = value
                        if key == 'tags':
                            currentTags = value
                        if key == 'stats':
                            item_dict[currentItem] = [currentTags, value]
                #print(list(value.values())[0])
                #print(value)
print(item_dict)

'''
for key, value in champ_data.items():
    current_value = value.items()
    for key, value in current_value:
        if key == 'id':
            #LIST OF CHAMPS
            print("Champ Name:", value)
'''
dict_of_champs = {}
currentChamp = ''
currentChampInfo = {}

list_of_champs = []
list_of_champ_objs = []

for key, value in champ_data.items():
    current_value = value.items()
    for key, value in current_value:
        if key == 'id':
            #print("Champ name:", value)
            if value == 'MonkeyKing':
                currentChamp = 'Wukong'
            else:
                currentChamp = value
            list_of_champs.append(currentChamp)
        if key == 'info':
            currentChampInfo = value
        if key == 'tags':
            currentChampTags = value
            dict_of_champs[currentChamp] = [value, currentChampInfo]

print(dict_of_champs)

#riotResponse = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/Doublelift?api_key=" + RiotAPIKey)
#print(riotResponse.json())

#dataReponse = requests.get("https://raw.communitydragon.org/")
#dataReponse = requests.get("https://raw.communitydragon.org/latest/game/data/characters/aatrox/aatrox.bin.json")
#print(dataReponse.json())

bootsImage = requests.get("http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/1001.png")


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("League of Builds - Select the Champion you are Playing")
        #self.resize(1280, 720)
        self.matchup = []
        self.ChampionPage = 0
        self.displayChampions()
        #self.createChampionPages()

    def displayChampions(self):
        #scroll = QScrollArea(self)
        #layout = QVBoxLayout(self)
        #layout = QGridLayout(self)
        #layout.addWidget(scroll)
        #scroll.setWidgetResizable(True)
        #scrollContent = QWidget(scroll)
        #scrollLayout = QVBoxLayout(scrollContent)
        #scrollLayout = QGridLayout(scrollContent)

        grid = QGridLayout()

        positions = [(i, j) for i in range(18) for j in range(10)]

        '''
        for key, value in champ_data.items():
            current_value = value.items()
            for (key, value), position in zip(current_value, positions):
                if key == 'id':
                    list_of_champs.append(value)
                    #button = QPushButton(value)
                    #scrollLayout.addWidget(button)
                    #button.clicked.connect(self.test)
                    #grid.addWidget(button, *position)
        '''

        list_of_champs.remove('Wukong')
        list_of_champs.insert(144, 'Wukong')

        buttons = {}
        [buttons.setdefault(i, []) for i in range(len(list_of_champs))]
        champ_id = 0
        for position, name in zip(positions, list_of_champs):
            button = QPushButton(name)
            grid.addWidget(button, *position)
            buttons[champ_id].append(name)
            buttons[champ_id].append(button)
            champ_id += 1

        for value in buttons.values():
            value[1].clicked.connect(lambda checked, a=value[0]: self.addChampToMatchUp(a))
            #value[1].clicked.connect(lambda checked, a=value[0]: self.switchChampionPage(a))

        #scrollContent.setLayout(scrollLayout)
        #scroll.setWidget(scrollContent)
        #self.setLayout(layout)
        self.setLayout(grid)
        self.show()

    def addChampToMatchUp(self, champName):
        self.matchup.append(champName)
        if len(self.matchup) % 2 == 0:
            self.setWindowTitle("League of Builds - Select the Champion you are Playing")
            firstChamp = self.matchup[len(self.matchup)-2]
            secondChamp = self.matchup[len(self.matchup)-1]
            #self.switchChampionPage(self.matchup[0], self.matchup[1])
            self.switchChampionPage(firstChamp, secondChamp)
        else:
            self.setWindowTitle("League of Builds - Select the Champion you are Playing Against")

    def switchChampionPage(self, playerChampionName, enemyChampionName):
        #champIndex = list_of_champs.index(playerChampionName)
        self.MatchupPage = champions.MatchUpPage(playerChampionName, enemyChampionName)
        #list_of_champ_objs[champIndex].showChampPage()


'''
    def createChampionPages(self):
        for champion in list_of_champs:
            list_of_champ_objs.append(champions.ChampionPage(champion))
'''

'''
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        with open('file.png', 'wb') as f:
            f.write(requests.get("http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/2003.png").content)
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)

        label = QLabel(self)
        pixmap = QPixmap('file.png')
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

        self.show()
'''



def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    #image = MainWindow()
    #champWindow = mainWindow.displayChampions()
    #mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
