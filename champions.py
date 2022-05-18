from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


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

        self.findSelfItems(self.selfClass)
        self.findEnemyItems(self.enemyInfo)

        self.itemsForChampSet = set(self.itemsForChamp)
        self.itemsForEnemySet = set(self.itemsForEnemy)
        self.finalItemsToShow = self.itemsForChampSet.intersection(self.itemsForEnemySet)
        #if self.selfClass == 'Tank' and self.enemyInfo[2]:
#            self.finalItemsToShow = self.itemsForChampSet

        self.itemID = 0
        print(len(self.finalItemsToShow))
        while len(self.finalItemsToShow) < 6:
            self.finalItemsToShow.add(self.itemsForChamp[self.itemID])
            self.itemID += 1
            #for item in self.itemsForChampSet:
                #self.finalItemsToShow

        print(self.itemsForChampSet)
        print(self.itemsForEnemySet)
        print(self.finalItemsToShow)


        #self.resize(1280, 720)
        self.show()

    def showChampPage(self):
        print("showing matchup")
        self.show()

    def findSelfClass(self):
        champ_tags = self.champs[self.name][0]
        champ_stats = self.champs[self.name][1]
        #print(champ_tags)
        #print(champ_stats)

        if 'Support' in champ_tags:
            if champ_stats['defense'] > 6:
                #print("Tank support")
                #self.selfClass = 'TankSupport'
                return 'TankSupport'
            elif champ_stats['magic'] > champ_stats['attack']:
                #print("AP support")
                #self.selfClass = 'APSupport'
                return 'APSupport'
            else:
                #print("AD support")
                #self.selfClass = 'ADSupport'
                return 'ADSupport'

        elif champ_tags[0] == 'Assassin':
            if champ_stats['attack'] > champ_stats['magic']:
                #print("AD assassin")
                #self.selfClass = 'ADAssassin'
                return 'ADAssassin'
            else:
                #print("AP assassin")
                #self.selfClass = 'APAssassin'
                return 'APAssassin'
        elif champ_tags[0] == 'Marksman':
            if champ_stats['attack'] > champ_stats['magic']:
                #print("ADC")
                #self.selfClass = 'ADC'
                return 'ADC'
            else:
                #print("AP marksman")
                #self.selfClass = 'APMarksman'
                return 'APMarksman'
        elif champ_tags[0] == 'Mage':
            #print("Mage")
            #self.selfClass = 'Mage'
            return 'Mage'
        elif champ_tags[0] == 'Tank':
            #print("Tank")
            #self.selfClass = 'Tank'
            return 'Tank'
        elif champ_tags[0] == 'Fighter':
            if champ_stats['defense'] > 6:
                #print("Tank")
                #self.selfClass = 'Tank'
                return 'Tank'
            elif champ_stats['attack'] > champ_stats['magic']:
                #print("AD fighter")
                #self.selfClass = 'ADFighter'
                return 'ADFighter'
            else:
                #print("AP fighter")
                #self.selfClass = 'APFighter'
                return 'APFighter'
        #print(self.selfClass)

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
                self.itemsForChamp = value
                #for item in value:
                    #print(item)
                    #pass
        #print(self.itemsForChamp)

    def findEnemyItems(self, champInfo):
        for key, value in self.items.items():
            itemTags = value[1]
            if key == 'AgainstAD':
                #Find items good against high AD
                if champInfo[0]:
                    self.itemsForEnemy = value
                    #print(value)
            if key == 'AgainstAP':
                #Find items good against high AP
                if champInfo[1]:
                    self.itemsForEnemy = value
                    #print(value)
            if key == 'AgainstTank':
                # Find items good against tanks
                if champInfo[2]:
                    self.itemsForEnemy = value
                    #print(value)
        #print(self.itemsForEnemy)