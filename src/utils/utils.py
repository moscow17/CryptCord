import os
import ujson
import discord

from threading import Thread

def load_config(func):

    def inner(self, *args, **kwargs):
        config = ujson.load(open("opt/config.json", "r"))
        args += (config, )
        return func(self, *args)
    return inner

def threaded(func):

    def inner(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        return thread.start()
    return inner
