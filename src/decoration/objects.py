import os
import time
import PyQt5
import ujson
import threading

from datetime import datetime

class Channels(object):

    channels = []

    def add_channel(self, channel):
        if not channel in self.channels:
            self.channels.append(channel) 

    def remove_channel(self, channel):
        if channel in self.channels:
            self.channels.remove(channel)

class Channel(object):

    messages = []
    clients = []

    def __init__(self, self_client, client):
        self.self_client = self_client
        self.client = client

        self.id = hex(id(self))

    def add_message(self, message):
        self.messages.append(message)

class Message(object):

    def __init__(self, client, content):
        self.content = content
        self.client = client

        self.created_at = time.time()
        self.created_str = str(datetime.now())

class Client(object):

    def __init__(self, name, uid):
        self.name = name
        self.uid = uid

        self._id = hex(id(self))
