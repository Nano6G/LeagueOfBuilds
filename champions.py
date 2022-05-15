from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ChampionPage(QWidget):
    def __init__(self, name):
        super(ChampionPage, self).__init__()
        self.name = name
        self.setWindowTitle(name)
        #self.resize(1280, 720)

    def showChampPage(self):
        self.show()

    def displayChampion(self):
        pass

