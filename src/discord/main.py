import discord
import asyncio
from discord.ext import commands

from src.utils.utils import threaded

client = commands.Bot(command_prefix="--")

async def start(app):
    client.app = app

    client.load_extension("src.discord.listener")
    await client.start(app.config['token'], bot=False)

@threaded
def run_it_forever(loop):
    loop.run_forever()

def run_client(app):
    loop = asyncio.get_event_loop()
    loop.create_task(start(app))
    run_it_forever(loop)
