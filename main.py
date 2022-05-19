import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from riotwatcher import LolWatcher

import champions
import collections
import requests
import os.path


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
currentItemID = 0;
currentItem = ''
currentTags = []
itemsToRemove = []
for key, value in items.items():
    if type(value) is dict:
        if list(value.keys())[0] == '1001':
            for key, value in value.items():
                #print(key)
                #print(value)
                if key > '3000':
                    #print(key)
                    currentItemID = key
                #print(value)
                if 'inStore' not in value.keys() and key > '3000':
                    #print(key)
                    #print(value)
                    for key, value in value.items():
                        #print(key)
                        #print(value)
                        if key == 'name':
                            currentItem = value
                        if key == 'tags':
                            currentTags = value
                        if key == 'stats':
                            #item_dict[currentItem] = [currentTags, value]
                            item_dict[currentItemID] = [currentItem, currentTags, value]
                        if key == 'into':
                            #print(currentItem)
                            #print(key)
                            #print(value)
                            if len(value) != 1:
                                itemsToRemove.append(currentItemID)
                        if key == 'maps':
                            if not value['11']:
                                itemsToRemove.append(currentItemID)

for items in itemsToRemove:
    item_dict.pop(items)
item_dict.pop('3076')
item_dict.pop('3330')
item_dict.pop('3155')
item_dict.pop('3191')
item_dict.pop('4630')
item_dict.pop('4632')
item_dict.pop('4635')

updatedItemDict = collections.defaultdict(list)
for key, value in item_dict.items():
    itemTags = value[1]
    if 'Boots' in itemTags:
        if 'AttackSpeed' in itemTags:
            updatedItemDict['ADC'].append((key, value[0]))
        if 'Armor' in itemTags:
            updatedItemDict['ADC'].append((key, value[0]))
            updatedItemDict['Tank'].append((key, value[0]))
            updatedItemDict['TankSupport'].append((key, value[0]))
            updatedItemDict['ADFighter'].append((key, value[0]))
            updatedItemDict['ADSupport'].append((key, value[0]))
            updatedItemDict['Mage'].append((key, value[0]))
            updatedItemDict['APSupport'].append((key, value[0]))
            updatedItemDict['APFighter'].append((key, value[0]))
            updatedItemDict['ADAssassin'].append((key, value[0]))
            updatedItemDict['APAssassin'].append((key, value[0]))
            updatedItemDict['APMarksman'].append((key, value[0]))
        if 'SpellBlock' in itemTags:
            updatedItemDict['ADC'].append((key, value[0]))
            updatedItemDict['Tank'].append((key, value[0]))
            updatedItemDict['TankSupport'].append((key, value[0]))
            updatedItemDict['ADFighter'].append((key, value[0]))
            updatedItemDict['ADSupport'].append((key, value[0]))
            updatedItemDict['Mage'].append((key, value[0]))
            updatedItemDict['APSupport'].append((key, value[0]))
            updatedItemDict['APFighter'].append((key, value[0]))
            updatedItemDict['ADAssassin'].append((key, value[0]))
            updatedItemDict['APAssassin'].append((key, value[0]))
            updatedItemDict['APMarksman'].append((key, value[0]))
        if 'MagicPenetration' in itemTags:
            updatedItemDict['Mage'].append((key, value[0]))
    if 'Armor' in itemTags:
        updatedItemDict['AgainstAD'].append((key, value[0]))
    if 'SpellBlock' in itemTags:
        updatedItemDict['AgainstAP'].append((key, value[0]))
    if 'ArmorPenetration' in itemTags:
        updatedItemDict['AgainstTank'].append((key, value[0]))
    #if 'Damage' in itemTags:
#        updatedItemDict['AgainstTank'].append(value[0])
    if 'MagicPenetration' in itemTags:
        if value[0] != 'Divine Sunderer':
            updatedItemDict['AgainstTank'].append((key, value[0]))
    if 'Vision' in itemTags:
        updatedItemDict['TankSupport'].append((key, value[0]))
        updatedItemDict['ADSupport'].append((key, value[0]))
        updatedItemDict['APSupport'].append((key, value[0]))
    elif 'GoldPer' in itemTags:
        updatedItemDict['TankSupport'].append((key, value[0]))
        updatedItemDict['ADSupport'].append((key, value[0]))
        updatedItemDict['APSupport'].append((key, value[0]))
    elif 'ManaRegen' in itemTags:
        updatedItemDict['APSupport'].append((key, value[0]))
    elif 'SpellDamage' in itemTags:
        updatedItemDict['APSupport'].append((key, value[0]))
    if 'Health' in itemTags:
        if 'Armor' and 'SpellBlock' in itemTags:
            updatedItemDict['Tank'].append((key, value[0]))
            updatedItemDict['TankSupport'].append((key, value[0]))
        elif 'Armor' in itemTags:
            #print(value[0], "is a health armour item")
            updatedItemDict['Tank'].append((key, value[0]))
            updatedItemDict['TankSupport'].append((key, value[0]))
        elif 'SpellBlock' in itemTags:
            updatedItemDict['Tank'].append((key, value[0]))
            updatedItemDict['TankSupport'].append((key, value[0]))
        elif 'Damage' in itemTags and 'CriticalStrike' not in itemTags and 'Vision' not in itemTags:
            updatedItemDict['ADFighter'].append((key, value[0]))
            updatedItemDict['ADSupport'].append((key, value[0]))
    if 'Damage' in itemTags:
        if 'AttackSpeed' and 'CriticalStrike' in itemTags:
            updatedItemDict['ADC'].append((key, value[0]))
        elif 'ArmorPenetration' in itemTags:
            updatedItemDict['ADAssassin'].append((key, value[0]))
        elif 'Armor' in itemTags:
            updatedItemDict['ADSupport'].append((key, value[0]))
            updatedItemDict['ADFighter'].append((key, value[0]))
            updatedItemDict['ADC'].append((key, value[0]))
    if 'SpellDamage' in itemTags and 'Vision' not in itemTags and 'ManaRegen' not in itemTags:
        updatedItemDict['Mage'].append((key, value[0]))
        updatedItemDict['APFighter'].append((key, value[0]))
        updatedItemDict['APAssassin'].append((key, value[0]))
        updatedItemDict['APMarksman'].append((key, value[0]))


dict_of_champs = {}
currentChamp = ''
currentChampInfo = {}

list_of_champs = []
listOfChampImages = []

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
            currentChampInfo.pop('difficulty')
        if key == 'tags':
            currentChampTags = value
            dict_of_champs[currentChamp] = [value, currentChampInfo]

for keys in item_dict.keys():
    itemDirectory = "src/" + keys + ".png"
    if os.path.isfile(itemDirectory) == False:
        itemImage = requests.get("http://ddragon.leagueoflegends.com/cdn/12.9.1/img/item/" + keys + ".png").content
        with open(itemDirectory, 'wb') as f:
            f.write(itemImage)

#champImage = requests.get("http://ddragon.leagueoflegends.com/cdn/12.9.1/img/champion/Katarina.png").content
for champ in list_of_champs:
    champDirectory = "src/" + champ + ".png"
    if os.path.isfile(champDirectory) == False:
        if champ == 'Wukong':
            champImage = requests.get("http://ddragon.leagueoflegends.com/cdn/12.9.1/img/champion/MonkeyKing.png").content
        else:
            champImage = requests.get("http://ddragon.leagueoflegends.com/cdn/12.9.1/img/champion/" + champ + ".png").content
        with open(champDirectory, 'wb') as f:
            f.write(champImage)


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("League of Builds - Select the Champion you are Playing")
        self.matchup = []
        self.ChampionPage = 0
        self.displayChampions()

    def displayChampions(self):
        list_of_champs.remove('Wukong')
        list_of_champs.insert(144, 'Wukong')

        buttons = {}
        [buttons.setdefault(i, []) for i in range(len(list_of_champs))]

        '''
        positions = [(i, j) for i in range(18) for j in range(10)]
        champ_id = 0
        for position, name in zip(positions, list_of_champs):
            button = QPushButton(name)
            grid.addWidget(button, *position)
            buttons[champ_id].append(name)
            buttons[champ_id].append(button)
            champ_id += 1
        '''

        widget = QWidget()
        # Layout of Container Widget
        grid = QGridLayout(self)
        grid.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(grid)

        # Scroll Area Properties
        scroll = QScrollArea()
        #scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        # Scroll Area Layer add
        scroll_layout = QGridLayout(self)
        scroll_layout.addWidget(scroll)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(scroll_layout)

        imgSize = 60
        self.row = 0
        self.col = 0
        champID = 0
        for champName in list_of_champs:
            champImageDirectory = "src/" + champName + ".png"
            champImage = QLabel()
            image = QPixmap(champImageDirectory)
            scaledImage = image.scaled(imgSize, imgSize)
            champImage.setPixmap(scaledImage)
            grid.addWidget(champImage, self.row, self.col)
            self.col += 1

            button = QPushButton(champName)
            grid.addWidget(button, self.row, self.col)
            self.col += 1
            if self.col % 20 == 0:
                self.row += 1
                self.col = 0
            buttons[champID].append(champName)
            buttons[champID].append(button)
            champID += 1

        for value in buttons.values():
            value[1].clicked.connect(lambda checked, a=value[0]: self.addChampToMatchUp(a))

        self.setLayout(grid)
        self.resize(1560, 1080)
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
        self.MatchupPage = champions.MatchUpPage(playerChampionName, enemyChampionName, dict_of_champs, updatedItemDict)


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    #image = MainWindow()
    #champWindow = mainWindow.displayChampions()
    #mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
