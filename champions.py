from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MatchUpPage(QWidget):
    def __init__(self, playerChampionName, enemyChampionName):
        super(MatchUpPage, self).__init__()
        self.name = playerChampionName
        self.enemyName = enemyChampionName
        self.setWindowTitle(playerChampionName + " vs " + enemyChampionName)
        #self.resize(1280, 720)
        self.show()

    def showChampPage(self):
        print("showing matchup")
        self.show()

    def displayChampion(self):
        pass

