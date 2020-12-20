import os
import time
import PyQt5
import ujson
import threading

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow

from src.discord import Communication

comm = Communication()

class options(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.friends = comm.get_friends()

        self.setObjectName("self")
        self.resize(402, 600)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.List = QtWidgets.QListWidget(self.centralwidget)
        self.List.setGeometry(QtCore.QRect(10, 50, 381, 481))
        self.List.setObjectName("listView")

        for item in self.friends:
            self.List.addItem(item['user']['username'])

        self.List.clicked.connect(self.add_friend)

        self.Text = QtWidgets.QLineEdit(self.centralwidget)
        self.Text.setGeometry(QtCore.QRect(60, 20, 271, 20))
        self.Text.setObjectName("keySequenceEdit")
        self.Text.textChanged.connect(self.sort_list)

        self.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()

    def get_userid(self, username):
        for friend in self.friends:
            if friend['user']['username'] == username:
                return friend['user']['id']

    def add_items(self, keyword):
        for item in self.friends:
            if keyword in item['user']['username'].lower():
                self.List.addItem(item['user']['username'])

    def sort_list(self):
        data = self.Text.text()

        self.List.clear()
        self.add_items(data)

    def add_friend(self):
        channel = comm.get_channel(self.get_userid(
            self.List.currentItem().text())).json()
        comm.send_message(channel['id'], "!add")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Add a friend"))