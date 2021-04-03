import logging
import os

import discord
from discord.ext import commands

COG_FOLDER = './cogs'
PREFIX = os.environ.get('PREFIX', '|')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)

client.remove_command('help')

logging.basicConfig(
    filename="connor_bot.log",
    format="%(levelname)s %(asctime)s: %(message)s",
    filemode='w',
    level=logging.INFO
)
log = logging.getLogger(name=__name__)

for filename in os.listdir(COG_FOLDER):
    if filename.endswith('.py'):
        if n:=os.environ.get(filename[:-3].upper()):
            if n.lower() == 'true':
                client.load_extension(f'cogs.{filename[:-3]}')
client.load_extension('cogs.help_command')
client.load_extension('cogs.handlers')
client.load_extension('cogs.essentials')

client.run(os.environ.get('BOT_TOKEN'))
