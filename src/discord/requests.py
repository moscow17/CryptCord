import os
import sys
import time
import ujson
import discord
import requests

from src.utils.utils import threaded, load_config

session = requests.session()

class Communication(object):

    @load_config
    def __init__(self, config):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "authorization": "",
            "Origin": "https://discordapp.com",
            "Accept-Language": "en-US",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "authorization": config['token'],
            "DNT": "1"
        }

    def get_channel(self, userid):
        return requests.post("https://discordapp.com/api/v8/users/@me/channels",
            json={"recipients": [userid]}, headers=self.header)

    def get_friends(self):
        return requests.get("https://discordapp.com/api/v8/users/@me/relationships", 
            headers=self.header).json()

    def delete_message(self, channel, message):
        time.sleep(5)
        session.delete("https://discordapp.com/api/v8/channels/%s/messages/%s" 
            %(channel, message), headers=self.header)

    @threaded
    def send_message(self, channel, content):
        data = {"content": content}

        session.post("https://discordapp.com/api/v8/channels/%s/messages" 
            %(channel), json=data, headers=self.header)
