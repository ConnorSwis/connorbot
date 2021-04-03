import json
import logging

import discord
import helpers
from discord.ext import commands
from connor_bot import PREFIX, COG_FOLDER


LIST = '**`The List`**'
log = logging.getLogger(__name__)

class TheList(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(brief="Adds member to list", usage=f"{PREFIX}add @member")
    async def add(self, ctx, member: discord.Member):
        with open(f'{COG_FOLDER}/TheList.json') as file:
            the_list = json.load(file)
            if ctx.author.id not in the_list:
                await ctx.send(f"You have to be on {LIST} to add people to {LIST}")
            if member.id not in the_list:
                the_list.append(member.id)
            else:
                await ctx.send(f"{member.name} is already on {LIST}")
                return
        with open(f'{COG_FOLDER}/TheList.json', 'w') as file:
            json.dump(the_list, file, indent=2)
        await ctx.send(f"Added {member.name} to {LIST}")
        log.info("%s added %s to The List", ctx.author, member)


    @commands.command(brief="Removes member from list", usage=f"{PREFIX}remove @member")
    async def remove(self, ctx, member: discord.Member):
        if member.id == 640393413425889314:
            await ctx.send("Cannot remove God")
            return
        with open(f'{COG_FOLDER}/TheList.json') as file:
            the_list = json.load(file)
            if ctx.author.id not in the_list:
                await ctx.send(f"You have to be on {LIST} to remove people from {LIST}")
            if member.id in the_list:
                the_list.remove(member.id)
            else:
                await ctx.send(f"{member.name} is not on {LIST}")
                return
        with open(f'{COG_FOLDER}/TheList.json', 'w') as file:
            json.dump(the_list, file, indent=2)
        await ctx.send(f"Removed {member.name} from {LIST}")
        log.info("%s removed %s from The List", ctx.author, member)

    
    @commands.command(name="TheList",
                      brief="Shows the list", usage=f"{PREFIX}TheList")
    async def the_list(self, ctx):
        with open(f'{COG_FOLDER}/TheList.json') as file:
            the_list = json.load(file)
        embed = helpers.make_embed(
            title="The List",
            description='\n'.join(['- '+self.client.get_user(user).mention for user in the_list]),
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)



def setup(client):
    client.add_cog(TheList(client))
