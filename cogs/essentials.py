import logging

import discord
import helpers
from connor_bot import PREFIX
from discord.ext import commands


log = logging.getLogger(__name__)

class Essentials(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(brief="Sends invite for ConnorBot.", usage=f"{PREFIX}invite")
    async def invite(self, ctx):
        perms = discord.Permissions(8)
        await ctx.send(discord.utils.oauth_url(self.client.user.id, perms))


    @commands.command(brief="Kicks mentioned member.", usage=f"{PREFIX}kick @member *reason")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member}.')
    

    @commands.command(brief="Bans mentioned Member.", usage=f"{PREFIX}ban @member *reason")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member}.')


    @commands.command(brief="Unbans member.", usage=f"{PREFIX}unban member#0000")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == \
               (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {member}.')

    

def setup(client):
    client.add_cog(Essentials(client))
