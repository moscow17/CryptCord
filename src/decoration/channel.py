import os
import time
import PyQt5
import ujson
import threading

from datetime import datetime
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow

from src.protocol import StandardProtocol

class MessageChannel(QMainWindow): 

    def __init__(self, client):
        QMainWindow.__init__(self)

        self.client = client

        uic.loadUi("ext/message.ui", self)

        self.protocol = StandardProtocol(client)

        self.send_message.returnPressed.connect(self.begin_message_auth)
        self.messages.append("[%s] secure channel started with user: %s" %(
            self.time, client.name))
        self.show()

    @property
    def time(self):
        return datetime.now()

    def begin_receive_auth(self, content):
        content = self.protocol.receive(content)
        self.messages.append("(%s) %s: %s" %(self.time, self.client.name, content))

    def begin_message_auth(self):
        content = self.send_message.text()
        self.send_message.clear()

        self.messages.append("(%s) %s: %s" %(self.time, "me", content))
        self.protocol.send(content)
