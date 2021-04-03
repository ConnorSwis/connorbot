import discord
import pyfiglet
from connor_bot import PREFIX
from discord.ext import commands


class Ascii(commands.Cog):
    def __init__(self, client):
        self.client = client

        
    @commands.command(name="ascii",
                      brief="Converts your message to ASCII art",
                      usage=f"{PREFIX}ascii message")
    async def _ascii(self, ctx, *, text: str):
        ascii_banner = pyfiglet.figlet_format(text)
        await ctx.send('```'+ascii_banner+'```')


def setup(client):
    client.add_cog(Ascii(client))