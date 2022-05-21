from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import random


class MatchUpPage(QWidget):
    def __init__(self, playerChampionName, enemyChampionName, dict_of_champs, item_dict):
        super(MatchUpPage, self).__init__()
        self.champs = dict_of_champs
        self.items = item_dict
        self.name = playerChampionName
        self.enemyName = enemyChampionName
        self.setWindowTitle(playerChampionName + " vs " + enemyChampionName)

        self.selfClass = self.findSelfClass()
        self.enemyInfo = self.findEnemyClass()

        self.itemsForChamp = []
        self.itemsForEnemy = []
        self.itemsForChampID = []
        self.itemsForEnemyID = []

        self.findSelfItems(self.selfClass)
        self.findEnemyItems(self.enemyInfo)

        self.finalItemsToShowList = []
        self.finalImagesToShowList = []
        for item in self.itemsForChamp:
            if item in self.itemsForEnemy:
                self.finalItemsToShowList.append(item)
        for ID in self.itemsForChampID:
            if ID in self.itemsForEnemyID:
                self.finalImagesToShowList.append(ID)

        #print(self.finalItemsToShowList)
        #print(self.itemsForChamp)
        #print(self.itemsForChampID)

        #self.grid = QGridLayout()
        #Container widget
        widget = QWidget()
        #Layout of Container Widget
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(self.grid)

        #Scroll Area Properties
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        #Scroll Area Layer add
        scroll_layout = QGridLayout(self)
        scroll_layout.addWidget(scroll)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(scroll_layout)

        imgSize = 60

        self.champLabel = QLabel()
        self.champLabel.setFont(QFont('Arial', 14))
        self.champLabel.setText("Recommended items as " + self.name + ":")
        self.grid.addWidget(self.champLabel, 0, 0, 1, 2)

        self.enemyLabel = QLabel()
        self.enemyLabel.setFont(QFont('Arial', 14))
        self.enemyLabel.setText("Recommended items against " + self.enemyName + ":")
        self.grid.addWidget(self.enemyLabel, 0, 2, 1, 2)

        self.row = 1
        self.col = 0
        for itemID in self.itemsForChampID:
            self.itemImage = QLabel()
            self.imageDirectory = "src/" + itemID + ".png"
            self.image = QPixmap(self.imageDirectory)
            self.scaledImage = self.image.scaled(imgSize, imgSize)
            self.itemImage.setPixmap(self.scaledImage)
            self.grid.addWidget(self.itemImage, self.row, self.col)
            self.row += 1


        self.row = 1
        self.col = 1
        for itemName in self.itemsForChamp:
            self.item = QLabel()
            self.item.setFont(QFont('Arial', 10))
            self.item.setText(itemName)
            self.grid.addWidget(self.item, self.row, self.col)
            self.row += 1

        self.row = 1
        self.col = 2
        for itemID in self.itemsForEnemyID:
            self.itemImage = QLabel()
            self.imageDirectory = "src/" + itemID + ".png"
            self.image = QPixmap(self.imageDirectory)
            self.scaledImage = self.image.scaled(imgSize, imgSize)
            self.itemImage.setPixmap(self.scaledImage)
            self.grid.addWidget(self.itemImage, self.row, self.col)
            self.row += 1

        self.row = 1
        self.col = 3
        for itemName in self.itemsForEnemy:
            self.item = QLabel()
            self.item.setFont(QFont('Arial', 10))
            self.item.setText(itemName)
            self.grid.addWidget(self.item, self.row, self.col)
            self.row += 1

        self.finalLabel = QLabel()
        self.finalLabel.setFont(QFont('Arial', 14))
        if len(self.finalItemsToShowList) != 0:
            self.finalLabel.setText("Best items when playing " + self.name + " vs " + self.enemyName + ":")
            self.grid.addWidget(self.finalLabel, 0, 4, 1, 2)

        self.row = 1
        self.col = 4
        for itemID in self.finalImagesToShowList:
            self.itemImage = QLabel()
            self.imageDirectory = "src/" + itemID + ".png"
            self.image = QPixmap(self.imageDirectory)
            self.scaledImage = self.image.scaled(imgSize, imgSize)
            self.itemImage.setPixmap(self.scaledImage)
            self.grid.addWidget(self.itemImage, self.row, self.col)
            self.row += 1

        self.row = 1
        self.col = 5
        for itemName in self.finalItemsToShowList:
            self.item = QLabel()
            self.item.setFont(QFont('Arial', 10))
            self.item.setText(itemName)
            self.grid.addWidget(self.item, self.row, self.col)
            self.row += 1

        self.resize(1080, 1080)
        self.show()

    def findSelfClass(self):
        champ_tags = self.champs[self.name][0]
        champ_stats = self.champs[self.name][1]
        #print(champ_tags)
        #print(champ_stats)

        if 'Support' in champ_tags:
            if champ_stats['defense'] > 6:
                return 'TankSupport'
            elif champ_stats['magic'] > champ_stats['attack']:
                return 'APSupport'
            else:
                return 'ADSupport'

        elif champ_tags[0] == 'Assassin':
            if champ_stats['attack'] > champ_stats['magic']:
                return 'ADAssassin'
            else:
                return 'APAssassin'
        elif champ_tags[0] == 'Marksman':
            if champ_stats['attack'] > champ_stats['magic']:
                return 'ADC'
            else:
                return 'APMarksman'
        elif champ_tags[0] == 'Mage':
            return 'Mage'
        elif champ_tags[0] == 'Tank':
            return 'Tank'
        elif champ_tags[0] == 'Fighter':
            if champ_stats['defense'] > 6:
                return 'Tank'
            elif champ_stats['attack'] > champ_stats['magic']:
                return 'ADFighter'
            else:
                return 'APFighter'

    def findEnemyClass(self):
        enemy_tags = self.champs[self.enemyName][0]
        enemy_stats = self.champs[self.enemyName][1]

        highAD = False
        highAP = False
        highTank = False

        if enemy_stats['attack'] > 5:
            highAD = True
        if enemy_stats['magic'] > 5:
            highAP = True
        if enemy_stats['defense'] > 5:
            highTank = True

        return [highAD, highAP, highTank]

    def findSelfItems(self, champClass):
        for key, value in self.items.items():
            if key == self.selfClass:
                #self.itemsForChamp = value
                for item in value:
                    self.itemsForChampID.append(item[0])
                    self.itemsForChamp.append(item[1])
        #print(self.itemsForChamp)

    def findEnemyItems(self, champInfo):
        for key, value in self.items.items():
            if key == 'AgainstAD':
                #Find items good against high AD
                if champInfo[0]:
                    #self.itemsForEnemy = value
                    #self.itemsForEnemy.append(value)
                    for tuple in value:
                        self.itemsForEnemyID.append(tuple[0])
                        self.itemsForEnemy.append(tuple[1])
            if key == 'AgainstAP':
                #Find items good against high AP
                if champInfo[1]:
                    #self.itemsForEnemy = value
                    #self.itemsForEnemy.append(value)
                    for tuple in value:
                        self.itemsForEnemyID.append(tuple[0])
                        self.itemsForEnemy.append(tuple[1])
            if key == 'AgainstTank':
                # Find items good against tanks
                if champInfo[2]:
                    #self.itemsForEnemy = value
                    #self.itemsForEnemy.append(value)
                    for tuple in value:
                        self.itemsForEnemyID.append(tuple[0])
                        self.itemsForEnemy.append(tuple[1])
        #print(self.itemsForEnemy)