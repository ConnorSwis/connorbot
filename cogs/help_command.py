import discord
from discord.ext import commands
from connor_bot import PREFIX
from discord.ext.commands.errors import *
import helpers


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(brief="Lists commands and gives info.", usage=f"{PREFIX}help *command")
    async def help(self, ctx, request=None):
        if not request:
            embed = helpers.make_embed(title="Commands")
            commands_list = [(name, [command for command in cog.get_commands()]) for name, cog in self.client.cogs.items()]
            commands_list.sort(key=lambda x: len(x[1]))
            for name, cog_commands in commands_list:
                if len(cog_commands) != 0:
                    embed.add_field(
                        name=name,
                        value='\n'.join([f'{PREFIX}{command}' for command in cog_commands]),
                        inline=True
                        )
        else:
            com = self.client.get_command(request)
            if not com:
                await ctx.send(f"Command '{request}' doesn't exist")
                return
            embed = helpers.make_embed(
                title=com.name,
                description=com.brief,
                footer="* optional"
            )                       
            embed.add_field(name='Usage:', value='`'+com.usage+'`')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
