import random
from datetime import datetime

import discord


def make_embed(title=None, description=None, color=None, author=None, \
               image=None, link=None, footer=None) -> discord.Embed:
    """ Wrapper for making discord embeds """
    if not color: color = random.randint(0, 0xffffff)
    embed = discord.Embed(
        title=title,
        url=link,
        description=description,
        color=color
    )
    if author: embed.set_author(name=author)
    if image: embed.set_image(url=image)
    if footer: embed.set_footer(text=footer)
    else:
        now = datetime.now()
        embed.set_footer(text=now.strftime("%m/%d/%Y %H:%M:%S"))
    return embed
