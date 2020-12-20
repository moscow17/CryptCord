import os
import ujson
import discord
from discord.ext import commands

Session = []

from src.protocol import save_key 

class MessageCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def send_pub_key(self, message):
        await message.channel.send(file=discord.File("opt/mykeys/pub.pem"))

    async def write_client_to_file(self, message, attachment):
        path = "opt/keys/%s" %(message.channel.id)

        if not os.path.exists(path):
            os.mkdir(path)

        with open(path + "/info.json", "w") as fp:
            fp.write(ujson.dumps({"id": message.channel.id, "name": message.author.name}, indent=4))
        await save_key(message, attachment)

    @commands.Cog.listener()
    async def on_message(self, message):

        if isinstance(message.channel, discord.DMChannel) and message.author != self.client.user:

            if message.content == "!add":
                if not str(message.channel.id) in self.client.app.return_friends():
                    self.client.app.friends.addItem("%s(%s)" %(message.author.name, message.channel.id))
                    await self.send_pub_key(message)
                    await message.channel.send("!add")

            if str(message.channel.id) in self.client.app.return_friends():
                if "key: " in message.content and "msg: " in message.content:
                    if self.client.app.client.uid == str(message.channel.id):
                        self.client.app.channel.begin_receive_auth(message.content)
                    else:
                        self.client.app.messages.append(message.content)

            for attachment in message.attachments:
                if attachment.filename == "pub.pem":
                    await self.write_client_to_file(message, attachment)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        pass

def setup(client):
    client.add_cog(MessageCog(client))
