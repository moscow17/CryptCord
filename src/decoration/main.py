import os
import time
import PyQt5
import ujson
import threading

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow

from src.decoration import FriendsList, Client, Channel, Message, Channels, MessageChannel
from src.utils.utils import load_config
from src.discord.main import run_client

class Application(QMainWindow): 

    messages = []

    @load_config
    def __init__(self, config):
        self.config = config

        QMainWindow.__init__(self)
        uic.loadUi("ext/chat.ui", self)

        self.add_friends = self.findChild(QtWidgets.QAction, "add_friend")
        self.friends = self.findChild(QtWidgets.QListWidget, "friends")
        self.add_friends.triggered.connect(self.load_friends)

        self.friends.clicked.connect(self.load_channel)

        if config.get("token"):
            self.load_discord()

        self.preload_friends()

        self.show()

    def return_friends(self):
        _list = []
        for index in range(self.friends.count()):
            _list.append(self.friends.item(index).text().split("(")[1].split(")")[0])
        return _list

    def select_friend(self):
        pass

    def load_channel(self):
        id = self.friends.currentItem().text().split("(")[1].split(")")[0]
        name = self.friends.currentItem().text().split("(")[0]

        self.client = Client(name, id)
        self.channel = MessageChannel(self.client)

    def preload_friends(self):
        for friend in os.listdir("opt/keys"):
            client = ujson.load(open("opt/keys/%s/info.json" %(friend)))
            self.friends.addItem("%s(%s)" %(client['name'], client['id']))

    def load_discord(self):
        run_client(self)

    def load_friends(self):
        self.__friendslist = FriendsList()
