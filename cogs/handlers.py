import logging
import json

import discord
from discord.ext import commands
from discord.ext.commands.errors import *
from connor_bot import COG_FOLDER

log = logging.getLogger(__name__)

class Handlers(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        """ Event when bot is ready """
        log.info("Bot start up.")
        print(f"{self.client.user.name} is ready")


    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        """ Event for every message """
        if msg.author.id != self.client.user.id:
            if msg.author.id == 462885213215916034:
                with open(f"{COG_FOLDER}/emojis.json", 'r') as f:
                    emojis = json.load(f)
                for emoji in emojis:
                    try:
                        await msg.add_reaction(emoji)
                    except:
                        continue

    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        eType = type(error)
        if eType is CommandNotFound:
            await ctx.send("Command not found.")
        elif eType is MissingRequiredArgument:
            await ctx.send(f"Missing argument: `{error.param}`.")
        elif eType is TooManyArguments:
            await ctx.send("You used too many arguments.")
        elif eType in [UserNotFound, MemberNotFound]:
            await ctx.send(f"Member, `{error.argument}`, was not found.")
        elif eType is MissingPermissions:
            await ctx.send("Must have following permission(s): " + ", ".join([f'`{perm}`' for perm in error.missing_perms]))
        elif eType is BotMissingPermissions:
            await ctx.send("I must have following permission(s): " + ", ".join([f'`{perm}`' for perm in error.missing_perms]))
        else:
            raise error
        log.error("%s raised error: %s", ctx.author, error)

    
    @commands.Cog.listener()
    async def on_command(self, ctx):
        log.info("%s invoked command: %s", ctx.author, ctx.message.content)


def setup(client):
    client.add_cog(Handlers(client))
